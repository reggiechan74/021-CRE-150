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
    """Gate tier is one of: statutory | rfp_specified | prudent_evaluator.
    Statutory = can fail regardless of RFP text.
    RFP-specified = can fail only if the RFP invokes it.
    Prudent-evaluator = never fail; clarify only."""
    rfp = _rfp(mandatory_requirements={"bid_bond_percent": 10})
    assert gate_tier("wsib_clearance", rfp) == "statutory"
    assert gate_tier("working_at_heights", rfp) == "statutory"
    assert gate_tier("bid_bond", rfp) == "rfp_specified"
    assert gate_tier("addenda_acknowledgment", rfp) == "prudent_evaluator"
    assert gate_tier("non_collusion_declaration", rfp) == "prudent_evaluator"
