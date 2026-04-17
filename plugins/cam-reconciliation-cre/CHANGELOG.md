# Changelog

## 0.2.0 - 2026-04-16

Breaking: dependency swap to target the Claude Cowork sandbox with minimum
Python deps. Reconciliation logic and manifest shape are unchanged; only
third-party packages and the on-disk formats that required them have
changed.

- Removed `pydantic`, `reportlab`, and `PyYAML` runtime dependencies
- Removed `scripts/bootstrap.py`, `requirements.txt`, and `.bootstrapped`
  marker handling
- Models are now stdlib `@dataclass` classes with explicit `from_dict`
  classmethods; added `scripts/validation.py` with `ValidationError`,
  `ManifestJSONEncoder`, and `check_unknown_keys`
- Config format changed: `property.yaml` → `property.json` everywhere
  (matheson fixture + 10 benchmark cases + templates)
- Statement format changed: per-tenant PDF → per-tenant Markdown
  (`tenant_statements/{tenant_id}.md`)
- Benchmark suite builder emits `property.json` instead of `property.yaml`
- Tests migrated off `pydantic.ValidationError` and `model_validate` /
  `model_dump` / `model_copy` APIs
- No changes to reconciliation math, manifest shape, or tenant charge
  outputs; the v0.1.0 `allocated_manifest.json` fixture remains the
  regression baseline

## 0.1.0 - 2026-04-15

- Added typed manifest, ingest pipeline, deterministic classification, and allocation engine
- Added Matheson workshop fixtures and golden regression manifest
- Added tenant statement renderer, workpaper export, audit log, and Anthropic comparison report
- Added slash-command docs and supporting skills
- Added pytest coverage for schema, ingest, classification, allocation, rendering, comparison, and full pipeline regression
