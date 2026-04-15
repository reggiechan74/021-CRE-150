# Memorandum

**To:** {{project.owner}} — {{memo.recipient_title}}
**From:** {{memo.author}}
**Date:** {{generated_at|date}}
**Re:** Roof Replacement Tender — Recommendation of Award, {{project.property}}

---

## 1. Recommendation

Award the roof replacement contract for **{{project.property}}** to **{{recommended_bid.bidder_name}}** at a contract price of **${{recommended_bid.pricing.grand_total|comma}} (incl. HST)**, subject to the award conditions set out in §5.

Basis: highest weighted score ({{recommended_bid.scores.weighted_total}}/100) among compliant bidders, with no critical red flags and {{recommended_bid.qualifications.years_in_business}} years of relevant Ontario experience.

---

## 2. Tender Summary

| Item | Detail |
|---|---|
| RFP issued | {{rfp.issued_date}} |
| Submissions received | {{bids|length}} |
| Compliant after mandatory gates | {{comparison.compliant_bidders_count}} |
| Low compliant bid | ${{comparison.price_low_cad|comma}} |
| High compliant bid | ${{comparison.price_high_cad|comma}} |
| Price spread | {{comparison.price_spread_percent}}% |
| Roof type | {{project.roof_type|humanize}} |
| Area | {{project.roof_area_sqft|comma}} sq ft |
| Building classification | {{project.building_classification|upper}} |
| Occupied during work | {{project.occupied_during_work}} |

---

## 3. Ranking

| Rank | Bidder | Price | Weighted Score | Status |
|---:|---|---:|---:|---|
{{#each ranked_bids}}
| {{scores.rank}} | {{bidder_name}} | ${{pricing.grand_total|comma}} | {{scores.weighted_total}} | {{status|humanize}} |
{{/each}}
{{#each non_compliant_bids}}
| — | {{bidder_name}} | ${{pricing.grand_total|comma}} | excluded | Non-compliant: {{exclusion_reason}} |
{{/each}}

See `scoring_matrix.md` for detailed sub-scores and `redflag_report.md` for gate results and qualitative issues.

---

## 4. Rationale for Recommendation

### Why {{recommended_bid.bidder_name}}

{{#each recommendation_rationale.strengths}}
- {{this}}
{{/each}}

### Why not the low bid
{{#if low_bid_not_recommended}}

The lowest-priced compliant bid ({{low_compliant_bid.bidder_name}} at ${{low_compliant_bid.pricing.grand_total|comma}}) was not recommended because:

{{#each low_bid_concerns}}
- {{this}}
{{/each}}

The {{recommended_vs_low_price_delta_percent}}% price premium over the low bid is justified by {{price_premium_justification}}.

{{else}}

The recommended bidder also submitted the lowest compliant bid.

{{/if}}

---

## 5. Conditions of Award

Contract execution should be subject to the following items being resolved in writing:

{{#each award_conditions}}
{{@index}}. {{this}}
{{/each}}

---

## 6. Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
{{#each risks}}
| {{description}} | {{likelihood}} | {{impact}} | {{mitigation}} |
{{/each}}

---

## 7. Contract Administration Notes

- **Contract form recommended:** {{contract_form_recommendation}}
- **Holdback:** 10% statutory holdback under Ontario's *Construction Act*
- **Progress payments:** Monthly, certified by {{progress_payment_certifier}}
- **Substantial performance:** Publish at 97% completion per *Construction Act* s. 2
- **Warranty commencement:** From date of substantial performance
- **Post-installation inspection:** Schedule manufacturer inspection within {{warranty_inspection_days}} days of substantial performance to validate warranty

---

## 8. Decision Requested

Approval to award the roof replacement contract to **{{recommended_bid.bidder_name}}** at ${{recommended_bid.pricing.grand_total|comma}} (incl. HST), subject to the award conditions in §5.

---

**Attachments**
- A: Scoring Matrix (`scoring_matrix.md`)
- B: Red Flag Report (`redflag_report.md`)
- C: Tender Manifest (`manifests/tender_manifest.json`)
- D: Extraction Audit Log (`audit_log.md`)

*Prepared using `roof-replacement-review` plugin v{{plugin_version}}. Source citations in audit log.*
