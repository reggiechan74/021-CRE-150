# Changelog — tenant-credit

## [1.0.0] — 2026-04-14

### Added
- Initial plugin import from `vp-real-estate/Credit_Analysis` (2025-10-30 source)
- `credit_analysis.py` — 1,100+ line calculator with 15+ financial ratios, 100-point weighted
  credit scoring (A–F rating), default probability estimation, expected loss calculation,
  risk-adjusted security recommendations, multi-year trend analysis, and red flag identification
- `financial_utils.py` — minimal extraction of `safe_divide` and `calculate_financial_ratios`
  from the source repo's `Shared_Utils/financial_utils.py` (avoids scipy/numpy-financial
  transitive dependencies not needed by the credit calculator)
- `run_credit_analysis.py` — JSON input loader and calculator runner
- `SKILL.md` — subagent-dispatched workflow: PDF extraction → JSON generation → JSON
  verification → calculator execution → markdown report generation
- Subagent architecture applied per cowork_lessons_learned.md Lesson 1
- Nested verifier subagent with distinct `=== BEGIN/END VERIFIER CHECK ===` delimiters
  per Lesson 2
- JSON verified before calculator runs per Lesson 3 (verify intermediate artifacts)
- Operational lookup tables (JSON schema, field mappings, security logic) embedded in
  subagent prompt; strategy narrative kept in primary SKILL.md per Lesson 4

### Import path fixes (from source repo structure)
- `credit_analysis.py`: `from Shared_Utils.financial_utils import` → `from financial_utils import`
- `run_credit_analysis.py`: `from Credit_Analysis.credit_analysis import` → `from credit_analysis import`
