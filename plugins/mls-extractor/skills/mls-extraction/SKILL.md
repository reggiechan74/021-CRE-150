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
For the complete 34-field mapping, read `${CLAUDE_PLUGIN_ROOT}/skills/mls-extraction/references/field_mapping.md`.

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
PDF  →  [1] pdf_extractor.py  →  raw.json  →  [2] LLM review  →  cleaned.json  →  [3] excel_formatter.py  →  .xlsx
```

**Do NOT use the `Read` tool on the PDF.** The deterministic extractor is faster and more accurate for structured fields.

---

## Step 1 — Deterministic extraction

```bash
pip install pdfplumber openpyxl --break-system-packages -q
python3 "${CLAUDE_PLUGIN_ROOT}/skills/mls-extraction/scripts/pdf_extractor.py" \
  "<pdf-path>" /tmp/mls_raw.json
```

The script uses `pdfplumber.extract_tables()` to parse both column-aligned and vertical `Field | Value` layouts. Output JSON, per property:
- All 34 canonical fields populated where pdfplumber found them
- `_raw_text` — the full text block for that property (Stage 2 input)
- `_gaps` — fields the extractor couldn't fill or flagged suspicious (e.g. `net_asking_rent_suspicious` when value is $0 or $1 placeholder)

---

## Step 2 — LLM review pass

Read `/tmp/mls_raw.json`. For each property, validate against its `_raw_text`:

### Fill gaps
- `net_asking_rent_suspicious` → $0/$1 usually means "Contact LA" or unpublished; leave as-is unless a real number appears in remarks
- `year_built` missing → check for "Apx Age" band or phrases like "new construction"
- `pct_office_space` missing → scan remarks for "X,XXX sf of office"
- Any critical field with obvious extraction error (e.g. `pct_office > 1`, truncated address) → correct from `_raw_text`

### Subject property
1. Scan `client_remarks` for "Subject" → mark that one
2. Else if `--subject="..."` given → fuzzy match against `address`
3. Else → mark the first property

Exactly one property has `is_subject: true`.

### Market + derived
- Set `reported_market` on every property (e.g. "Mississauga - Industrial") from PDF content
- Recompute: `gross_rent = net_asking_rent + tmi`; `building_age_years = current_year - year_built`

### Strip scaffolding
Remove `_raw_text` and `_gaps` from each property before Step 3.

---

## Step 3 — Write outputs

Workspace folder: current working directory, or `ls /sessions/*/mnt/` if running in a sandbox. Create `Reports/` if absent.

Timestamp: `TZ=America/Toronto date +%Y-%m-%d_%H%M%S`

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/mls-extraction/scripts/excel_formatter.py" \
  <cleaned-json-path> \
  <workspace>/Reports/<timestamp>_mls_extraction_<market>.xlsx
```

The formatter handles all visual design (header styling, subject-row highlight, column order, number formats). See `PRODUCT_SPEC.md`.

---

## Step 4 — Verify + report

Before reporting success:
- `total_properties` unchanged from Stage 1
- Exactly one `is_subject: true`
- No `_raw_text` or `_gaps` in final JSON
- Excel file size > 0

Report:

```
✅ Extracted {N} properties from {PDF filename} in {elapsed}s
🎯 Subject: {address}
📊 Excel: Reports/{filename}.xlsx
📄 JSON:  Reports/{filename}.json
```

---

## Error handling

- **0 properties segmented** → the PDF may not use `MLS#:` anchors. Inspect with `pdftotext -layout <pdf> -` or `pdfplumber` and either extend `MLS_RE` in `pdf_extractor.py` or fall back to vision `Read`.
- **Most fields empty across all properties** → unknown broker format; extend `LABEL_MAP` aliases in `pdf_extractor.py` with the labels you see in the raw text.
- Single bad field → log, use type default (`0`, `false`, `""`), continue.
