# tenant-credit — v1.0.0

Tenant credit analysis for commercial real estate lease approvals. Extracts financial data from
PDF financial statements, runs 15+ ratio analysis with a 100-point weighted credit scoring
algorithm (A–F rating), estimates default probability and expected loss, and generates a
comprehensive credit report with security deposit recommendations.

## Trigger phrases

- `tenant credit analysis`
- `run credit analysis`
- `analyze tenant financials`
- `creditworthiness assessment`
- `security deposit recommendation`
- `default risk`
- `lease approval`
- `/tenant-credit`

## Usage

```
/tenant-credit /path/to/2024_financials.pdf
/tenant-credit /path/to/2024_financials.pdf /path/to/2023_financials.pdf
/tenant-credit /path/to/2024_financials.pdf /path/to/lease_proposal.pdf
```

- **First argument** (required): most recent financial statements PDF
- **Second argument** (optional): prior year financials or lease document PDF
- **Third argument** (optional): additional year of financials

## What it does

1. **PDF extraction** — reads balance sheet and income statement line items from provided PDFs
2. **JSON generation** — creates structured input file in `credit_inputs/`
3. **JSON verification** — validates balance sheet integrity and required fields before running
4. **Calculator execution** — runs `credit_analysis.py` (15+ ratios, 100-point scoring, trend analysis)
5. **Report generation** — creates a timestamped markdown report in `Reports/`
6. **Summary output** — credit rating, score, recommendation, security amount, expected loss

## Credit scoring breakdown

| Component | Max Points | Factors |
|-----------|------------|---------|
| Financial Strength | 40 | Current ratio, D/E ratio, profitability, EBITDA-to-rent |
| Business Quality | 30 | Years in business, industry stability, financial trend |
| Credit History | 20 | Payment history, credit score (if available) |
| Lease-Specific | 10 | Rent % of revenue, use criticality |

## Output files

All files written to current working directory:

| File | Description |
|------|-------------|
| `credit_inputs/<tenant>_<date>_input.json` | Structured financial input |
| `credit_inputs/<tenant>_<date>_results.json` | Calculator output (all ratios + scores) |
| `Reports/<timestamp>_<tenant>_credit_analysis.md` | Full credit report |

## Dependencies

- Python 3.x
- `numpy`
- `pandas`

## Source

Ported from `vp-real-estate/Credit_Analysis` (2025-10-30).
Calculator authored by Claude Code for GitHub Issue #6.
