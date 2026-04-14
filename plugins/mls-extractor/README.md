# MLS Extractor Plugin

Extract commercial real estate property listings from MLS PDF reports into professionally formatted Excel spreadsheets. One skill. Zero configuration. Perfect output.

---

## Components

### Skill: `mls-extraction`

Activates when you ask to extract MLS data, parse an MLS report, or create an MLS Excel spreadsheet from a PDF.

**Usage:**
- "Extract MLS data from Mississauga_industrial.pdf"
- "Process this MLS report" + attach PDF
- "Extract MLS listings --subject='2550 Stanfield'"

**Outputs** (saved to `Reports/` in your workspace folder):
- `YYYY-MM-DD_HHMMSS_mls_extraction_<market>.xlsx` — professionally formatted Excel
- `YYYY-MM-DD_HHMMSS_mls_extraction_<market>.json` — structured JSON data

### Bundled Scripts

| File | Purpose |
|------|---------|
| `skills/mls-extraction/scripts/excel_formatter.py` | Python formatter — creates the Excel file with perfect styling |

### Reference Files

| File | Purpose |
|------|---------|
| `skills/mls-extraction/references/PRODUCT_SPEC.md` | Design philosophy, visual spec, quality bar |
| `skills/mls-extraction/references/field_mapping.md` | Complete 34-field reference with parsing rules |

---

## What You Get

**Excel formatting:**
- Dark blue header row, white bold text, frozen + auto-filter
- Subject property highlighted in bright yellow — impossible to miss
- Alternating white/gray rows, subtle borders
- Columns ordered by decision importance (Net Rent, TMI, Size first)
- Perfect number formatting: `$#,##0.00` for rent, `#,##0` for SF, `0.0` for heights

**Extraction intelligence:**
- 34 fields per property including derived `gross_rent` and `building_age_years`
- Auto-detects subject property from remarks or `--subject` flag
- Parses complex fields: bay depth from "55 x 52", ESFR from Client Remarks, lot size unit conversion
- Handles missing fields gracefully — never crashes

---

## Setup

Requires Python with `openpyxl`. The skill installs it automatically via pip when run. No other setup needed.
