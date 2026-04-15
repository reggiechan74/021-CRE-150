---
description: Produce only the red-flag report from an existing tender manifest
argument-hint: "<tender-manifest.json>"
---

# /roof-redflags

Resolve the plugin root from `CLAUDE_PLUGIN_ROOT` or use:

`/home/reggiechan/021-CRE-150/plugins/roof-replacement-review`

Invoke the `roof-qualification-check` and `roof-technical-review` skills against the supplied manifest (re-evaluates gates and qualitative flags without rebuilding from PDFs), then run:

```bash
python3 "$CLAUDE_PLUGIN_ROOT/scripts/redflags.py" \
  --manifest "<tender-manifest.json>" \
  --out "<tender-manifest-dir>/../redflag_report.md"
```

## Summary

Report:

- Count of bids by compliance status
- Critical red flags by bidder
- Cross-bid patterns (common exclusions, price spread alert, substitution convergence)
- Recommended next actions (addendum, clarification request, rejection)
