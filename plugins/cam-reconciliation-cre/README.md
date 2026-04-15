# cam-reconciliation-cre

CAM reconciliation for commercial real estate training workflows. The plugin combines lease-aware recoverability rules with deterministic Python math so the same inputs always produce the same tenant charges, landlord absorption totals, and comparison output.

## Scope

- Landlord-side CAM true-up for a single property
- Lease-aware corrections for duplicate invoices, turnover charges, management fee basis errors, modified-gross exclusions, restaurant carve-outs, base years, and CAM caps
- Output artifacts: typed manifests, tenant PDFs, workpaper workbook, audit log, category commentary, and Anthropic comparison report

## Commands

- `/cam-reconcile <property-dir>`
- `/cam-explain <allocated-manifest.json> <tenant-id-or-line-id>`
- `/cam-compare-vs-anthropic <allocated-manifest.json> <anthropic-output.txt>`

## Fixture Demo

The bundled Matheson fixture demonstrates the workshop payoff:

- Anthropic draft recoverable opex: `$1,178,692`
- Corrected recoverable opex: `$1,150,292`
- Tenant overbilling avoided: `$28,400`

## Inputs

Expected files in `<property-dir>`:

- `property.yaml`
- `leases.json`
- `gl.csv`
- `budget.md` or `budget.json`
- `anthropic_output.txt` optional, only for comparison

## Outputs

Running `/cam-reconcile` or the underlying scripts writes to `<property-dir>/reconciliation-output/`:

- `manifests/raw_manifest.json`
- `manifests/classification_decisions.json`
- `manifests/classified_manifest.json`
- `manifests/allocated_manifest.json`
- `tenant_statements/*.pdf`
- `workpaper.xlsx`
- `audit_log.md`
- `narrative_commentary.md`
- `compare_report.md` when comparison is run

## Python Scripts

- `scripts/ingest.py`
- `scripts/classify_validator.py`
- `scripts/allocate.py`
- `scripts/statement.py`
- `scripts/compare.py`
- `scripts/bootstrap.py`

## Setup

```bash
python3 plugins/cam-reconciliation-cre/scripts/bootstrap.py
```

## Manual Run

```bash
python3 plugins/cam-reconciliation-cre/scripts/ingest.py \
  --property-dir plugins/cam-reconciliation-cre/fixtures/matheson \
  --run-timestamp 2026-04-15T10:50:00

python3 plugins/cam-reconciliation-cre/scripts/classify_validator.py \
  --manifest plugins/cam-reconciliation-cre/fixtures/matheson/reconciliation-output/manifests/raw_manifest.json

python3 plugins/cam-reconciliation-cre/scripts/allocate.py \
  --manifest plugins/cam-reconciliation-cre/fixtures/matheson/reconciliation-output/manifests/classified_manifest.json

python3 plugins/cam-reconciliation-cre/scripts/statement.py \
  --manifest plugins/cam-reconciliation-cre/fixtures/matheson/reconciliation-output/manifests/allocated_manifest.json

python3 plugins/cam-reconciliation-cre/scripts/compare.py \
  --manifest plugins/cam-reconciliation-cre/fixtures/matheson/reconciliation-output/manifests/allocated_manifest.json \
  --anthropic plugins/cam-reconciliation-cre/fixtures/matheson/anthropic_output.txt
```

## Tests

```bash
python3 -m pytest plugins/cam-reconciliation-cre/tests -q
```
