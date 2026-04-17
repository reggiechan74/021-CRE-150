# Plan: Fix Cowork Python Package Compatibility

**Date:** 2026-04-16
**Branch:** main
**Context:** Two plugins have third-party Python packages not pre-installed in the
Claude Cowork code execution sandbox, causing silent failures or crashes.

---

## Background

Claude Cowork's code execution sandbox pre-installs: numpy, pandas, scipy,
scikit-learn, openpyxl, matplotlib, seaborn.

NOT pre-installed: pydantic, requests, numpy_financial.

numpy_financial was already fixed in effective-rent-analyzer v1.0.1 with an
inline fallback. Two plugins remain.

---

## Plugin 1: mcda-lease-comparison

**File:** `plugins/mcda-lease-comparison/skills/mcda-lease-comparison/scripts/calculate_distances.py`

**Package:** `requests`

**Usage:** Single call on line 70:
```python
response = requests.get(url, params=params)
```

**Fix:** Inline try/except fallback using stdlib `urllib.request`. Same pattern
as the numpy_financial fix. No behavior change.

```python
try:
    import requests
    def _http_get(url, params=None):
        return requests.get(url, params=params).json()
except ImportError:
    import urllib.request
    import urllib.parse
    import json as _json
    def _http_get(url, params=None):
        if params:
            url = url + "?" + urllib.parse.urlencode(params)
        with urllib.request.urlopen(url) as r:
            return _json.loads(r.read().decode())
```

Then replace the `requests.get(url, params=params)` call to use `_http_get`.

**Risk:** Low. urllib.request is stdlib, behavior identical for simple GET requests.

---

## Plugin 2: cam-reconciliation-cre

**Files:**
- `plugins/cam-reconciliation-cre/scripts/manifest.py` — imports `BaseModel, ConfigDict, Field`
- `plugins/cam-reconciliation-cre/scripts/classify_validator.py` — imports `BaseModel`
- `plugins/cam-reconciliation-cre/tests/test_manifest.py` — imports `ValidationError`

**Package:** `pydantic>=2.0`

**Usage summary:**
- 10+ model classes (LeaseCitation, CapConfig, Lease, Pool, Property,
  Classification, GLLine, ExclusionApplied, DirectBillApplied, TenantCharge,
  Provenance, Manifest, DecisionRecord)
- `Field(default_factory=list/dict)` throughout
- `model_dump(mode="json")` for JSON serialization
- `model_validate(data)` for reconstruction from JSON (recurses into nested models)
- `ConfigDict(extra="forbid")` on Manifest root model
- `ValidationError` in tests

**Why NOT a shim:** model_validate() recursively constructs nested model instances
from dicts. A plain dataclass cls(**data) won't handle nested dicts → child model
auto-conversion. Reimplementing this safely requires a metaclass-level recursive
constructor — too risky for a drop-in shim.

**Fix:** requirements.txt + bootstrap pip install.

Cam-reconciliation-cre runs a full multi-script pipeline via bootstrap.py in
the VM shell (not the sandbox). PyPI is allowlisted in the Cowork web VM.

### Step 1 — Create requirements.txt

Create `plugins/cam-reconciliation-cre/requirements.txt`:
```
pydantic>=2.0
```

### Step 2 — Add install step to bootstrap.py

Read bootstrap.py first. Add a pip install guard at the top of main():

```python
import subprocess, sys

def _ensure_deps():
    try:
        import pydantic
    except ImportError:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "pydantic>=2.0", "-q"]
        )

_ensure_deps()
```

This runs once; subsequent imports hit the cache.

### Step 3 — Document in plugin README

Add a "Requirements" section to the cam-reconciliation-cre README noting
pydantic>=2.0 is required and auto-installed on first run.

**Risk:** Medium. Depends on pip being available and PyPI being reachable. If
the plugin runs in the code execution sandbox (no pip), this fails. Mitigation:
add a clear error message if pip install fails rather than a silent crash.

---

## Version Bumps

After both fixes are implemented and tested:

- `mcda-lease-comparison`: bump to v1.0.1 (or current patch + 1)
- `cam-reconciliation-cre`: bump to current patch + 1
- `marketplace.json`: update both versions

---

## Test Approach

For mcda-lease-comparison: confirm calculate_distances.py imports without
requests installed by temporarily renaming the package and running the script.

For cam-reconciliation-cre: confirm bootstrap.py runs end-to-end in a fresh
venv without pydantic pre-installed.

---

## Files to Touch

```
plugins/mcda-lease-comparison/skills/mcda-lease-comparison/scripts/calculate_distances.py
plugins/cam-reconciliation-cre/scripts/bootstrap.py
plugins/cam-reconciliation-cre/requirements.txt          (new)
plugins/cam-reconciliation-cre/README.md                 (update)
plugins/mcda-lease-comparison/.claude-plugin/plugin.json (version bump)
plugins/cam-reconciliation-cre/.claude-plugin/plugin.json (version bump)
.claude-plugin/marketplace.json                          (version bumps)
```
