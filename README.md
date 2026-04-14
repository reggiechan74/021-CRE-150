# 021 — Claude Cowork for Real Estate (CRE-150)

Plugin repository for the **CRE-150** training workshop in the **021 Events** series.

CRE-150 covers applied AI workflows for commercial real estate professionals using Claude Cowork. These plugins are the hands-on toolkit for the session — participants install them into their Cowork workspace and run the live extraction exercises against real lease documents and MLS reports.

---

## Plugins

### `cre-lease-abstraction` — v0.3.0

Abstracts commercial real estate leases using the REIXS-LA-NA-001 extraction standard and a 258-field Domain Data Dictionary across 25 sections.

**Trigger:** "Abstract this lease" + point to a PDF or DOCX

**Default mode — Full Abstraction**

Extracts all 25 DDD sections with FACT / INFERENCE / MISSING / CONFLICT status tagging, AutoFail guards, Schedule G override detection, and financial risk analysis. Output: Markdown (30–40 KB) or JSON (50–60 KB), saved to your workspace `Reports/` folder.

**`--criticaldates` mode — Critical Dates Calendar**

Extracts every date-triggered obligation across 10 categories, assigns P1–P4 priority, and calculates cascading reminders. Optional `--ics` and `--csv` output for import into Outlook, Google Calendar, or lease management software.

```
Abstract this lease /path/to/lease.pdf
Abstract this lease /path/to/lease.pdf --criticaldates --ics --csv
Abstract this lease /path/to/lease.pdf -json
```

---

### `mls-extractor` — v0.5.1

Extracts commercial MLS property listings from PDF reports into professionally formatted Excel spreadsheets.

**Trigger:** "Extract MLS data from" + point to a PDF

Reads the PDF with LLM vision, extracts a 34-field schema for every listing, verifies the extracted JSON against the source PDF, then produces an Excel file with subject property highlighting and correct column ordering.

```
Extract MLS data from Mississauga_industrial.pdf
Extract MLS data from report.pdf --subject="2550 Stanfield"
```

---

## Cowork Optimization

Both plugins are designed specifically for Claude Cowork's context architecture. Each skill follows a three-step dispatch pattern:

1. **Primary context (thin)** — resolves file paths and environment variables, dispatches a subagent
2. **Extraction subagent (full 200k window)** — handles all document reads, extraction, and file writes
3. **Primary context** — relays the structured result to the user

This keeps the primary context from being exhausted by large document reads, which is the most common failure mode for multi-step skills in Cowork. See `cowork_lessons_learned.md` for the full design rationale.

---

## Installation

Load both plugins into your Claude Cowork workspace by pointing to this repository in your plugin settings. No API keys or external services required — everything runs on Claude with access to your workspace folder.

---

## Workshop

**Series:** 021 Events
**Session:** CRE-150 — Claude Cowork for Real Estate
**Author:** Reggie Chan
