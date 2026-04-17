---
name: roof-qualification-check
description: >
  Use when evaluating a roofing contractor bid's mandatory pass/fail gates — WSIB
  clearance, CGL insurance, bonding, working-at-heights training, addenda, references,
  years in business. Populates `mandatory_gates` and contributes qualification-related
  red flags and sub-scores.
---

# Roof Qualification Check

You are the gatekeeper for **administrative and qualification** gates. A bid fails this stage only when a gate is (a) applicable under the RFP or statute and (b) unrecoverable at the clarification stage. Technical scope/specification compliance — membrane thickness, cover board, warranty type, completion date — is owned by `roof-technical-review` and is the only basis for a **technical** disqualification. Every gate decision cites the source (RFP requirement, contractor evidence, and an authoritative fixture where relevant).

## What goes in `mandatory_gates` — and what does NOT

`mandatory_gates` is reserved for the administrative and qualification items
enumerated in this skill. **Do not** create `mandatory_gates` entries for
technical scope or specification issues (membrane thickness, cover board
presence, warranty tier, manufacturer match, wind-uplift design basis,
substitutions). Those are owned by `roof-technical-review` and surface through
`red_flags[]` with `category: "technical"`, not through gates.

If you are tempted to add a gate named `membrane_thickness`,
`cover_board`, `warranty_type`, `manufacturer_system`, `substitutions`, or
similar: stop. That's a technical finding. It belongs in a red flag, not a
gate. Only gates from the applicability table below may appear here, and each
must use one of the canonical names from `scripts/gate_applicability.py`.

Why this matters: `scripts/score.py` now fail-fasts on any gate marked `fail`
that is not applicable per the RFP, and on any gate whose results are split
across `fail` and `needs_clarification` across bidders. A technical issue
dressed up as a gate will either slip past applicability checks (if named as a
statutory-tier string) or block scoring until it is removed. Either way you
have created a defect. Keep technical findings in `red_flags[]`.

## Gate applicability — which gates can fail a bidder?

Before evaluating any gate, classify it into one of three tiers. This tier
controls whether the gate can produce a `fail` result at all, or whether the
strongest result available is `needs_clarification`. Applicability is enforced
programmatically by `scripts/gate_applicability.py` and cross-checked by
`scripts/reconcile_gates.py` — the code is the source of truth; this section
documents the contract.

- **Statutory** — Ontario law or Construction Act baseline. Always applicable,
  regardless of RFP text. Can fail a bidder.
  - `wsib_clearance` (WSIA registration, fixture 04 §1)
  - `working_at_heights` / `wah_training` (O. Reg. 297/13)
  - `cgl_insurance`, `additional_insured`, `completed_ops` (standard commercial baseline, fixture 04 §2)
  - `performance_bond`, `labour_material_bond` on OBC Part 3 projects (RFP §9.2 / Construction Act)
- **RFP-specified** — applicable only if the RFP invokes the gate via a
  populated `rfp.mandatory_requirements.<field>` OR names the item verbatim in
  `rfp.submission_requirements[]`. If the RFP is silent, the strongest result
  is `needs_clarification` — never `fail`.
  - `bid_bond` (applicable only if `bid_bond_percent` > 0 or submission_requirements mentions it)
  - `site_visit` / `site_visit_required`
  - `minimum_years_in_business` / `years_in_business`
  - `similar_project_references` / `references`
- **Prudent-evaluator** — items a careful evaluator asks about but which are
  not RFP requirements unless explicitly declared. Default: clarify only.
  Never a fail.
  - `addenda_acknowledgment` / `addenda`
  - `non_collusion_declaration` / `non_collusion`

If you cannot tell which tier a gate belongs to, treat it as
**prudent-evaluator** and mark `needs_clarification` rather than `fail`.

## Compliance Rule (revised)

Three-tier status, computed by `scripts/score.py` from the set of gate results:

