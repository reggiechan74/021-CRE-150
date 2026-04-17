# Changelog

## [Unreleased]

### Changed
- `/roof-review` now dispatches subagents in two parallel waves instead of three serial steps:
  - **Wave 1:** `roof-rfp-extract` in parallel with N × `roof-bid-extract`. Authorized because `roof-bid-extract` is RFP-independent (extracts bid facts only, defers comparison).
  - **Wave 2:** N × (`roof-qualification-check` ∥ `roof-technical-review`). Each skill writes a disjoint sidecar (`bid_<slug>.qual.json`, `bid_<slug>.tech.json`); they are safe to run concurrently because their output ownership (gate names, sub-scores, red-flag categories) is disjoint by design.
  - Expected wall-clock reduction: ~45–55% on a 5-bid tender.
- `scripts/normalize.py` gains `--qual-sidecars` and `--tech-sidecars` flags and deep-merges sidecar files onto base bid manifests. Collisions on `mandatory_gates`, `scores`, or `scoring_rationale` keys are fatal — they indicate a skill wrote outside its ownership boundary.
- `roof-qualification-check` and `roof-technical-review` SKILL.md files now specify allowlisted fixture reads to reduce per-subagent context load.

### Added
- Gate-applicability tier model: `scripts/gate_applicability.py` and `scripts/reconcile_gates.py` classify gates as statutory / RFP-specified / prudent-evaluator and refuse to score a tender when a bidder was failed on a gate the RFP never invoked, or when identical evidence was treated asymmetrically across bidders. The qualification-check SKILL picked up the matching three-tier `compliant` / `conditional` / `non_compliant` compliance model. This work originated alongside the pipeline-speedup commits and landed together with them.
- Deterministic renderer scripts (`render_matrix.py`, `render_memo.py`) produce the scoring matrix and recommendation memo mechanically from the tender manifest, with optional LLM refinement passes layered on top via the baseline-refinement pattern.

### Migration notes
- Legacy base-bid manifests that already carry merged gates/scores still work when `normalize.py` is called without sidecar globs. Fixtures under `fixtures/sample_bids/` are unchanged.
- Any caller that ran `normalize.py` with the old two-flag shape is untouched; the two new flags are optional.

## 0.1.0 - 2026-04-15

- Added normalized tender manifest schema covering Ontario commercial (OBC Part 3) and residential (OBC Part 9) roof replacement
- Added six skills: roof-rfp-extract, roof-bid-extract, roof-technical-review, roof-qualification-check, roof-score-matrix, roof-recommendation-memo
- Added Python pipeline scripts for ingest, normalization, MCDA scoring, red-flag gating, and memo rendering
- Added slash commands: /roof-review, /roof-extract-rfp, /roof-extract-bid, /roof-redflags, /roof-memo
- Added domain-knowledge fixtures with citations to OBC, CRCA, WSIB, Skilled Trades Ontario, and CCDC-23
- Added synthetic Ontario tender fixture (RFP plus three bids) for pipeline testing
