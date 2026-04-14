---
name: lease-abstraction
description: >
  This skill should be used when the user asks to "abstract a lease", "extract lease terms",
  "summarize a commercial lease", "analyze a CRE lease", "review lease provisions",
  "identify lease risks", "extract critical dates from a lease", "generate a critical dates
  calendar", "create an ICS file from a lease", "export lease dates to CSV", or needs to
  apply REIXS methodology, the 258-field Domain Data Dictionary, or REIXS-LA-NA-001
  extraction standards to a commercial real estate lease document.
---

## Step 0 — Resolve paths (runs in primary context)

Before dispatching any subagent, resolve these values in the primary context.

**Plugin root** — run in Bash:
```bash
echo "${CLAUDE_PLUGIN_ROOT}"
```
If the result is empty, find it:
```bash
find ~ -path "*/cre-lease-abstraction/skills/lease-abstraction/SKILL.md" -maxdepth 8 2>/dev/null | head -1 | sed 's|/skills/lease-abstraction/SKILL.md||'
```
If that also fails, check known paths: `/home/reggiechan/021-CRE-150/plugins/cre-lease-abstraction`

**Workspace path** — try Cowork sandbox first, fall back to current directory:
```bash
ls /sessions/*/mnt/ 2>/dev/null | head -1
```
If empty, use `pwd` as workspace root. Create `Reports/` under it if absent.

**Today's date** — run `date +%Y-%m-%d`.

From the resolved plugin root, construct:
- `REIXS_JSON` = `<plugin_root>/skills/lease-abstraction/references/reixs.runtime.json`
- `DDD_MD` = `<plugin_root>/skills/lease-abstraction/references/lease_abstraction_ddd.md`

Verify both files exist. If either is missing, report the error and stop.

---

## Mode Detection

Inspect the user's message for the `--criticaldates` flag or equivalent intent (e.g., "critical dates only", "just the dates", "generate calendar").

- **Default mode** — dispatch the full REIXS abstraction subagent
- **`--criticaldates` mode** — dispatch the critical dates subagent

If no document path is provided, scan the workspace folder for lease documents (PDF, DOCX, MD) and ask the user which file to process before dispatching.

---

## DEFAULT MODE — Full Lease Abstraction

### Step 1 — Dispatch extraction subagent

Use the **Agent tool** to dispatch a subagent. This offloads the entire document reading and
extraction pipeline to a fresh 200k-token context window, keeping the primary context clean.

If the Agent tool is unavailable, execute Steps A through H directly in the current context.

Substitute the resolved values for `{{ }}` placeholders, then call the Agent tool with
`description: "Lease abstraction"` and the prompt below:

--- BEGIN SUBAGENT PROMPT ---

You are a commercial lease abstraction agent applying the REIXS-LA-NA-001 standard. Your sole
job is to complete the abstraction pipeline below and return a structured summary. Do not ask
questions — execute all steps and report results.

## Parameters

- Lease document: {{ DOCUMENT_PATH }}
- Output format: {{ "json" if -json flag present, else "markdown" }}
- Workspace: {{ WORKSPACE_PATH }}
- Reports folder: {{ WORKSPACE_PATH }}/Reports/
- Today's date: {{ TODAY }}
- REIXS rules: {{ REIXS_JSON }}
- Domain Data Dictionary: {{ DDD_MD }}

## Step A — Load Governance Frameworks

Read both reference files now before touching the source document:
- Read(file_path="{{ REIXS_JSON }}")
- Read(file_path="{{ DDD_MD }}")

Internalize both fully. Do not proceed to Step B without reading them.

## Step B — Parse Input

Identify the document path from the parameters above. Output format: JSON (50–60 KB target)
if the format parameter is "json", otherwise Markdown (30–40 KB target).

## Step C — Load and Prepare Document

- **PDF / MD / TXT**: Use the `Read` tool directly
- **DOCX**: Use the `Read` tool — it handles Word documents natively in Cowork. If it returns
  garbled output, fall back to Python:
  `pip install python-docx --break-system-packages -q`
  then `python3 -c "import docx; doc=docx.Document('<path>'); print('\n'.join([p.text for p in doc.paragraphs]))"`
- **URL**: Use `WebFetch`
- **Large documents**: Process in sections; merge results

Do not assume `pandoc` or any other CLI tool is pre-installed on the user's machine.

## Step D — Classify Lease Type

Identify the lease as **Industrial** or **Office** based on permitted use, building type, and
operational provisions. State the classification explicitly before extraction begins.

## Step E — Extract with REIXS Rules

