---
name: roof-technical-review
description: >
  Use when evaluating a roofing bid's technical content against the RFP and Ontario
  codes — materials adequacy, warranty validity, OBC compliance, manufacturer
  system compatibility, wind uplift, insulation R-value compliance, and cover-board
  presence. Produces raw sub-scores and technical red flags.
---

# Roof Technical Review

You are evaluating whether the bid's proposed system will (a) meet the RFP specification, (b) comply with the Ontario Building Code, and (c) qualify for the warranty the contractor claims. Every finding cites an authoritative source.

## Division of responsibility vs roof-qualification-check

This skill owns **technical disqualification** — gate fails caused by
scope/materials/warranty/schedule failures that cannot be cured by
clarification without a re-bid. `roof-qualification-check` owns
**administrative disqualification** — WSIB/CGL/bonds/training/declarations
where an applicability filter decides whether `fail` is even permitted.

The two skills must not fail the same bidder on the same underlying issue.
If you notice a qualification-tier problem (certification lapsed,
subcontractor undisclosed, WSIB missing), leave it for qualification-check.
If qualification-check notices a technical-tier problem (wrong membrane
thickness, missing cover board), it must leave it for this skill.

## Technical Disqualification Gates

Emit a `fail` result into `bid.mandatory_gates.<gate_name>` only when the
RFP-specified requirement cannot be met by the proposed bid and cannot be
cured by clarification. These are the gates this skill owns:

