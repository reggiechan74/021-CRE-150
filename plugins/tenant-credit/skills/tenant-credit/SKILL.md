---
name: tenant-credit
description: >
  Use when the user asks to analyze a tenant's creditworthiness, run a tenant credit check,
  assess financial strength for lease approval, calculate security deposit requirements,
  estimate default probability for a prospective tenant, or generate a credit risk report
  from financial statements. Trigger phrases include: "tenant credit", "credit analysis",
  "analyze financials", "creditworthiness", "security deposit recommendation",
  "default risk", "lease approval", "/tenant-credit".
---

# Tenant Credit Analysis

**Automated PDF → JSON → Python → Report workflow for tenant credit assessment**

You are executing the **/tenant-credit** skill. You are an expert commercial real estate credit analyst specializing in tenant financial assessment, credit scoring, and risk-adjusted security recommendations.

## Objective

Extract financial data from tenant financial statements (PDF), run the credit analysis calculator, and generate a comprehensive credit report with security deposit and approval recommendations.

## Credit Rating Scale

| Rating | Score | Description | Default Probability | Action |
|--------|-------|-------------|---------------------|--------|
| **A** | 80–100 | Excellent | ~10% over 5yr lease | Approve with minimal security |
| **B** | 65–79 | Good | ~15% over 5yr lease | Approve with standard security |
| **C** | 50–64 | Moderate | ~25% over 5yr lease | Approve with conditions + elevated security |
| **D** | 35–49 | Weak | ~40% over 5yr lease | Conditional — strong security or guarantor |
| **F** | 0–34 | Poor | ~60% over 5yr lease | Decline or require full lease guarantee |

## Credit Scoring Components (100 points total)

| Component | Max | Key Factors |
|-----------|-----|-------------|
| Financial Strength | 40 | Current ratio, debt-to-equity, profitability, EBITDA-to-rent |
| Business Quality | 30 | Years in business, industry stability, financial trend |
| Credit History | 20 | Payment history, credit score |
| Lease-Specific | 10 | Rent % of revenue, use criticality |

## Industry Stability Classification

| Stable | Moderate | Volatile |
|--------|----------|---------|
| Medical/healthcare | Office services | Retail |
| Government contractors | Light manufacturing | Restaurants |
| Essential services | Technology (established) | Hospitality |
| Professional services | Distribution | Startups |

## Security Recommendation Logic

Security amount scales with credit rating and expected loss:
- **Rating A**: 2–3 months' rent (rent deposit)
- **Rating B**: 3–4 months' rent (rent deposit)
- **Rating C**: 4–6 months' rent (letter of credit preferred)
- **Rating D**: 6–9 months' rent (letter of credit required)
- **Rating F**: Full lease guarantee or decline

Step-down schedules apply: security reduces if no defaults over preceding 12 months.

---

## Step 0 — Resolve plugin paths (runs in primary context before subagent dispatch)

**Plugin root** — run in Bash:
```bash
echo "${CLAUDE_PLUGIN_ROOT}"
```
If empty, find it:
```bash
find ~ -path "*/tenant-credit/skills/tenant-credit/SKILL.md" -maxdepth 8 2>/dev/null | head -1 | sed 's|/skills/tenant-credit/SKILL.md||'
```
If still empty, use: `/home/reggiechan/021-CRE-150/plugins/tenant-credit`

**Workspace** — current working directory. Create required directories if absent:
```bash
mkdir -p "$(pwd)/Reports"
mkdir -p "$(pwd)/credit_inputs"
```

**Timestamp** — run `TZ=America/Toronto date +%Y-%m-%d_%H%M%S`.

From the resolved plugin root, construct absolute paths:
- `SCRIPTS_DIR` = `<plugin_root>/skills/tenant-credit/scripts`
- `CALCULATOR` = `<SCRIPTS_DIR>/credit_analysis.py`
- `RUNNER` = `<SCRIPTS_DIR>/run_credit_analysis.py`

Verify the calculator exists:
```bash
ls "<CALCULATOR>"
```
If missing, report the error and stop.

