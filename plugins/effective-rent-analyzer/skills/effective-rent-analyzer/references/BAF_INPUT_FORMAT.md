# BAF Calculator — JSON Input Format Guide

Sourced from the `vp-real-estate` repository (`Eff_Rent_Calculator/BAF_INPUT_FORMAT.md`).
See that document for the canonical reference. This copy is included for offline use.

## Quick Start

```bash
cd plugins/effective-rent-analyzer/skills/effective-rent-analyzer/scripts
python3 eff_rent_calculator.py baf_input_example.json
python3 eff_rent_calculator.py your_deal.json -o results.json
```

## Input File Structure

### Required Fields

| Section | Field | Type | Description |
|---------|-------|------|-------------|
| `property_info` | `area_sf` | number | Rentable area in square feet |
| `lease_terms` | `lease_term_months` | integer | Total lease term in months |
| `lease_terms` | `operating_costs_psf` | number | Annual operating costs $/sf |
| `rent_schedule` | `rent_psf_by_year` | array | Annual net rent $/sf per year (up to 10) |
| `financial_assumptions` | `nominal_discount_rate` | number | Discount rate as decimal (0.10 = 10%) |

### Commission Methods

Use **ONE method only**. Mixing causes incorrect results.

**Industrial (% of net rent):**
```json
"leasing_costs": {
  "listing_agent_year1_pct": 0.05,
  "listing_agent_subsequent_pct": 0.025,
  "tenant_rep_year1_pct": 0.05,
  "tenant_rep_subsequent_pct": 0.025
}
```

**Office (flat $/sf):**
```json
"leasing_costs": {
  "listing_agent_commission_psf": 2.0,
  "tenant_rep_commission_psf": 2.0
}
```

### Free Rent Types

- `net_free_rent_months` — tenant pays $0 base rent, still pays operating costs
- `gross_free_rent_months` — tenant pays nothing (base rent + operating costs waived)

### Investment Parameters

Required for breakeven analysis. If acquisition_cost = 0, breakeven thresholds will be zero.

| Field | Description | Typical |
|-------|-------------|---------|
| `acquisition_cost` | Property purchase price ($) | Actual |
| `going_in_ltv` | Loan-to-value ratio | 0.50–0.65 |
| `mortgage_amortization_months` | Amortization period | 300 (25 yr) |
| `dividend_yield` | Required equity yield | 0.0650–0.0750 |
| `interest_cost` | Mortgage interest rate | 0.035–0.050 |
| `principal_payment_rate` | Annual principal rate | 0.025–0.033 |

## Output

The calculator produces console output and a `_results.json` file with:
- `npv_analysis` — NPV of net rent, costs, and net deal
- `effective_rent` — NER and GER (lease term only and with fixturing)
- `metrics` — effective term, incentives %, breakeven months
- `breakeven_analysis` — 5 breakeven thresholds
- `investment_assessment` — pass/fail against each threshold
- `cost_breakdown` — itemized costs in dollars
