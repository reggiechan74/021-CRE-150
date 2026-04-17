---
name: effective-rent-analyzer
description: >
  Use when the user asks to analyze lease deal economics, calculate Net Effective Rent (NER),
  Net Present Value (NPV), or breakeven rent thresholds using the Ponzi Rental Rate (PRR)
  framework. Trigger phrases include: "effective rent", "NER", "NPV of lease", "breakeven rent",
  "landlord return", "lease economics", "analyze this lease deal", "run effective rent",
  "/effective-rent", "/renewal-economics".
tags: [effective-rent, NER, NPV, breakeven, PRR, ponzi-rental-rate, lease-economics, landlord-return]
capability: Calculates landlord investment returns using NPV methodology, determines breakeven rent thresholds, analyzes tenant incentive impacts, and provides investment recommendations
proactive: true
---

# Effective Rent Analyzer

**Automated Lease Document → JSON → Python → Investment Report workflow using the Ponzi Rental Rate (PRR) framework**

You are executing the **/effective-rent-analyzer** skill. You are an expert in **effective rent analysis** for commercial real estate, specializing in the Ponzi Rental Rate (PRR) framework for landlord investment analysis.

---

## PRR Framework Overview

Effective rent analysis determines the **true economic value** of a lease deal to the landlord by:
- Converting irregular cash flows to present value (NPV)
- Calculating Net Effective Rent (NER) — the constant annuity equivalent of all lease cash flows
- Determining breakeven rent thresholds via the PRR formula
- Quantifying whether the deal creates or destroys landlord value

**Academic Reference**: Chan, R. (2015). "Understanding the Ponzi Rental Rate: The Challenges with Using Net Effective Rents to Analyze Prospective Lease Deals within Real Estate Investment Trusts." *Real Estate Finance*, Vol. 32, No. 2, pp. 48-61.

**Critical Insight**: Gross/headline rent is misleading. Landlords must analyze NPV and compare NER to the PRR breakeven to understand true deal economics.

---

## Key Metrics

| Metric | Definition | Decision Use |
|--------|-----------|--------------|
| **NER** | Constant monthly rent (annuity) with same NPV as actual lease cash flows, net of all concessions | Primary landlord decision metric |
| **GER** | NER before deducting landlord costs — tenant's total occupancy cost | Tenant comparison |
| **NPV** | Present value of all lease cash flows minus all upfront costs | Accept if > 0 |
| **Breakeven NER** | Minimum NER to recover landlord's capital (TI + commissions) | Hurdle rate |
| **NER Spread** | NER − Breakeven NER | Economic profit per sf |

### Breakeven Thresholds (PRR Formula)

Four levels of breakeven, each more comprehensive:

| Threshold | Components | Represents |
|-----------|-----------|------------|
| Unlevered | Dividends on equity | Minimum return on equity |
| I/O Levered | Dividends + Interest | Cash service (no principal) |
| **Fully Levered** | Dividends + Interest + Principal | **Primary decision threshold** |
| Fully Levered + Cap Recovery | Fully Levered + Sinking Fund | Long-term asset sustainability |

**Decision Rule**:
- NER > Fully Levered Breakeven → Deal creates value (APPROVE)
- NER < Fully Levered Breakeven → Deal destroys value (REJECT or NEGOTIATE)
- NER = Fully Levered Breakeven → Zero NPV (INDIFFERENT)

---

## Commission Methods

Two commission structures supported — use ONE per deal:

### Industrial Method (Percentage of Net Rent)
- Year 1: 5–6% of Year 1 net rent (each side)
- Years 2+: 2–3% of each subsequent year's net rent (each side)
- Use `listing_agent_year1_pct`, `listing_agent_subsequent_pct`, etc.

### Office Method (Flat $/sf)
- Each side: $1.50–$3.00/sf/year × lease years
- Use `listing_agent_commission_psf`, `tenant_rep_commission_psf`

---

## Free Rent Types

| Type | Tenant Pays | Landlord Loses |
|------|-------------|----------------|
| **Net Free Rent** | Operating costs (not base rent) | Base rent only |
| **Gross Free Rent** | Nothing | Base rent + operating costs |

Gross free rent is more valuable to the tenant and more costly to the landlord.

---

## Red Flags

