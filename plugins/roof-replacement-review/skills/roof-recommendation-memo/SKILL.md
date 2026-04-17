---
name: roof-recommendation-memo
description: >
  Use when drafting the final owner-facing recommendation memo for a roof replacement
  tender award, after scoring and red-flag consolidation are complete. Synthesizes
  scoring matrix, red flags, and project context into an executive memo.
---

# Roof Recommendation Memo

You are drafting the memo the owner (or their board/council) will read to authorize award. The memo must be decision-ready: clear recommendation in the first paragraph, defensible rationale, risks named with mitigations, and award conditions that protect the owner.

## Reference Material

- `fixtures/domain_knowledge/03_tender_evaluation_methodology.md` §5 — recommendation memo structure
- `fixtures/domain_knowledge/04_contractor_qualification.md` §6 — BPS disclosure requirements (if applicable)

## Preconditions

Manifest must have:
- `comparison.recommended_bidder_id` populated (from scoring)
- All ranked bids have `scores.weighted_total` and `scores.rank`
- Red flags consolidated on each bid

## Working From a Deterministic Baseline

The `/roof-review` command runs `scripts/render_memo.py` before invoking this skill, which writes a mechanical baseline to `<manifest-dir>/../recommendation_memo.md`. Your job is **refinement, not regeneration**:

- **Read the baseline first.** Do not rewrite sections that are already correct.
- **Polish §1 Recommendation** — the auto-generated prose is accurate but terse; tighten for owner tone.
- **Trim and reorder §5 Award Conditions** — the renderer lists every needs_clarification gate plus every medium/high red flag, which can exceed what an owner memo should surface. Consolidate related conditions, prioritize critical ones, cut low-value clarifications.
- **Leave §3 Scoring, §4 Compliance, §6 Risk, §7 Contract Form, §8 Next Steps alone** unless the data is wrong. These are mechanical and the renderer already handled them.
- **Add §2 Why-Not-Low-Bid depth** only if the recommended bid is NOT the low compliant bid; the renderer's default prose is generic.

If no baseline exists (e.g., the command was run without step 5, or the renderer failed), draft from scratch using the procedure below.

## Drafting Procedure

1. **Identify the recommended bid.** Use `comparison.recommended_bidder_id`. This is the highest weighted score among compliant bids.

2. **Why-not-low-bid analysis.** If the recommended bid is NOT the lowest compliant bid, you must explain. Locate the lowest compliant bid and articulate the reasoning against three lenses:
   - Technical differentiation (warranty tier, certified installer, cover board, etc.)
   - Qualification differentiation (references, years, certifications)
   - Risk differentiation (red flags on the low bid, price spread vs normal range)
   - Acknowledge the price premium percentage and justify with concrete value received

3. **Award conditions.** Assemble from:
   - Every `needs_clarification` gate on the recommended bid → "Prior to contract execution, bidder to provide written confirmation of..."
   - Every medium-severity red flag on the recommended bid → "Prior to contract execution, clarify..."
   - Standard conditions (add these on every award memo regardless of bid specifics):
     - WSIB clearance re-verification at `clearances.wsib.ca` within 7 days of contract signing — the PDF attached to the bid is presumptive but not authoritative per WSIB policy. Record the verification reference number in the contract file.
     - Statutory 10% holdback under Ontario *Construction Act*
     - Monthly progress certification
     - Substantial performance declaration at 97% per *Construction Act* s. 2
     - Manufacturer inspection within 30 days of substantial performance
   - If BPS owner: AODA training confirmation, French-language service capability where applicable

4. **Risk assessment.** Populate a risk table. For each significant risk, assign likelihood (low/med/high), impact (low/med/high), and mitigation. Typical risks:
   - Weather delay during tear-off phase (mitigation: staging plan, tarping protocol)
   - Wood deck replacement exceeding allowance (mitigation: unit price in bid, site review before tear-off)
   - Tenant/occupant disruption on occupied buildings (mitigation: communication plan, work hours restrictions)
   - Change orders from discovered conditions (mitigation: allowance for unforeseen, owner's rep reviews each)
   - Contractor insolvency during project (mitigation: performance bond, L&M bond, payment holdback)

5. **Contract form recommendation.**
   - OBC Part 3, value >$500K: CCDC 2 (2020)
   - OBC Part 3, value ≤$500K: CCA-1 stipulated price (2021)
   - OBC Part 9, residential: simple stipulated-price contract
   - Per fixture 03 §1

6. **Render the template.** Populate `templates/recommendation_memo.md` with manifest values. Write to `<manifest-dir>/../recommendation_memo.md`.

## Voice & Tone

- First paragraph: unambiguous recommendation with contract price. No hedging.
- Second paragraph forward: defensible rationale, not marketing copy.
- Risk section: name risks plainly; owners distrust polished memos that pretend nothing can go wrong.
- No em dashes (owner memos read as formal; use semicolons or new sentences).
- Dollar amounts with comma separators. Percentages to one decimal.

## BPS Note

If `project.owner_type` is `municipal`, `school_board`, `hospital`, or `other_bps`:
- Recommendation section must cite compliance with BPS Procurement Directive (fixture 04 §6)
- Add a disclosure paragraph confirming the procurement was conducted openly, fairly, and competitively

## Output

- `recommendation_memo.md` at `<manifest-dir>/../recommendation_memo.md`

## Summary to User

- Recommended bidder + contract price (incl. HST)
- Whether recommendation is the low compliant bid or a premium (with %)
- Top 3 award conditions
- Top 3 risks with mitigations
- File path
