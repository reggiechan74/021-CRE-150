# CRE Lease Abstraction Plugin

Commercial real estate lease abstraction for North American office and industrial leases. Uses the REIXS-LA-NA-001 extraction standard and a 258-field Domain Data Dictionary (DDD) to produce structured, provenance-tracked lease abstracts and critical dates calendars.

---

## Components

### Skill: `lease-abstraction`

Single entry point for all lease abstraction work. Activates when you ask to abstract a lease, extract terms, analyze CRE provisions, generate critical dates, or apply REIXS/DDD methodology.

**Default mode — Full Lease Abstraction**

Runs the complete 8-step REIXS extraction workflow across all 25 DDD sections with FACT/INFERENCE/MISSING/CONFLICT status tagging, AutoFail guards, Schedule G override detection, and financial/risk analysis. Output saved to `<workspace>/Reports/`.

Example triggers:
- "Abstract this lease" + attach or point to a PDF/DOCX
- "Extract all terms from this lease agreement"
- "Analyze this CRE lease and flag risks"
- "Abstract this lease -json" — produces JSON output instead of Markdown

**`--criticaldates` mode — Critical Dates Calendar**

Extracts all date-triggered obligations across 10 categories, assigns P1–P4 priority, calculates cascading reminders, and generates calendar outputs.

Example triggers:
- "Abstract this lease --criticaldates"
- "Extract critical dates from this lease"
- "Generate a critical dates calendar --ics --csv"

Output flags:
- *(default)* Markdown table with priority, notice requirements, financial impact
- `--ics` — RFC 5545 iCalendar file importable into Outlook and Google Calendar
- `--csv` — CSV file for Excel and lease management software
- `--all` — all three formats

### Reference Files (bundled)

| File | Purpose |
|------|---------|
| `skills/lease-abstraction/references/reixs.runtime.json` | REIXS-LA-NA-001 behavioral extraction rules |
| `skills/lease-abstraction/references/lease_abstraction_ddd.md` | 258-field Domain Data Dictionary (25 sections) |

---

## Extraction Standards

All abstractions conform to REIXS-LA-NA-001:

- **FACT** — verbatim extraction with page + clause provenance
- **INFERENCE** — derived values with confidence score and reasoning
- **MISSING** — absent fields set to null; never fabricated
- **CONFLICT** — contradictory values cited with all sources

Critical sections (Parties, Premises, Term, Rent) carry 2× scoring weight. Schedule G provisions override main body terms and are flagged `[SCHEDULE_G_OVERRIDE]`.

---

## Setup

No API keys or external services required. The plugin runs entirely on Claude with access to your workspace folder. Ensure lease documents are saved in your selected workspace folder before running.