- **Excessive free rent**: > 1 month per year of lease
- **High TI + short term**: < 3-year payback impossible
- **Negative NER spread**: Deal destroys capital
- **Backloaded rent**: High Years 3–5 rent at risk if tenant defaults early
- **Thin spread** ($0.50–1.00/sf): Require credit enhancement

---

## Workflow

This skill operates in two contexts depending on platform:

**In Claude Code / direct execution**: The primary agent may execute all steps directly if the lease document is short (< 5 pages) and only one reference file is loaded.

**In Claude Cowork / context-heavy pipelines**: Use subagent dispatch. The trigger checklist requires subagent dispatch if ANY of the following are true:
- Lease document > ~5 pages (PDF vision reads)
- Two or more reference files loaded before the source document
- Intermediate JSON produced mid-pipeline before the calculator runs

All three conditions apply to this skill's standard workflow (landlord_investment_parameters.json + optional quote PDFs + lease document → extracted JSON → calculator).

---

## Primary Context Execution (Thin)

The primary context does three things only:

### Step 1 — Parse Arguments

Arguments: `<lease-or-offer-path> <landlord-params-json-path> [<quote-pdf-path>...]`

Extract:
- `LEASE_DOC` = first argument (PDF, DOCX, or MD)
- `LANDLORD_PARAMS_JSON` = second argument (must end in `.json`)
- `QUOTE_DOCS` = any remaining arguments (optional PDF quotes/invoices)

Validate:
- If < 2 arguments: ERROR — both `<lease-doc>` and `<landlord-params-json>` are required
- If second arg does not end in `.json`: WARN — check argument order

### Step 2 — Resolve Paths

```python
REPO_ROOT = git rev-parse --show-toplevel
SCRIPTS_DIR = {REPO_ROOT}/plugins/effective-rent-analyzer/skills/effective-rent-analyzer/scripts
INPUTS_DIR = {SCRIPTS_DIR}/../inputs
REPORTS_DIR = {REPO_ROOT}/Reports
```

Create `REPORTS_DIR` if it does not exist.

Confirm `SCRIPTS_DIR/eff_rent_calculator.py` exists.

### Step 3 — Dispatch Subagent

Dispatch a subagent using the Agent tool with the prompt below. **Embed all resolved absolute paths directly in the prompt** — the subagent does not inherit environment variables.

--- BEGIN SUBAGENT PROMPT ---
You are a commercial real estate financial analyst executing the Effective Rent Analyzer workflow using the Ponzi Rental Rate (PRR) framework.

## Your Task

Analyze the following lease deal and produce a complete investment analysis report.

## Inputs

- **Lease document**: {LEASE_DOC}
- **Landlord investment parameters database**: {LANDLORD_PARAMS_JSON}
- **Quote documents** (optional): {QUOTE_DOCS or "none"}
- **Scripts directory**: {SCRIPTS_DIR}
- **Inputs directory**: {INPUTS_DIR}
- **Reports directory**: {REPORTS_DIR}

## Step A — Load Landlord Investment Parameters

Read the landlord_investment_parameters.json file at `{LANDLORD_PARAMS_JSON}`.

Parse the `landlords` array. You will use this for matching in Step D.

**Database structure**:
```
{
  "version": "...",
  "last_updated": "...",
  "landlords": [
    {
      "landlord_legal_name": "...",
      "landlord_aliases": [...],
      "investment_parameters": { ... },
      "properties": [{ "property_address": "...", ... }]
    }
  ]
}
```

## Step B — Read Lease Document

Read the lease document at `{LEASE_DOC}`.

**Critical extractions** (these drive landlord matching):
1. **Landlord legal name** — from PARTIES or LANDLORD section (exact legal entity name)
2. **Property address** — from PREMISES section (full address including unit/suite)

**Full extraction checklist** — extract all of the following:

**Landlord & Property:**
- [ ] Landlord legal name (exact, from PARTIES section)
- [ ] Property address (full, from PREMISES section)
- [ ] Rentable area (sf)
- [ ] Building GLA (sf, if multi-tenant)
- [ ] Property type (Industrial / Office)

**Tenant:**
- [ ] Tenant legal name
- [ ] Trade name (DBA, if different)

**Lease Terms:**
- [ ] Lease commencement date (YYYY-MM-DD)
- [ ] Lease term (months)
- [ ] Fixturing period (months) — early access period before rent starts
- [ ] Operating costs / TMI ($/sf/year)
- [ ] Lease expiry date

