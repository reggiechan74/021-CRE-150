# mcda-lease-comparison

MCDA competitive positioning analysis for commercial real estate — ranks a subject property against market comparables on up to 25 weighted variables and provides strategic pricing recommendations to achieve Top 3 market positioning.

## What it does

1. **Extracts** property data from PDF reports (CoStar, broker packages, market surveys)
2. **Builds** a structured JSON input with all 25 variables per property
3. **Calculates** driving distances via Distancematrix.ai API (optional)
4. **Ranks** properties using MCDA ordinal ranking with dynamic weight redistribution
5. **Generates** a strategic report with sensitivity analysis and recommendations
6. **Exports** to Markdown + landscape PDF

## Skill

`/mcda-lease-comparison <pdf-or-json-path> [--full] [--stats] [--persona <name>]`

## Variables

**9 Core (always included):** Net Asking Rent (11%), Parking Ratio (9%), TMI (9%), Clear Height (7%), Area Difference (7%), Distance (7%), % Office Space (6%), Class (5%), Building Age (4%)

**16 Optional (included when ≥50% of properties have data):** Bay Depth, Shipping Doors TL/DI, Lot Size, HVAC Coverage, Sprinkler Type, Power, Trailer Parking, Rail Access, Crane, Occupancy Status, Grade Level Doors, Days on Market, Zoning, Secure Shipping, Excess Land

## Tenant Personas

| Persona | Flag | Emphasis |
|---------|------|----------|
| Default/Balanced | `--persona default` | General industrial |
| 3PL/Distribution | `--persona 3pl` | Bay depth, clear height, shipping doors |
| Manufacturing | `--persona manufacturing` | Power, crane, rail access |
| Office/Flex | `--persona office` | Office space, class, parking, HVAC |

## Output Files

All timestamped in Eastern Time (`YYYY-MM-DD_HHMMSS`):
- `Reports/TIMESTAMP_mcda_lease_comparison_input.json`
- `Reports/TIMESTAMP_mcda_lease_comparison_output.json`
- `Reports/TIMESTAMP_mcda_lease_comparison_report.md`
- `Reports/TIMESTAMP_mcda_lease_comparison_report.pdf`

## Scripts

| File | Purpose |
|------|---------|
| `relative_valuation_calculator.py` | Main MCDA ranking engine |
| `statistics_module.py` | Regression, correlation, outlier analysis |
| `calculate_distances.py` | Driving distance via Distancematrix.ai |
| `weights_loader.py` | Tenant persona weight profiles |
| `weights_config.json` | Default + 3PL + manufacturing + office weights |

## Environment Variables

- `DISTANCEMATRIX_API_KEY` — Required for automatic distance calculation (free tier: 1,000 elements/month at distancematrix.ai)

## References

- `references/RANKING_METHODOLOGY.md` — Dynamic weighting, tie-breaking, scoring algorithm
- `references/SCHEMA.md` — Complete field documentation
- `references/WEIGHTS_CONFIG_GUIDE.md` — How to create custom weight profiles
- `inputs/schema_template.json` — JSON Schema (Draft 2020-12) for input validation
