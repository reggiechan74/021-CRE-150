"""Allocation engine tests."""

from __future__ import annotations

import json
from decimal import Decimal


def _charge(manifest, tenant_id: str):
    return next(charge for charge in manifest.tenant_charges if charge.tenant_id == tenant_id)


def _load_archetype(plugin_root, name: str):
    path = plugin_root / "fixtures" / "archetypes" / f"{name}.json"
    return json.loads(path.read_text(encoding="utf-8"))


def test_balance_invariant(allocated_matheson_manifest):
    tenant_total = sum(charge.final_charge for charge in allocated_matheson_manifest.tenant_charges)
    recoverable_total = sum(
        line.classification.recoverable_amount or Decimal("0")
        for line in allocated_matheson_manifest.gl_lines
        if line.classification and line.classification.recoverable
    )
    assert tenant_total + allocated_matheson_manifest.landlord_absorbed_total == recoverable_total
    assert recoverable_total == Decimal("1150292.00")


def test_landlord_absorbed_total_matches_expected(allocated_matheson_manifest):
    assert allocated_matheson_manifest.landlord_absorbed_total == Decimal("131149.03")


def test_modified_gross_exclusions(plugin_root, allocated_matheson_manifest):
    fx = _load_archetype(plugin_root, "unit_104_modified_gross")
    charge = _charge(allocated_matheson_manifest, fx["tenant_id"])
    assert charge.final_charge == Decimal(fx["expected_final_charge"])
    exclusions = {item.category: item.amount_removed for item in charge.exclusions_applied}
    assert exclusions["utilities"] == Decimal(fx["expected_exclusions"]["utilities"])
    assert exclusions["repairs_maintenance"] == Decimal(fx["expected_exclusions"]["repairs_maintenance"])


def test_pronto_grease_trap_exclusion(plugin_root, allocated_matheson_manifest):
    fx = _load_archetype(plugin_root, "unit_105_restaurant_exclusions")
    charge = _charge(allocated_matheson_manifest, fx["tenant_id"])
    assert charge.final_charge == Decimal(fx["expected_final_charge"])
    exclusion = charge.exclusions_applied[0]
    assert exclusion.amount_removed == Decimal(fx["expected_exclusions"]["repairs_maintenance"])


def test_base_year_tenants(plugin_root, allocated_matheson_manifest):
    unit_103 = _load_archetype(plugin_root, "unit_103_base_year_2024")
    suite_310 = _load_archetype(plugin_root, "suite_310_base_year_2023")

    charge_103 = _charge(allocated_matheson_manifest, unit_103["tenant_id"])
    charge_310 = _charge(allocated_matheson_manifest, suite_310["tenant_id"])

    assert charge_103.final_charge == Decimal(unit_103["expected_final_charge"])
    assert Decimal(charge_103.base_year_adjustment["amount_removed"]) == Decimal(unit_103["expected_base_year_amount_removed"])
    assert charge_310.final_charge == Decimal(suite_310["expected_final_charge"])
    assert Decimal(charge_310.base_year_adjustment["amount_removed"]) == Decimal(suite_310["expected_base_year_amount_removed"])


def test_canadafirst_cap_math(plugin_root, allocated_matheson_manifest):
    fx = _load_archetype(plugin_root, "unit_101_cam_cap")
    charge = _charge(allocated_matheson_manifest, fx["tenant_id"])
    assert charge.final_charge == Decimal(fx["expected_final_charge"])
    assert Decimal(charge.cap_adjustment["controllable_uncapped"]) == Decimal(fx["expected_controllable_uncapped"])
    assert Decimal(charge.cap_adjustment["controllable_cap_ceiling_total"]) == Decimal(fx["expected_cap_ceiling_total"])
    assert Decimal(charge.cap_adjustment["landlord_absorbed"]) == Decimal(fx["expected_cap_landlord_absorbed"])
