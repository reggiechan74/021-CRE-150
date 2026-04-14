---
name: lease-abstraction
description: >
  This skill should be used when the user asks to "abstract a lease", "extract lease terms",
  "summarize a commercial lease", "analyze a CRE lease", "review lease provisions",
  "identify lease risks", "extract critical dates from a lease", "generate a critical dates
  calendar", "create an ICS file from a lease", "export lease dates to CSV", or needs to
  apply REIXS methodology, the 258-field Domain Data Dictionary, or REIXS-LA-NA-001
  extraction standards to a commercial real estate lease document.
version: 0.2.0
---

## Mode Detection

Inspect the user's message for the `--criticaldates` flag or equivalent intent (e.g., "critical dates only", "just the dates", "generate calendar").

- **Default mode** — run the full 8-step REIXS lease abstraction (Sections 1–25)
- **`--criticaldates` mode** — skip full abstraction; run only the critical dates extraction and calendar generation workflow

If no document path is provided, scan the workspace folder for lease documents (PDF, DOCX, MD) and ask the user which file to process before starting.

---

## Governance Reference Files

Load both reference files before any extraction work:

- `${CLAUDE_PLUGIN_ROOT}/skills/lease-abstraction/references/reixs.runtime.json` — REIXS-LA-NA-001 behavioral rules: status classifications, AutoFail conditions, validation thresholds
- `${CLAUDE_PLUGIN_ROOT}/skills/lease-abstraction/references/lease_abstraction_ddd.md` — 258-field Domain Data Dictionary: 25 sections, field definitions, data types, critical scoring weights

---

## DEFAULT MODE — Full Lease Abstraction

### Step 1 — Load Governance Frameworks

Read both reference files above. Internalize both fully before touching the source document.

### Step 2 — Parse Input

Identify the document path or URL from the user's message. If a `-json` flag or "JSON output" is requested, output format is JSON (50–60 KB target). Default is Markdown (30–40 KB target).

### Step 3 — Load and Prepare Document

- **PDF / MD / TXT**: Use the `Read` tool directly
- **DOCX**: Use the `Read` tool — it handles Word documents natively in Cowork. If it returns garbled output, fall back to Python: `pip install python-docx --break-system-packages -q` then `python3 -c "import docx; doc=docx.Document('<path>'); print('\n'.join([p.text for p in doc.paragraphs]))"`
- **URL**: Use `WebFetch`
- **Large documents**: Process in sections; merge results

Do not assume `pandoc` or any other CLI tool is pre-installed on the user's machine.

### Step 4 — Classify Lease Type

Identify the lease as **Industrial** or **Office** based on permitted use, building type, and operational provisions. State the classification explicitly before extraction begins.

### Step 5 — Extract with REIXS Rules

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

**Schedule G override rule:** Special Provisions that contradict the main body take precedence. Tag every such override `[SCHEDULE_G_OVERRIDE]`.

**Financial rule:** Extract verbatim text first; provide normalized numeric form as a separate field. Determine currency from document context — never assume.

**Date rule:** Normalize all dates to ISO 8601 (`YYYY-MM-DD`).

**Critical sections (2× scoring weight):** Parties (2), Premises (3), Term (4), Rent (5).

### Step 6 — Format Output

**Markdown (30–40 KB):**
1. Executive Summary — lease type, parties, key dates, total financial exposure
2. Key Terms snapshot
3. Sections 1–21 (extracted)
4. Section 22 — Critical Dates table
5. Section 23 — Financial Obligations summary
6. Section 24 — Key Issues & Risks (top 5 red flags, top 5–7 favorable, top 5–7 unfavorable, top 10 items for legal/business review)
7. Section 25 — Notes & Comments

**JSON (50–60 KB):** One object with all 25 DDD sections; each field carries its status tag and metadata inline.

### Step 7 — Validate Quality

