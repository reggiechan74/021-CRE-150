"""Tests for scripts/gate_applicability.py — enforces Tasks A and B.

A gate is applicable only if the RFP actually invokes it. Statutory gates
(WSIB, working-at-heights, performance/L&M bonds on Part 3) are always
applicable. RFP-specified gates are applicable when the RFP populates the
corresponding mandatory_requirements field or lists the item in the verbatim
submission_requirements block. Everything else is clarifiable, not failable."""
from __future__ import annotations

import sys
from pathlib import Path

PLUGIN_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PLUGIN_ROOT / "scripts"))

from gate_applicability import is_gate_applicable, gate_tier  # noqa: E402


def _rfp(**kwargs) -> dict:
    base = {
        "mandatory_requirements": {},
        "submission_requirements": [],
        "project_classification": "obc_part_3",
    }
    base.update(kwargs)
    return base


def test_statutory_gates_always_applicable():
    rfp = _rfp()
    assert is_gate_applicable("wsib_clearance", rfp) is True
    assert is_gate_applicable("working_at_heights", rfp) is True
    # Statutory on Part 3: performance + L&M bonds are Construction Act baseline
    assert is_gate_applicable("performance_bond", rfp) is True


def test_bid_bond_not_applicable_when_rfp_silent():
    """The Exercise 6 bug: Heritage and friends were failed on bid_bond when
    the RFP §6.2 did not list it. Gate must be inapplicable unless the RFP
    specifies bid_bond_percent OR lists 'bid bond' in submission_requirements."""
    rfp = _rfp()  # no bid_bond_percent, no mention in submission_requirements
    assert is_gate_applicable("bid_bond", rfp) is False


def test_bid_bond_applicable_when_rfp_specifies_percent():
    rfp = _rfp(mandatory_requirements={"bid_bond_percent": 10})
    assert is_gate_applicable("bid_bond", rfp) is True


def test_bid_bond_applicable_when_in_submission_requirements():
    """Verbatim §6.2 mention also makes the gate applicable, even if the
    structured mandatory_requirements.bid_bond_percent is unset."""
    rfp = _rfp(submission_requirements=[
        "Bid Bond — 10% of the base bid, issued by a surety licensed in Ontario"
    ])
    assert is_gate_applicable("bid_bond", rfp) is True


def test_addenda_acknowledgment_defaults_to_clarifiable():
    """addenda_acknowledgment is a prudent-evaluator clarification, not a
    statutory gate. Without explicit RFP requirement it must be clarifiable."""
    rfp = _rfp(mandatory_requirements={"addenda_acknowledgment_required": False})
    assert is_gate_applicable("addenda_acknowledgment", rfp) is False
    rfp2 = _rfp(mandatory_requirements={"addenda_acknowledgment_required": True})
    assert is_gate_applicable("addenda_acknowledgment", rfp2) is True


def test_non_collusion_defaults_to_clarifiable():
    rfp = _rfp(mandatory_requirements={"non_collusion_declaration_required": False})
    assert is_gate_applicable("non_collusion_declaration", rfp) is False


def test_gate_tier_classification():
    """Gate tier is one of: statutory | rfp_specified | rfp_scope | prudent_evaluator.
    Statutory = can fail regardless of RFP text.
    RFP-specified = administrative gate; can fail only if RFP invokes it.
    RFP-scope = technical gate; applicability driven by scope_of_work / warranty_requirements.
    Prudent-evaluator = never fail; clarify only."""
    rfp = _rfp(mandatory_requirements={"bid_bond_percent": 10})
    assert gate_tier("wsib_clearance", rfp) == "statutory"
    assert gate_tier("working_at_heights", rfp) == "statutory"
    assert gate_tier("bid_bond", rfp) == "rfp_specified"
    assert gate_tier("addenda_acknowledgment", rfp) == "prudent_evaluator"
    assert gate_tier("non_collusion_declaration", rfp) == "prudent_evaluator"
    assert gate_tier("membrane_thickness", rfp) == "rfp_scope"
    assert gate_tier("cover_board", rfp) == "rfp_scope"
    assert gate_tier("warranty_type", rfp) == "rfp_scope"
    assert gate_tier("warranty_duration", rfp) == "rfp_scope"
    assert gate_tier("scope_compliance", rfp) == "rfp_scope"


