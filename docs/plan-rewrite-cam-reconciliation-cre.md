# Plan: Remove third-party dependencies from cam-reconciliation-cre

**Date:** 2026-04-16
**Branch:** main
**Plugin:** `cam-reconciliation-cre`
**Current version:** v0.1.0 → target v0.2.0

---

## Framing

This is a **dependency swap**, not a rewrite. Reconciliation logic,
manifest schema, and file layouts stay identical. What changes: three
third-party packages get replaced by stdlib equivalents, plus the
runtime install machinery that pip-installed them.

cam-reconciliation-cre currently depends on three third-party packages
that are not pre-installed in the Claude Cowork code execution sandbox:

- `pydantic>=2.0` — models, validation, JSON serialization
- `reportlab>=4.0` — PDF tenant-statement rendering
- `PyYAML>=6.0` — reading `property.yaml` config (and writing it from
  the benchmark suite builder)

It also ships a `scripts/bootstrap.py` + `requirements.txt` pair that
pip-installs these at runtime via `/cam-reconcile`. Under the repo's
rule that plugins target the Cowork sandbox with minimum deps, **the
dependencies and the install machinery both have to go.**

**Cowork pre-install list** (source of truth is user-memory
`project_cowork_minimum_deps.md`; a companion work item is to promote
this to a committed `docs/cowork_environment.md` so plans can cite
it):

- numpy, pandas, scipy, scikit-learn, openpyxl, matplotlib, seaborn
- Python stdlib

Anything outside that list is not available at runtime.

### Terminology

- **Shape** — the logical structure of the manifest (fields, nesting,
  types). Preserved. Out of scope to change.
- **Format** — the on-disk serialization (YAML, JSON, PDF, Markdown).
  In scope to change where a dep depends on it.

So: manifest **shape** stays; config **format** goes YAML → JSON;
statement **format** goes PDF → Markdown.

---

## Scope

### In scope
- Replace `pydantic` with stdlib `dataclasses` + explicit per-model
  validation (no generic coercion framework — see Alternatives)
- Replace `PyYAML` with `json.load` (config format YAML → JSON)
- Replace `reportlab` with Markdown tenant statements
- Delete `scripts/bootstrap.py`, `requirements.txt`, `.bootstrapped`
  marker handling
- Update every command/skill/test/fixture/benchmark that touches the
  old surface (enumerated in "Files to touch")
- Convert all 11 `property.yaml` files + 2 YAML templates to JSON
- Rewrite `scripts/build_unseen_benchmark_suite.py` to emit
  `property.json` instead of `property.yaml`

