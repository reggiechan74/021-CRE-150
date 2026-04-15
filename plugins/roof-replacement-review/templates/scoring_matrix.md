# Roof Replacement Tender — Scoring Matrix

**Project:** {{project.property}}
**Owner:** {{project.owner}}
**RFP:** {{rfp.rfp_id}} — issued {{rfp.issued_date}}
**Submissions received:** {{comparison.compliant_bidders_count}} of {{bids|length}}
**Evaluation date:** {{generated_at}}

---

## Weighting Applied

| Criterion | Weight |
|---|---:|
| Price | {{rfp.evaluation_criteria.weighting.price}}% |
| Technical Approach | {{rfp.evaluation_criteria.weighting.technical_approach}}% |
| Experience & References | {{rfp.evaluation_criteria.weighting.experience_references}}% |
| Warranty & Materials | {{rfp.evaluation_criteria.weighting.warranty_materials}}% |
| Schedule | {{rfp.evaluation_criteria.weighting.schedule}}% |
| Qualifications & Certifications | {{rfp.evaluation_criteria.weighting.qualifications_certifications}}% |
| **Total** | **100%** |

Price scoring method: `{{rfp.evaluation_criteria.price_scoring_method}}`.

---

## Compliance Summary

{{#each bids}}
- **{{bidder_name}}** — {{#if all_mandatories_pass}}✅ Compliant{{else}}❌ Non-compliant ({{failed_gates|join:", "}}){{/if}}
{{/each}}

*Non-compliant bids are excluded from rated scoring below.*

---

## Rated Scoring (Compliant Bids Only)

| Rank | Bidder | Price ({{rfp.evaluation_criteria.weighting.price}}) | Technical ({{rfp.evaluation_criteria.weighting.technical_approach}}) | Experience ({{rfp.evaluation_criteria.weighting.experience_references}}) | Warranty ({{rfp.evaluation_criteria.weighting.warranty_materials}}) | Schedule ({{rfp.evaluation_criteria.weighting.schedule}}) | Qualifications ({{rfp.evaluation_criteria.weighting.qualifications_certifications}}) | **Weighted Total** |
|---:|---|---:|---:|---:|---:|---:|---:|---:|
{{#each ranked_bids}}
| {{scores.rank}} | {{bidder_name}} | {{scores.price}} | {{scores.technical_approach}} | {{scores.experience_references}} | {{scores.warranty_materials}} | {{scores.schedule}} | {{scores.qualifications_certifications}} | **{{scores.weighted_total}}** |
{{/each}}

---

## Pricing Comparison

| Bidder | Base Bid | HST | Allowances | Total | Δ vs Low |
|---|---:|---:|---:|---:|---:|
{{#each bids}}
| {{bidder_name}} | ${{pricing.base_bid_cad|comma}} | {{pricing.hst_included}} | ${{pricing.allowances_total|comma}} | ${{pricing.grand_total|comma}} | {{pricing.delta_vs_low_percent}}% |
{{/each}}

**Low bid:** ${{comparison.price_low_cad|comma}}
**High bid:** ${{comparison.price_high_cad|comma}}
**Spread:** {{comparison.price_spread_percent}}%

{{#if comparison.price_spread_percent > 15}}
> ⚠️ Spread exceeds 15% — review for scope divergence or low-bid risk (see red-flag report).
{{/if}}

---

## Scoring Rationale

{{#each ranked_bids}}
### {{scores.rank}}. {{bidder_name}} — {{scores.weighted_total}} pts

**Strengths:** {{scoring_rationale.strengths|join:"; "}}
**Weaknesses:** {{scoring_rationale.weaknesses|join:"; "}}
**Key differentiator:** {{scoring_rationale.differentiator}}

{{/each}}

---

*Scoring produced by `roof-score-matrix` skill. Mandatory gate evaluation per `roof-qualification-check`. Technical evaluation per `roof-technical-review`.*
