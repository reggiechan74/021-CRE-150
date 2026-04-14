# Changelog — cre-lease-abstraction

All notable changes to this plugin are documented here.

---

## [0.3.0] — 2026-04-14

### Changed
- Refactored skill to subagent dispatch pattern — primary context handles path resolution and relay only
- Added Step 0: resolves `CLAUDE_PLUGIN_ROOT`, workspace path, reference file absolute paths, and today's date before dispatch
- Both default and `--criticaldates` modes now dispatch via Agent tool with `--- BEGIN/END SUBAGENT PROMPT ---` delimiters
- Removed `${CLAUDE_PLUGIN_ROOT}` from subagent prompts; reference files injected as `{{ REIXS_JSON }}` / `{{ DDD_MD }}` literals
- Added workspace path fallback: `/sessions/*/mnt/` with `pwd` fallback for non-Cowork environments
- Added structured return blocks (`ABSTRACTION_RESULT`, `CRITICALDATES_RESULT`) for clean primary-context relay
- Added graceful fallback: executes pipeline directly if Agent tool is unavailable

### Fixed
- `reixs.runtime.json`: added missing AutoFail condition — MISSING field rate exceeding 30%
- `reixs.runtime.json`: removed dead ADR references (ADR-001, ADR-003, ADR-004 files do not exist)

---

## [0.2.0] — 2026-04-13

### Added
- Initial plugin release
- Full 8-step REIXS-LA-NA-001 lease abstraction workflow across 25 DDD sections
- FACT / INFERENCE / MISSING / CONFLICT status tagging with provenance on every FACT field
- AutoFail conditions: fabricated values, swapped parties, missing provenance, wrong currency, template placeholders
- Schedule G override detection with `[SCHEDULE_G_OVERRIDE]` tagging
- `--criticaldates` mode: extracts all date-triggered obligations across 10 categories
- P1–P4 priority classification with cascading reminder calculation
- Optional `--ics` (RFC 5545) and `--csv` output formats for critical dates calendar
- Bundled reference files: `reixs.runtime.json` (behavioral rules) and `lease_abstraction_ddd.md` (258-field DDD)
