# MCDA Sales Comparison Plugin

![Version](https://img.shields.io/badge/version-1.0.0-blue?style=flat-square)
![Platform](https://img.shields.io/badge/platform-Claude_Cowork-5436DA?style=flat-square)
![Workshop](https://img.shields.io/badge/021_Events-CRE--150-0066cc?style=flat-square)
![Method](https://img.shields.io/badge/method-MCDA_Ordinal_Ranking-lightgrey?style=flat-square)
![Output](https://img.shields.io/badge/output-Markdown_%2B_JSON-brightgreen?style=flat-square)

Multi-Criteria Decision Analysis for commercial real estate fee simple valuation. Ranks subject and comparables on weighted characteristics, maps composite scores to value via interpolation and regression. More robust than traditional DCA for heterogeneous comparable sets.

---

## Components

### Skill: `mcda-sales-comparison`

Activates when you ask to run an MCDA sales comparison, value a property using ordinal ranking, or produce an MCDA valuation report from a comparable sales JSON file.

**Usage:**
- "Run MCDA sales comparison on inputs/hamilton_industrial.json"
- "Value 2550 Industrial Parkway using MCDA comps"
- "/mcda-sales-comparison inputs/data.json --profile industrial_logistics"

**Outputs** (saved to `Reports/` in your workspace folder):
- `YYYY-MM-DD_HHMMSS_mcda_sales_comparison.md` — presentation-ready valuation report
- `YYYY-MM-DD_HHMMSS_mcda_sales_comparison.json` — full structured results with all scores and regression data

### Bundled Scripts

| File | Purpose |
|------|---------|
| `skills/mcda-sales-comparison/scripts/mcda_sales_calculator.py` | Main MCDA engine — ranking, composite scores, score-to-price mapping |
| `skills/mcda-sales-comparison/scripts/score_to_price.py` | Interpolation, OLS/monotonic/Theil-Sen regression, LOO cross-validation |
| `skills/mcda-sales-comparison/scripts/validation.py` | Input validation, transaction checks, time adjustment, monotonicity checks |
| `skills/mcda-sales-comparison/scripts/weight_profiles.py` | Weight profiles by property type and use (industrial, office, retail) |

### Sample Input

| File | Purpose |
|------|---------|
| `skills/mcda-sales-comparison/inputs/sample_input.json` | Hamilton industrial example — 5 comparables, demonstrates full schema |

---

## Weight Profiles

| Profile | Key Weights | Best For |
|---------|-------------|----------|
| `industrial_default` | Location 20%, Clear Height 15%, Condition 15%, Age 15% | General industrial |
| `industrial_logistics` | Clear Height 20%, Docks 15%, Highway 12% | Distribution centres |
| `industrial_manufacturing` | Clear Height 18%, Power 8%, Crane 5% | Manufacturing |
| `office_default` | Location 25%, Class 18%, Condition 15% | Office buildings |
| `retail_default` | Location 30%, Traffic 15%, Frontage 12% | Retail |

Profile auto-detected from `property_type` in the input JSON if not specified.

---

## Input Schema

Minimum required JSON structure:

```json
{
  "valuation_date": "YYYY-MM-DD",
  "property_type": "industrial",
  "subject_property": {
    "address": "...",
    "building_sf": 50000
  },
  "comparable_sales": [
    {
      "id": "COMP_1",
      "address": "...",
      "sale_price": 4650000,
      "sale_date": "YYYY-MM-DD",
      "building_sf": 48500,
      "property_rights": "fee_simple",
      "financing": {"type": "cash"},
      "conditions_of_sale": {"arms_length": true}
    }
  ]
}
```

Minimum 3 arm's-length comparable sales required. Non-arm's-length sales are automatically excluded.

---

## Setup

Pure Python stdlib — no pip installs required. Requires Python 3.8+.

Optional: `pip install jsonschema` enables strict JSON schema validation (gracefully skipped if absent).