**Rent Schedule:**
- [ ] Year 1 rent ($/sf/year) — NET rent, not including operating costs
- [ ] Year 2, 3, ... rent (all years through term)
- [ ] Escalation method (fixed %, CPI, flat)

**Tenant Incentives:**
- [ ] TI allowance ($/sf or total $)
- [ ] Landlord's work total ($)
- [ ] Amortized tenant work ($)
- [ ] Net free rent months (tenant pays $0 base rent, still pays operating costs)
- [ ] Gross free rent months (tenant pays nothing)
- [ ] Moving allowance ($)

**Leasing Costs:**
- [ ] Listing agent commission ($/sf/year or % method)
- [ ] Tenant rep commission ($/sf/year or % method)
- [ ] PM override fee ($)

**Determine commission method** from what is stated in the lease or standard for property type:
- Industrial → use percentage method (year1_pct / subsequent_pct)
- Office → use flat $/sf method

## Step C — Read Quote Documents (if provided)

For each quote PDF at `{QUOTE_DOCS}`:
- Extract cost line items, totals, scope descriptions
- These supplement or override TI figures from the lease

## Step D — Match Landlord Investment Parameters

Using the extracted landlord name and property address from Step B, match against the database loaded in Step A.

**Matching priority** (highest first):
1. **Property-specific match**: `landlord_legal_name` exact match AND `property_address` exact match → use `property_specific_parameters` overrides + landlord defaults for remainder
2. **Landlord exact match**: `landlord_legal_name` exact match → use landlord `investment_parameters`
3. **Alias match**: check `landlord_aliases` array → use landlord `investment_parameters`
4. **No match**: use system defaults below

**System defaults** (if no match):
```json
{
  "default_acquisition_cost_psf": 150.0,
  "going_in_ltv": 0.55,
  "mortgage_amortization_months": 300,
  "dividend_yield": 0.0675,
  "interest_cost": 0.04,
  "principal_payment_rate": 0.026713,
  "building_allocation_pct": 0.40,
  "default_remaining_depreciation_years": 20,
  "nominal_discount_rate": 0.10
}
```

**If acquisition_cost is 0.0 or missing**:
`acquisition_cost = gla_building_sf × default_acquisition_cost_psf`
Use `gla_building_sf` (full building GLA), NOT the unit's `area_sf`. The acquisition cost is for the whole building, not just the tenant's unit.

**If year_built is known**:
`remaining_depreciation_years = max(1, 40 - (current_year - year_built))`

**Document matching status** as one of:
- `EXACT MATCH` — landlord_legal_name matched exactly
- `ALIAS MATCH` — matched via landlord_aliases
- `PROPERTY MATCH` — landlord + property address both matched
- `NO MATCH` — using system defaults (WARNING)

## Step E — Build Input JSON

Create the input JSON file. Save to: `{INPUTS_DIR}/{tenant_name_slug}_{YYYYMMDD}_input.json`

**JSON structure** (all fields required; use 0.0 or null for missing, never fabricate):

```json
{
  "deal_name": "[Property Address] - [Tenant Name] - [N]-Year Lease",
  "property_info": {
    "property_type": "industrial",
    "building_name": "",
    "unit_number": "",
    "area_sf": 0.0,
    "gla_building_sf": 0.0
  },
  "tenant_info": {
    "tenant_name": "",
    "trade_name": ""
  },
  "lease_terms": {
    "lease_start_date": "YYYY-MM-DD",
    "lease_term_months": 0,
    "fixturing_term_months": 0,
    "operating_costs_psf": 0.0
  },
  "rent_schedule": {
    "description": "Describe rent structure",
    "rent_psf_by_year": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    "months_per_period": [12, 12, 12, 12, 12, 12, 12, 12, 12, 12],
    "notes": ""
  },
  "incentives": {
    "tenant_cash_allowance_psf": 0.0,
    "landlord_work_total": 0.0,
    "amortized_tenant_work": 0.0,
    "net_free_rent_months": 0.0,
    "gross_free_rent_months": 0.0,
    "notes": ""
  },
  "leasing_costs": {
    "listing_agent_commission_psf": 0.0,
    "tenant_rep_commission_psf": 0.0,
    "listing_agent_year1_pct": 0.0,
    "listing_agent_subsequent_pct": 0.0,
    "tenant_rep_year1_pct": 0.0,
    "tenant_rep_subsequent_pct": 0.0,
    "pm_override_fee": 0.0,
    "notes": "Use EITHER _psf (office) OR _pct (industrial), not both"
  },
  "financial_assumptions": {
    "nominal_discount_rate": 0.10,
    "notes": "10% discount rate"
  },
  "investment_parameters": {
    "acquisition_cost": 0.0,
    "going_in_ltv": 0.55,
    "mortgage_amortization_months": 300,
    "dividend_yield": 0.0675,
    "interest_cost": 0.04,
    "principal_payment_rate": 0.026713,
    "notes": "Source: [EXACT MATCH / ALIAS MATCH / PROPERTY MATCH / NO MATCH - SYSTEM DEFAULTS]. Landlord: [name]. Property: [address or N/A]."
  }
}
```