**Parse user arguments:**
- First argument: path to most recent financial statements PDF (required)
- Second argument (optional): path to prior year financials or lease document PDF
- Third argument (optional): additional financials PDF

Resolve each provided path to absolute form and verify it exists.

---

## Step 1 — Dispatch analysis subagent

Once all paths are resolved, dispatch a single subagent to handle all heavy work. **Do not perform any PDF reading, JSON generation, or script execution in the primary context.**

The subagent prompt must be fully self-contained — embed all resolved absolute paths as literal values. Do not reference shell variables like `${SCRIPTS_DIR}` inside the prompt.

--- BEGIN SUBAGENT PROMPT ---
You are a commercial real estate credit analyst. Your task is to:
1. Extract financial data from tenant financial statement PDFs
2. Generate a structured JSON input file for the credit analysis calculator
3. Run the calculator
4. Generate a comprehensive markdown credit report

## Resolved Paths (use these literal values — do not re-resolve)

- SCRIPTS_DIR: <SCRIPTS_DIR>
- RUNNER: <RUNNER>
- WORKSPACE: <WORKSPACE>
- TIMESTAMP: <TIMESTAMP>
- Financial statement PDF(s): <PDF_PATH_1> [<PDF_PATH_2>] [<PDF_PATH_3>]

## Step A — Extract Financial Data from PDFs

For each provided PDF, use the Read tool to load it and extract financial data from the balance sheet and income statement.

**Key data to extract:**

**Balance Sheet:**
- Current Assets ($)
- Total Assets ($)
- Inventory ($) — use 0 if not applicable
- Cash and Cash Equivalents ($)
- Current Liabilities ($)
- Total Liabilities ($)
- Shareholders' Equity ($)
- Fiscal year or date

**Income Statement:**
- Revenue / Sales ($)
- Gross Profit ($)
- EBIT (Earnings Before Interest & Tax) ($)
- EBITDA — if not stated, calculate: EBIT + Depreciation + Amortization
- Net Income ($)
- Interest Expense ($) — use 0 if not found

**Tenant and Lease Information:**
- Legal name
- Industry / sector
- Years in business (or calculate from incorporation date)
- Proposed annual rent (from lease document or user input)
- Lease term (years)

**Data quality rules:**
- Extract EXACT numbers — do NOT estimate or approximate
- Check that Assets = Liabilities + Equity (balance sheet must balance)
- Flag any missing or unclear data points
- If multiple years provided, extract all years (most recent first)

## Step B — Generate JSON Input File

Create the input JSON at: `<WORKSPACE>/credit_inputs/<tenant_name_slug>_<YYYY-MM-DD>_input.json`

Use this exact schema:

```json
{
  "tenant_name": "Legal Name",
  "industry": "Industry / sector",
  "years_in_business": 0,
  "credit_score": null,
  "payment_history": "good",
  "lease_term_years": 5,
  "use_criticality": "important",
  "industry_stability": "moderate",
  "current_security": 0,
  "security_type": "None",
  "financial_data": [
    {
      "year": 2024,
      "current_assets": 0.0,
      "total_assets": 0.0,
      "inventory": 0.0,
      "cash_and_equivalents": 0.0,
      "current_liabilities": 0.0,
      "total_liabilities": 0.0,
      "shareholders_equity": 0.0,
      "revenue": 0.0,
      "gross_profit": 0.0,
      "ebit": 0.0,
      "ebitda": 0.0,
      "net_income": 0.0,
      "interest_expense": 0.0,
      "annual_rent": 0.0
    }
  ]
}
```

**Field guidance:**
- `payment_history`: "excellent", "good", "fair", or "poor" — default "good"
- `use_criticality`: "mission-critical", "important", or "discretionary" — default "important"
- `industry_stability`: "stable", "moderate", or "volatile" — infer from industry:
  - Stable: medical, government, essential services, professional services (law, accounting)
  - Moderate: office services, light manufacturing, established tech, distribution
  - Volatile: retail, restaurants, hospitality, startups
- `credit_score`: only populate if available from a formal credit report (300–850 scale)
- Include one entry per year in `financial_data`, most recent first

## Step C — Verify JSON Before Running Calculator

Before running the calculator, verify the JSON is valid and complete:

