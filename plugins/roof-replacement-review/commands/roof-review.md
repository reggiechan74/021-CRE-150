---
description: Run the full roof replacement tender review pipeline — extracts RFP and bids, evaluates mandatories, scores bids, flags risks, and writes the recommendation memo
argument-hint: "<rfp.pdf> <bid1.pdf> <bid2.pdf> [bid3.pdf ...]"
---

# /roof-review

Resolve the plugin root from `CLAUDE_PLUGIN_ROOT` or use:

`/home/reggiechan/021-CRE-150/plugins/roof-replacement-review`

## Pipeline

1. **Extract RFP.** Invoke the `roof-rfp-extract` skill on the first argument. Writes `roof-review-output/manifests/rfp.json` in the RFP's directory.

2. **Extract each bid.** Invoke the `roof-bid-extract` skill on each subsequent argument, passing the RFP manifest for schema alignment. Writes one `roof-review-output/manifests/bid_<n>.json` per bid.

3. **Check mandatories.** Invoke the `roof-qualification-check` skill per bid. Populates `mandatory_gates` and qualification-category `red_flags` on each bid.

4. **Technical review.** Invoke the `roof-technical-review` skill per bid. Populates technical red flags and raw technical/warranty/experience sub-scores.

5. **Merge manifests.** Run the merge script:

```bash
python3 "$CLAUDE_PLUGIN_ROOT/scripts/normalize.py" \
  --rfp "<rfp-output-dir>/manifests/rfp.json" \
  --bids "<rfp-output-dir>/manifests/bid_*.json" \
  --out "<rfp-output-dir>/manifests/tender_manifest.json"
```

6. **Score.** Run the scoring engine:

```bash
python3 "$CLAUDE_PLUGIN_ROOT/scripts/score.py" \
  --manifest "<rfp-output-dir>/manifests/tender_manifest.json"
```

7. **Render deliverables.** Invoke `roof-score-matrix` (writes `scoring_matrix.md`), then the red-flag consolidator:

```bash
python3 "$CLAUDE_PLUGIN_ROOT/scripts/redflags.py" \
  --manifest "<rfp-output-dir>/manifests/tender_manifest.json" \
  --out "<rfp-output-dir>/redflag_report.md"
```

Then invoke `roof-recommendation-memo` (writes `recommendation_memo.md`).

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
