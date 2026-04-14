---
name: mls-extraction
description: >
  This skill should be used when the user asks to "extract MLS data", "parse an MLS report",
  "extract properties from an MLS PDF", "create an MLS Excel spreadsheet", "extract MLS listings",
  "process an MLS PDF", "get property data from MLS", or any request to extract commercial real
  estate property listings from a PDF report into a structured Excel or JSON format.
version: 0.1.0
---

## Philosophy

Perfect is the only acceptable standard. The output Excel file must be something the user would be proud to send to their CEO immediately — zero cleanup, zero formatting fixes.

For design specification and quality bar, read `${CLAUDE_PLUGIN_ROOT}/skills/mls-extraction/references/PRODUCT_SPEC.md`.
For the complete 34-field mapping reference, read `${CLAUDE_PLUGIN_ROOT}/skills/mls-extraction/references/field_mapping.md`.

---

## Invocation

Triggered by a user message such as:
- "Extract MLS data from Mississauga_industrial.pdf"
- "Extract this MLS report --subject='2550 Stanfield'"

Parse the user's message for:
- A PDF file path or uploaded file reference
- An optional `--subject="partial address"` to identify the subject property
- If no path is given, scan the workspace folder for PDF files and ask the user which one to process

---

## Step 1 — Read the PDF

Use the `Read` tool on the PDF file path. This returns the full text content. If the file is large, read in sections and hold all content in context before proceeding.

---

## Step 2 — Extract All 34 Fields Per Property

Identify every property listing in the PDF. For each one, extract these fields:

### Critical Fields (always extract)
| Field | Type | Notes |
|-------|------|-------|
| `address` | string | Full geocodable address: "123 Main St, Mississauga, ON L4Y 1S2, Canada" |
| `unit` | string | Unit/suite number; empty string if not applicable |
| `available_sf` | integer | Rentable square footage |
| `net_asking_rent` | float | Net asking rent $/SF/year (e.g., 13.95) |
| `tmi` | float | TMI/operating costs $/SF/year |
| `year_built` | integer | Year constructed |
| `clear_height_ft` | float | Clear ceiling height in feet |
| `pct_office_space` | float | 0–1 decimal (e.g., 0.03 = 3%) |
| `parking_ratio` | float | Spaces per 1,000 SF |
| `class` | integer | A=1, B=2, C=3 |

### Optional Fields (extract if present)
| Field | Type | Parsing Rule |
|-------|------|-------------|
| `shipping_doors_tl` | integer | Truck-level doors |
| `shipping_doors_di` | integer | Drive-in doors |
| `power_amps` | integer | Electrical service in amps |
| `bay_depth_ft` | float | Parse "Bay Size: 55 x 52" → 55.0 (first number) |
| `lot_size_acres` | float | Convert sq ft to acres (÷ 43,560) if needed |
| `hvac_coverage` | integer | Y=1, Partial=2, N=3 |
| `sprinkler_type` | integer | ESFR=1, Standard=2, None=3 — check Client Remarks for "ESFR" |
| `rail_access` | boolean | Y/N |
| `crane` | boolean | Y/N |
| `occupancy_status` | integer | Vacant=1, Occupied=2 |
| `trailer_parking` | boolean | Y/N |
| `secure_shipping` | boolean | Y/N |
| `excess_land` | boolean | Y/N |
| `grade_level_doors` | integer | Count |
| `days_on_market` | integer | DOM field |
| `zoning` | string | e.g., "M2", "I2" |

### Metadata Fields
| Field | Type | Source |
|-------|------|--------|
| `availability_date` | string | e.g., "Immediate", "Q3 2025" |
| `mls_number` | string | MLS# or ML# |
| `broker_name` | string | Listing broker |
| `client_remarks` | string | Truncate to 500 chars |
| `is_subject` | boolean | See Step 3 |
| `reported_market` | string | Auto-detect from PDF content |
| `report_generated_at` | string | Today's date from environment |
| `source_pdf` | string | PDF filename |

---

## Step 3 — Auto-Detect Subject Property

Apply this logic in order:
1. Check `client_remarks` for the word "Subject" — if found, mark that property
2. If `--subject` flag provided, fuzzy match (case-insensitive partial) against `address`
3. Default: mark the first property if no subject found

Set `is_subject: true` for exactly **one** property.

---

## Step 4 — Calculate Derived Fields

For every property:
- `gross_rent` = `net_asking_rent` + `tmi`
- `building_age_years` = current year (from environment) − `year_built`

---

## Step 5 — Write JSON Output

Locate the workspace folder (`ls /sessions/*/mnt/` in Bash). Create a `Reports/` subdirectory if it does not exist. Write the extracted data as:

`<workspace-folder>/Reports/YYYY-MM-DD_HHMMSS_mls_extraction_<market>.json`

Use Eastern Time for the timestamp. Derive `<market>` from the PDF content (e.g., "mississauga"). Get the current time via Bash: `date -u +%Y-%m-%dT%H:%M:%SZ` converted to ET.

**JSON structure:**
```json
{
  "extraction_date": "YYYY-MM-DD",
  "source_pdf": "filename.pdf",
  "market": "Mississauga - Industrial",
  "total_properties": 23,
  "properties": [ ... ]
}
```

---

## Step 6 — Create the Excel File

Install the dependency and run the bundled formatter:

```bash
pip install openpyxl --break-system-packages -q
python3 "${CLAUDE_PLUGIN_ROOT}/skills/mls-extraction/scripts/excel_formatter.py" \
  "<json-output-path>" \
  "<workspace-folder>/Reports/YYYY-MM-DD_HHMMSS_mls_extraction_<market>.xlsx"
```

The formatter applies:
- Dark blue header row (#2C3E50), white bold text, frozen, auto-filter
- Subject property row highlighted bright yellow (#FFFF00), bold
- Alternating white / light gray (#F8F9FA) data rows
- Columns ordered by decision importance (see PRODUCT_SPEC.md)
- Perfect number formatting: `$#,##0.00` for rent/TMI, `#,##0` for SF, `0.0` for heights
- Auto-sized column widths (10–50 char range)

If the formatter fails for any reason, write a fallback `.csv` file instead and notify the user.

---

## Step 7 — Quality Check

Before reporting success, verify:
- [ ] At least 90% of critical fields extracted per property (9 of 10 minimum)
- [ ] Exactly one property marked `is_subject: true`
- [ ] `gross_rent` calculated for all properties
- [ ] Excel file opens without error (check file size > 0)
- [ ] Output filename uses correct timestamp format

If quality check fails, warn the user but still deliver the file.

---

## Step 8 — Report to User

```
✅ Extracted {N} properties from {PDF filename}
🎯 Subject property: {address}
📊 Excel file: Reports/{filename}.xlsx
📄 JSON data: Reports/{filename}.json
```

Ask: "Would you be proud to send this Excel file to your CEO?" — if not, iterate.

---

## Error Handling

- Missing numeric field → use `0`
- Missing boolean field → use `false`
- Missing string field → use `""`
- Never crash on a single bad field — log warning and continue
- If 0 properties found, report the error and ask the user to verify the PDF is an MLS report
