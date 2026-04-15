---
description: Extract a single roofing contractor bid PDF against an already-parsed RFP schema
argument-hint: "<rfp-manifest.json> <bid.pdf>"
---

# /roof-extract-bid

Resolve the plugin root from `CLAUDE_PLUGIN_ROOT` or use:

`/home/reggiechan/021-CRE-150/plugins/roof-replacement-review`

Invoke the `roof-bid-extract` skill with both arguments. The skill:

1. Loads the RFP manifest to know what fields to populate.
2. Reads the bid PDF.
3. Extracts: bidder identity, pricing (base bid, alternates, unit prices, allowances), scope response (compliance, exclusions, substitutions), materials system, warranty offered, qualifications (WSIB/CGL/bonding/WAH/references), schedule, technical approach.
4. Records `evidence_page` references back to the source PDF for each extracted value.
5. Writes to `<rfp-dir>/roof-review-output/manifests/bid_<bidder_slug>.json`.

## Summary

Report:

- Bidder name
- Base bid price (and HST status)
- Declared exclusions count
- Substitutions proposed count
- Warranty headline (years, type)
- Any fields that could not be extracted (list for owner follow-up)