| Gate | Emit `fail` when | RFP authority (must be present) | Cures available |
|---|---|---|---|
| `scope_compliance` | Bid excludes or alters a work item the RFP required without offering an equivalent | `rfp.scope_of_work.included_items` enumerates the items | Only by rebid |
| `membrane_thickness` | Proposed thickness is below the RFP minimum (e.g., 45 mil where RFP spec'd 60 mil) | `rfp.scope_of_work.membrane_system_specified.thickness_spec` populated | Only by rebid |
| `cover_board` | Commercial single-ply over polyiso without a cover board when the RFP required one (or the warranty program requires one and the contractor claims that program) | `rfp.scope_of_work.included_items` mentions cover board, OR membrane is TPO/PVC/EPDM with included_items enumerated | Only by rebid |
| `insulation_upgrade` | Does not meet SB-10/SB-12 when retrofit triggers the code requirement | `rfp.scope_of_work.insulation_upgrade_to_code: true` | Only by rebid |
| `warranty_type` | Offered warranty type is weaker than RFP-required (e.g., `material_only` when RFP required `total_system_ndl`) | `rfp.warranty_requirements.warranty_type_required` populated | Only by rebid |
| `warranty_duration` | Offered years below RFP minimum | `rfp.warranty_requirements.minimum_manufacturer_years` or `minimum_workmanship_years` populated | Only by rebid |
| `completion_date` | Proposed substantial-completion date misses the RFP-stated deadline | `rfp.required_substantial_completion_date` populated | Only by rebid (or owner-approved schedule change) |
| `mobilization_date` | Mobilization day misses RFP's latest-mobilization requirement | `rfp.required_mobilization_by_date` populated | Only by rebid |
| `fire_rating` | Proposed assembly does not meet the RFP-specified fire rating | `rfp.scope_of_work.fire_rating_required` populated | Only by rebid |
| `wind_uplift` | Proposed assembly's wind-uplift rating below RFP requirement (not merely "design basis not stated" — that is a red flag, not a fail) | `rfp.scope_of_work.wind_uplift_rating_required` populated | Only by rebid |

**Applicability gate (enforced by `scripts/reconcile_gates.py`):** the
"RFP authority" column is not advisory. The reconciler uses
`gate_applicability.is_gate_applicable()` (tier `rfp_scope`) to confirm
the RFP actually specified the requirement before allowing a `fail`. If
the spec field is absent (e.g., the RFP never set
`warranty_type_required`), demote your finding from `fail` to
`needs_clarification` and capture the underlying concern as a red flag —
the reconciler will reject the manifest otherwise.

**When in doubt, prefer a red flag with `recommendation: clarify` over a
gate fail.** A gate fail excludes the bid from rated scoring entirely; a red
flag informs scoring and the memo without foreclosing the bid. Only fail
when no clarification can cure the issue without re-tendering.

## Reference Material

**Read only these fixtures — do not load `03_tender_evaluation_methodology.md` or `04_contractor_qualification.md`, which are owned by `roof-qualification-check`:**

Treat these as ground truth — cite section numbers in your findings:

- `fixtures/domain_knowledge/01_ontario_roofing_codes.md` — OBC Part 3 (commercial) and Part 9 (residential), wind uplift, SB-10/SB-12 R-values, ventilation ratios
- `fixtures/domain_knowledge/02_roofing_materials_warranties.md` — membrane/shingle specs, warranty taxonomy, certified installer programs, red flags catalogue

## Decision Order

1. **Scope compliance.** Does the bid propose the specified system or a substitution? If substitution, evaluate equivalence against the RFP and fixture 02.

2. **Thickness & membrane class.** For commercial single-ply: minimum 60 mil TPO/PVC for commercial per fixture 02 §1 — 45 mil is a red flag for commercial. For mod-bit: confirm 2-ply cap + base, not just cap sheet.

3. **Attachment method.** Matches RFP spec and manufacturer approved methods? Induction-welded over mechanically-fastened is an upgrade, not a deficiency; ballasted over wind-design-required is a deficiency.

4. **Insulation & cover board.** Is insulation R-value specified? Does it meet SB-10/SB-12 for the climate zone (fixture 01 §1.3)? For commercial over polyiso: is a cover board (HD polyiso, DensDeck, or gypsum fiber) included? Missing cover board = critical red flag (fixture 02 §4).

5. **Warranty validity.**
   - Years and type meet/exceed RFP requirement? (Match `warranty_requirements` in rfp.json)
   - Is the contractor certified by the named manufacturer for the warranty tier claimed? (Fixture 02 §3)
   - Any system component substitutions that would void the manufacturer system warranty? (Fixture 02 §4 — mis-matched components)
   - "25 year" without type specified = `unclear` from extraction → warranty red flag

6. **Wind uplift basis.** Commercial low-slope: bid should state the wind uplift design (CSA A123.21 or FM 1-29) basis. Missing = high-severity flag (fixture 01 §1.2).

7. **Fall protection & safety.** Bid describes fall arrest approach, anchor points (CSA Z91 compliance), guardrail vs tie-off for parapet work? Missing plan = safety red flag (fixture 01 §3).

8. **Waste & environmental.** Asphalt shingle disposal plan? If pre-1980 built-up roof, DSA / asbestos plan per O. Reg. 278/05 (fixture 01 §4)?

9. **OBC Part 9 specifics (if residential).**
   - Slope meets shingle minimum (4:12 asphalt)
   - Ice & water shield at eaves per OBC 9.26.5.1 (900mm past wall plane, 300mm past eave)
   - Ventilation 1:300 (or 1:150 without 60/40 split) per OBC 9.19.1.2
   - Drip edge, starter strip, 4-nail (or 6-nail high wind) fastening

## Sub-Score Outputs

Produce raw sub-scores (0-100) for the two rated criteria this skill owns. Each is computed as the **sum of sub-factor points**, not a single anchor match. Record the per-sub-factor points in `bid.scoring_rationale.<sub_score>.sub_factors` so the audit trail shows the math.

### `technical_approach` (sum of five sub-factors, max 100)

| Sub-factor | Points | Criterion |
|---|---|---|
| Tear-off & staging | 0 | missing |
|  | 10 | mentioned |
|  | 20 | phased with interim protection |
|  | 25 | detailed (dumpster placement, lift strategy, staging zones, adjacent-property protection) |
| Weather protection / dry-in | 0 | not addressed |
|  | 10 | generic "tarp at end of day" |
|  | 20 | specific dry-in plan per phase with forecast protocol |
| Fall protection & safety | 0 | not addressed |
|  | 10 | generic WAH compliance statement |
|  | 20 | named anchor points + specific fall-arrest equipment |
|  | 25 | site-specific plan addressing parapets/perimeters |
| Waste / environmental / logistics | 0 | not addressed |
|  | 8 | disposal mentioned |
|  | 15 | DSA plan (if pre-1980) + recycling commitments |
| Quality control / inspection protocol | 0 | not addressed |
|  | 8 | final walk-through only |
|  | 15 | in-progress QC checkpoints + manufacturer inspection scheduled per warranty requirements |

### `warranty_materials` (sum of five sub-factors, max 100)

| Sub-factor | Points | Criterion |
|---|---|---|
| Warranty type (vs RFP requirement) | 0 | non-compliant or `unclear` |
|  | 10 | prorated |
|  | 20 | material_only |
|  | 30 | labour_and_material |
|  | 35 | ndl (no attached system-warranty program) |
|  | 40 | total_system_ndl (attached named system program) |
| Warranty years vs RFP minimum | 0 | below minimum |
|  | 12 | meets minimum |
|  | 20 | exceeds minimum by 5+ yrs |
| Installer certification at claimed warranty tier | 0 | none claimed |
|  | 8 | certified but not at claimed tier |
|  | 20 | certified at claimed tier (pre-install review + mid-job inspection schedulable) |
| Workmanship warranty years | 0 | not stated |
|  | 3 | <2 yrs |
|  | 6 | 2-4 yrs |
|  | 10 | 5+ yrs |
| Materials quality (thickness, cover board, premium line) | 0 | below industry standard (e.g., 45 mil commercial TPO, no cover board) |
|  | 6 | meets standard |
|  | 10 | exceeds standard (60+ mil, HD cover, premium line) |

If the sum exceeds 100 due to downstream fixture changes, cap at 100 and note in `scoring_rationale`.

## Red Flag Category Ownership

To prevent double-writing the same issue, each `red_flags.category` is owned by exactly one skill:

| Category | Owner skill |
|---|---|
| `warranty` | roof-technical-review (this skill) |
| `materials` | roof-technical-review |
| `safety` | roof-technical-review |
| `scope` | roof-technical-review |
| `substitutions` | roof-technical-review |
| `qualifications` | roof-qualification-check |

If you notice an issue that would fall under `qualifications` (e.g., certification lapsed, subcontractor undisclosed), leave it for roof-qualification-check — do not write it here.

## Red Flag Output

Append to `bid.red_flags[]`:

```json
{
  "severity": "critical|high|medium|low",
  "category": "warranty|materials|safety|scope|substitutions",
  "description": "brief human-readable issue",
  "citation": "OBC 9.26.5.1 | CRCA bulletin | fixture 02 §1.3",
  "evidence": "page reference from extraction + direct quote if short",
  "recommendation": "clarify|negotiate|reject|accept-with-condition"
}
```

## Severity Calibration

**Overriding rule:** if a flag voids the warranty the contractor is claiming, fails the Ontario Building Code, or creates a worker/occupant safety hazard, it is **critical** — regardless of which bucket the example lists below suggest. Apply the rule first, then use the examples to calibrate.

- **Critical:** non-compliance voids warranty, fails OBC, or is a safety hazard. Examples: no cover board on commercial polyiso with NDL warranty claim; installer not certified for the warranty tier claimed; no fall protection plan on a parapet-less roof; 45 mil TPO proposed where RFP specified 60 mil (voids the spec and likely the NDL warranty); warranty type `unclear` when RFP required `total_system_ndl` (owner cannot confirm they are getting what they required).
- **High:** material deviation from RFP or industry best practice that does not void warranty/code/safety. Examples: wind uplift design basis not stated but implied; workmanship warranty below market median (2 years vs typical 5); substitution proposed with weak equivalence justification on a non-critical component.
- **Medium:** ambiguity worth clarifying. Examples: insulation R-value not explicitly stated but the proposed system implies compliance; substitution with partial justification on an accessory component.
- **Low:** cosmetic or documentation gaps. Examples: missing product data sheet for accessory materials; page references missing from bid index.

## Sidecar Output File

Write your results to a **sidecar** JSON file so the qualification-check skill can
run in parallel without clobbering your writes:

**Path:** `<rfp-dir>/roof-review-output/manifests/bid_<slug>.tech.json`

**Shape:**

```json
{
  "bidder_id": "<same as base bid manifest>",
  "mandatory_gates": { "<technical_gate_name>": { "result": "...", "evidence": "..." } },
  "scores": {
    "technical_approach": <0-100>,
    "warranty_materials": <0-100>
  },
  "scoring_rationale": {
    "technical_approach": { "sub_factors": { "...": <points> } },
    "warranty_materials": { "sub_factors": { "...": <points> } }
  },
  "red_flags": [
    { "severity": "...", "category": "scope|materials|warranty|safety|substitutions", ... }
  ]
}
```

**Do NOT** touch the base `bid_<slug>.json` — the qualification-check skill is
writing `bid_<slug>.qual.json` concurrently and `scripts/normalize.py` will
merge all three files. A write to `bid_<slug>.json` from this skill is a bug.

Keys this sidecar MAY contain: `bidder_id`, `mandatory_gates` (only from the
technical gate table above), `scores.technical_approach`,
`scores.warranty_materials`, `scoring_rationale.technical_approach`,
`scoring_rationale.warranty_materials`, `red_flags` (categories `scope`,
`materials`, `warranty`, `safety`, `substitutions`).

Keys this sidecar MUST NOT contain: `scores.experience_references`,
`scores.qualifications_certifications`, `scores.schedule`, any administrative
`mandatory_gates` entry (`wsib_clearance`, `cgl_insurance`, `bid_bond`,
`working_at_heights`, `addenda`, `non_collusion`, `site_visit`,
`years_in_business`, `references`), or any `red_flags` with
`category: "qualifications"`.

## Summary to User

- Bidder name
- Sub-scores (technical_approach, warranty_materials)
- Critical/high red flag counts
- Top 3 technical concerns
