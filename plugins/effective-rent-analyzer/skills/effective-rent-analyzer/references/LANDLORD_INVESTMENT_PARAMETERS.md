# Landlord Investment Parameters Database

Sourced from the `vp-real-estate` repository (`Eff_Rent_Calculator/LANDLORD_INVESTMENT_PARAMETERS.md`).
This copy is included for offline reference.

## Purpose

The `landlord_investment_parameters.json` database provides centralized investment assumptions
for different landlord entities, enabling automatic breakeven calculation based on the landlord
identified in the lease document.

## Matching Priority (Highest First)

1. **Property-specific**: landlord name + property address both match → use `property_specific_parameters`
2. **Landlord default**: landlord name matches → use `investment_parameters`
3. **Alias match**: check `landlord_aliases` → use `investment_parameters`
4. **System defaults**: no match → use conservative REIT defaults (55% LTV, 6.75% yield, 10% discount)

## Parameter Definitions

| Parameter | Description | Typical Range |
|-----------|-------------|---------------|
| `default_acquisition_cost_psf` | Default $/sf if property-specific cost unknown | $100–$500/sf |
| `going_in_ltv` | Loan-to-value at acquisition | 40–70% |
| `mortgage_amortization_months` | Amortization period | 240–360 months |
| `dividend_yield` | Required equity return | 6–10% |
| `interest_cost` | Mortgage interest rate | 3–6% |
| `principal_payment_rate` | Annual principal payment rate | Calculated |
| `building_allocation_pct` | Building % of property value (for sinking fund) | 35–45% |
| `default_remaining_depreciation_years` | Remaining building life | 15–30 years |
| `nominal_discount_rate` | NPV discount rate | 8–12% |

## Landlord Types

| Type | LTV | Dividend Yield | Discount Rate |
|------|-----|----------------|---------------|
| REIT | 50–60% | 6.5–7.5% | 9–11% |
| Institutional | 40–50% | 6–7% | 8–10% |
| Private Equity | 60–70% | 8–10% | 10–12% |
| Private Owner | 55–70% | 7–9% | 10–12% |

## Adding a New Landlord

```json
{
  "landlord_legal_name": "Exact Legal Name From Lease Inc.",
  "landlord_aliases": ["Short Name", "DBA Name"],
  "landlord_type": "REIT",
  "primary_asset_class": "Industrial",
  "active": true,
  "notes": "Source and date of parameters",
  "investment_parameters": {
    "default_acquisition_cost_psf": 150.0,
    "going_in_ltv": 0.55,
    "mortgage_amortization_months": 300,
    "dividend_yield": 0.0675,
    "interest_cost": 0.04,
    "principal_payment_rate": 0.026713,
    "building_allocation_pct": 0.40,
    "default_remaining_depreciation_years": 20,
    "nominal_discount_rate": 0.10,
    "notes": "Updated YYYY-QN based on [source]"
  },
  "properties": []
}
```

**Key naming rule**: Use the exact legal name as it appears in the PARTIES section of lease
documents. Add common variations to `landlord_aliases` for fuzzy matching.

## Validating the Database

```bash
cd plugins/effective-rent-analyzer/skills/effective-rent-analyzer/scripts
python3 -c "import json; json.load(open('landlord_investment_parameters.json')); print('OK')"
```