- **compliant** — every applicable gate `pass`.
- **conditional** — no gate `fail`, but at least one `needs_clarification`.
  These bids **are scored and ranked** alongside compliant bids. Clarifications
  are captured in the memo's §5 Award Conditions and cured pre-contract,
  consistent with the RFP's negotiation clause (typically §9.1). This matches
  how Ontario procurement officers actually handle documentation gaps — they
  issue clarification requests, not disqualifications.
- **non_compliant** — at least one gate `fail` on a statutory or
  RFP-specified gate. Excluded from rated scoring. Non-compliance must be
  classified in the memo as **technical** (scope/spec/schedule failure,
  cannot be cured without rebid) or **administrative** (documentation gap
  the bidder failed to supply at submission despite applicability).

## Reference Material

**Read only these fixtures — do not load `01_ontario_roofing_codes.md` or `02_roofing_materials_warranties.md`, which are owned by `roof-technical-review`:**

- `fixtures/domain_knowledge/04_contractor_qualification.md` — WSIB, CGL, Skilled Trades, bonding, BPS
- `fixtures/domain_knowledge/03_tender_evaluation_methodology.md` §2 — mandatory vs rated split, Contract A/B doctrine (Ron Engineering 1981 SCC)

## Gate Evaluation

For each mandatory requirement in `rfp.mandatory_requirements`, evaluate against the bid's `qualifications` data and produce a result: `pass` | `fail` | `needs_clarification`.

### 1. WSIB Clearance

