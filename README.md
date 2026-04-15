# 021 — Claude Cowork for Real Estate (CRE-150)

![Workshop](https://img.shields.io/badge/021_Events-CRE--150-0066cc?style=flat-square)
![Platform](https://img.shields.io/badge/platform-Claude_Cowork-5436DA?style=flat-square)
![Plugins](https://img.shields.io/badge/plugins-7-brightgreen?style=flat-square)
![cre-lease-abstraction](https://img.shields.io/badge/cre--lease--abstraction-v0.3.0-blue?style=flat-square)
![mls-extractor](https://img.shields.io/badge/mls--extractor-v0.5.1-blue?style=flat-square)
![mcda-sales-comparison](https://img.shields.io/badge/mcda--sales--comparison-v1.0.0-blue?style=flat-square)
![mcda-lease-comparison](https://img.shields.io/badge/mcda--lease--comparison-v1.0.0-blue?style=flat-square)
![tenant-credit](https://img.shields.io/badge/tenant--credit-v1.0.0-blue?style=flat-square)
![cam-reconciliation-cre](https://img.shields.io/badge/cam--reconciliation--cre-v0.1.0-blue?style=flat-square)
![roof-replacement-review](https://img.shields.io/badge/roof--replacement--review-v0.1.0-blue?style=flat-square)

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

### `mcda-sales-comparison` — v1.0.0

MCDA ordinal ranking for fee simple sales comparison valuation. Ranks a subject property and comparables on weighted characteristics, maps composite scores to value via interpolation and regression.

**Trigger:** "Run MCDA sales comparison" + point to a PDF or JSON

Accepts CoStar or broker comparable sale reports, extracts property attributes, calculates a composite MCDA score for each sale, and interpolates a value opinion for the subject property. Supports up to 25 weighted variables with dynamic weight redistribution when data is sparse.

```
Run MCDA sales comparison /path/to/comparables.pdf
Run MCDA sales comparison /path/to/input.json --stats
```

---

### `mcda-lease-comparison` — v1.0.0

MCDA competitive positioning analysis for commercial real estate leasing. Ranks a subject property against market comparables on up to 25 weighted variables and provides strategic pricing recommendations to achieve Top 3 market positioning.

**Trigger:** "Relative valuation" / "competitive positioning" / "rank this property" + point to a PDF or JSON

Extracts property data from CoStar or broker market reports, calculates driving distances (optional, requires Distancematrix.ai API key), runs the MCDA ranking engine, and produces a sensitivity analysis showing exactly what it would take to reach the Top 3 competitive tier.

Supports four tenant personas — Default, 3PL/Distribution, Manufacturing, Office/Flex — each with pre-tuned variable weights.

```
/mcda-lease-comparison /path/to/market_report.pdf
/mcda-lease-comparison /path/to/input.json --persona 3pl --full --stats
```

---

### `tenant-credit` — v1.0.0

Tenant credit analysis for commercial real estate lease approvals. Extracts financial data from PDF financial statements, runs a 100-point weighted credit scoring algorithm (A–F rating), estimates default probability and expected loss, and generates a comprehensive credit report with security deposit and approval recommendations.

**Trigger:** "Tenant credit analysis" / "analyze tenant financials" / "creditworthiness" + point to a PDF

Accepts one to three years of financial statements. Extracts balance sheet and income statement data, calculates 15+ financial ratios across four categories (liquidity, leverage, profitability, rent coverage), scores the tenant on a 100-point scale, and recommends a security amount with step-down schedule.

```
/tenant-credit /path/to/2024_financials.pdf
/tenant-credit /path/to/2024_financials.pdf /path/to/2023_financials.pdf
/tenant-credit /path/to/2024_financials.pdf /path/to/lease_proposal.pdf
```

---

### `cam-reconciliation-cre` — v0.1.0

Landlord-side CAM true-up for commercial real estate. Combines lease-aware recoverability rules with deterministic Python math so the same inputs always produce the same tenant charges, landlord absorption totals, and comparison output.

**Trigger:** `/cam-reconcile <property-dir>`

Ingests a property package (`property.yaml`, `leases.json`, `gl.csv`, `budget.md`), applies lease-aware corrections for duplicate invoices, turnover charges, management-fee basis errors, modified-gross exclusions, restaurant carve-outs, base years, and CAM caps, then emits typed manifests, tenant PDF statements, a workpaper workbook, an audit log, and an optional Anthropic comparison report.

```
/cam-reconcile <property-dir>
/cam-explain <allocated-manifest.json> <tenant-id-or-line-id>
/cam-compare-vs-anthropic <allocated-manifest.json> <anthropic-output.txt>
```

---

### `roof-replacement-review` — v0.1.0

Owner-side tender evaluation for Ontario roof replacement projects. Scores contractor bids against the owner's RFP using mandatory pass/fail gates plus a weighted MCDA rubric. Supports commercial (OBC Part 3) low-slope membrane systems and residential (OBC Part 9) steep-slope systems.

**Trigger:** `/roof-review <rfp.pdf> <bid1.pdf> <bid2.pdf> ...`

Parses the RFP and each bid into a normalized tender manifest, applies qualification gates (WSIB, CGL, bonding, WAH training, Skilled Trades Ontario, financial capacity), scores a weighted matrix across Price / Technical / Experience / Warranty / Schedule / Qualifications, and produces a scoring matrix, a red-flag report, and a recommendation memo with citations to OBC, CRCA, and CCDC-23.

```
/roof-review <rfp.pdf> <bid1.pdf> <bid2.pdf> ...
/roof-redflags <manifest.json>
/roof-memo <manifest.json>
```

---

## Cowork Optimization

All seven plugins are designed specifically for Claude Cowork's context architecture. Each skill follows a three-step dispatch pattern:

1. **Primary context (thin)** — resolves file paths and environment variables, dispatches a subagent
2. **Extraction subagent (full 200k window)** — handles all document reads, extraction, and file writes
3. **Primary context** — relays the structured result to the user

This keeps the primary context from being exhausted by large document reads, which is the most common failure mode for multi-step skills in Cowork. See `cowork_lessons_learned.md` for the full design rationale.

---

## Installation

Load all plugins into your Claude Cowork workspace by pointing to this repository in your plugin settings.

- `cre-lease-abstraction`, `mls-extractor`, `mcda-sales-comparison`, `mcda-lease-comparison`, `tenant-credit`, `cam-reconciliation-cre`, `roof-replacement-review` — no API keys required
- `mcda-lease-comparison` — optional: set `DISTANCEMATRIX_API_KEY` for automatic driving distance calculation (free tier: 1,000 elements/month at distancematrix.ai)
- `cam-reconciliation-cre`, `roof-replacement-review` — require Python dependencies from each plugin's `requirements.txt`

---

## Workshop

**Series:** 021 Events
**Session:** CRE-150 — Claude Cowork for Real Estate
**Author:** Reggie Chan