1. Confirm the JSON file exists and is valid JSON
2. Check that `financial_data` has at least one entry
3. Verify all required numeric fields are numbers (not strings or null)
4. Confirm `annual_rent` is non-zero (calculator needs this for rent coverage ratios)
5. Check balance sheet balances: `total_assets` ≈ `total_liabilities` + `shareholders_equity` (within 5%)

If verification fails:
- Fix the specific issue in the JSON
- Re-verify once
- If still failing, report the specific problem clearly and stop

=== BEGIN VERIFIER CHECK ===
Run this quick sanity check:
```bash
python3 -c "
import json, sys
data = json.load(open('<WORKSPACE>/credit_inputs/<tenant_slug>_<YYYY-MM-DD>_input.json'))
fd = data['financial_data'][0]
asset_check = abs(fd['total_assets'] - (fd['total_liabilities'] + fd['shareholders_equity']))
balance_pct = asset_check / fd['total_assets'] * 100 if fd['total_assets'] > 0 else 0
print(f'Balance sheet variance: {balance_pct:.1f}%')
print(f'Annual rent: \${fd[\"annual_rent\"]:,.0f}')
print(f'Revenue: \${fd[\"revenue\"]:,.0f}')
print(f'Years of data: {len(data[\"financial_data\"])}')
print('VERIFY_OK')
"
```
=== END VERIFIER CHECK ===

## Step D — Run the Credit Analysis Calculator

```bash
cd "<SCRIPTS_DIR>" && python3 run_credit_analysis.py "<WORKSPACE>/credit_inputs/<tenant_slug>_<YYYY-MM-DD>_input.json"
```

Capture the full console output — it contains all the data for the report.

If the calculator fails:
- Check for Python import errors (numpy, pandas must be installed)
- Verify the JSON input has no type errors (numbers must be floats, not strings)
- Check for division-by-zero: if `shareholders_equity` or `revenue` is 0, set them to a small non-zero value and note the assumption

## Step E — Generate Comprehensive Credit Report

Create the markdown report at: `<WORKSPACE>/Reports/<TIMESTAMP>_<tenant_name_slug>_credit_analysis.md`

Use this structure (populate all sections from the calculator output):

