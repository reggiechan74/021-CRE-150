---
name: roof-bid-extract
description: >
  Use when the user asks to parse, extract, or normalize a roofing contractor's bid
  or tender submission PDF against a previously-parsed RFP. Captures pricing, scope
  response, materials, warranty, qualifications, schedule, and technical approach,
  with page-level evidence citations.
---

# Roof Bid Extract

You are extracting a single contractor's bid submission into the `bids[]` schema
in `templates/bid_schema.json`. The RFP manifest (`rfp.json`) defines what must
be populated and what values are expected.

## Inputs

1. **Bid PDF** — the contractor's submission. This is the only input this skill
   needs. It extracts bid facts verbatim from the submission.

**This skill does NOT require the RFP manifest.** Comparison against the RFP
(mandatory-gate evaluation, warranty-tier match, spec compliance) is performed
by `roof-qualification-check` and `roof-technical-review` in the next pipeline
wave. Keeping bid-extract RFP-independent is what lets `/roof-review` dispatch
`roof-rfp-extract` and `roof-bid-extract` in parallel during wave 1.

If you feel you need to check a value against the RFP here, stop — record what
the bid says in `extraction_notes` and defer the comparison to the downstream
skills.

## Reference Material

Cite these when flagging extraction anomalies (to be graduated into red flags later):

- `fixtures/domain_knowledge/02_roofing_materials_warranties.md` — warranty taxonomy (material-only vs NDL), membrane thickness conventions, certified installer programs
- `fixtures/domain_knowledge/04_contractor_qualification.md` — WSIB, CGL, bonding, Skilled Trades, WAH evidence expectations
- `fixtures/domain_knowledge/03_tender_evaluation_methodology.md` — typical bid document structure (CCDC 23 §5)

## Extraction Order

1. **Bidder identity.** Legal name (important — must match COI named insured), bid bond principal, and any trade names. Flag mismatches.

2. **Pricing.**
   - Base bid (note HST-included vs plus-HST — a silent HST treatment is a red flag to raise later)
   - Alternates, each with description + price
   - Unit prices (deck replacement per bf, flashing per lf, insulation per sq ft per R)
   - Allowances carried (each with item + amount)

3. **Scope response.**
   - Full-compliance claim (yes/no)
   - Explicit exclusions — capture verbatim
   - Clarifications / qualifications to the scope
   - Substitutions proposed — capture `spec_item`, `substitute_offered`, and the contractor's equivalence justification verbatim

4. **Materials system.** Manufacturer + system name, actual membrane thickness (for commercial) or shingle line (for residential), insulation stack including cover board, product data sheet attachments.

5. **Warranty offered.**
   - Manufacturer years and type. Use this taxonomy (derived from fixture 02 §1 and §4.5):
     - `material_only` — manufacturer replaces defective materials; labour and consequential damages are the owner's problem. Typical 10-15 yr.
     - `labour_and_material` — materials plus contractor labour to re-install covered by the manufacturer, but coverage is capped (e.g., prorated, or a dollar cap equal to original system cost).
     - `ndl` — no dollar limit on materials replacement; labour may or may not be included; read the exemplar warranty to confirm. If the bid says "NDL" without a system-warranty document attached, treat as `ndl` (not `total_system_ndl`).
     - `total_system_ndl` — the premium tier: no dollar limit on the full assembly (membrane + insulation + flashings + labour to reinstall). Requires certified installer, pre-install drawing review, and manufacturer mid-job inspection. Examples: Soprema Sopra-Garantie Mammouth Platinum, Firestone Red Shield Platinum, Sika Sarnafil 30-yr NDL. If the bid attaches a named system-warranty program meeting these prerequisites, use this value.
     - `prorated` — coverage declines on a schedule (common on asphalt shingle residential).
     - `unclear` — if the bid says "25 year" without specifying which of the above, set `unclear` and raise a red flag later. Do not guess.
   - Workmanship years from the contractor (typically 2-10 yrs — fixture 02 §3)
   - Wind uplift coverage mph
   - Certified installer status + program name (e.g., GAF Master Elite, Soprema PAQ+S, Firestone Red Shield)

6. **Qualifications.**
   - Years in business
   - WSIB clearance (attached? date? good standing? — fixture 04 §1)
   - CGL (limit, completed ops years, owner as additional insured? — fixture 04 §2)
   - Bid bond attached? Bonding capacity declared?
   - Working-at-heights training declared? — fixture 04 §3
   - CRCA member? Skilled Trades C of Q holders on crew?
   - References provided (project name, contact, value, completion year, similar scope?)
   - Subcontracting declared and subcontractors named?

7. **Schedule.** Mobilization days, work duration, substantial completion target, crew size, occupied-building accommodation plan.

8. **Technical approach.** Tear-off staging, weather protection, fall protection, waste disposal, site safety plan attached?

## Evidence Citations

For every non-trivial extracted value, record the page reference in the source PDF in `_provenance`:

```json
"_provenance": {
  "pricing.base_bid_cad": "Form of Tender, page 3",
  "warranty_offered.manufacturer_years": "Schedule C, page 11",
  "qualifications.wsib_clearance_date": "Appendix A, WSIB Clearance attached"
}
```

For the `warranty_offered` field specifically, also populate `warranty_offered.evidence_page` — the downstream technical review skill uses it directly.

## Extraction Notes

Record in `extraction_notes` (array on the bid) any:

- Fields you could not extract (with PDF page where you looked)
- Ambiguous language (e.g., "25-year warranty" with no type specified)
- Contradictions (e.g., Form of Tender says $450,000 but Schedule A totals $465,000)
- Attachments claimed but missing from the PDF

## Output

Write to `<rfp-dir>/roof-review-output/manifests/bid_<slug>.json`. Return the single bid object — the normalize script will array these together.

## Summary to User

- Bidder legal name
- Base bid (and HST treatment)
- Declared exclusions count
- Substitutions proposed count
- Warranty headline (years + type)
- Any fields flagged in `extraction_notes` for owner follow-up
- Path to written manifest
