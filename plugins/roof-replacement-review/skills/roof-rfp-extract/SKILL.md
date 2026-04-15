---
name: roof-rfp-extract
description: >
  Use when the user asks to parse, extract, or normalize an owner's roof replacement RFP
  or tender document PDF into a structured schema. Works on Ontario commercial (OBC Part 3)
  and residential (OBC Part 9) roof projects.
---

# Roof RFP Extract

You are parsing an owner's roof replacement RFP into the normalized schema at
`templates/bid_schema.json` (§`project` and §`rfp` sections). Your output drives
every downstream skill in this plugin — extraction accuracy is the foundation.

## Reference Material

Before extracting, be aware of the fixtures you must cite for classification decisions:

- `fixtures/domain_knowledge/01_ontario_roofing_codes.md` — OBC Part 3 vs Part 9 triggers, SB-10/SB-12 applicability, WAH and environmental requirements
- `fixtures/domain_knowledge/02_roofing_materials_warranties.md` — membrane/shingle system categories, thickness conventions
- `fixtures/domain_knowledge/03_tender_evaluation_methodology.md` — default MCDA weighting, price scoring methods, mandatory gate conventions

## Extraction Order

1. **Classify the project.** Determine `building_classification`:
   - `obc_part_3` if: >3 storeys, >600 m² footprint, or occupancy is assembly/institutional/business/mercantile/industrial/high-hazard
   - `obc_part_9` if: houses, duplexes, small residential, or buildings ≤3 storeys AND ≤600 m²
   - If ambiguous, default to the more restrictive (`obc_part_3`) and flag in `extraction_notes`.

2. **Classify the roof type.** `low_slope_commercial` (<2:12), `steep_slope_residential`, `steep_slope_commercial`, or `mixed`.

3. **Extract scope.** From the tender's scope of work section:
   - Tear-off vs recover
   - Specified membrane/shingle system, thickness, attachment
   - Manufacturer acceptable list
   - Allowances (especially wood deck replacement per board-foot)
   - Insulation upgrade to SB-10/SB-12 (retrofits must comply per §1.3 of the Ontario codes fixture)
   - Included items, excluded items, alternates requested

4. **Extract warranty requirements.** Minimum years, warranty type (material-only vs NDL — see fixture 02 §1 for taxonomy), manufacturer certification requirement.

5. **Extract mandatory requirements.** Each gate in §`rfp.mandatory_requirements` — set to actual value if specified in RFP, otherwise leave default.

6. **Extract evaluation criteria weighting.** If the RFP states weights, use them. If not, apply defaults from fixture 03 §3 adjusted for project context:
   - Occupied commercial → raise schedule + technical approach
   - Heritage/complex → raise technical
   - BPS/public → raise price (BPS Procurement Directive implications)
   - Straightforward re-roof → defaults

7. **Record extraction provenance.** For each non-default value, record the RFP page/section where you found it in `_provenance` (sidecar structure keyed by JSON path).

## Output

Write the manifest to `<rfp-dir>/roof-review-output/manifests/rfp.json`, conforming to the `project` and `rfp` portions of the schema. Include:

```json
{
  "project": { ... },
  "rfp": { ... },
  "_provenance": {
    "rfp.scope_of_work.membrane_system_specified.category": "page 12, §3.2",
    "rfp.warranty_requirements.warranty_type_required": "page 18, §5.1"
  },
  "extraction_notes": ["classified as obc_part_3 due to 4-storey occupied office"]
}
```

## Defaults to Apply if RFP Is Silent

- `owner_type`: infer from owner name (condo/municipal/school board/hospital obvious; else `private_commercial` or `private_residential` based on building classification)
- `evaluation_criteria.weighting`: apply defaults (Price 45 / Technical 15 / Experience 15 / Warranty 10 / Schedule 5 / Qualifications 10) — note in `extraction_notes` that defaults were used
- `mandatory_requirements.cgl_minimum_cad`: 5000000 for OBC Part 3, 2000000 for OBC Part 9
- `warranty_requirements.warranty_type_required`: `total_system_ndl` for Part 3, `labour_and_material` for Part 9

## Red Flags to Raise at RFP Extraction Stage

If the RFP itself is deficient, record these in `extraction_notes` so the owner can fix before receiving bids:

- Mandatory requirements missing entirely (bids will be non-comparable)
- Evaluation weighting not disclosed (Ontario Contract A/B law — privilege clauses don't cure undisclosed criteria; see fixture 03 §1)
- Warranty type not specified (bidders will offer cheapest interpretation)
- No allowance for wood deck replacement (extras will blow the budget)
- No specification for cover board over polyiso on commercial (voids most NDL warranties per fixture 02 §1)

## Summary to User

When done, tell the user:
- Classification outcome (Part 3 or Part 9, roof type)
- Roof area and specified system
- Mandatory gate count
- Evaluation weighting applied (default or from RFP)
- Any RFP-level deficiencies noted
- Path to the written manifest