```markdown
# Tenant Credit Analysis Report
## [Tenant Legal Name]

**Analysis Date:** [Current Date]
**Prepared Using:** Credit Analysis Calculator (credit_analysis.py)
**Analyst:** Claude Code — Credit Risk Assessment

---

## Executive Summary

**Credit Rating: [A/B/C/D/F]** ([Excellent/Good/Moderate/Weak/Poor])

**Credit Score: XX / 100**

**Recommendation: [APPROVE / APPROVE_WITH_CONDITIONS / DECLINE]**

**Key Findings:**
- Credit rating of [X] with score [XX]/100
- Overall trend: [IMPROVING/STABLE/DETERIORATING]
- [Key strength 1]
- [Key strength 2]
- [Key concern 1]

**Security Recommendation:**
- Type: [Rent Deposit / Letter of Credit]
- Amount: $XXX,XXX ([X.X] months' rent)

**Risk Metrics:**
- Probability of Default: XX.X%
- Exposure at Default: $XXX,XXX (total rent over X years)
- Expected Loss: $XXX,XXX
- Security Coverage: X.Xx

---

## Tenant Profile

**Corporate Information:**
- Legal Name: [Name]
- Industry: [Industry/Sector]
- Years in Business: [X years]

**Proposed Lease:**
- Annual Rent: $XXX,XXX
- Lease Term: X years
- Total Lease Value: $XXX,XXX

---

## Financial Analysis

### Balance Sheet (Most Recent Year: [Year])

| Item | Amount | % of Total Assets |
|------|--------|-------------------|
| Current Assets | $XXX,XXX | XX% |
| Total Assets | $X,XXX,XXX | 100% |
| Cash & Equivalents | $XXX,XXX | XX% |
| Current Liabilities | $XXX,XXX | XX% |
| Total Liabilities | $XXX,XXX | XX% |
| Shareholders' Equity | $XXX,XXX | XX% |

### Income Statement (Most Recent Year: [Year])

| Item | Amount | % of Revenue |
|------|--------|--------------|
| Revenue | $X,XXX,XXX | 100% |
| Gross Profit | $XXX,XXX | XX% |
| EBITDA | $XXX,XXX | XX% |
| Net Income | $XXX,XXX | XX% |

### Financial Ratios

**Liquidity:**

| Ratio | Value | Target | Assessment |
|-------|-------|--------|------------|
| Current Ratio | X.XX | > 1.5 | [Strong / Acceptable / Weak] |
| Quick Ratio | X.XX | > 1.0 | [Strong / Acceptable / Weak] |
| Cash Ratio | X.XX | > 0.5 | [Strong / Acceptable / Weak] |

**Leverage:**

| Ratio | Value | Target | Assessment |
|-------|-------|--------|------------|
| Debt-to-Equity | X.XX | < 1.0 | [Strong / Moderate / Weak] |
| Debt-to-Assets | X.XX | < 0.5 | [Strong / Moderate / Weak] |
| Interest Coverage | X.XXx | > 3.0x | [Strong / Acceptable / Weak] |

**Profitability:**

| Ratio | Value | Target | Assessment |
|-------|-------|--------|------------|
| Net Profit Margin | XX.X% | > 10% | [Strong / Moderate / Weak] |
| ROA | XX.X% | > 10% | [Strong / Moderate / Weak] |
| ROE | XX.X% | > 15% | [Strong / Moderate / Weak] |

**Rent Coverage:**

| Ratio | Value | Target | Assessment |
|-------|-------|--------|------------|
| Rent-to-Revenue | X.X% | < 5% | [Low / Moderate / High Risk] |
| EBITDA-to-Rent | X.XXx | > 2.0x | [Strong / Acceptable / Weak] |

---

## Credit Score Breakdown

**Total Score: XX / 100** → **Credit Rating: [X]**

| Component | Max | Awarded | Details |
|-----------|-----|---------|---------|
| Financial Strength | 40 | XX | |
| — Current Ratio | 10 | X | [Value: X.XX] |
| — Debt-to-Equity | 10 | X | [Value: X.XX] |
| — Profitability | 10 | X | [Net Margin: XX%] |
| — EBITDA-to-Rent | 10 | X | [Coverage: X.XXx] |
| Business Quality | 30 | XX | |
| — Years in Business | 10 | X | [X years] |
| — Industry Stability | 10 | X | [Stable/Moderate/Volatile] |
| — Financial Trend | 10 | X | [Improving/Stable/Deteriorating] |
| Credit History | 20 | XX | |
| — Payment History | 10 | X | [Excellent/Good/Fair/Poor] |
| — Credit Score | 10 | X | [Score: XXX or N/A] |
| Lease-Specific | 10 | XX | |
| — Rent % of Revenue | 5 | X | [X.X%] |
| — Use Criticality | 5 | X | [Mission-critical/Important/Discretionary] |

---

## Trend Analysis

**Overall Trend: [IMPROVING / STABLE / DETERIORATING]**

| Metric | Direction | Notes |
|--------|-----------|-------|
| Revenue | [↑ / → / ↓] | [YoY details] |
| Profitability | [↑ / → / ↓] | [YoY details] |
| Liquidity | [↑ / → / ↓] | [YoY details] |
| Leverage | [↑ / → / ↓] | [YoY details] |

---

## Risk Assessment

**Expected Loss Calculation:**

| Component | Value | Explanation |
|-----------|-------|-------------|
| Probability of Default (PD) | XX.X% | Based on credit rating [X] |
| Exposure at Default (EAD) | $XXX,XXX | Total rent over X-year lease |
| Loss Given Default (LGD) | XX% | (1 — Recovery Rate) |
| **Expected Loss** | **$XXX,XXX** | PD × EAD × LGD |

---

## Red Flags

[List all red flags from result.red_flags — or "None identified" if clean]

**Total Red Flags: X** | **Severity: [Low / Moderate / High / Critical]**

---

## Security Recommendations

**Type:** [From result.risk_assessment.security_type_recommendation]

**Amount:** $XXX,XXX ([X.X] months' rent)

**Step-Down Schedule:**

| Year | Security Required | Months Rent |
|------|-------------------|-------------|
| 0 (Initial) | $XXX,XXX | X.X months |
| [Year X] | $XXX,XXX | X.X months |

**Conditions for Step-Down:**
- No payment defaults in preceding 12 months
- All financial covenants met
- Timely financial reporting

---

## Approval Recommendation

### [APPROVE / APPROVE_WITH_CONDITIONS / DECLINE]

[Insert result.recommendation_notes]

**Conditions (if APPROVE_WITH_CONDITIONS):**
1. Security: [Type and amount]
2. Financial Reporting: Quarterly unaudited, annual audited
3. Financial Covenants (if rating C or below):
   - Maintain current ratio ≥ [X.X]
   - Maintain debt-to-equity ≤ [X.X]
   - Maintain EBITDA-to-rent ≥ [X.X]x

---

## Appendices

### A. Data Sources

- Financial Statements: [List PDFs analyzed]
- Fiscal Year: [Year] | Type: [Audited / Unaudited / Internal]

### B. Assumptions and Limitations

- Financial statements assumed accurate and complete
- Payment history: assumed "Good" in absence of credit report data
- Industry stability: [classification and basis]
- Analysis based on historical data — future performance may differ

### C. Supporting Files

- Input JSON: `credit_inputs/<tenant_slug>_<date>_input.json`
- Results JSON: `credit_inputs/<tenant_slug>_<date>_results.json`
- Report: `Reports/<TIMESTAMP>_<tenant_slug>_credit_analysis.md`
- Source Documents: [List PDF paths]

---

**Report Generated:** <TIMESTAMP> (Eastern Time)
**Analyst:** Claude Code — Credit Analysis Calculator
**Valid for:** 90 days from analysis date
```

