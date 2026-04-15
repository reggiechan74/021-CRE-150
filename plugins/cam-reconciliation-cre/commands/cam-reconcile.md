---
description: Run the full CAM reconciliation pipeline for a property directory
argument-hint: "<property-dir>"
---

# /cam-reconcile

Resolve the plugin root from `CLAUDE_PLUGIN_ROOT` or use:

`/home/reggiechan/021-CRE-150/plugins/cam-reconciliation-cre`

Then run:

```bash
python3 "$CLAUDE_PLUGIN_ROOT/scripts/bootstrap.py"
python3 "$CLAUDE_PLUGIN_ROOT/scripts/ingest.py" --property-dir "<property-dir>"
python3 "$CLAUDE_PLUGIN_ROOT/scripts/classify_validator.py" \
  --manifest "<property-dir>/reconciliation-output/manifests/raw_manifest.json"
python3 "$CLAUDE_PLUGIN_ROOT/scripts/allocate.py" \
  --manifest "<property-dir>/reconciliation-output/manifests/classified_manifest.json"
python3 "$CLAUDE_PLUGIN_ROOT/scripts/statement.py" \
  --manifest "<property-dir>/reconciliation-output/manifests/allocated_manifest.json"
```

If `<property-dir>/anthropic_output.txt` exists, also run:

```bash
python3 "$CLAUDE_PLUGIN_ROOT/scripts/compare.py" \
  --manifest "<property-dir>/reconciliation-output/manifests/allocated_manifest.json" \
  --anthropic "<property-dir>/anthropic_output.txt"
```

After the scripts complete, summarize:

- recoverable opex after corrections
- landlord absorbed total
- tenant statement count
- whether the Anthropic comparison report was produced
