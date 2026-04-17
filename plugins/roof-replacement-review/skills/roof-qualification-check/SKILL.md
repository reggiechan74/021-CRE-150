---
name: roof-qualification-check
description: >
  Use when evaluating a roofing contractor bid's mandatory pass/fail gates — WSIB
  clearance, CGL insurance, bonding, working-at-heights training, addenda, references,
  years in business. Populates `mandatory_gates` and contributes qualification-related
  red flags and sub-scores.
---

# Roof Qualification Check

You are the gatekeeper. Bids failing any mandatory requirement are non-compliant and excluded from rated scoring. Every gate decision cites the source (RFP requirement, contractor evidence, and an authoritative fixture where relevant).

## Reference Material

Ground truth for evaluation:

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

- Bid bond attached at the required percentage?
- Bonding capacity declared ≥ project value? (Fixture 04 §5)
- Consent of surety for performance and L&M bonds present?
- **Fail criteria:** Missing bid bond when required; no surety consent.

### 4. Working-at-Heights Training

- Contractor confirms all on-site workers have current O. Reg. 297/13 training (3-year validity)? (Fixture 04 §3)
- **Fail criteria:** Explicit denial or no mention when RFP requires confirmation.

### 5. Addenda Acknowledgment

- All issued addenda acknowledged in the Form of Tender?
- **Fail criteria:** Missing acknowledgment per CCDC 23 guidance (fixture 03).

### 6. Non-Collusion Declaration

- Signed and dated?
- **Fail criteria:** Missing or unsigned.

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

## Output per Gate

Write each gate result to `bid.mandatory_gates.<gate_name>`:

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

## Compliance Rule

A bid is compliant if and only if all gates are `pass`. `needs_clarification` blocks ranking until resolved — mark the bid as needing owner clarification, not yet compliant or non-compliant.

## Summary to User

- Bidder name
- Gate pass / fail / needs-clarification counts
- Compliance status
- Sub-scores (experience_references, qualifications_certifications, schedule)
- Critical qualification issues