## Step F — Return Structured Result

After all files are created, return this exact block:

```
CREDIT_ANALYSIS_RESULT
tenant: <tenant_name>
rating: <A/B/C/D/F>
score: <XX>/100
recommendation: <APPROVE / APPROVE_WITH_CONDITIONS / DECLINE>
security_amount: $<XXX,XXX>
security_type: <Rent Deposit / Letter of Credit>
security_months: <X.X> months
probability_of_default: <XX.X>%
expected_loss: $<XXX,XXX>
red_flags: <count>
overall_trend: <IMPROVING / STABLE / DETERIORATING>
years_of_data: <N>
input_json: <full path>
results_json: <full path>
report: <full path>
```

--- END SUBAGENT PROMPT ---

---

## Step 2 — Relay results to user

Once the subagent returns, extract the `CREDIT_ANALYSIS_RESULT` block and present it to the user as a clean summary:

**Credit Assessment: [Tenant Name]**

| Field | Value |
|-------|-------|
| Credit Rating | [A/B/C/D/F] — [Excellent/Good/Moderate/Weak/Poor] |
| Credit Score | XX / 100 |
| Recommendation | APPROVE / APPROVE_WITH_CONDITIONS / DECLINE |
| Recommended Security | $XXX,XXX ([X.X] months — [Type]) |
| Default Probability | XX.X% |
| Expected Loss | $XXX,XXX |
| Red Flags | X |
| Trend | IMPROVING / STABLE / DETERIORATING |

**Output Files:**
- Report: `Reports/<TIMESTAMP>_<tenant>_credit_analysis.md`
- Results JSON: `credit_inputs/<tenant>_<date>_results.json`

**Next steps:**
- Review the detailed report in `Reports/`
- Verify extracted financials against source PDFs
- Prepare lease with recommended security package

---

## Fallback — If subagent dispatch unavailable

If the Agent tool is not available, execute Steps A–F directly in the primary context, following the same sequence. Note that this may encounter context limitations on large PDFs — process one year at a time if needed.

---

## Example Usage

```
/tenant-credit /path/to/2024_financials.pdf
/tenant-credit /path/to/2024_financials.pdf /path/to/2023_financials.pdf
/tenant-credit /path/to/2024_financials.pdf /path/to/lease_proposal.pdf
```
