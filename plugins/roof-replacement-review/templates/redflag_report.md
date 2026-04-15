# Roof Replacement Tender — Red Flag Report

**Project:** {{project.property}}
**Owner:** {{project.owner}}
**RFP:** {{rfp.rfp_id}}
**Report date:** {{generated_at}}

---

## Executive Summary

- **Bids received:** {{bids|length}}
- **Compliant after mandatory gates:** {{comparison.compliant_bidders_count}}
- **Critical red flags:** {{red_flags_count.critical}} across {{red_flags_count.critical_bidders}} bidder(s)
- **High-severity red flags:** {{red_flags_count.high}}
- **Medium/low flags:** {{red_flags_count.medium}} / {{red_flags_count.low}}

---

## Stage 1 — Mandatory Gate Results

Pass/fail gates derived from the RFP. Any failure excludes the bid from rated scoring unless the owner accepts the deficiency.

{{#each bids}}
### {{bidder_name}}

| Gate | Result | Evidence |
|---|:---:|---|
| WSIB clearance, in good standing | {{mandatory_gates.wsib.result}} | {{mandatory_gates.wsib.evidence}} |
| CGL ≥ ${{rfp.mandatory_requirements.cgl_minimum_cad|comma}} | {{mandatory_gates.cgl.result}} | {{mandatory_gates.cgl.evidence}} |
| Owner named as additional insured | {{mandatory_gates.additional_insured.result}} | {{mandatory_gates.additional_insured.evidence}} |
| Completed-operations coverage ≥ {{rfp.mandatory_requirements.completed_operations_years}} yr | {{mandatory_gates.completed_ops.result}} | {{mandatory_gates.completed_ops.evidence}} |
| Bid bond {{rfp.mandatory_requirements.bid_bond_percent}}% | {{mandatory_gates.bid_bond.result}} | {{mandatory_gates.bid_bond.evidence}} |
| Working-at-heights training (O. Reg. 297/13) | {{mandatory_gates.wah_training.result}} | {{mandatory_gates.wah_training.evidence}} |
| Addenda acknowledgment | {{mandatory_gates.addenda.result}} | {{mandatory_gates.addenda.evidence}} |
| Non-collusion declaration | {{mandatory_gates.non_collusion.result}} | {{mandatory_gates.non_collusion.evidence}} |
| Minimum {{rfp.mandatory_requirements.minimum_years_in_business}} years in business | {{mandatory_gates.years_in_business.result}} | {{mandatory_gates.years_in_business.evidence}} |
| ≥ {{rfp.mandatory_requirements.minimum_similar_projects}} similar project references | {{mandatory_gates.references.result}} | {{mandatory_gates.references.evidence}} |

**Stage 1 status:** {{mandatory_summary}}

{{/each}}

---

## Stage 2 — Qualitative Red Flags

{{#each bids}}
### {{bidder_name}}

{{#if red_flags|length == 0}}
*No red flags identified.*
{{else}}
{{#each red_flags}}
**[{{severity|upper}}] {{category|title}} — {{description}}**
- Citation: {{citation}}
- Evidence: {{evidence}}
- Recommended owner action: {{recommendation}}

{{/each}}
{{/if}}

{{/each}}

---

## Cross-Bid Patterns

{{#if comparison.price_spread_percent > 15}}
- **Price spread {{comparison.price_spread_percent}}%** — exceeds 15% threshold. Review whether bids are scoped equivalently or if one is a low-bid outlier (Ron Engineering risk).
{{/if}}
{{#if cross_bid_patterns.common_exclusions|length > 0}}
- **Common exclusions:** {{cross_bid_patterns.common_exclusions|join:", "}} — consider issuing addendum or clarifying scope.
{{/if}}
{{#if cross_bid_patterns.substitution_convergence}}
- **Substitution convergence:** Multiple bidders substituting same item — may indicate specified product is unavailable or priced above market.
{{/if}}

---

## Severity Definitions

| Severity | Meaning | Default owner action |
|---|---|---|
| **Critical** | Non-compliant, voids warranty, or safety risk | Reject or require cure before award |
| **High** | Material deviation from RFP or industry standard | Negotiate correction or reject |
| **Medium** | Ambiguity or moderate risk | Request written clarification |
| **Low** | Minor note, document for file | Accept, note for contract admin |

---

*Red flags identified by `roof-technical-review` and `roof-qualification-check` skills against fixtures in `fixtures/domain_knowledge/`.*