Extract all 25 DDD sections. Apply one of four status tags to every field:

| Status | Requirement |
|--------|-------------|
| `FACT` | Verbatim value from source — include page, clause reference, verbatim quote |
| `INFERENCE` | Derived value — include confidence (0.0–1.0) and reasoning; flag if < 0.5 |
| `MISSING` | Field absent — set to `null` (JSON) or `"Not specified"` (Markdown); never fabricate |
| `CONFLICT` | Multiple contradictory values — cite all sources; do not silently resolve |

**AutoFail conditions — halt and report immediately if any occur:**
- Parties (landlord / tenant) misidentified or swapped
- Template placeholders (e.g., `[Insert value]`) remain in output
- Financial values lack verbatim + normalized numeric forms
- Wrong currency used
- Commencement or expiry dates lack provenance
- MISSING field rate exceeds 30% — escalate for human review

**Schedule G override rule:** Special Provisions that contradict the main body take precedence.
Tag every such override `[SCHEDULE_G_OVERRIDE]`.

**Financial rule:** Extract verbatim text first; provide normalized numeric form as a separate
field. Determine currency from document context — never assume.

**Date rule:** Normalize all dates to ISO 8601 (`YYYY-MM-DD`).

**Critical sections (2× scoring weight):** Parties (2), Premises (3), Term (4), Rent (5).

## Step F — Format Output

**Markdown (30–40 KB):**
1. Executive Summary — lease type, parties, key dates, total financial exposure
2. Key Terms snapshot
3. Sections 1–21 (extracted)
4. Section 22 — Critical Dates table
5. Section 23 — Financial Obligations summary
6. Section 24 — Key Issues & Risks (top 5 red flags, top 5–7 favorable, top 5–7 unfavorable,
   top 10 items for legal/business review)
7. Section 25 — Notes & Comments

**JSON (50–60 KB):** One object with all 25 DDD sections; each field carries its status tag
and metadata inline.

## Step G — Validate Quality

Before writing output, confirm:
- [ ] No fabricated fields — every FACT has complete provenance
- [ ] Parties correctly identified and not swapped
- [ ] All financial values have verbatim + normalized form
- [ ] Currency explicitly stated and verified
- [ ] All Schedule G overrides flagged
- [ ] MISSING count < 30% of DDD fields
- [ ] All dates in ISO 8601 format
- [ ] Output meets size target for selected format

## Step H — Save to Workspace

Save the abstract to:

`{{ WORKSPACE_PATH }}/Reports/[Location]_Lease_Abstract_{{ TODAY }}.{md|json}`

where `[Location]` is the building address from the extracted Premises section.

## Return format

Return ONLY this block — no other commentary:

ABSTRACTION_RESULT
lease_type: <Office or Industrial>
parties: <Landlord name> / <Tenant name>
premises: <building address>
term: <YYYY-MM-DD> to <YYYY-MM-DD>
output: Reports/<filename>.<ext>
missing_rate: <N% of DDD fields with MISSING status>
schedule_g_overrides: <count, or "none">
autofail: <none, or description of what triggered AutoFail>
errors: <none, or description>

## Error handling

- Unreadable document (corrupt, password-protected) → set errors field and stop.
- AutoFail triggered → set autofail field with reason; do not write incomplete output.
- MISSING rate > 30% → report in autofail field and escalate for human review.

--- END SUBAGENT PROMPT ---

---

### Step 2 — Relay result to user

When the subagent returns, parse the `ABSTRACTION_RESULT` block and report:

```
✅ Lease abstract complete
📋 Type:     {lease_type}
👥 Parties:  {parties}
📍 Premises: {premises}
📅 Term:     {term}
📄 Output:   {output}
```

If `schedule_g_overrides` is not "none":
> ⚠️ {schedule_g_overrides} Schedule G override(s) detected — review flagged provisions.

If `autofail` is not "none":
> ❌ AutoFail triggered: {autofail}

If `errors` is not "none":
> ❌ Errors: {errors}

---

## `--criticaldates` MODE — Critical Dates Calendar

### Step 1 — Dispatch subagent

Use the **Agent tool** to dispatch a subagent. If the Agent tool is unavailable, execute
Steps A through F directly in the current context.

Substitute the resolved values for `{{ }}` placeholders, then call the Agent tool with
`description: "Critical dates extraction"` and the prompt below:

--- BEGIN SUBAGENT PROMPT ---

You are a lease critical dates extraction agent. Your sole job is to complete the pipeline
below and return a structured summary. Do not ask questions — execute all steps and report results.

## Parameters