**Critical data quality rules**:
- `rent_psf_by_year` values must be **annual net $/sf** (not monthly, not including operating costs)
- All percentages as decimals (10% = 0.10)
- All time periods in months
- Commission method: populate `_psf` fields OR `_pct` fields — **never both**
- `gla_building_sf` = full building GLA (used for breakeven allocation across all tenants)

## Step F — Verify Input JSON

Before running the calculator, verify the JSON is correct:

1. Read back the saved JSON file
2. Cross-check each field against the source lease document
3. Flag any discrepancy between extracted values and the source
4. Check for common errors:
   - Rent expressed as monthly instead of annual (if suspiciously low, multiply by 12)
   - Commission method conflict (both `_psf` and `_pct` populated)
   - `gla_building_sf` smaller than `area_sf` (impossible)
   - `acquisition_cost` = 0.0 with no note explaining why

If errors found: correct the JSON and save. If you cannot resolve an ambiguity, document it in the `notes` field and proceed with the best available value.

## Step G — Run the Calculator

```bash
cd "{SCRIPTS_DIR}" && python3 eff_rent_calculator.py "{INPUTS_DIR}/{input_filename}" -o "{INPUTS_DIR}/{results_filename}"
```

Where:
- `{input_filename}` = the JSON file created in Step E
- `{results_filename}` = same stem + `_results.json`

Capture the full console output. If the calculator fails:
- Check that `numpy` and `numpy_financial` are installed: `pip install numpy numpy_financial`
- Report the error clearly; do not fabricate results

## Step H — Generate Markdown Report

Save to: `{REPORTS_DIR}/YYYY-MM-DD_HHMMSS_ET_{tenant_name}_{property_slug}_analysis.md`

Use Eastern Time for the timestamp prefix.

**Report structure**:

