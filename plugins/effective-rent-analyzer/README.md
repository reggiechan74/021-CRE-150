# effective-rent-analyzer — v1.0.0

Lease deal investment analysis using the **Ponzi Rental Rate (PRR) framework**.

Extracts lease terms from documents, matches landlord investment parameters, calculates NER/GER/NPV, determines breakeven thresholds, and generates an investment recommendation report.

**Academic reference**: Chan, R. (2015). "Understanding the Ponzi Rental Rate." *Real Estate Finance*, Vol. 32, No. 2, pp. 48–61.

---

## Trigger

```
Analyze this lease deal    /path/to/lease.pdf  /path/to/landlord_investment_parameters.json
Calculate effective rent   /path/to/offer.pdf  /path/to/landlord_params.json
Run NER analysis           /path/to/lease.pdf  /path/to/landlord_params.json  /path/to/ti-quote.pdf
```

Or invoke directly: `/effective-rent <lease-path> <landlord-params-json>`

---

## What It Produces

1. **Input JSON** — extracted lease terms + matched landlord parameters (`inputs/`)
2. **Results JSON** — all computed metrics (`inputs/*_results.json`)
3. **Markdown report** — full investment analysis with recommendation (`Reports/`)

### Key Metrics

| Metric | Description |
|--------|-------------|
| **NER** | Net Effective Rent — constant annuity equivalent of all cash flows net of concessions |
| **GER** | Gross Effective Rent — tenant's total occupancy cost (NER + operating costs) |
| **NPV** | Present value of lease deal after all landlord costs |
| **Fully Levered Breakeven** | Minimum NER to cover dividends + interest + principal |
| **NER Spread** | NER minus breakeven — positive = deal creates value |

### Breakeven Thresholds

Four levels from the PRR framework:

1. Unlevered (dividends only)
2. I/O Levered (dividends + interest)
3. **Fully Levered** (dividends + interest + principal) ← primary decision threshold
4. Fully Levered + Capital Recovery (includes Inwood sinking fund)

---

## Landlord Parameter Matching

The skill automatically matches the landlord named in the lease against `landlord_investment_parameters.json` to determine the correct breakeven thresholds.

**Matching priority**: Property-specific → Landlord default → Alias → System defaults

Add your landlord entities to `scripts/landlord_investment_parameters.json` following the schema in `scripts/landlord_investment_parameters_schema.json`.

---

## Scripts

| File | Purpose |
|------|---------|
| `eff_rent_calculator.py` | Core BAF/NER/GER/breakeven calculator |
| `baf_input_example.json` | Example 10-year industrial lease input |
| `landlord_investment_parameters.json` | Landlord database (add your entities here) |
| `landlord_investment_parameters_schema.json` | JSON schema for database validation |

### Dependencies

```bash
pip install numpy numpy_financial
```

### Direct CLI Usage

```bash
cd plugins/effective-rent-analyzer/skills/effective-rent-analyzer/scripts
python3 eff_rent_calculator.py baf_input_example.json
python3 eff_rent_calculator.py your_deal.json -o your_deal_results.json
```

---

## Commission Methods

**Industrial** (percentage of net rent):
- Year 1: 5–6% each side
- Years 2+: 2–3% each side

**Office** (flat $/sf):
- $1.50–$3.00/sf/year each side

Use one method per deal — not both.

---

## References

- `references/BAF_INPUT_FORMAT.md` — complete JSON input field reference
- `references/LANDLORD_INVESTMENT_PARAMETERS.md` — database structure and maintenance guide
