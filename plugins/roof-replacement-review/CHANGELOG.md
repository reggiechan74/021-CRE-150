# Changelog

## 0.1.0 - 2026-04-15

- Added normalized tender manifest schema covering Ontario commercial (OBC Part 3) and residential (OBC Part 9) roof replacement
- Added six skills: roof-rfp-extract, roof-bid-extract, roof-technical-review, roof-qualification-check, roof-score-matrix, roof-recommendation-memo
- Added Python pipeline scripts for ingest, normalization, MCDA scoring, red-flag gating, and memo rendering
- Added slash commands: /roof-review, /roof-extract-rfp, /roof-extract-bid, /roof-redflags, /roof-memo
- Added domain-knowledge fixtures with citations to OBC, CRCA, WSIB, Skilled Trades Ontario, and CCDC-23
- Added synthetic Ontario tender fixture (RFP plus three bids) for pipeline testing
