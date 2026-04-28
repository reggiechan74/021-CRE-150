"""Gate applicability — decides when a mandatory gate can fail a bidder.

Motivating bug (Exercise 6 roof-review output): bidders were failed on gates
the RFP never invoked (e.g., `bid_bond` when the RFP §6.2 did not list a bid
bond). A gate that the RFP does not invoke is at most a clarification item;
it cannot be grounds for disqualification.

Four tiers:
  - `statutory`        — Ontario law or Construction Act baseline. Always
                          applicable regardless of RFP text (WSIB clearance,
                          working-at-heights training, performance and L&M
                          bonds on OBC Part 3 projects).
  - `rfp_specified`    — Administrative gate. Applicable only if the RFP
                          invokes the gate via `mandatory_requirements.<field>`
                          or names the item verbatim in
                          `submission_requirements`.
  - `rfp_scope`        — Technical-disqualification gate owned by
                          `roof-technical-review`. Applicable when the RFP's
                          `scope_of_work` or `warranty_requirements` block
                          specifies the requirement (membrane thickness,
                          cover board, warranty type, etc.). The
                          authoritative RFP text is the spec section, not
                          the §6.2 documentation list — so applicability is
                          checked against the structured scope fields.
  - `prudent_evaluator`— Items a careful evaluator asks about (non-collusion,
                          addenda acknowledgment) but which are not in the
                          RFP unless explicitly required. Default: clarify,
                          never fail.

Consumed by `roof-qualification-check` (decides pass/fail/needs_clarification)
and by `reconcile_gates.py` (detects asymmetric application across bidders).
"""
from __future__ import annotations


GATE_TIERS: dict[str, str] = {
    # Canonical names — administrative gates owned by roof-qualification-check
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
    # Technical-disqualification gates owned by roof-technical-review.
    # Applicability is driven by rfp.scope_of_work and rfp.warranty_requirements,
    # not by mandatory_requirements / submission_requirements.
    "scope_compliance": "rfp_scope",
    "membrane_thickness": "rfp_scope",
    "cover_board": "rfp_scope",
    "insulation_upgrade": "rfp_scope",
    "warranty_type": "rfp_scope",
    "warranty_duration": "rfp_scope",
    "completion_date": "rfp_scope",
    "mobilization_date": "rfp_scope",
    "fire_rating": "rfp_scope",
    "wind_uplift": "rfp_scope",
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


def _scope_specifies(rfp: dict, gate_name: str) -> bool:
    """True iff the RFP's `scope_of_work` / `warranty_requirements` block
    actually specifies the requirement that this technical gate enforces.

    The authority for technical-disqualification gates is the spec, not the
    §6.2 documentation list. Each gate maps to the structured RFP fields the
    `roof-rfp-extract` skill populates from the spec sections.
    """
    rfp = rfp or {}
    scope = rfp.get("scope_of_work") or {}
    warranty = rfp.get("warranty_requirements") or {}
    membrane = scope.get("membrane_system_specified") or {}

    def _truthy(v) -> bool:
        return v not in (None, "", [], {}, 0, False)

    if gate_name == "membrane_thickness":
        return _truthy(membrane.get("thickness_spec"))
    if gate_name == "cover_board":
        # Cover board is invoked when the RFP names it in included_items
        # or when the manufacturer-system-specified path requires one.
        included = scope.get("included_items") or []
        if any("cover board" in str(item).lower() for item in included):
            return True
        # Membrane category that typically requires a cover board
        return str(membrane.get("category", "")).lower() in {
            "tpo", "pvc", "epdm",
        } and bool(scope.get("included_items"))
    if gate_name == "insulation_upgrade":
        return bool(scope.get("insulation_upgrade_to_code"))
    if gate_name == "scope_compliance":
        # Applicable whenever the RFP enumerates included_items at all —
        # those are the items a bidder cannot silently exclude.
        return bool(scope.get("included_items"))
    if gate_name == "warranty_type":
        return _truthy(warranty.get("warranty_type_required"))
    if gate_name == "warranty_duration":
        # Either the manufacturer or workmanship floor invokes the gate.
        return _truthy(warranty.get("minimum_manufacturer_years")) or _truthy(
            warranty.get("minimum_workmanship_years")
        )
    if gate_name == "completion_date":
        return _truthy(rfp.get("required_substantial_completion_date")) or _truthy(
            (rfp.get("schedule") or {}).get("required_substantial_completion_date")
        )
    if gate_name == "mobilization_date":
        return _truthy(rfp.get("required_mobilization_by_date")) or _truthy(
            (rfp.get("schedule") or {}).get("required_mobilization_by_date")
        )
    if gate_name == "fire_rating":
        return _truthy(scope.get("fire_rating_required")) or _truthy(
            membrane.get("fire_rating_required")
        )
    if gate_name == "wind_uplift":
        return _truthy(scope.get("wind_uplift_rating_required")) or _truthy(
            membrane.get("wind_uplift_rating_required")
        )
    return False


def gate_tier(gate_name: str, rfp: dict | None = None) -> str:
    """Return `statutory`, `rfp_specified`, or `prudent_evaluator`.

    Unknown gate names default to `prudent_evaluator` — the conservative tier
    that can never be grounds for disqualification."""
    return GATE_TIERS.get(gate_name, "prudent_evaluator")


def is_gate_applicable(gate_name: str, rfp: dict) -> bool:
    """True iff the gate can legitimately fail a bidder for this RFP.

    - Statutory gates: always applicable.
    - RFP-specified (administrative) gates: applicable only if the RFP
      invokes the gate via mandatory_requirements or submission_requirements.
    - RFP-scope (technical) gates: applicable when the RFP's scope_of_work
      or warranty_requirements block specifies the underlying requirement.
    - Prudent-evaluator gates: applicable only if the RFP explicitly requires
      the declaration (e.g., `addenda_acknowledgment_required: true`)."""
    tier = gate_tier(gate_name)
    if tier == "statutory":
        return True

    if tier == "rfp_scope":
        return _scope_specifies(rfp or {}, gate_name)

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
