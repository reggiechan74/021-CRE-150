---
description: Compare the corrected CAM output against Anthropic finance output
argument-hint: "<allocated_manifest.json> <anthropic-output.txt>"
---

# /cam-compare-vs-anthropic

Resolve the plugin root from `CLAUDE_PLUGIN_ROOT` or use:

`/home/reggiechan/021-CRE-150/plugins/cam-reconciliation-cre`

Then run:

```bash
python3 "$CLAUDE_PLUGIN_ROOT/scripts/compare.py" \
  --manifest "<allocated_manifest.json>" \
  --anthropic "<anthropic-output.txt>"
```

Summarize:

- Anthropic-reported recoverable opex
- CAM-native corrected recoverable opex
- total overbilling avoided
- the three correction buckets: duplicate invoice, turnover cleaning, management fee basis
