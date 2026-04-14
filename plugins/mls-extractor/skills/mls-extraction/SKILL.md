---
name: mls-extraction
description: >
  This skill should be used when the user asks to "extract MLS data", "parse an MLS report",
  "extract properties from an MLS PDF", "create an MLS Excel spreadsheet", "extract MLS listings",
  "process an MLS PDF", "get property data from MLS", or any request to extract commercial real
  estate property listings from a PDF report into a structured Excel or JSON format.
---

## Philosophy

Perfect is the only acceptable standard. The output Excel file must be something the user would be proud to send to their CEO immediately — zero cleanup, zero formatting fixes.

For design spec, read `${CLAUDE_PLUGIN_ROOT}/skills/mls-extraction/references/PRODUCT_SPEC.md`.
For the complete 34-field schema, read `${CLAUDE_PLUGIN_ROOT}/skills/mls-extraction/references/field_mapping.md`.

---

## Invocation

Triggered by messages such as:
- "Extract MLS data from Mississauga_industrial.pdf"
- "Extract this MLS report --subject='2550 Stanfield'"

Parse the user's message for:
- A PDF file path
- An optional `--subject="partial address"` flag
- If no path is given, scan the workspace for PDFs and ask which one

---

## Pipeline

```
PDF  →  [1] Read tool (vision)  →  [2] structured JSON  →  [3] excel_formatter.py  →  .xlsx
```

The LLM is the extractor. Pdfplumber-based parsing was brittle across broker templates (TREB dense vs. sanitized vs. other MLS boards); vision-based reading handles all layouts uniformly at the cost of ~30–60s runtime per PDF.

---

## Step 1 — Read the PDF

Use the `Read` tool on the PDF. For PDFs > 10 pages, read in batches of ≤20 pages using the `pages` parameter:

```
Read(file_path="<pdf>", pages="1-20")
Read(file_path="<pdf>", pages="21-40")
...
```

Continue until all pages are read. Each property listing typically occupies 1–2 pages.

---

## Step 2 — Emit structured JSON

From the pages you read, extract **every** property into a JSON array. Each property object must contain all 34 fields from `field_mapping.md`. Use type-appropriate defaults for missing values: `0` for numbers, `false` for booleans, `""` for strings.

### Field extraction rules

**Numeric/enum fields** (follow `field_mapping.md` parsing rules):
- `available_sf`: total building SF offered (not the "Indust Area" breakdown)
- `net_asking_rent`: $ / SF / year; placeholder values like `$1` or `$0` usually mean "Contact LA" — keep as `0.0` and let the user know
- `tmi`: from `Taxes: $X/YYYY/T.M.I.` — extract the first dollar figure
- `clear_height_ft`: `"36 0"` means 36'0" → `36.0`; `"40 6"` → `40.5`
- `pct_office_space`: as a fraction (`3%` → `0.03`). If only sqft is given (`5,674 Sq Ft office`), compute `office_sf / available_sf`
- `year_built`: if listed as a band ("New", "6-15", "16-30", "31-50", "51-99"), use the midpoint subtracted from current year. Store `year_built = current_year - age_midpoint`
- `class`: infer when not stated — A if clear height ≥ 32' and ESFR/modern, B if ≥ 28', C otherwise
- `hvac_coverage`, `sprinkler_type`, `occupancy_status`: integer enums per `field_mapping.md`
- `days_on_market`: from `DOM:` field
- `gross_rent`: computed → `net_asking_rent + tmi`
- `building_age_years`: computed → `current_year - year_built`

**Text fields**:
- `address`: full street + city + province + postal code + ", Canada"
- `client_remarks`: the `Client Remks:` / `Client Remarks:` block, up to 500 chars
- `broker_name`: the listing salesperson name (UPPERCASE)
- `reported_market`: a descriptive label derived from the PDF (e.g., `"Mississauga - Industrial (100-400K SF For Lease)"`)

**Subject property** (exactly one per extraction):
1. If `client_remarks` contains the word "Subject" → mark that one
2. Else if the user passed `--subject="..."` → fuzzy match against `address`
3. Else → mark the first property

**Metadata** (same for all properties):
- `source_pdf`: basename of the input PDF
- `report_generated_at`: today's date in `YYYY-MM-DD`

### Write the JSON

```json
{
  "source_pdf": "<basename>",
  "total_properties": N,
  "extraction_method": "llm-vision",
  "extraction_date": "YYYY-MM-DD",
  "properties": [ { ...34 fields... }, ... ]
}
```

Write to `/tmp/mls_cleaned.json` using the Write tool.

---

## Step 3 — Write Excel

Workspace folder: current working directory, or `ls /sessions/*/mnt/` if running in a sandbox. Create `Reports/` if absent.

Timestamp: `TZ=America/Toronto date +%Y-%m-%d_%H%M%S`

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/mls-extraction/scripts/excel_formatter.py" \
  /tmp/mls_cleaned.json \
  <workspace>/Reports/<timestamp>_mls_extraction_<market>.xlsx
```

Also copy the JSON next to the Excel file for reproducibility.

---

## Step 4 — Verify + report

Before declaring success:
- `total_properties` matches the number of listings you saw in the PDF
- Exactly one `is_subject: true`
- Every property has all 34 fields
- Excel file size > 0

Report:

```
✅ Extracted {N} properties from {PDF filename}
🎯 Subject: {address}
📊 Excel: Reports/{filename}.xlsx
📄 JSON:  Reports/{filename}.json
```

Call out any properties where `net_asking_rent = 0` (placeholder pricing → user should contact the listing agent).

---

## Error handling

- **Pages won't render** (corrupt PDF, password-protected) → tell the user and stop.
- **Schema mismatch after extraction** → re-emit the offending property from the raw page content; don't synthesize values.
- **Ambiguous subject** → ask the user to specify `--subject="..."`.
