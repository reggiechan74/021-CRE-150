---
description: Produce only the recommendation memo from an existing scored tender manifest
argument-hint: "<tender-manifest.json>"
---

# /roof-memo

Resolve the plugin root from `CLAUDE_PLUGIN_ROOT` or use:

`/home/reggiechan/021-CRE-150/plugins/roof-replacement-review`

Requires a manifest that has already been scored (has `scores` and `red_flags` populated on each bid, and `comparison` populated at the top level). If not, run `/roof-review` instead.

Invoke the `roof-recommendation-memo` skill. The skill:

1. Reads the scored tender manifest.
2. Identifies the recommended bidder (highest weighted score among compliant).
3. Drafts rationale — strengths, why-not-low-bid analysis if applicable, risks and mitigations.
4. Assembles award conditions from unresolved red flags.
5. Renders the `templates/recommendation_memo.md` with all variables populated.
6. Writes `<tender-manifest-dir>/../recommendation_memo.md`.

## Summary

Report:

- Recommended bidder and weighted score
- Contract price recommended (incl. HST)
- Top 3 award conditions
- Whether the recommendation is the low compliant bid or a premium over low
