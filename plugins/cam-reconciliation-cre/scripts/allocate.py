"""Stage 3: deterministic CAM allocation engine."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from decimal import Decimal, ROUND_FLOOR
import sys
from pathlib import Path
from typing import Any

PLUGIN_ROOT = Path(__file__).resolve().parent.parent
if str(PLUGIN_ROOT) not in sys.path:
    sys.path.insert(0, str(PLUGIN_ROOT))

from scripts.manifest import (
    BASE_YEAR_CITATION,
    CANADAFIRST_CAP,
    CANADAFIRST_UNCONTROLLABLE,
    ExclusionApplied,
    Lease,
    LeaseCitation,
    LeaseType,
    Manifest,
    PoolName,
    PRONTO_GREASE_TRAP_CITATION,
    PEAK_RM_CITATION,
    PEAK_UTILITIES_CITATION,
    STANDARD_FORM_ALLOCATION,
    TenantCharge,
    canonical_category,
    money,
)


def split_amount(total: Decimal, weighted_items: list[tuple[str, Decimal]]) -> dict[str, Decimal]:
    if not weighted_items:
        return {}
    total_weight = sum(weight for _, weight in weighted_items)
    if total_weight == 0:
        return {key: Decimal("0.00") for key, _ in weighted_items}

    total_cents = int((money(total) * 100).to_integral_value())
    raw_cents = {
        key: Decimal(total_cents) * weight / total_weight for key, weight in weighted_items
    }
    floor_cents = {
        key: int(value.to_integral_value(rounding=ROUND_FLOOR))
        for key, value in raw_cents.items()
    }
    remaining = total_cents - sum(floor_cents.values())
    remainders = sorted(
        ((raw_cents[key] - floor_cents[key], key) for key in raw_cents),
        key=lambda item: (-item[0], item[1]),
    )
    for _, key in remainders[:remaining]:
        floor_cents[key] += 1
    return {key: Decimal(cents) / Decimal("100") for key, cents in floor_cents.items()}


def pool_portions(manifest: Manifest, line_amount: Decimal, line_pool: PoolName) -> dict[PoolName, Decimal]:
    if line_pool != PoolName.SHARED:
        return {line_pool: money(line_amount)}
    weights = [
        (PoolName.OFFICE.value, Decimal(manifest.property.rsf_office)),
        (PoolName.RETAIL.value, Decimal(manifest.property.rsf_retail)),
    ]
    split = split_amount(line_amount, weights)
    return {
        PoolName.OFFICE: split[PoolName.OFFICE.value],
        PoolName.RETAIL: split[PoolName.RETAIL.value],
    }


def _line_citation_for_charge(lease: Lease, category_key: str) -> LeaseCitation:
    if lease.lease_type == LeaseType.MODIFIED_GROSS:
        return lease.clause_refs.get("allocation", STANDARD_FORM_ALLOCATION)
    if lease.lease_type == LeaseType.NET_WITH_CAP:
        if category_key in (lease.cap.uncontrollable_categories if lease.cap else []):
            return lease.clause_refs.get("cap_uncontrollable", CANADAFIRST_UNCONTROLLABLE)
        return lease.clause_refs.get("cap", CANADAFIRST_CAP)
    return lease.clause_refs.get("allocation", STANDARD_FORM_ALLOCATION)


def _specific_exclusion_match(rule: dict[str, Any], line_category_key: str, raw_category: str, memo: str) -> bool:
    if rule.get("category") and rule["category"] != line_category_key:
        return False
    if rule.get("match_category_raw") and rule["match_category_raw"] != raw_category:
        return False
    keywords = rule.get("match_keywords") or []
    if keywords and not all(keyword.lower() in memo.lower() for keyword in keywords):
        return False
    return True


def exclusion_for_line(lease: Lease, line_category_key: str, raw_category: str, memo: str) -> tuple[bool, str | None, LeaseCitation | None]:
    if lease.is_vacant:
        return False, None, None

    if lease.lease_type == LeaseType.MODIFIED_GROSS and line_category_key in lease.excluded_categories:
        if line_category_key == "utilities":
            return True, "modified_gross_utilities", lease.clause_refs.get("modified_gross_utilities", PEAK_UTILITIES_CITATION)
        if line_category_key == "repairs_maintenance":
            return True, "modified_gross_repairs_maintenance", lease.clause_refs.get("modified_gross_repairs_maintenance", PEAK_RM_CITATION)

    for rule in lease.specific_exclusions:
        if _specific_exclusion_match(rule, line_category_key, raw_category, memo):
            citation = LeaseCitation.model_validate(rule["citation"]) if "citation" in rule else lease.clause_refs.get("restaurant_exclusion", PRONTO_GREASE_TRAP_CITATION)
            return True, rule.get("reason", "specific_exclusion"), citation

    return False, None, None


def _aggregate_exclusion(
    tracker: dict[str, dict[tuple[str, str], ExclusionApplied]],
    tenant_id: str,
    category: str,
    reason: str,
    amount: Decimal,
    citation: LeaseCitation | None,
    reallocated_to: list[str],
) -> None:
    bucket = tracker.setdefault(tenant_id, {})
    key = (category, reason)
    if key not in bucket:
        bucket[key] = ExclusionApplied(
            category=category,
            amount_removed=money(amount),
            reason=reason,
            citation_ref=citation,
            reallocated_to=list(reallocated_to),
        )
        return
    existing = bucket[key]
    existing.amount_removed = money(existing.amount_removed + amount)
    existing.reallocated_to = sorted(set(existing.reallocated_to + reallocated_to))


def _lease_weights(leases: list[Lease]) -> list[tuple[str, Decimal]]:
    return [(lease.tenant_id, Decimal(lease.rsf)) for lease in leases]


def allocate_manifest(manifest: Manifest) -> Manifest:
    if any(line.classification is None for line in manifest.gl_lines):
        raise ValueError("All GL lines must be classified before allocation.")

    leases = list(manifest.leases)
    lease_by_id = {lease.tenant_id: lease for lease in leases}
    active_leases = [lease for lease in leases if not lease.is_vacant]
    active_by_pool = {
        PoolName.OFFICE: [lease for lease in active_leases if lease.pool == PoolName.OFFICE],
        PoolName.RETAIL: [lease for lease in active_leases if lease.pool == PoolName.RETAIL],
    }
    all_by_pool = {
        PoolName.OFFICE: [lease for lease in leases if lease.pool == PoolName.OFFICE],
        PoolName.RETAIL: [lease for lease in leases if lease.pool == PoolName.RETAIL],
    }

    gross_before_exclusions: dict[str, Decimal] = defaultdict(lambda: Decimal("0.00"))
    running_totals: dict[str, Decimal] = defaultdict(lambda: Decimal("0.00"))
    category_totals: dict[str, dict[str, Decimal]] = defaultdict(lambda: defaultdict(lambda: Decimal("0.00")))
    line_totals: dict[str, dict[str, Decimal]] = defaultdict(lambda: defaultdict(lambda: Decimal("0.00")))
    exclusion_tracker: dict[str, dict[tuple[str, str], ExclusionApplied]] = {}
    landlord_absorbed_total = Decimal("0.00")
    landlord_breakdown: dict[str, Decimal] = defaultdict(lambda: Decimal("0.00"))
    recoverable_total = Decimal("0.00")

    for line in manifest.gl_lines:
        classification = line.classification
        if not classification or not classification.recoverable:
            continue
        line_recoverable = classification.recoverable_amount or line.amount
        if line_recoverable <= 0:
            continue

        recoverable_total = money(recoverable_total + line_recoverable)
        line_pool = classification.pool or PoolName(line.pool_hint.lower())
        line_category_key = classification.normalized_category or canonical_category(line.category_raw)
        line_allocation: dict[str, Decimal] = {}

        for pool_name, pool_amount in pool_portions(manifest, line_recoverable, line_pool).items():
            pool_leases = all_by_pool[pool_name]
            pool_active = active_by_pool[pool_name]
            base_shares = split_amount(pool_amount, _lease_weights(pool_leases))

            for lease in pool_active:
                gross_before_exclusions[lease.tenant_id] = money(
                    gross_before_exclusions[lease.tenant_id] + base_shares[lease.tenant_id]
                )

            shares = dict(base_shares)
            excluded_leases: list[tuple[Lease, str, LeaseCitation | None]] = []
            for lease in pool_active:
                excluded, reason, citation = exclusion_for_line(lease, line_category_key, line.category_raw, line.memo)
                if excluded:
                    excluded_leases.append((lease, reason or "specific_exclusion", citation))

            if excluded_leases:
                excluded_amount = money(sum(base_shares[lease.tenant_id] for lease, _, _ in excluded_leases))
                eligible = [lease for lease in pool_active if lease.tenant_id not in {item[0].tenant_id for item in excluded_leases}]
                if eligible:
                    reallocated = split_amount(excluded_amount, _lease_weights(eligible))
                    for lease in eligible:
                        shares[lease.tenant_id] = money(shares[lease.tenant_id] + reallocated[lease.tenant_id])
                else:
                    landlord_absorbed_total = money(landlord_absorbed_total + excluded_amount)
                    landlord_breakdown["excluded_all_recipients"] = money(landlord_breakdown["excluded_all_recipients"] + excluded_amount)

                reallocated_to = [lease.tenant_id for lease in eligible]
                for lease, reason, citation in excluded_leases:
                    removed = base_shares[lease.tenant_id]
                    shares[lease.tenant_id] = Decimal("0.00")
                    _aggregate_exclusion(
                        tracker=exclusion_tracker,
                        tenant_id=lease.tenant_id,
                        category=line_category_key,
                        reason=reason,
                        amount=removed,
                        citation=citation,
                        reallocated_to=reallocated_to,
                    )

            for lease in pool_leases:
                allocated = shares.get(lease.tenant_id, Decimal("0.00"))
                if lease.is_vacant:
                    landlord_absorbed_total = money(landlord_absorbed_total + allocated)
                    landlord_breakdown["vacancy"] = money(landlord_breakdown["vacancy"] + allocated)
                    continue

                if allocated:
                    running_totals[lease.tenant_id] = money(running_totals[lease.tenant_id] + allocated)
                    category_totals[lease.tenant_id][line_category_key] = money(
                        category_totals[lease.tenant_id][line_category_key] + allocated
                    )
                    line_totals[lease.tenant_id][line.line_id] = money(
                        line_totals[lease.tenant_id][line.line_id] + allocated
                    )
                    line_allocation[lease.tenant_id] = money(line_allocation.get(lease.tenant_id, Decimal("0.00")) + allocated)

        line_allocation = {tenant_id: amount for tenant_id, amount in sorted(line_allocation.items())}
        line.allocation = line_allocation

    tenant_charges: list[TenantCharge] = []
    total_final = Decimal("0.00")

    for lease in sorted(active_leases, key=lambda item: item.tenant_id):
        preliminary = money(running_totals[lease.tenant_id])
        steps = [f"Gross share before exclusions: ${money(gross_before_exclusions[lease.tenant_id]):,.2f}."]

        exclusions = list(exclusion_tracker.get(lease.tenant_id, {}).values())
        for exclusion in exclusions:
            steps.append(
                f"Excluded {exclusion.category} under {exclusion.reason}: -${exclusion.amount_removed:,.2f}."
            )

        base_adjustment: dict[str, Any] | None = None
        if lease.base_year:
            base_amount = money(Decimal(lease.rsf) * lease.base_year.cam_psf)
            absorbed = min(preliminary, base_amount)
            preliminary = money(max(Decimal("0.00"), preliminary - base_amount))
            landlord_absorbed_total = money(landlord_absorbed_total + absorbed)
            landlord_breakdown["base_year"] = money(landlord_breakdown["base_year"] + absorbed)
            base_adjustment = {
                "base_year": lease.base_year.year,
                "base_amount": base_amount,
                "amount_removed": absorbed,
                "citation": lease.clause_refs.get("base_year", BASE_YEAR_CITATION).model_dump(mode="json"),
            }
            steps.append(f"Applied base year credit of ${absorbed:,.2f}.")

        cap_adjustment: dict[str, Any] | None = None
        if lease.cap:
            uncontrollable = money(
                sum(category_totals[lease.tenant_id].get(key, Decimal("0.00")) for key in lease.cap.uncontrollable_categories)
            )
            controllable = money(sum(category_totals[lease.tenant_id].values()) - uncontrollable)
            years_elapsed = manifest.fiscal_year - lease.cap.base_year
            cap_psf = money(lease.cap.base_year_cam_psf * ((Decimal("1.00") + lease.cap.annual_increase_rate) ** years_elapsed))
            cap_ceiling_total = money(cap_psf * Decimal(lease.rsf))
            landlord_absorbed = Decimal("0.00")
            if controllable > cap_ceiling_total:
                landlord_absorbed = money(controllable - cap_ceiling_total)
                preliminary = money(preliminary - landlord_absorbed)
                landlord_absorbed_total = money(landlord_absorbed_total + landlord_absorbed)
                landlord_breakdown["cam_cap"] = money(landlord_breakdown["cam_cap"] + landlord_absorbed)
            cap_adjustment = {
                "controllable_uncapped": controllable,
                "uncontrollable_uncapped": uncontrollable,
                "controllable_cap_ceiling_psf": cap_psf,
                "controllable_cap_ceiling_total": cap_ceiling_total,
                "landlord_absorbed": landlord_absorbed,
                "citation": lease.clause_refs.get("cap", CANADAFIRST_CAP).model_dump(mode="json"),
            }
            steps.append(
                f"Applied CAM cap check: controllable ${controllable:,.2f} vs ceiling ${cap_ceiling_total:,.2f}."
            )

        annual_prebilled = money(lease.annual_prebilled or Decimal("0.00"))
        vs_prebilled = money(preliminary - annual_prebilled)
        total_final = money(total_final + preliminary)

        citations = []
        for line_id, contribution in sorted(line_totals[lease.tenant_id].items()):
            category_key = canonical_category(
                next(gl_line.category_raw for gl_line in manifest.gl_lines if gl_line.line_id == line_id)
            )
            citations.append(
                {
                    "gl_line_id": line_id,
                    "lease_citation_ref": _line_citation_for_charge(lease, category_key).model_dump(mode="json"),
                    "contribution_amount": contribution,
                }
            )

        tenant_charges.append(
            TenantCharge(
                tenant_id=lease.tenant_id,
                gross_share_before_exclusions=money(gross_before_exclusions[lease.tenant_id]),
                exclusions_applied=exclusions,
                base_year_adjustment=base_adjustment,
                cap_adjustment=cap_adjustment,
                final_charge=preliminary,
                annual_prebilled=annual_prebilled,
                vs_prebilled=vs_prebilled,
                citations=citations,
                math_trace={
                    "category_totals_before_base_or_cap": {
                        key: money(value) for key, value in sorted(category_totals[lease.tenant_id].items())
                    },
                    "steps": steps,
                },
            )
        )

    landlord_absorbed_total = money(landlord_absorbed_total)
    if money(total_final + landlord_absorbed_total) != money(recoverable_total):
        raise AssertionError(
            f"Balance invariant failed: tenants {total_final} + landlord {landlord_absorbed_total} != recoverable {recoverable_total}"
        )

    return manifest.model_copy(
        update={
            "gl_lines": manifest.gl_lines,
            "tenant_charges": tenant_charges,
            "landlord_absorbed_total": landlord_absorbed_total,
        }
    )


def allocated_output_path(classified_manifest_path: Path) -> Path:
    return classified_manifest_path.parent / "allocated_manifest.json"


def main() -> None:
    parser = argparse.ArgumentParser(description="Allocate classified CAM lines into tenant charges.")
    parser.add_argument("--manifest", type=Path, required=True, help="Path to classified_manifest.json.")
    parser.add_argument("--output", type=Path, help="Path to allocated_manifest.json.")
    args = parser.parse_args()

    manifest = Manifest.load(args.manifest)
    allocated = allocate_manifest(manifest)
    output = args.output or allocated_output_path(args.manifest)
    output.parent.mkdir(parents=True, exist_ok=True)
    allocated.save(output)

    print(
        json.dumps(
            {
                "allocated_manifest": str(output),
                "tenant_count": len(allocated.tenant_charges),
                "landlord_absorbed_total": str(allocated.landlord_absorbed_total),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
