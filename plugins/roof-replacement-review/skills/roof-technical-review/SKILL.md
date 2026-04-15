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

## Reference Material

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

Produce raw sub-scores (0-100) for rated criteria this skill owns. Write them into `bid.scores`:

| Sub-score | What to grade | Anchors |
|---|---|---|
| `technical_approach` | Methodology quality, sequencing, protection plans, site safety | 100 = comprehensive, PM-level detail; 75 = solid outline; 50 = minimum narrative; 25 = boilerplate; 0 = missing |
| `warranty_materials` | Warranty tier + materials quality | 100 = total-system NDL 20-30 yr, certified installer, premium materials; 75 = labour+material 15-20 yr, quality materials; 50 = material-only 10-15 yr; 25 = prorated or unclear; 0 = non-compliant |

Use fixture 03 §3 five-point rubric anchors for consistency.

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

- **Critical:** non-compliance voids warranty, fails OBC, or is a safety hazard. Examples: no cover board on commercial polyiso with NDL warranty claim; installer not certified for the warranty tier claimed; no fall protection plan on a parapet-less roof.
- **High:** material deviation from RFP or industry best practice. Examples: 45 mil TPO proposed for commercial; wind uplift basis missing; warranty type `unclear`.
- **Medium:** ambiguity worth clarifying. Examples: substitution with partial justification; insulation R-value not explicitly stated but system implies compliance.
- **Low:** cosmetic or documentation gaps. Examples: missing product data sheet for accessory materials.

## Output

Append to the bid manifest in-place (update `red_flags`, `scores.technical_approach`, `scores.warranty_materials`). Do not touch mandatory gates — that's the qualification-check skill.

## Summary to User

- Bidder name
- Sub-scores (technical_approach, warranty_materials)
- Critical/high red flag counts
- Top 3 technical concerns
