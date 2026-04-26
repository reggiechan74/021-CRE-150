# CAM Reconciliation Pipeline

A 5-stage deterministic CAM (Common Area Maintenance) reconciliation engine for commercial real estate. Takes a property directory containing lease terms, a general ledger, and budget data, then produces audit-ready tenant charge statements with a full citation trail back to specific lease clauses. All scripts are stdlib Python (plus `openpyxl` for Excel output).

---

## Stage 1 — `ingest.py` (Parse & Normalize)

**Input:** Four files from `<property-dir>/`:

| File | Contents |
|------|----------|
| `property.json` | Property metadata (name, address, RSF by pool, GPI/EGI) |
| `leases.json` | Tenant lease terms with cap configs, base-year configs, exclusions |
| `gl.csv` | General ledger (date, account, category, vendor, invoice ref, memo, amount, pool hint) |
| `budget.md` or `budget.json` | FY budget by category |

**Output:** `reconciliation-output/manifests/raw_manifest.json`

Reads all input files, normalizes category names against a canonical map, creates typed dataclass objects (`Property`, `Lease`, `GLLine`), computes a SHA-256 provenance hash of all inputs, and serializes the complete manifest. This is pure parsing — no business logic decisions yet.

---

## Stage 2 — `classify_validator.py` (Recoverability Decisions)

**Input:** `raw_manifest.json` (and optionally a pre-made `classification_decisions.json`)

**Output:** `classified_manifest.json` + `classification_decisions.json`

For each GL line, decides whether the expense is recoverable from tenants or absorbed by the landlord. Applies a priority-ordered rule engine:

1. **Duplicate detection** — Finds (vendor, invoice_ref, amount) duplicates; marks the later posting as non-recoverable citing §6.03(g).
2. **Turnover charges** — Memos containing "move-out" or "turnover" are flagged as extraordinary tenant charges, non-recoverable per §6.03(c).
3. **Management fee EGI adjustment** — Recalculates the management fee as 4% x EGI (not the raw GL posting), clipping the excess as non-recoverable per §4.1.
4. **Everything else** — Classified as standard recoverable operating expense.

Each classification includes a `LeaseCitation` (document, section, quote), a confidence level, and a human-review flag.

---

## Stage 3 — `allocate.py` (Tenant Charge Distribution)

**Input:** `classified_manifest.json`

**Output:** `allocated_manifest.json`

The core engine. For every recoverable GL line, distributes the cost to tenants according to five different lease structures:

1. **Pool splitting** — Shared expenses are split between office and retail pools by RSF weight.
2. **Direct-bill rules** — Specific items (e.g., grease trap to Pronto restaurant) are charged directly to one tenant, bypassing pool distribution.
3. **Exclusion handling** — Modified-gross tenants exclude certain categories (utilities, repairs); those amounts get reallocated to remaining eligible tenants, or absorbed by the landlord if nobody qualifies.
4. **Base-year adjustment** — Tenants with base-year leases only pay the increase above their baseline (`base_year_cam_psf x RSF`).
5. **CAM cap adjustment** — Controllable expenses are capped at `base_year_psf x (1 + annual_rate)^years`; uncontrollable categories (realty tax, insurance, utilities, snow) pass through uncapped.

Produces a `TenantCharge` per tenant with a complete math trace: gross share, exclusions, direct bills, base-year adjustment, cap adjustment, final charge, prebilled amount, and true-up.

A balance verification ensures: `sum(tenant charges) + direct_billed + landlord_absorbed = recoverable_total`.

---

## Stage 4 — `statement.py` (Render Artifacts)

**Input:** `allocated_manifest.json`

**Output:** Four artifacts in `reconciliation-output/`:

| Artifact | Description |
|----------|-------------|
| `workpaper.xlsx` | Three sheets: Tenant Charges summary, Category-level budget-vs-actual, GL Classification detail |
| `audit_log.md` | Corrections applied (duplicates, turnover, mgmt fee), landlord absorption total, provenance |
| `narrative_commentary.md` | Budget-vs-corrected-recoverable variance table with English-language commentary |
| `tenant_statements/*.md` | Per-tenant markdown files with charge breakdown, exclusion tables, direct-bill items, cap/base-year details, and citation trails |

---

## Stage 5 — `compare.py` (Optional Benchmark)

**Input:** `allocated_manifest.json` + `anthropic_output.txt` (if it exists in the property directory)

**Output:** `compare_report.md`

Parses the Anthropic finance workflow's reported recoverable total via regex, compares it against this plugin's corrected total, and produces a side-by-side report showing the delta and what drove it.

This stage runs only when `<property-dir>/anthropic_output.txt` is present.

---

## Data Flow

```
property.json  ─┐
leases.json    ─┤─> ingest.py ─> raw_manifest.json
gl.csv         ─┤                      |
budget.json    ─┘                      v
                    classify_validator.py ─> classified_manifest.json
                                                   |
                                                   v
                               allocate.py ─> allocated_manifest.json
                                                   |
                              ┌────────────────────┤
                              v                    v
                        statement.py          compare.py (optional)
                              |                    |
                    ┌─────────┼─────────┐          v
                    v         v         v    compare_report.md
              workpaper  audit_log  narrative
               .xlsx      .md     commentary.md
```

Each manifest is a complete snapshot — later stages add fields (classifications, tenant charges) without removing earlier data, so any manifest can be inspected independently for debugging or audit.

---

## Key Domain Concepts

| Concept | Description |
|---------|-------------|
| **Pool** | Physical space grouping (OFFICE, RETAIL, SHARED) used to weight cost allocation by RSF |
| **RSF** | Rentable square footage — the basis for pro-rata tenant shares within a pool |
| **Classification** | Per-GL-line decision on recoverability, with reason code, lease citation, and confidence |
| **LeaseCitation** | Pointer to a specific lease clause (document, section, quoted text) that authorizes a charge |
| **TenantCharge** | Complete per-tenant charge record with full audit trail from GL lines through adjustments |
| **CAM Cap** | Contractual ceiling on controllable expense growth, expressed as compound annual rate over a base year |
| **Base Year** | Fixed PSF baseline; tenant only pays increases above this amount |
| **Modified Gross** | Lease type where certain categories (typically utilities and repairs) are excluded from tenant recovery |
| **Direct Bill** | Expense charged to a single tenant by rule rather than distributed across the pool |
| **Provenance** | SHA-256 hash of all input files, plugin version, and timestamp for audit traceability |

## Lease Types Supported

| Type | Behavior |
|------|----------|
| `NET` | Standard pro-rata share of all recoverable expenses |
| `NET_WITH_CAP` | Net with compound annual cap on controllable categories |
| `BASE_YEAR` | Only pays increase above fixed PSF baseline |
| `MODIFIED_GROSS` | Net minus excluded categories (reallocated to other tenants or absorbed) |
| `NET_WITH_EXCLUSIONS` | Net with specific per-item exclusion rules and direct-bill treatments |
