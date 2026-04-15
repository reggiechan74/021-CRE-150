---
description: Extract an owner's roof replacement RFP PDF into the normalized tender schema
argument-hint: "<rfp.pdf>"
---

# /roof-extract-rfp

Resolve the plugin root from `CLAUDE_PLUGIN_ROOT` or use:

`/home/reggiechan/021-CRE-150/plugins/roof-replacement-review`

Invoke the `roof-rfp-extract` skill on the argument. The skill:

1. Reads the RFP PDF.
2. Classifies the project (OBC Part 3 vs Part 9, roof type, building occupancy status).
3. Extracts scope, specified membrane/shingle system, warranty requirements, mandatory requirements, and evaluation weighting.
4. Writes a manifest conforming to `templates/bid_schema.json` §`project` + §`rfp` to:
   `<rfp-dir>/roof-review-output/manifests/rfp.json`

## Summary

Report:

- Classification (Part 3 / Part 9, roof type)
- Roof area and membrane/shingle system specified
- Mandatory gates active
- Evaluation weighting (default or custom)
- Submission deadline
- Any extraction ambiguities flagged for owner clarification