### Out of scope
- Changing reconciliation logic or the manifest schema's shape
- Backward compatibility: the plugin is pre-release; v0.2.0 is a hard
  break. No dual-format ingest (no "try `.json` then fall back to
  `.yaml`"). Every `property.yaml` in the repo gets converted in this
  PR; there are no external consumers to worry about.
- Refactors not mechanically required by the dep swap (don't clean up
  `sys.path` hacks, don't restructure manifest.py, don't extract
  helpers "while we're in there")

---

## Step 1 — Complete pydantic surface inventory

Corrected from v0.1.0 review. Source files grep'd for
`BaseModel|model_validate|model_dump|model_copy|ValidationError|Field`.

### Model classes (14 total, not 13)

| File | Model class |
|---|---|
| `scripts/manifest.py` | 13 BaseModel subclasses (Manifest root, CapConfig, BaseYearConfig, Property, Lease, LeaseCitation, Pool, GLLine, Classification, ExclusionApplied, DirectBillApplied, TenantCharge, Provenance) |
| `scripts/classify_validator.py` | `DecisionRecord(BaseModel)` |

### Pydantic features used and their replacements

| pydantic feature | Where | Replacement |
|---|---|---|
| `BaseModel` class hierarchy | 14 models across 2 files | `@dataclass` on each |
| `Field(default_factory=list)` etc. | 12+ uses | `field(default_factory=list)` from `dataclasses` |
| `Literal["high", "medium", "low"]` | Confidence fields | Runtime check in `__post_init__` |
| `Optional[Decimal]` coercion | Money fields across 7 models | Explicit `Decimal(str(value))` in `__post_init__` |
| Enum coercion (`LeaseType`, `PoolName`) | Lease.pool, Lease.lease_type | Explicit `PoolName(value)` / `LeaseType(value)` in `__post_init__` |
| `datetime` from ISO string | `Provenance.run_timestamp` | Explicit `datetime.fromisoformat(value)` in `__post_init__` |
| `ConfigDict(extra="forbid")` | Manifest root only | Explicit unknown-key check in `Manifest.from_dict()` |
| `model_validate(data)` (JSON load) | `manifest.py` (Manifest.load), `classify_validator.py` (DecisionRecord load), `ingest.py` (Property, Lease load from disk), `allocate.py` lines 111, 132 | Per-model `from_dict(cls, data)` classmethod |
| `model_dump(mode="json")` | `manifest.py` Manifest.save; `allocate.py` lines 357, 382, 402; `run_unseen_benchmark.py` line 58; `classify_validator.py` line 208 | Custom `ManifestJSONEncoder(json.JSONEncoder)` — handles Decimal, datetime, Enum, dataclass |
| `model_copy(update=...)` | `classify_validator.py`; `allocate.py` line 440 | `dataclasses.replace(obj, **update)` |
| `ValidationError` raised on bad input | tests + runtime | `class ValidationError(ValueError)` in new `scripts/validation.py` |

### Fields that need manual coercion attention

Pydantic silently coerces `dict[str, Any]` and `list[dict[str, Any]]`
contents on round-trip. These are stored and read as dicts, but some
values inside them are Decimals used in arithmetic:

- `Lease.clause_refs: dict[str, LeaseCitation]` — dict of dataclass
- `Lease.specific_exclusions: list[dict[str, Any]]` — arbitrary
- `GLLine.allocation: dict[str, Decimal]` — dict of Decimals
- `TenantCharge.base_year_adjustment: Optional[dict[str, Any]]` — read at `allocate.py:84` as Decimal
- `TenantCharge.cap_adjustment: Optional[dict[str, Any]]`
- `TenantCharge.citations: list[dict[str, Any]]`
- `TenantCharge.math_trace: dict[str, Any]`
- `Manifest.budget: dict[str, Decimal]`

**Convention:** In JSON round-trip, every money-valued field is
serialized as a string (via `ManifestJSONEncoder`) and rehydrated as
`Decimal` at the `from_dict` call site. For `dict[str, Any]` fields
with embedded Decimals (e.g., `base_year_adjustment['amount_removed']`),
`from_dict` walks the known-key subset and coerces those specific keys
to Decimal. Read-sites that consume raw `dict[str, Any]` values must
wrap with `Decimal(str(...))` defensively — audit `allocate.py` and
`statement.py` for these sites.

---

## Step 2 — `scripts/validation.py` (small, explicit)

No generic recursive coercion engine. Only three things live here:

```python
from __future__ import annotations
from dataclasses import fields, is_dataclass
from decimal import Decimal
from enum import Enum
from datetime import date, datetime
import json


class ValidationError(ValueError):
    """Raised on unknown fields, missing required fields, or bad types."""


class ManifestJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return str(o)
        if isinstance(o, (date, datetime)):
            return o.isoformat()
        if isinstance(o, Enum):
            return o.value
        if is_dataclass(o):
            return {f.name: getattr(o, f.name) for f in fields(o)}
        return super().default(o)


def check_unknown_keys(cls, data, known_keys):
    unknown = set(data) - known_keys
    if unknown:
        raise ValidationError(
            f"{cls.__name__} got unknown fields: {sorted(unknown)}"
        )
```

**Why no generic engine:** A generic `from_dict(cls, data)` that walks
`dataclasses.fields()` and dispatches on annotations is effectively a
tiny pydantic. With `from __future__ import annotations` in force (all
relevant source files use it), `fields(cls)[i].type` returns strings
like `'Optional[Decimal]'` or `'dict[str, LeaseCitation]'`, not types —
so any generic coercion needs `typing.get_type_hints(cls)` plus
`typing.get_origin`/`get_args` to unwrap Optional/Union/list/dict, plus
special cases for str-Enum subclasses, forward references, and
`dict[str, Any]` leakage. That's 150-300 lines of framework code,
fragile under annotation evolution, and works against the teaching
goal of "obvious stdlib Python."

Instead, each model writes an explicit `@classmethod from_dict(cls,
data)` that names its own fields, recurses into children by name, and
coerces at the field level. Verbose, but each model is auditable on
one screen, and `_coerce` never exists to hide bugs in.

---

## Step 3 — Model conversion

### scripts/manifest.py (13 dataclasses)

For each model:
- Replace `class X(BaseModel)` with `@dataclass class X`.
- Replace `Field(default_factory=...)` with `field(default_factory=...)`.
- Add `__post_init__` to **every model with Decimal, Enum, or datetime
  fields** (most of them — not just Manifest/Classification/Lease):
  - Coerce `Decimal(str(value))` on money fields if value is not
    already a Decimal.
  - Coerce `EnumClass(value)` on Enum fields if value is a string.
  - Coerce `datetime.fromisoformat(value)` on datetime fields if value
    is a string.
  - Check Literal fields against allowed values.
- Add `@classmethod from_dict(cls, data)`:
  - `Manifest.from_dict` calls `check_unknown_keys` (replaces
    `extra="forbid"` at the root).
  - Each `from_dict` recursively invokes child `from_dict` by field
    name — no generic dispatch.
  - Handles `list[ChildModel]` with a list comprehension calling
    `ChildModel.from_dict(item)`.
  - Handles `dict[str, ChildModel]` with a dict comprehension.
  - Handles `dict[str, Any]` by copying as-is, then patching known
    Decimal-valued keys (e.g., `base_year_adjustment['amount_removed']`)
    with explicit Decimal conversion.
- Replace `Manifest.load` / `Manifest.save`:
  - `load`: `json.load` → `Manifest.from_dict(data)`.
  - `save`: `json.dump(manifest, f, cls=ManifestJSONEncoder, indent=2)`.

### scripts/classify_validator.py

- `DecisionRecord(BaseModel)` → `@dataclass DecisionRecord` with
  `from_dict` classmethod. This is a second JSON serialization surface
  (line 168-170 dumps/loads `classification_decisions.json`) — route
  it through `ManifestJSONEncoder`.
- Replace `model_copy(update=...)` with `dataclasses.replace(obj, **update)`.

### scripts/allocate.py

- Lines 111, 132: `LeaseCitation.model_validate(...)` → `LeaseCitation.from_dict(...)`.
- Lines 357, 382, 402: `obj.model_dump(mode="json")` → serialize via
  `ManifestJSONEncoder` (if producing JSON string) or walk dataclass
  to dict (if producing Python dict for in-memory use).
- Line 440: `manifest.model_copy(update=...)` → `dataclasses.replace(manifest, **update)`.
- Audit `charge.base_year_adjustment['amount_removed']` (line 84 etc.):
  ensure Decimal type, not string.

### scripts/ingest.py

- Line 78-79: `Property.model_validate(data)` → `Property.from_dict(data)`.
- Line 86: `Lease.model_validate(item)` → `Lease.from_dict(item)`.
- Line 105: `GLLine(amount=row["Amount"].strip())` — `__post_init__`
  must coerce the string to Decimal (pydantic used to).
- Line 120: `property_dir / "property.yaml"` → `property_dir / "property.json"`.
- Remove `import yaml` and the `yaml.safe_load` call.

### scripts/run_unseen_benchmark.py

- Line 58: `allocated.model_dump(mode="json")` → serialize via encoder.

### scripts/build_unseen_benchmark_suite.py

- Line 12: remove `import yaml`.
- Line 55-57 (write_yaml helper): remove, or replace with
  `json.dump(data, f, indent=2)`.
- Line 875 and any other `write_yaml(case_dir / "property.yaml", ...)`
  → `json.dump(payload, (case_dir / "property.json").open("w"), indent=2)`.

### scripts/bootstrap.py

- Delete the file.

### scripts/compare.py, score_anthropic_benchmark.py

- Audit only — these don't appear to use pydantic directly, but
  indirectly consume manifests. Confirm no regressions.

---

## Step 4 — Config format YAML → JSON

### File conversions

All 11 `property.yaml` files convert to `property.json`:

- `fixtures/matheson/property.yaml`
- `benchmarks/unseen_cam_suite/cases/01_harborpoint_exchange/property.yaml`
- `benchmarks/unseen_cam_suite/cases/02_kingsway_commons/property.yaml`
- `benchmarks/unseen_cam_suite/cases/03_cedar_ridge_plaza/property.yaml`
- `benchmarks/unseen_cam_suite/cases/04_airport_north_hub/property.yaml`
- `benchmarks/unseen_cam_suite/cases/05_riverfront_market_centre/property.yaml`
- `benchmarks/unseen_cam_suite/cases/06_westmount_professional_campus/property.yaml`
- `benchmarks/unseen_cam_suite/cases/07_meadowvale_station_centre/property.yaml`
- `benchmarks/unseen_cam_suite/cases/08_lakeshore_atrium/property.yaml`
- `benchmarks/unseen_cam_suite/cases/09_northline_commerce_court/property.yaml`
- `benchmarks/unseen_cam_suite/cases/10_university_gate_centre/property.yaml`

Templates convert:
- `templates/property_template.yaml` → `templates/property_template.json`
- `templates/lease_template.yaml` → `templates/lease_template.json`
- Update `templates/lease_template_docs.md` to reference the JSON variant.

### Docs to update

- All 10 `benchmarks/unseen_cam_suite/cases/*/README_CASE.md` —
  search/replace `property.yaml` → `property.json` in "Required Inputs"
  sections.
- Plugin `README.md` — any references.

### Conversion method

Use a one-shot script (not committed) that `yaml.safe_load`s each
file and writes `json.dump(data, indent=2)`. Delete the `.yaml`
versions after conversion.

---

## Step 5 — Statement format PDF → Markdown

### Decision: Markdown per-tenant statements

Rejected alternatives:
- **Excel sheets (openpyxl).** openpyxl is pre-installed, so this
  would work, but it adds sheets to the workpaper that mix audit data
  with narrative — poor separation. Also, per-tenant markdown renders
  inline in Cowork's file viewer, which matters for the teaching flow
  (students read statements, then diff against the Anthropic benchmark).
- **Drop statement generation entirely.** The
  `cam-statement-narrative` skill exists precisely to generate these
  artifacts; dropping them would orphan a shipped skill. Keep them.

### Scope of the statement.py rewrite

`scripts/statement.py` is 369 lines with reportlab imports at module
scope (lines 12-16: `colors`, `LETTER`, `getSampleStyleSheet`,
`Paragraph`, `SimpleDocTemplate`, `Spacer`, `Table`, `TableStyle`).
This is not a one-liner:

- Remove all reportlab imports.
- Rewrite `render_tenant_pdf` (line 113) → `render_tenant_markdown`
  returning a string; write to `tenant_<id>_statement.md`.
- Preserve the existing Excel workpaper pipeline (openpyxl) that
  co-lives in this file — don't touch it.
- Update any CLI args or call sites that referenced PDF output paths.
- Rewrite `tests/test_statement.py` assertions from PDF fidelity
  (which were likely file-size or byte checks) to structural
  invariants on the markdown output: every exclusion line appears,
  every citation referenced, summary totals match manifest.

### Artifact cleanup

Delete the 9 committed PDFs at
`fixtures/matheson/reconciliation-output/tenant_statements/*.pdf`.
Regenerate as `.md` by running `/cam-reconcile` on the matheson fixture
after the rewrite.

---

## Step 6 — Remove install machinery

Delete:
- `scripts/bootstrap.py`
- `requirements.txt`
- `.bootstrapped` marker handling (check for references in
  `cam-reconcile.md` and `bootstrap.py`'s imports-check list)

Edit `commands/cam-reconcile.md` to drop the bootstrap invocation in
step 1.

Edit plugin `README.md`: remove the "Setup" section; under
Dependencies, replace with:

> Runs in Claude Cowork's code execution sandbox. Uses only the Python
> stdlib plus Cowork pre-installs (numpy, pandas, scipy, scikit-learn,
> openpyxl, matplotlib, seaborn). No setup required.

---

## Step 7 — Downstream artifacts (skills + commands)

Grep every skill and command for references to `.pdf`, `pydantic`,
`property.yaml`, or `reportlab`:

- `skills/cam-classify/SKILL.md`
- `skills/cam-statement-narrative/SKILL.md` — likely references PDF
  output naming
- `skills/cam-explain/SKILL.md`
- `commands/cam-reconcile.md` (already in Step 6)
- `commands/cam-explain.md`
- `commands/cam-compare-vs-anthropic.md`

Update any references to PDF artifact names or YAML config paths.
Add a `CHANGELOG.md` entry documenting the break.

---

## Step 8 — Version bump

- `plugins/cam-reconciliation-cre/.claude-plugin/plugin.json`: v0.1.0 → v0.2.0
- `.claude-plugin/marketplace.json`: update to match

v0.2.0 marks a pre-release break. We are not claiming semver stability
at v1.0.0 yet — workshop delivery will surface additional changes
before that happens. The version bump is a signal to anyone pulling
the plugin that outputs and config format changed; it is not a
semver-on-public-API claim.

---

## Alternatives considered and rejected

- **Generic `from_dict` + `_coerce` engine in validation.py.** Rejected
  above (see Step 2). Would be a tiny pydantic; fragile with `from
  __future__ import annotations`; teaching-unfriendly.
- **Vendor a 200-line single-file pydantic alternative into
  `scripts/`.** The Cowork rule is "no pip-installed third-party deps",
  not "no vendored code", so this is technically permitted. Rejected:
  still adds a framework layer students have to learn; per-model
  explicit classmethods are more pedagogically useful.
- **`typing.NamedTuple` instead of `@dataclass`.** NamedTuple gives
  basic type hints but no `__post_init__`, no field defaults for
  mutable types (no `default_factory`), and immutability forces
  `dataclasses.replace`-everywhere. `@dataclass` is closer to the
  pydantic mental model the current code uses.
- **`attrs`.** Not a Cowork pre-install; same problem as pydantic.
- **Hand-rolled YAML parser.** Any real-world config breaks a naive
  parser; `json` is already in stdlib and the config shape is trivially
  JSON-able.
- **Dual-format ingest (try `.json`, fall back to `.yaml`).** Keeps
  PyYAML dependency. Rejected: defeats the goal. Pre-release means no
  external consumers to migrate.

---

## Files to touch

### Rewrite
- `plugins/cam-reconciliation-cre/scripts/manifest.py` — 13 models → dataclasses
- `plugins/cam-reconciliation-cre/scripts/classify_validator.py` — DecisionRecord + model_copy swap
- `plugins/cam-reconciliation-cre/scripts/allocate.py` — model_validate/model_dump/model_copy swaps
- `plugins/cam-reconciliation-cre/scripts/ingest.py` — yaml→json + model_validate swaps
- `plugins/cam-reconciliation-cre/scripts/statement.py` — reportlab → markdown
- `plugins/cam-reconciliation-cre/scripts/run_unseen_benchmark.py` — model_dump swap
- `plugins/cam-reconciliation-cre/scripts/build_unseen_benchmark_suite.py` — write YAML → write JSON

### New
- `plugins/cam-reconciliation-cre/scripts/validation.py` — ValidationError, ManifestJSONEncoder, check_unknown_keys

### Delete
- `plugins/cam-reconciliation-cre/scripts/bootstrap.py`
- `plugins/cam-reconciliation-cre/requirements.txt`
- `plugins/cam-reconciliation-cre/fixtures/matheson/reconciliation-output/tenant_statements/*.pdf` (9 files, regenerate as .md)

### Test updates
- `plugins/cam-reconciliation-cre/tests/test_manifest.py` — swap `from pydantic import ValidationError` for `from scripts.validation`; swap `Manifest.model_validate(data)` for `Manifest.from_dict(data)`; keep the unknown-fields test
- `plugins/cam-reconciliation-cre/tests/test_allocate.py` — swap any model_validate/model_dump calls
- `plugins/cam-reconciliation-cre/tests/test_classify_validator.py` — DecisionRecord swaps
- `plugins/cam-reconciliation-cre/tests/test_compare.py` — audit
- `plugins/cam-reconciliation-cre/tests/test_full_pipeline_matheson.py` — model_dump on fixture; yaml→json fixture reference
- `plugins/cam-reconciliation-cre/tests/test_ingest.py` — property.yaml → property.json fixture reference
- `plugins/cam-reconciliation-cre/tests/test_statement.py` — PDF assertions → markdown structural invariants

### Command / skill updates
- `plugins/cam-reconciliation-cre/commands/cam-reconcile.md` — drop bootstrap step; update output references
- `plugins/cam-reconciliation-cre/commands/cam-explain.md` — grep for PDF/yaml references
- `plugins/cam-reconciliation-cre/commands/cam-compare-vs-anthropic.md` — grep for PDF/yaml references
- `plugins/cam-reconciliation-cre/skills/cam-classify/SKILL.md` — grep
- `plugins/cam-reconciliation-cre/skills/cam-statement-narrative/SKILL.md` — likely references PDF output
- `plugins/cam-reconciliation-cre/skills/cam-explain/SKILL.md` — grep

### Config / docs
- `plugins/cam-reconciliation-cre/README.md` — rewrite deps section; remove Setup
- `plugins/cam-reconciliation-cre/CHANGELOG.md` — add v0.2.0 entry
- `plugins/cam-reconciliation-cre/.claude-plugin/plugin.json` — v0.1.0 → v0.2.0
- `.claude-plugin/marketplace.json` — version bump

### Data / fixture conversions (YAML → JSON)
- `plugins/cam-reconciliation-cre/fixtures/matheson/property.yaml` → `property.json`
- `plugins/cam-reconciliation-cre/benchmarks/unseen_cam_suite/cases/01_harborpoint_exchange/property.yaml` → `.json`
- `plugins/cam-reconciliation-cre/benchmarks/unseen_cam_suite/cases/02_kingsway_commons/property.yaml` → `.json`
- `plugins/cam-reconciliation-cre/benchmarks/unseen_cam_suite/cases/03_cedar_ridge_plaza/property.yaml` → `.json`
- `plugins/cam-reconciliation-cre/benchmarks/unseen_cam_suite/cases/04_airport_north_hub/property.yaml` → `.json`
- `plugins/cam-reconciliation-cre/benchmarks/unseen_cam_suite/cases/05_riverfront_market_centre/property.yaml` → `.json`
- `plugins/cam-reconciliation-cre/benchmarks/unseen_cam_suite/cases/06_westmount_professional_campus/property.yaml` → `.json`
- `plugins/cam-reconciliation-cre/benchmarks/unseen_cam_suite/cases/07_meadowvale_station_centre/property.yaml` → `.json`
- `plugins/cam-reconciliation-cre/benchmarks/unseen_cam_suite/cases/08_lakeshore_atrium/property.yaml` → `.json`
- `plugins/cam-reconciliation-cre/benchmarks/unseen_cam_suite/cases/09_northline_commerce_court/property.yaml` → `.json`
- `plugins/cam-reconciliation-cre/benchmarks/unseen_cam_suite/cases/10_university_gate_centre/property.yaml` → `.json`
- `plugins/cam-reconciliation-cre/templates/property_template.yaml` → `property_template.json`
- `plugins/cam-reconciliation-cre/templates/lease_template.yaml` → `lease_template.json`
- `plugins/cam-reconciliation-cre/templates/lease_template_docs.md` — update references
- All 10 `benchmarks/unseen_cam_suite/cases/*/README_CASE.md` — `property.yaml` → `property.json` references
- `fixtures/matheson/expected_manifest.json` — regenerate after rewrite; compare numerically to pre-rewrite version (see Test approach)

---

## Test approach

### 1. Regression baseline (commit BEFORE starting work)

Before touching any code, run `/cam-reconcile` on the matheson fixture
with the current (v0.1.0) codebase and commit
`fixtures/matheson/reconciliation-output/manifests/allocated_manifest.json`
as the golden baseline. Label it in a pre-rewrite commit so it can be
identified: "chore: freeze v0.1.0 allocated_manifest baseline before
dep rewrite".

### 2. Unit

Existing unit tests pass after the import/API swaps described in the
Test updates section. Add:
- `test_manifest_unknown_fields_raise` — confirms
  `Manifest.from_dict({"bogus": 1, ...})` raises
  `scripts.validation.ValidationError` (replaces the
  `ConfigDict(extra="forbid")` check).
- `test_decision_record_roundtrip` — confirms `DecisionRecord.from_dict`
  and JSON encoding round-trip losslessly through
  `classification_decisions.json`.

### 3. Integration

Run `/cam-reconcile` end-to-end on matheson in a fresh venv with **only**
Cowork pre-installs: numpy, pandas, scipy, scikit-learn, openpyxl,
matplotlib, seaborn. No pydantic, no reportlab, no PyYAML. Confirm:

- Manifest loads (`property.json`, `leases.json`, `budget.md`, `gl.csv`)
- Manifest builds and serializes to JSON via `ManifestJSONEncoder`
- Classification pass produces `DecisionRecord` entries and
  `classification_decisions.json` round-trips
- Workpaper Excel writes
- Per-tenant markdown statements write with expected names

**Authoritative check (separate gate):** after local pass, run in an
actual Cowork sandbox (or exact replica) to confirm imports succeed
there. A local venv is a defensive approximation, not the deployment
oracle.

### 4. Numeric regression

Compare the post-rewrite
`fixtures/matheson/reconciliation-output/manifests/allocated_manifest.json`
against the v0.1.0 golden baseline from step 1:

- **Tolerance:** every money-valued field (Decimal) matches within
  `Decimal("0.01")` (one cent).
- **Exact match required:** enums, reason strings, line_ids, tenant
  ids, pool names, counts of allocated lines, counts of exclusions,
  citation references.
- **Structural match:** for tenant statement markdown files, every
  exclusion line present in v0.1.0 PDF content is present in the new
  markdown; every citation references the same lease section.

### 5. Benchmark suite spot check

Run `scripts/run_unseen_benchmark.py` on one benchmark case (e.g.,
`01_harborpoint_exchange`) and confirm output parity against its
pre-rewrite baseline. Full-suite regression is out of scope for this
PR.

---

## Risks

- **Scope creep during model conversion.** 14 models × per-model
  `from_dict` = 14 auditable chunks of work. Mitigation: the Step 1
  inventory is the scope contract; anything outside it gets filed,
  not fixed. Do not "clean up while we're in there."
- **`dict[str, Any]` Decimal leakage.** The convention is "JSON stores
  as string, read-sites convert to Decimal." Any read-site missed
  becomes a runtime arithmetic error. Mitigation: grep
  `base_year_adjustment|cap_adjustment|math_trace|citations|budget`
  in `allocate.py` and `statement.py`; wrap with `Decimal(str(...))`.
- **Markdown statements lose PDF fidelity.** Acceptable for a teaching
  workshop; print-ready PDFs are a post-v0.2.0 feature request, not a
  blocker.
- **YAML → JSON migration leaves stale references in skills or
  commands.** Mitigation: grep all of `plugins/cam-reconciliation-cre`
  for `.yaml` and `.pdf` before shipping.
- **Benchmark suite builder emits JSON now — existing benchmark
  outputs diff.** Each of the 10 case directories gets new
  `property.json` files; regenerating from
  `build_unseen_benchmark_suite.py` must produce deterministic output.
  Mitigation: use `json.dump(..., sort_keys=True, indent=2)` for
  byte-stable diffs.
- **Cowork pre-install list is user-memory, not in-repo.** If Cowork
  changes its sandbox, every plugin built on this assumption breaks
  silently. Mitigation (separate work item, not blocking this PR):
  commit `docs/cowork_environment.md` naming the pre-install set and
  dating it.