- Bid attaches certificate? `wsib_clearance_attached = true`?
- Date within current validity window (per fixture 04 §1.3 — standard 90 days, but check WSIB's current cycle; the fixture notes a temporary quarterly renewal program active through 2026)?
- "In good standing" text present on the attached certificate?
- **Pass criteria:** Certificate attached + within validity window + good-standing text present. The PDF is not the final word (fixture 04 §1.4 — only the online verifier at `clearances.wsib.ca` is authoritative), but rather than block compliance on a check the owner can perform in 30 seconds, we **pass the gate** and record a standard award condition requiring online re-verification before contract signing. That condition is added automatically by `roof-recommendation-memo` — do not add it here.
- **Needs_clarification criteria:** Certificate attached but unclear validity window (no date or ambiguous "in good standing" wording).
- **Fail criteria:** No certificate, expired, or the certificate itself says "not in good standing" / "account in arrears."

### 2. CGL Insurance

- Limit ≥ RFP minimum (`cgl_minimum_cad`)?
- Owner named as additional insured on the COI?
- Completed-operations coverage ≥ required years? (Fixture 04 §2 — critical for the post-install warranty period)
- Named insured matches bidder legal entity? (Shell-company risk per fixture 04 §5)
- **Fail criteria:** Limit below required, owner not named, no completed-ops tail, named insured mismatch.

### 3. Bid Bond / Bonding

**Applicability check first:** bid bond is RFP-specified. Fail is allowed only
if `rfp.mandatory_requirements.bid_bond_percent` is set or
`rfp.submission_requirements` names a bid bond. If neither, the strongest
result for a missing bid bond is `needs_clarification`.

- Bid bond attached at the required percentage (if applicable)?
- Bonding capacity declared ≥ project value? (Fixture 04 §5) — always evaluable; below project value is a `needs_clarification` when the RFP is silent on bid bonds, not a fail.
- Consent of surety for performance and L&M bonds present? — performance/L&M are statutory on Part 3; missing consent of surety on the successful bidder is a fail at contract signing, not at submission. At submission stage, mark `needs_clarification`.
- **Fail criteria:** Missing bid bond when the RFP specifies bid_bond_percent or explicitly lists a bid bond in submission_requirements.

### 4. Working-at-Heights Training

- Contractor confirms all on-site workers have current O. Reg. 297/13 training (3-year validity)? (Fixture 04 §3)
- **Fail criteria:** Explicit denial or no mention when RFP requires confirmation.

### 5. Addenda Acknowledgment

**Prudent-evaluator tier.** Never fail. If missing, mark `needs_clarification`
so the owner can request a signed acknowledgment before contract execution.

- All issued addenda acknowledged in the Form of Tender?
- **Needs_clarification criteria:** Missing acknowledgment. Per CCDC 23 the
  owner can still accept the bid and require the acknowledgment as a
  condition of award.
- **Fail criteria:** Only when `rfp.mandatory_requirements.addenda_acknowledgment_required`
  is explicitly true AND the bid contradicts or refuses addenda terms.

### 6. Non-Collusion Declaration

**Prudent-evaluator tier.** Never fail. A missing declaration is clarifiable;
a declaration present but contradicted by evidence of collusion is a separate
matter (escalate to the owner's counsel).

- Signed and dated?
- **Needs_clarification criteria:** Missing or unsigned. Owner requests a
  signed declaration before award.
- **Fail criteria:** Only when `rfp.mandatory_requirements.non_collusion_declaration_required`
  is explicitly true AND the declaration is not signed after clarification.

### 7. Minimum Years in Business

- Meets RFP minimum?
- **Fail criteria:** Below threshold.

### 8. Similar Project References

A reference is **comparable** to this project if ALL three hold:
1. Same building-code class (commercial ↔ commercial, residential ↔ residential — Part 3 and Part 9 don't substitute for each other)
2. Project value within 0.5× to 2× the subject project's value
3. Completed within the last 5 years

- Count of **comparable** references ≥ RFP minimum?
- **Needs_clarification criteria:** References present and count meets minimum, but one or more fail the comparable test above (scope or size or recency divergence).
- **Fail criteria:** Count of comparable references below RFP minimum.

### 9. Site Visit (if required)

- Bid confirms attendance at mandatory pre-bid site meeting?
- **Fail criteria:** Required but not attended.

## Sidecar Output File

Write your results to a **sidecar** JSON file so the technical-review skill can
run in parallel without clobbering your writes:

**Path:** `<rfp-dir>/roof-review-output/manifests/bid_<slug>.qual.json`

**Shape:**

```json
{
  "bidder_id": "<same as base bid manifest>",
  "mandatory_gates": { "<gate_name>": { "result": "...", "evidence": "...", "notes": "..." } },
  "scores": {
    "experience_references": <0-100>,
    "qualifications_certifications": <0-100>,
    "schedule": <0-100>
  },
  "scoring_rationale": {
    "experience_references": { "sub_factors": { "...": <points> } },
    "qualifications_certifications": { "sub_factors": { "...": <points> } },
    "schedule": { "sub_factors": { "...": <points> } }
  },
  "red_flags": [
    { "severity": "...", "category": "qualifications", "description": "...", ... }
  ]
}
```

**Do NOT** touch the base `bid_<slug>.json` — the technical-review skill is
writing `bid_<slug>.tech.json` concurrently and `scripts/normalize.py` will
merge all three files. A write to `bid_<slug>.json` from this skill is a bug.

Keys this sidecar MAY contain: `bidder_id`, `mandatory_gates`, `scores`,
`scoring_rationale`, `red_flags` (only `category: "qualifications"`).

Keys this sidecar MUST NOT contain: `scores.technical_approach`,
`scores.warranty_materials`, any `mandatory_gates` entry from the technical
table in `roof-technical-review` (scope_compliance, membrane_thickness,
cover_board, insulation_upgrade, warranty_type, warranty_duration,
completion_date, mobilization_date, fire_rating, wind_uplift), or any
`red_flags` with a category other than `qualifications`.

## Output per Gate

Write each gate result into the sidecar file's `mandatory_gates.<gate_name>`:

```json
{
  "result": "pass|fail|needs_clarification",
  "evidence": "page reference + what was found or missing",
  "notes": "any calibration comments"
}
```

## Red Flag Category Ownership

This skill owns exactly one `red_flags.category` value: `qualifications`. Everything warranty/materials/safety/scope/substitutions belongs to `roof-technical-review` — do not write those categories here even if you notice the issue. If a single problem has two aspects (e.g., a lapsed certification that also affects warranty eligibility), record the qualifications aspect here and let technical-review record the warranty aspect.

## Qualification Red Flags

In addition to gate results, append qualitative flags to `bid.red_flags[]` with `category: "qualifications"` for issues that don't rise to a fail but warrant owner attention:

- Certification programs claimed but lapsed (fixture 02 §3)
- Subcontracting the actual roofing crew to unnamed entities (fixture 04 §5)
- References that include affiliated entities
- Pattern of Ministry of Labour orders in past 3 years (if surfaced in extraction)
- WSIB rate notably above industry average (financial-distress signal per fixture 04 §5)

## Sub-Scores

Produce raw sub-scores (0-100) for the three rated criteria this skill owns. Each is computed as the **sum of sub-factor points**, not a single anchor match. Record the per-sub-factor points in `bid.scoring_rationale.<sub_score>.sub_factors` so the audit trail shows the math.

### `experience_references` (sum of three sub-factors, max 100)

| Sub-factor | Points | Criterion |
|---|---|---|
| Count of **comparable** references (Gate 8 definition) | 0 | zero comparable |
|  | 20 | 1-2 comparable |
|  | 40 | 3-4 comparable |
|  | 60 | 5+ comparable |
| Recency of most-recent comparable reference | 0 | >5 yrs or none |
|  | 10 | 3-5 yrs |
|  | 20 | 1-2 yrs |
|  | 25 | <1 yr |
| Verifiability (named contact, value, date, photo/contact for site) | 0 | missing most fields |
|  | 8 | partial (contact only, or value only) |
|  | 15 | complete on every reference |

If `experience_references` = 0 and RFP minimum reference count is unmet, the bid fails Gate 8 (handled there, not here).

### `qualifications_certifications` (sum of four sub-factors, max 100)

| Sub-factor | Points | Criterion |
|---|---|---|
| Years in business (from `qualifications.years_in_business`) | 0 | <5 yrs |
|  | 15 | 5-9 yrs |
|  | 25 | 10-14 yrs |
|  | 35 | 15+ yrs |
| Manufacturer certification at or above warranty tier claimed | 0 | none |
|  | 15 | certified at required tier with one manufacturer |
|  | 25 | multiple manufacturer certifications |
|  | 30 | top-tier program (e.g., GAF Master Elite, Soprema PAQ+S, Firestone Platinum Master Contractor) |
| Skilled Trades C of Q crew | 0 | none identified |
|  | 10 | foreman only |
|  | 15 | majority of crew |
|  | 20 | full crew |
| Industry membership | 0 | none |
|  | 8 | regional/provincial association |
|  | 15 | CRCA member |

### `schedule` (sum of four sub-factors, max 100)

| Sub-factor | Points | Criterion |
|---|---|---|
| Timeline realism vs scope | 0 | unrealistic or absent |
|  | 15 | aggressive with thin justification |
|  | 30 | realistic duration |
|  | 40 | detailed phase sequencing + milestones |
| Crew adequacy | 0 | crew size not stated |
|  | 15 | minimum crew for scope |
|  | 20 | adequate + named foreman |
|  | 25 | multiple crews / surge capacity for occupied buildings |
| Mobilization and completion dates vs RFP | 0 | misses RFP dates |
|  | 10 | meets substantial completion only |
|  | 20 | meets both mobilization and completion |
| Occupied-building accommodation (auto-15 if building is vacant — do not penalize) | 0 | not addressed |
|  | 8 | generic after-hours / dust commitments |
|  | 15 | named tenant-coordination plan + communication protocol |

## Compliance Rule (see the revised rule at the top of this skill)

The three-tier model (`compliant` / `conditional` / `non_compliant`) is
computed in `scripts/score.py::compliance_status()`. Do not reimplement
compliance logic here — emit gate results and let the scoring pipeline
assemble the tier. Cross-bid uniformity and applicability are audited by
`scripts/reconcile_gates.py` after scoring.

## Summary to User

- Bidder name
- Gate pass / fail / needs-clarification counts
- Compliance status
- Sub-scores (experience_references, qualifications_certifications, schedule)
- Critical qualification issues
