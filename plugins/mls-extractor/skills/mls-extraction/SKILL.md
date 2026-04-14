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

## Step 0 — Resolve paths (runs in primary context)

Before dispatching the subagent, resolve these values.

**Plugin root** — run in Bash:
```bash
echo "${CLAUDE_PLUGIN_ROOT}"
```
If the result is empty, find it:
```bash
find ~ -path "*/mls-extractor/skills/mls-extraction/SKILL.md" -maxdepth 8 2>/dev/null | head -1 | sed 's|/skills/mls-extraction/SKILL.md||'
```
If that also fails, check known paths: `/home/reggiechan/021-CRE-150/plugins/mls-extractor`

**Workspace path** — current working directory, or `ls /sessions/*/mnt/` if in a sandbox.
Create `Reports/` under it if absent.

**Timestamp** — run `TZ=America/Toronto date +%Y-%m-%d_%H%M%S`.

From the resolved plugin root, construct:
- `FIELD_MAP` = `<plugin_root>/skills/mls-extraction/references/field_mapping.md`
- `FORMATTER` = `<plugin_root>/skills/mls-extraction/scripts/excel_formatter.py`

Verify all three exist. If any are missing, report the error and stop.

---

## Step 1 — Dispatch extraction subagent

Use the **Agent tool** to dispatch a subagent. This offloads the entire PDF vision pipeline
to a fresh 200k-token context window, keeping the primary context clean.

If the Agent tool is unavailable, execute Steps A through E directly in the current context.

Substitute the resolved values for `{{ }}` placeholders, then call the Agent tool with
`description: "MLS PDF extraction"` and the prompt below:

--- BEGIN SUBAGENT PROMPT ---

You are an MLS data extraction agent. Your sole job is to complete the extraction pipeline
below and return a structured summary. Do not ask questions — execute all steps and report results.

## Parameters

- PDF path: {{ PDF_FILE_PATH }}
- Subject hint: {{ --subject value, or "none" }}
- Workspace: {{ WORKSPACE_PATH }}
- Reports folder: {{ WORKSPACE_PATH }}/Reports/
- Timestamp: {{ TIMESTAMP }}
- Formatter: {{ FORMATTER }}
- Field map reference: {{ FIELD_MAP }}

## Step A — Read reference files

Read the field map reference now using the Read tool:
- Read(file_path="{{ FIELD_MAP }}")

This defines the exact 34-field schema, parsing rules, column order, and number formats.
Apply it throughout. Do not proceed without reading it.

## Step B — Read the PDF

Use the Read tool on the PDF path. For PDFs longer than 10 pages, read in batches of up to 20 pages
using the pages parameter ("1-20", "21-40", etc.). Continue until all pages are read. Each property
listing typically occupies 1-2 pages.

## Step C — Extract structured JSON

From the pages you read, extract every property into a JSON array. Follow the 34-field schema
and all parsing rules exactly as specified in field_mapping.md (which you read in Step A).

Supplementary notes beyond what field_mapping.md covers:

- `net_asking_rent`: placeholder values like $1 or $0 usually mean "Contact LA" — keep as 0.0
  and flag for the user
- `year_built`: if listed as an age band ("New", "6-15", "16-30", "31-50", "51-99"), use the
  midpoint subtracted from current year
- `class`: infer when not stated — A if clear height >= 32' and ESFR/modern, B if >= 28', C otherwise
- `client_remarks`: the Client Remks: / Client Remarks: block, up to 500 chars
- `reported_market`: a descriptive label derived from the PDF
  (e.g., "Mississauga - Industrial (100-400K SF For Lease)")
- `source_pdf`: basename of the input PDF
- `report_generated_at`: today's date in YYYY-MM-DD

Subject property (exactly one per extraction — priority order):
1. If client_remarks contains the word "Subject" -> mark that one
2. Else if subject hint is provided -> fuzzy match against address (case-insensitive)
3. Else -> mark the first property

Write the result to /tmp/mls_cleaned.json using the Write tool:

```json
{
  "source_pdf": "<basename>",
  "total_properties": N,
  "extraction_method": "llm-vision",
  "extraction_date": "YYYY-MM-DD",
  "properties": [ { ...34 fields... }, ... ]
}
```

## Step D — Generate Excel

Derive the market slug from the PDF filename or reported_market: lowercase, underscores,
alphanumeric only. Example: "mississauga_industrial".

Run the formatter:

```bash
python3 "{{ FORMATTER }}" \
  /tmp/mls_cleaned.json \
  "{{ WORKSPACE_PATH }}/Reports/{{ TIMESTAMP }}_mls_extraction_<market>.xlsx"
```

Copy the JSON alongside the Excel for reproducibility:

```bash
cp /tmp/mls_cleaned.json \
   "{{ WORKSPACE_PATH }}/Reports/{{ TIMESTAMP }}_mls_extraction_<market>.json"
```

## Step E — Verify

Check all of the following before returning:
- total_properties matches the number of listings seen in the PDF
- Exactly one property has is_subject: true
- Every property has all 34 fields present
- Excel file size > 0 (run: ls -lh <xlsx_path>)

## Return format

Return ONLY this block — no other commentary:

EXTRACTION_RESULT
total_properties: N
subject: <address of is_subject property>
excel: Reports/<filename>.xlsx
json: Reports/<filename>.json
zero_rent_properties: <comma-separated addresses with net_asking_rent=0, or "none">
errors: <any extraction errors, or "none">

## Error handling

- Pages won't render (corrupt or password-protected PDF) -> set errors field and stop.
- Schema mismatch after extraction -> re-emit the offending property from raw page content;
  do not synthesize values.
- Ambiguous subject -> set subject to "AMBIGUOUS — user must specify --subject" and continue.

--- END SUBAGENT PROMPT ---

---

## Step 2 — Relay result to user

When the subagent returns, parse the `EXTRACTION_RESULT` block and report:

```
✅ Extracted {total_properties} properties from {PDF filename}
🎯 Subject: {subject}
📊 Excel: {excel}
📄 JSON:  {json}
```

If `zero_rent_properties` is not "none":
> ⚠️ These properties show $0 net rent (likely "Contact LA" pricing): {list}

If `errors` is not "none":
> ❌ Extraction errors: {errors}
