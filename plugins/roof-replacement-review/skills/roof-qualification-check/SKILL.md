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
- "In good standing"? (Note: fixture 04 §1.4 — only the online verifier at `clearances.wsib.ca` is authoritative. If the bid attaches a PDF certificate, flag `needs_clarification` recommending the owner verify online before award.)
- **Fail criteria:** No certificate, expired, or not in good standing.

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

- Count ≥ RFP minimum?
- References similar in scope (not residential if this is commercial, etc.)?
- Project values within reasonable range of this project?
- **Needs_clarification criteria:** References present but similarity questionable (scope or size divergence).
- **Fail criteria:** Count below threshold.

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

## Qualification Red Flags

In addition to gate results, append qualitative flags to `bid.red_flags[]` for issues that don't rise to a fail but warrant owner attention:

- Certification programs claimed but lapsed (fixture 02 §3)
- Subcontracting the actual roofing crew to unnamed entities (fixture 04 §5)
- References that include affiliated entities
- Pattern of Ministry of Labour orders in past 3 years (if surfaced in extraction)
- WSIB rate notably above industry average (financial-distress signal per fixture 04 §5)

## Sub-Scores

Produce raw sub-scores (0-100) for:

- `experience_references` — based on count, similarity, and recency of references (100 = 5+ directly comparable projects completed within 3 yrs; 75 = 3-4 comparable; 50 = minimum count, partial similarity; 25 = bare minimum; 0 = inadequate, flagged as fail)
- `qualifications_certifications` — years in business, Skilled Trades C of Q count, CRCA membership, manufacturer certifications (100 = 15+ yrs + CRCA + multiple certifications + full C of Q crew; 75 = 10+ yrs + one certification; 50 = 5+ yrs + basic compliance; 25 = minimum; 0 = below minimum)
- `schedule` — reasonableness vs project scope, crew size adequacy, occupied-building accommodation (100 = detailed Gantt + surge crew on occupied buildings; 75 = realistic timeline + crew; 50 = meets required dates; 25 = aggressive/vague; 0 = unrealistic or absent)

## Compliance Rule

A bid is compliant if and only if all gates are `pass`. `needs_clarification` blocks ranking until resolved — mark the bid as needing owner clarification, not yet compliant or non-compliant.

## Summary to User

- Bidder name
- Gate pass / fail / needs-clarification counts
- Compliance status
- Sub-scores (experience_references, qualifications_certifications, schedule)
- Critical qualification issues