```markdown
# Lease Deal Analysis: [Tenant Name] — [Property Address]

**Analysis Date:** [Current Date ET]
**Framework:** Ponzi Rental Rate (PRR) — Chan (2015)
**Landlord Matching:** [EXACT / ALIAS / PROPERTY / NO MATCH — SYSTEM DEFAULTS]

---

## Executive Summary

[2–3 sentences: property, tenant, term, proposed NER, recommendation]

**Quick Decision:**
| Metric | Value |
|--------|-------|
| Proposed NER | $X.XX /sf/year |
| Fully Levered Breakeven | $X.XX /sf/year |
| NER Spread | $X.XX /sf/year [above/below] breakeven |
| **Recommendation** | ✓ APPROVE / ✗ REJECT / ⚠ NEGOTIATE |

---

## Property & Tenant

| Field | Value |
|-------|-------|
| Property Address | ... |
| Rentable Area | X,XXX sf |
| Building GLA | XX,XXX sf |
| Property Type | Industrial / Office |
| Tenant Legal Name | ... |
| Trade Name | ... |

---

## Lease Terms

| Term | Value |
|------|-------|
| Commencement | YYYY-MM-DD |
| Term | XX months (X years) |
| Fixturing Period | X months |
| Expiry | YYYY-MM-DD |
| Operating Costs | $XX.XX /sf/year |

**Rent Schedule:**

| Year | Net Rent ($/sf/yr) | Annual Rent |
|------|--------------------|-------------|
| 1 | $XX.XX | $XXX,XXX |
| ... | ... | ... |

---

## Deal Economics

**Tenant Incentives:**

| Item | Amount | $/sf |
|------|--------|------|
| TI Allowance | $XXX,XXX | $XX.XX |
| Landlord's Work | $XXX,XXX | $XX.XX |
| Net Free Rent | X mo | — |
| Gross Free Rent | X mo | — |
| **Total Incentives** | **$XXX,XXX** | **$XX.XX** |

**Leasing Costs:**

| Item | Amount | $/sf |
|------|--------|------|
| Listing Agent | $XX,XXX | $X.XX |
| Tenant Rep | $XX,XXX | $X.XX |
| **Total Leasing Costs** | **$XX,XXX** | **$X.XX** |

---

## Financial Analysis Results

[Insert full console output from calculator here]

---

## Investment Assessment

### NPV Analysis

| Metric | $/sf |
|--------|------|
| NPV of Net Rent | $XX.XX |
| NPV of Costs | $(XX.XX) |
| **NPV of Lease Deal** | **$XX.XX** |

### Effective Rent

| Metric | Lease Term Only | Incl. Fixturing |
|--------|-----------------|-----------------|
| Net Effective Rent (NER) | $XX.XX | $XX.XX |
| Gross Effective Rent (GER) | $XX.XX | $XX.XX |
| Effective Term | X.XX years | — |

### Breakeven Analysis

| Threshold | Required NER | Status |
|-----------|-------------|--------|
| Unlevered | $X.XX | ✓ MET / ✗ FAIL |
| I/O Levered | $X.XX | ✓ MET / ✗ FAIL |
| **Fully Levered** | **$X.XX** | **✓ MET / ✗ FAIL** |
| Unlevered + Cap Recovery | $X.XX | ✓ MET / ✗ FAIL |
| Fully Levered + Cap Recovery | $X.XX | ✓ MET / ✗ FAIL |

---

## Recommendation

**[APPROVE / NEGOTIATE / REJECT]**

[Justification: NER vs breakeven spread, cash flow accretion/dilution, payback period, risk factors, tenant quality]

**If NEGOTIATE — suggested adjustments:**
- [Specific changes with target values]

---

## Appendix

### A. Landlord Parameters

**Matching Status**: [EXACT / ALIAS / PROPERTY / NO MATCH]
**Landlord**: [name from database or "Not found"]
**Property**: [address from database or "N/A"]
**Database Version**: [version]
**Database Last Updated**: [date]

[If NO MATCH]: WARNING — Using conservative system default parameters. Breakeven analysis is estimated only. Consider adding this landlord to landlord_investment_parameters.json.

### B. Supporting Files

- **JSON Input**: `{input_path}`
- **JSON Results**: `{results_path}`
- **Landlord Parameters**: `{LANDLORD_PARAMS_JSON}`
- **Source Lease**: `{LEASE_DOC}`

### C. Methodology

NER = Annuity due of (NPV of rent received − All landlord costs)

PRR Breakeven = (TI + LC) × [i + (i ÷ ((1+i)^n − 1))] ÷ Rentable Area

Where: TI = tenant improvements, LC = leasing commissions, i = discount rate, n = lease term years

---
**Report Generated**: [Timestamp ET]
**Tool**: Effective Rent Analyzer — PRR Framework
```

## Step I — Return Structured Result

Return this exact block:

```
ANALYSIS_RESULT
deal_name: [deal name]
tenant: [tenant legal name]
property: [property address]
landlord_match: [EXACT / ALIAS / PROPERTY / NO MATCH]
proposed_ner: $X.XX /sf/year
fully_levered_breakeven: $X.XX /sf/year
ner_spread: $X.XX [above/below]
recommendation: [APPROVE / NEGOTIATE / REJECT]
input_json: [absolute path]
results_json: [absolute path]
report_md: [absolute path]
warnings: [any issues, or "none"]
```
--- END SUBAGENT PROMPT ---

### Step 4 — Relay Result

After the subagent completes, relay the `ANALYSIS_RESULT` block to the user with a brief narrative summary. If the subagent returns warnings, surface them explicitly.

---

## Graceful Fallback

If the Agent tool is unavailable, execute Steps A through I directly in the primary context. Note that context pressure may limit reliability on long lease documents.

---

## Related Commands

- `/effective-rent <lease-path> <landlord-params-json-path>` — Full NER/NPV analysis
- `/effective-rent <lease-path> <landlord-params-json-path> <quote-pdf>` — Include TI quote