- Input document: {{ DOCUMENT_PATH }} (raw lease or existing abstract)
- Output flags: {{ "--ics" and/or "--csv" if present, "--all" expands to both, or "default" }}
- Workspace: {{ WORKSPACE_PATH }}
- Reports folder: {{ WORKSPACE_PATH }}/Reports/
- Today's date: {{ TODAY }}

## Step A — Source Identification

Determine if the input is a raw lease document or an existing abstract (Markdown or JSON)
produced by the lease-abstraction skill. For an existing abstract, read the Critical Dates
section and cross-reference all other sections for dates not already captured.

## Step B — Extract Dates Across 10 Categories

Scan the entire document for every date, deadline, and notice period:

1. **Lease Term Milestones** — commencement, delivery, fixturing period end, expiry
2. **Option Exercise Deadlines** — renewal notice, purchase option, expansion option
3. **Financial Dates** — rent due dates, escalation dates, operating cost reconciliation,
   tax payments, deposit return
4. **Insurance Requirements** — certificate delivery, renewal notice, coverage review
5. **Compliance & Inspections** — regulatory inspections, environmental assessments,
   building standard reviews
6. **Maintenance Schedules** — HVAC service, capital improvement timelines, repair deadlines
7. **Special Provisions** — any date in Schedule G or equivalent
8. **Default Tracking** — cure period expiry, grace period end, notice of default deadlines
9. **Recurring Events** — annual obligations (capture recurrence rule for ICS)
10. **Custom Provisions** — any other date-triggered obligation

## Step C — Priority Classification

| Priority | Label | Examples |
|----------|-------|---------|
| P1 | CRITICAL | Renewal option notice deadlines, lease expiry, termination notices |
| P2 | HIGH | Rent payments, financial reporting, compliance filings |
| P3 | MEDIUM | Rent reviews, budget planning, scheduled inspections |
| P4 | LOW | Administrative reviews, internal audit reminders |

## Step D — Cascading Reminders

Calculate advance reminder dates for each event:

- **P1:** 365, 270, 180, 120, 90, 60, 30, 14, 7, 3, 1 days before; day-of
- **P2:** 180, 90, 60, 30, 14, 7, 1 days before; day-of
- **P3:** 90, 60, 30, 14, 7 days before
- **P4:** 30, 14 days before

Include estimated financial consequence of a missed deadline where determinable.

## Step E — Generate Outputs

**Always generate — Markdown Calendar Table:**

Columns: Date | Event | Category | Priority | Notice Required | Action Required | Financial Impact if Missed

Group by quarter. Include month-by-month narrative summary and a responsibility matrix
(Tenant / Landlord / Both).

**If `--ics` or `--all` — ICS File (RFC 5545):**
Each event: `SUMMARY`, `DESCRIPTION`, `DTSTART`, `RRULE` (recurring events), `VALARM` blocks
(one per reminder interval).
Save to: `{{ WORKSPACE_PATH }}/Reports/[Location]_Critical_Dates_{{ TODAY }}.ics`

**If `--csv` or `--all` — CSV File:**
Columns: `Date,Event,Category,Priority,Days Until,Notice Required,Action Required,Responsible Party,Financial Impact`
One row per reminder interval (not just per event).
Save to: `{{ WORKSPACE_PATH }}/Reports/[Location]_Critical_Dates_{{ TODAY }}.csv`

## Step F — Save and Confirm

Write all output files. Save the Markdown calendar to:
`{{ WORKSPACE_PATH }}/Reports/[Location]_Critical_Dates_{{ TODAY }}.md`

Include a change log table at the bottom of the Markdown output prepopulated with the
initial extraction entry dated today.

## Return format

Return ONLY this block — no other commentary:

CRITICALDATES_RESULT
location: <building address or document name>
total_dates: N
p1_count: N
p2_count: N
p3_count: N
p4_count: N
output_md: Reports/<filename>.md
output_ics: Reports/<filename>.ics (or "not generated")
output_csv: Reports/<filename>.csv (or "not generated")
errors: <none, or description>

--- END SUBAGENT PROMPT ---

---

### Step 2 — Relay result to user

When the subagent returns, parse the `CRITICALDATES_RESULT` block and report:

```
✅ Critical dates extracted: {total_dates} events ({p1_count} P1 / {p2_count} P2 / {p3_count} P3 / {p4_count} P4)
📅 Markdown: {output_md}
```

If `output_ics` is not "not generated":
> 📆 ICS: {output_ics}

If `output_csv` is not "not generated":
> 📊 CSV: {output_csv}

If `errors` is not "none":
> ❌ Errors: {errors}