# --- Technical-disqualification gates (rfp_scope tier) ---


def test_membrane_thickness_applicable_when_thickness_specified():
    """Exercise 6 regression: Lakeside proposed 45 mil where the RFP §3.1
    spec'd 60 mil. The tech reviewer correctly emitted a fail on
    `membrane_thickness`, but reconcile_gates rejected it because the gate
    was not invoked via mandatory_requirements/submission_requirements.
    Fix: applicability is driven by scope_of_work.membrane_system_specified."""
    rfp = _rfp(scope_of_work={
        "membrane_system_specified": {
            "category": "tpo",
            "thickness_spec": "Minimum 60 mil",
        }
    })
    assert is_gate_applicable("membrane_thickness", rfp) is True


def test_membrane_thickness_not_applicable_when_silent():
    rfp = _rfp(scope_of_work={"membrane_system_specified": {}})
    assert is_gate_applicable("membrane_thickness", rfp) is False


def test_cover_board_applicable_when_named_in_included_items():
    rfp = _rfp(scope_of_work={
        "included_items": [
            "Cover board: minimum 1/4 inch gypsum or HD polyiso",
        ]
    })
    assert is_gate_applicable("cover_board", rfp) is True


def test_cover_board_applicable_for_tpo_with_included_items():
    """TPO over polyiso typically requires a cover board for warranty
    validity. If the RFP names TPO and enumerates included items, the gate
    is applicable even if 'cover board' is not literally listed."""
    rfp = _rfp(scope_of_work={
        "membrane_system_specified": {"category": "tpo"},
        "included_items": ["New TPO membrane", "R-30 polyiso insulation"],
    })
    assert is_gate_applicable("cover_board", rfp) is True


def test_cover_board_not_applicable_when_no_membrane_or_included_items():
    rfp = _rfp()
    assert is_gate_applicable("cover_board", rfp) is False


def test_warranty_type_applicable_when_required():
    rfp = _rfp(warranty_requirements={"warranty_type_required": "total_system_ndl"})
    assert is_gate_applicable("warranty_type", rfp) is True


def test_warranty_type_not_applicable_when_silent():
    rfp = _rfp(warranty_requirements={})
    assert is_gate_applicable("warranty_type", rfp) is False


def test_warranty_duration_applicable_when_minimum_specified():
    rfp = _rfp(warranty_requirements={"minimum_manufacturer_years": 20})
    assert is_gate_applicable("warranty_duration", rfp) is True
    rfp2 = _rfp(warranty_requirements={"minimum_workmanship_years": 2})
    assert is_gate_applicable("warranty_duration", rfp2) is True


def test_warranty_duration_not_applicable_when_silent():
    rfp = _rfp(warranty_requirements={})
    assert is_gate_applicable("warranty_duration", rfp) is False


def test_scope_compliance_applicable_when_included_items_enumerated():
    """Exercise 6 regression: Metro excluded 25 RFP-required items. A
    bidder cannot silently exclude what the RFP enumerates as included."""
    rfp = _rfp(scope_of_work={"included_items": ["A", "B", "C"]})
    assert is_gate_applicable("scope_compliance", rfp) is True


def test_scope_compliance_not_applicable_when_no_included_items():
    rfp = _rfp(scope_of_work={})
    assert is_gate_applicable("scope_compliance", rfp) is False


def test_insulation_upgrade_applicable_when_code_required():
    rfp = _rfp(scope_of_work={"insulation_upgrade_to_code": True})
    assert is_gate_applicable("insulation_upgrade", rfp) is True


def test_insulation_upgrade_not_applicable_when_not_required():
    rfp = _rfp(scope_of_work={"insulation_upgrade_to_code": False})
    assert is_gate_applicable("insulation_upgrade", rfp) is False


def test_rfp_scope_gates_ignore_mandatory_requirements():
    """RFP-scope gates derive applicability from scope_of_work, not from
    mandatory_requirements. Populating mandatory_requirements should not
    accidentally enable a tech gate that the spec didn't specify."""
    rfp = _rfp(mandatory_requirements={
        "wsib_clearance_required": True,
        "cgl_minimum_cad": 5_000_000,
    })
    assert is_gate_applicable("membrane_thickness", rfp) is False
    assert is_gate_applicable("cover_board", rfp) is False
    assert is_gate_applicable("warranty_type", rfp) is False
