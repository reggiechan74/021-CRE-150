# Changelog — mls-extractor

All notable changes to this plugin are documented here.

---

## [0.5.1] — 2026-04-14

### Changed
- Added post-extraction verification subagent (Step D) between JSON write and Excel generation
- Verifier cross-checks property count, addresses, and key numeric fields against the source PDF
- On verification failure: re-extracts JSON with discrepancy hints, re-verifies once, then proceeds
- Excel is now only generated from a verified JSON file
- Renamed old Step D → Step E, Step E → Step F to accommodate new step

---

## [0.5.0] — 2026-04-14

### Changed
- Refactored skill to subagent dispatch pattern — primary context handles path resolution and relay only
- Subagent receives a fresh 200k-token context window for all heavy work (PDF reads, extraction, Excel)
- Removed `PRODUCT_SPEC.md` reference from subagent prompt (content was redundant)
- All paths resolved to absolute values in primary context and passed as `{{ }}` literals to subagent
- Added structured `EXTRACTION_RESULT` return block for clean primary-context relay
- Added graceful fallback: executes pipeline directly if Agent tool is unavailable

---

## [0.4.0] — 2026-04-14

### Changed
- Replaced pdfplumber deterministic parser with LLM vision-based extraction
- Pipeline simplified from PDF → pdfplumber → LLM review → Excel to PDF → LLM vision → Excel
- LLM reads PDF pages directly via Read tool; extracts all 34 fields in a single pass
- Batch processing for PDFs over 10 pages (20-page chunks)
- Handles TREB dense, sanitized, and other MLS board layouts uniformly without broker-specific label maps
- Eliminated intermediate scaffolding fields (`_raw_text`, `_gaps`)
- Trade-off: ~30–60s runtime increase per PDF in exchange for layout robustness

---

## [0.3.0] — 2026-04-14

### Added
- Support for sanitized PDF format (no MLS# anchors)
- Fallback extraction path for PDFs missing standard MLS number headers
- Address extraction for sanitized inline format

---

## [0.2.1] — 2026-04-13

### Fixed
- `net_asking_rent`: list price on same line as address in TREB format (`"795 Hazelhurst Rd List: $1"`) was captured as label; added `LIST_PRICE_RE` text-level fallback
- `pct_office_space`: "Ofc/Apt Area" appears as either `"3 %"` or `"5,674 Sq Ft"` depending on broker template; old parser blindly divided by 100, yielding values like 272.5 when raw was sqft
- `client_remarks`: fixed extraction for TREB abbreviation format
- `availability_date`: fixed parsing for concatenated possession values and edge cases

---

## [0.2.0] — 2026-04-13

### Changed
- Refactored extraction skill with pdfplumber table-based extractor
- Structured intermediate JSON with 34-field schema and scaffolding fields for LLM review pass

---

## [0.1.0] — 2026-04-13

### Added
- Initial plugin release
- Extract MLS property listings from PDF reports into Excel spreadsheets
- 34-field schema covering property details, financials, and operational specs
- Subject property detection and highlighting
- `excel_formatter.py` for deterministic Excel output with column ordering and formatting