Before writing output, confirm:
- [ ] No fabricated fields — every FACT has complete provenance
- [ ] Parties correctly identified and not swapped
- [ ] All financial values have verbatim + normalized form
- [ ] Currency explicitly stated and verified
- [ ] All Schedule G overrides flagged
- [ ] MISSING count < 30% of DDD fields
- [ ] All dates in ISO 8601 format
- [ ] Output meets size target for selected format

### Step 8 — Save to Workspace

Locate the workspace folder (run `ls /sessions/*/mnt/` in Bash). Create a `Reports/` subdirectory inside it if it does not exist. Save the abstract to:

`<workspace-folder>/Reports/[Location]_Lease_Abstract_[YYYY-MM-DD].{md|json}`

where `[Location]` is the building address from the extracted Premises section and `[YYYY-MM-DD]` is today's date from the environment. Confirm the full file path at the end of your response.

---

## `--criticaldates` MODE — Critical Dates Calendar

### Step 1 — Source Identification

Determine if the input is a raw lease document or an existing abstract (Markdown or JSON) produced by this skill. For an existing abstract, read the Critical Dates section and cross-reference all other sections for dates not already captured.

### Step 2 — Extract Dates Across 10 Categories

Scan the entire document for every date, deadline, and notice period:

1. **Lease Term Milestones** — commencement, delivery, fixturing period end, expiry
2. **Option Exercise Deadlines** — renewal notice, purchase option, expansion option
3. **Financial Dates** — rent due dates, escalation dates, operating cost reconciliation, tax payments, deposit return
4. **Insurance Requirements** — certificate delivery, renewal notice, coverage review
5. **Compliance & Inspections** — regulatory inspections, environmental assessments, building standard reviews
6. **Maintenance Schedules** — HVAC service, capital improvement timelines, repair deadlines
7. **Special Provisions** — any date in Schedule G or equivalent
8. **Default Tracking** — cure period expiry, grace period end, notice of default deadlines
9. **Recurring Events** — annual obligations (capture recurrence rule for ICS)
10. **Custom Provisions** — any other date-triggered obligation

### Step 3 — Priority Classification

| Priority | Label | Examples |
|----------|-------|---------|
| P1 | CRITICAL | Renewal option notice deadlines, lease expiry, termination notices |
| P2 | HIGH | Rent payments, financial reporting, compliance filings |
| P3 | MEDIUM | Rent reviews, budget planning, scheduled inspections |
| P4 | LOW | Administrative reviews, internal audit reminders |

### Step 4 — Cascading Reminders

Calculate advance reminder dates for each event:

- **P1:** 365, 270, 180, 120, 90, 60, 30, 14, 7, 3, 1 days before; day-of
- **P2:** 180, 90, 60, 30, 14, 7, 1 days before; day-of
- **P3:** 90, 60, 30, 14, 7 days before
- **P4:** 30, 14 days before

Include estimated financial consequence of a missed deadline where determinable.

### Step 5 — Generate Outputs

**Always generate — Markdown Calendar Table:**

```
| Date | Event | Category | Priority | Notice Required | Action Required | Financial Impact if Missed |
```

Group by quarter. Include month-by-month narrative summary and a responsibility matrix (Tenant / Landlord / Both).

**If `--ics` or `--all` — ICS File (RFC 5545):**
Each event: `SUMMARY`, `DESCRIPTION`, `DTSTART`, `RRULE` (recurring events), `VALARM` blocks (one per reminder interval).
Save to: `<workspace-folder>/Reports/[Location]_Critical_Dates_[YYYY-MM-DD].ics`

**If `--csv` or `--all` — CSV File:**
Columns: `Date,Event,Category,Priority,Days Until,Notice Required,Action Required,Responsible Party,Financial Impact`
One row per reminder interval (not just per event).
Save to: `<workspace-folder>/Reports/[Location]_Critical_Dates_[YYYY-MM-DD].csv`

### Step 6 — Save and Confirm

Locate the workspace folder (`ls /sessions/*/mnt/`). Create `Reports/` if needed. Write all output files. Confirm full paths and state total dates extracted with a breakdown by priority tier.

Include a change log table at the bottom of the Markdown output prepopulated with the initial extraction entry dated today.
