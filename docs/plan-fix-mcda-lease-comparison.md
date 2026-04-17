# Plan: Fix mcda-lease-comparison for Cowork sandbox

**Date:** 2026-04-16
**Branch:** main
**Plugin:** `mcda-lease-comparison`
**Current version:** v1.0.0 → target v1.0.1

---

## Problem

`plugins/mcda-lease-comparison/skills/mcda-lease-comparison/scripts/calculate_distances.py`
imports `requests`, which is not pre-installed in the Claude Cowork code
execution sandbox (pre-installed: numpy, pandas, scipy, scikit-learn,
openpyxl, matplotlib, seaborn). Running the script in Cowork raises
`ModuleNotFoundError: No module named 'requests'`.

---

## Approach

Follow the same stdlib-only inline fallback pattern as the `numpy_financial`
fix in `effective-rent-analyzer` v1.0.1: try the third-party import first,
fall back to a stdlib equivalent that preserves the caller's interface.

No bootstrap scripts, no requirements.txt, no pip install.

---

## The caller's interface

`calculate_distances.py` lines 70–75 use three attributes of the response:

```python
response = requests.get(url, params=params)
if response.status_code != 200:
    raise Exception(f"API request failed with status {response.status_code}: {response.text}")
data = response.json()
```

The shim must preserve `.status_code`, `.text`, and `.json()` — a plain
parsed-dict return will break the status check.

---

## Fix

Replace the `requests` import with a try/except block that exposes a
`_Response`-like object from either backend.

```python
try:
    import requests
    def _http_get(url, params=None, timeout=10):
        return requests.get(url, params=params, timeout=timeout)
except ImportError:
    import urllib.request
    import urllib.parse
    import urllib.error
    import json as _json

    class _Response:
        def __init__(self, status_code, text):
            self.status_code = status_code
            self.text = text
        def json(self):
            return _json.loads(self.text)

    def _http_get(url, params=None, timeout=10):
        if params:
            url = url + "?" + urllib.parse.urlencode(params)
        try:
            with urllib.request.urlopen(url, timeout=timeout) as r:
                return _Response(r.status, r.read().decode())
        except urllib.error.HTTPError as e:
            # HTTPError is a Response-like object; read body then wrap
            return _Response(e.code, e.read().decode(errors="replace"))
```

Then change line 70 from:

```python
response = requests.get(url, params=params)
```

to:

```python
response = _http_get(url, params=params)
```

Lines 72–75 remain untouched.

---

## Why the wrapper class matters

The original plan returned a parsed dict directly. That silently drops the
`status_code != 200` error branch, because:

1. `requests.get` returns a response object on both success and failure —
   the code's status-code check runs on every response.
2. `urllib.request.urlopen` *raises* `HTTPError` on non-2xx. A bare
   fallback would either propagate the exception (changing the error
   surface) or swallow it (silencing auth/rate-limit failures).

Wrapping both branches in `_Response` makes the two paths behaviorally
equivalent for the code that follows.

---

## Security hardening (minimal, stays in stdlib)

- `timeout=10` on both branches — prevents indefinite hang on slow or
  hung TCP connect. One line, no dependency. Note: this is a new constraint
  on the `requests` path too (original line 70 had no timeout), not just
  the stdlib fallback. Intentional, not a regression.
- `urllib.error.HTTPError` caught and wrapped so its default `str()`
  (which includes the full URL and therefore the `key=` API key) never
  escapes into a log line or uploaded traceback.

Skipped intentionally: hash-pinned wheels, SSL context configuration,
host allowlists. These add complexity without material teaching-session
value. The call site is a single hardcoded Distancematrix URL.

---

## Files to touch

```
plugins/mcda-lease-comparison/skills/mcda-lease-comparison/scripts/calculate_distances.py
plugins/mcda-lease-comparison/.claude-plugin/plugin.json   (v1.0.0 → v1.0.1)
.claude-plugin/marketplace.json                             (bump the mcda-lease-comparison entry's version field at line 43 only, NOT the top-level marketplace "version" at line 9)
```

---

## Test approach

1. Temporarily uninstall `requests` (or rename the site-packages dir) in
   a local venv matching the Cowork sandbox package set.
2. Run `calculate_distances.py` against a known subject/comparable pair.
3. Confirm distances return as expected (fallback branch taken).
4. Force a 4xx (bad API key) and confirm the error message contains
   the status code but does NOT contain the API key string.
5. Reinstall `requests` and re-run to confirm the native branch still
   works identically.
6. With `requests` reinstalled, re-run the 4xx test from step 4 and
   confirm the error message format is consistent across branches
   (status code present, API key not leaked).
