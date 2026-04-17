---
name: roof-score-matrix
description: >
  Use when producing a weighted MCDA scoring matrix across multiple roofing bids after
  mandatory gates and technical review are complete. Invokes the Python scoring engine,
  populates scores and rank, and renders the scoring matrix markdown.
---

# Roof Score Matrix

You are producing the cross-bid scoring matrix after the qualification-check and technical-review skills have populated sub-scores and gate results. This skill is deterministic — it delegates the math to `scripts/score.py`.

## Reference Material

- `fixtures/domain_knowledge/03_tender_evaluation_methodology.md` §3 — MCDA weighting patterns, price scoring formulas, 5-point rubric anchors

## Procedure

1. **Verify preconditions.** The manifest must have:
   - `rfp.evaluation_criteria.weighting` populated
   - Each bid has `mandatory_gates` populated (from qualification-check)
   - Each bid has rated sub-scores on `scores.technical_approach`, `scores.warranty_materials`, `scores.experience_references`, `scores.qualifications_certifications`, `scores.schedule`
   - Each bid has `pricing.base_bid_cad`

   If any missing, run the upstream skill or stop and tell the user what's missing.

2. **Invoke the scoring engine.** If the user supplied an `evaluation_config.yaml` (via `config=<path>` argument to the command), pass it with `--config`:

```bash
python3 "$CLAUDE_PLUGIN_ROOT/scripts/score.py" --manifest <tender_manifest.json> [--config <evaluation_config.yaml>]
```

Config overrides the RFP's `weighting` and/or `price_scoring_method` — useful when the owner wants to reweight for project type (occupied, heritage, BPS) without editing the parsed RFP. The engine validates that weights sum to 100 and records the source in `manifest.rfp.evaluation_criteria.weighting_source` for audit.

This:
- Computes price sub-score via the configured method (default: `(lowest/this) × 100`)
- Combines with rated sub-scores via weighted sum
- Ranks compliant bidders
- Writes `comparison.price_low_cad`, `price_high_cad`, `price_spread_percent`, `compliant_bidders_count`, `recommended_bidder_id` back to the manifest

3. **Produce scoring rationale.** For each ranked bid, write to `bid.scoring_rationale`:
   - `strengths`: top 2-3 sub-scores with brief justification
   - `weaknesses`: weakest 1-2 sub-scores with brief justification
   - `differentiator`: the single factor that most separates this bid from its neighbour in the ranking

4. **Render the matrix.** Prefer the deterministic path:

```bash
python3 "$CLAUDE_PLUGIN_ROOT/scripts/render_matrix.py" \
  --manifest <tender_manifest.json> \
  --out <manifest-dir>/../scoring_matrix.md
```

   If `scoring_matrix.md` already exists (the `/roof-review` command typically produces it in step 5), **read it and refine only if the mechanical output reads awkwardly**. Do not regenerate from scratch. Leave numbers and structure alone — they are authoritative. Only touch rationale prose if the pulled `scoring_rationale` text reads poorly.

## Weighting Integrity Check

Before running the engine, verify `sum(weighting.values()) == 100`. If not, raise an error and tell the user which criterion to adjust.

## Price Spread Warning

If `price_spread_percent > 15`, flag to the owner in the matrix rendering that:

> Scope divergence or low-bid risk is likely. Recommend reviewing the red flag report cross-bid section before award.

(Per fixture 03 §4 — 15% threshold is the CCA industry heuristic for bid outliers.)

## Output

- Updated tender manifest (in place)
- `scoring_matrix.md` rendered from template

## Summary to User

- Rank order with weighted totals
- Price spread %
- Winner's margin over #2
- Any weighting adjustments applied or integrity warnings raised
