---
description: Run the full roof replacement tender review pipeline — extracts RFP and bids, evaluates mandatories, scores bids, flags risks, and writes the recommendation memo
argument-hint: "<rfp.pdf> <bid1.pdf> <bid2.pdf> [bid3.pdf ...] [config=<evaluation_config.yaml>]"
---

# /roof-review

Resolve the plugin root from `CLAUDE_PLUGIN_ROOT` or use:

`/home/reggiechan/021-CRE-150/plugins/roof-replacement-review`

## Pipeline

1. **Extract RFP.** Invoke the `roof-rfp-extract` skill on the first argument. Writes `roof-review-output/manifests/rfp.json` in the RFP's directory. Runs in the main thread because every downstream bid needs the RFP manifest.

2. **Fan out per-bid processing (PARALLEL).** For each bid PDF passed as an argument, dispatch **one** `Agent` tool call. Send all bid-subagent calls in a **single message** so they run concurrently. Each subagent handles one bid end-to-end: extract → qualification check → technical review. This is the performance-critical step — do NOT run bids sequentially in the main thread.

   Per-bid subagent prompt template (substitute `<BID_PATH>`, `<RFP_MANIFEST_PATH>`, `<PLUGIN_ROOT>`):

   ```
   You are processing one roofing bid for the roof-replacement-review pipeline.

   Plugin root: <PLUGIN_ROOT>    (also available as $CLAUDE_PLUGIN_ROOT)
   RFP manifest: <RFP_MANIFEST_PATH>
   Bid PDF: <BID_PATH>

   Run these three skills in order on this single bid:
     a. roof-bid-extract — produces <rfp-dir>/roof-review-output/manifests/bid_<slug>.json
     b. roof-qualification-check — populates mandatory_gates + qualification red_flags + sub-scores in that same bid manifest
     c. roof-technical-review — populates technical red_flags + technical/warranty sub-scores in that same bid manifest

   Do NOT touch the RFP manifest or any other bid's manifest.

   Return ONLY:
     - Bidder legal name
     - Bid manifest path
     - Compliance status (compliant | non-compliant | needs-clarification)
     - Weighted sub-score snapshot (the five rated sub-scores)
     - Count of critical/high red flags
     - Any extraction_notes items that need owner follow-up
   ```

   The main thread waits for all subagents to return before proceeding to step 3.

3. **Merge manifests.** Run the merge script:

```bash
python3 "$CLAUDE_PLUGIN_ROOT/scripts/normalize.py" \
  --rfp "<rfp-output-dir>/manifests/rfp.json" \
  --bids "<rfp-output-dir>/manifests/bid_*.json" \
  --out "<rfp-output-dir>/manifests/tender_manifest.json"
```

4. **Score.** Run the scoring engine. If the user passed `config=<path>` in the arguments, append `--config <path>` to override the RFP's weights and price scoring method:

```bash
python3 "$CLAUDE_PLUGIN_ROOT/scripts/score.py" \
  --manifest "<rfp-output-dir>/manifests/tender_manifest.json" \
  [--config <evaluation_config.yaml>]
```

Example config at `templates/evaluation_config.yaml`. Common uses: occupied-building weighting (raise schedule + technical), BPS procurement (raise price, use `lowest_compliant` method), heritage/complex roof (raise technical).

5. **Render deliverables (deterministic fast path, then optional LLM polish).**

   Run all three renderer scripts first — pure Python, no LLM, typically <1s total:

```bash
python3 "$CLAUDE_PLUGIN_ROOT/scripts/render_matrix.py" \
  --manifest "<rfp-output-dir>/manifests/tender_manifest.json" \
  --out "<rfp-output-dir>/scoring_matrix.md"

python3 "$CLAUDE_PLUGIN_ROOT/scripts/redflags.py" \
  --manifest "<rfp-output-dir>/manifests/tender_manifest.json" \
  --out "<rfp-output-dir>/redflag_report.md"

python3 "$CLAUDE_PLUGIN_ROOT/scripts/render_memo.py" \
  --manifest "<rfp-output-dir>/manifests/tender_manifest.json" \
  --out "<rfp-output-dir>/recommendation_memo.md"
```

   Then invoke the skills **as refinement passes** over the generated files — not from-scratch regeneration:
   - `roof-score-matrix` — read `scoring_matrix.md`, refine wording only if the mechanical output reads awkwardly; leave numbers and structure alone.
   - `roof-recommendation-memo` — read `recommendation_memo.md`, polish §1 Recommendation prose and trim/reorder award conditions in §5 for owner tone; keep §3, §4, §6, §7, §8 as-is unless data is wrong.

   Skip the refinement passes entirely if the user asked for a fast/cheap run, or if the Python output already reads cleanly.

## Output

All artifacts land in `<rfp-dir>/roof-review-output/`:

- `manifests/tender_manifest.json` — complete normalized manifest
- `scoring_matrix.md` — weighted MCDA table
- `redflag_report.md` — mandatory gates + qualitative risks
- `recommendation_memo.md` — executive memo for the owner
- `audit_log.md` — extraction citations and decision provenance

## Summary

After all steps complete, report to the user:

- Number of bids received vs compliant
- Recommended bidder and weighted score
- Price delta between recommended and low compliant bid
- Count of critical/high red flags
- Top three award conditions the owner must resolve before signing
