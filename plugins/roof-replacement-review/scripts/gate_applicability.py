"""Gate applicability — decides when a mandatory gate can fail a bidder.

Motivating bug (Exercise 6 roof-review output): bidders were failed on gates
the RFP never invoked (e.g., `bid_bond` when the RFP §6.2 did not list a bid
bond). A gate that the RFP does not invoke is at most a clarification item;
it cannot be grounds for disqualification.

Three tiers:
  - `statutory`        — Ontario law or Construction Act baseline. Always
                          applicable regardless of RFP text (WSIB clearance,
                          working-at-heights training, performance and L&M
                          bonds on OBC Part 3 projects).
  - `rfp_specified`    — Applicable only if the RFP invokes the gate via
                          `mandatory_requirements.<field>` or names the item
                          verbatim in `submission_requirements`.
  - `prudent_evaluator`— Items a careful evaluator asks about (non-collusion,
                          addenda acknowledgment) but which are not in the
                          RFP unless explicitly required. Default: clarify,
                          never fail.

Consumed by `roof-qualification-check` (decides pass/fail/needs_clarification)
and by `reconcile_gates.py` (detects asymmetric application across bidders).
"""
from __future__ import annotations


GATE_TIERS: dict[str, str] = {
    # Canonical names
    "wsib_clearance": "statutory",
    "working_at_heights": "statutory",
    "performance_bond": "statutory",
    "labour_material_bond": "statutory",
    "cgl_insurance": "statutory",
    "additional_insured": "statutory",
    "completed_ops": "statutory",
    "bid_bond": "rfp_specified",
    "site_visit": "rfp_specified",
    "minimum_years_in_business": "rfp_specified",
    "similar_project_references": "rfp_specified",
    "addenda_acknowledgment": "prudent_evaluator",
    "non_collusion_declaration": "prudent_evaluator",
    # Short-form aliases used by bid fixtures / existing manifests
    "wsib": "statutory",
    "cgl": "statutory",
    "wah_training": "statutory",
    "working_at_heights_training": "statutory",
    "years_in_business": "rfp_specified",
    "references": "rfp_specified",
    "addenda": "prudent_evaluator",
    "non_collusion": "prudent_evaluator",
    "bonding": "rfp_specified",
    "bonds": "rfp_specified",
}


_RFP_SPECIFIED_FIELD_MAP: dict[str, str] = {
    "bid_bond": "bid_bond_percent",
    "bonds": "performance_bond_percent",
    "bonding": "performance_bond_percent",
    "site_visit": "site_visit_required",
    "minimum_years_in_business": "minimum_years_in_business",
    "years_in_business": "minimum_years_in_business",
    "similar_project_references": "minimum_similar_projects",
    "references": "minimum_similar_projects",
    "addenda_acknowledgment": "addenda_acknowledgment_required",
    "addenda": "addenda_acknowledgment_required",
    "non_collusion_declaration": "non_collusion_declaration_required",
    "non_collusion": "non_collusion_declaration_required",
}


_SUBMISSION_KEYWORDS: dict[str, tuple[str, ...]] = {
    "bid_bond": ("bid bond",),
    "site_visit": ("site meeting", "pre-bid meeting", "site visit"),
    "addenda_acknowledgment": ("addenda", "addendum"),
    "non_collusion_declaration": ("non-collusion", "non collusion", "noncollusion"),
}


def gate_tier(gate_name: str, rfp: dict | None = None) -> str:
    """Return `statutory`, `rfp_specified`, or `prudent_evaluator`.

    Unknown gate names default to `prudent_evaluator` — the conservative tier
    that can never be grounds for disqualification."""
    return GATE_TIERS.get(gate_name, "prudent_evaluator")


def is_gate_applicable(gate_name: str, rfp: dict) -> bool:
    """True iff the gate can legitimately fail a bidder for this RFP.

    - Statutory gates: always applicable.
    - RFP-specified gates: applicable only if the RFP invokes the gate.
    - Prudent-evaluator gates: applicable only if the RFP explicitly requires
      the declaration (e.g., `addenda_acknowledgment_required: true`)."""
    tier = gate_tier(gate_name)
    if tier == "statutory":
        return True

    mandatory = (rfp or {}).get("mandatory_requirements") or {}
    submission = (rfp or {}).get("submission_requirements") or []

    if tier == "prudent_evaluator":
        field = _RFP_SPECIFIED_FIELD_MAP.get(gate_name)
        if field and mandatory.get(field) is True:
            return True
        for kw in _SUBMISSION_KEYWORDS.get(gate_name, ()):
            if any(kw.lower() in str(item).lower() for item in submission):
                return True
        return False

    # rfp_specified
    field = _RFP_SPECIFIED_FIELD_MAP.get(gate_name)
    if field is not None:
        value = mandatory.get(field)
        if value not in (None, False, 0):
            return True
    for kw in _SUBMISSION_KEYWORDS.get(gate_name, ()):
        if any(kw.lower() in str(item).lower() for item in submission):
            return True
    return False
