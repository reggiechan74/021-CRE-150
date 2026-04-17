# Roof-Replacement-Review Pipeline Speedup Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Cut the `/roof-review` pipeline wall-clock by ~45–55% on a 5-bid tender by overlapping RFP extraction with bid extraction and parallelizing qualification-check and technical-review within each bid.

**Architecture:**
Today each bid subagent runs `bid-extract → qual-check → tech-review` serially, and RFP extraction blocks every bid from starting. After this change, the command fans out two waves: wave 1 runs `rfp-extract` in parallel with `bid-extract × N`; wave 2 runs `qual-check + tech-review` in parallel per bid. To make the two wave-2 skills safely concurrent, each writes a disjoint sidecar JSON (`bid_<slug>.qual.json`, `bid_<slug>.tech.json`) and `normalize.py` deep-merges the sidecars into the final bid manifest. The ownership boundaries between qual-check and tech-review (gate names, red-flag categories, sub-scores) are already disjoint by design — sidecar writes prevent the last-writer-wins race that the current single-file pattern would introduce.

**Tech Stack:** Python 3 stdlib only (no new deps — complies with the Cowork minimum-deps constraint). `pytest` for tests. Skill files are markdown; the `/roof-review` command is markdown.

---

## File Structure

Files touched by this plan and what each is responsible for after the change:

**Python (scripts/):**
- `scripts/normalize.py` — MODIFY. Adds `--qual-sidecars` and `--tech-sidecars` glob flags; deep-merges each sidecar onto the matching base bid manifest before writing the tender manifest. Collision detection on `mandatory_gates`, `scores`, `scoring_rationale` keys (disjoint-by-design).

**Tests (tests/):**
- `tests/test_normalize_sidecar_merge.py` — CREATE. Exercises the merge logic end-to-end: base + qual + tech → merged bid record with all three sections populated; collision raises; missing sidecar tolerated with warning.

**Skills (skills/*/SKILL.md):**
- `skills/roof-qualification-check/SKILL.md` — MODIFY. Output block says "write to `bid_<slug>.qual.json` sidecar, not the base bid manifest". Fixture allowlist: "read only §04 and §03" (trim the 2-fixture universe from 4).
- `skills/roof-technical-review/SKILL.md` — MODIFY. Output block says "write to `bid_<slug>.tech.json` sidecar". Fixture allowlist: "read only §01 and §02".
- `skills/roof-bid-extract/SKILL.md` — MODIFY. Add explicit statement: "This skill does NOT require the RFP manifest — it extracts bid facts only. qual-check and tech-review consume the RFP." This authorizes bid-extract to run in wave 1 alongside rfp-extract.

**Command (commands/):**
- `commands/roof-review.md` — MODIFY. Replace the current three-step LLM sequence with two parallel waves; update the `normalize.py` invocation with the new `--qual-sidecars` / `--tech-sidecars` flags; update each subagent prompt to reflect its wave assignment and sidecar output path.

**No files deleted.** No new Python scripts. No new dependencies.

---

## Task 1: Write failing tests for sidecar deep-merge

**Files:**
- Test: `plugins/roof-replacement-review/tests/test_normalize_sidecar_merge.py`

- [ ] **Step 1: Create the test file with three failing tests**

Create `plugins/roof-replacement-review/tests/test_normalize_sidecar_merge.py`:

```python
"""Tests for scripts/normalize.py sidecar merge logic.

Wave 2 of the /roof-review pipeline writes qualification-check and technical-review
outputs into disjoint sidecar JSON files (bid_<slug>.qual.json and bid_<slug>.tech.json).
normalize.py must deep-merge these onto the base bid manifest to produce the final
bid record inside the tender manifest.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest


PLUGIN_ROOT = Path(__file__).resolve().parents[1]
NORMALIZE = PLUGIN_ROOT / "scripts" / "normalize.py"


def _write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data), encoding="utf-8")


@pytest.fixture
def rfp_manifest(tmp_path: Path) -> Path:
    path = tmp_path / "rfp.json"
    _write_json(path, {"project": {"name": "Test"}, "rfp": {"mandatory_requirements": {}}})
    return path


@pytest.fixture
def base_bid(tmp_path: Path) -> Path:
    path = tmp_path / "bid_acme.json"
    _write_json(path, {
        "bidder_id": "acme",
        "bidder_name": "Acme Roofing",
        "pricing": {"base_bid_cad": 500000},
        "red_flags": [],
        "extraction_notes": ["hst treatment unclear"],
    })
    return path


@pytest.fixture
def qual_sidecar(tmp_path: Path) -> Path:
    path = tmp_path / "bid_acme.qual.json"
    _write_json(path, {
        "bidder_id": "acme",
        "mandatory_gates": {
            "wsib_clearance": {"result": "pass", "evidence": "p. 12"},
        },
        "scores": {
            "experience_references": 60,
            "qualifications_certifications": 55,
            "schedule": 70,
        },
        "scoring_rationale": {"experience_references": {"sub_factors": {"count": 40}}},
        "red_flags": [{"category": "qualifications", "severity": "low", "description": "WSIB rate high"}],
    })
    return path


@pytest.fixture
def tech_sidecar(tmp_path: Path) -> Path:
    path = tmp_path / "bid_acme.tech.json"
    _write_json(path, {
        "bidder_id": "acme",
        "mandatory_gates": {
            "cover_board": {"result": "pass", "evidence": "p. 18"},
        },
        "scores": {
            "technical_approach": 65,
            "warranty_materials": 70,
        },
        "scoring_rationale": {"technical_approach": {"sub_factors": {"tear_off": 20}}},
        "red_flags": [{"category": "warranty", "severity": "medium", "description": "workmanship yrs below median"}],
    })
    return path


def _run_normalize(
    tmp_path: Path,
    rfp: Path,
    bid_glob: str,
    qual_glob: str | None = None,
    tech_glob: str | None = None,
) -> dict:
    out = tmp_path / "tender_manifest.json"
    cmd = [
        sys.executable, str(NORMALIZE),
        "--rfp", str(rfp),
        "--bids", bid_glob,
        "--out", str(out),
    ]
    if qual_glob:
        cmd += ["--qual-sidecars", qual_glob]
    if tech_glob:
        cmd += ["--tech-sidecars", tech_glob]
    subprocess.run(cmd, check=True)
    return json.loads(out.read_text())


def test_merge_base_plus_qual_plus_tech_populates_all_sections(
    tmp_path: Path, rfp_manifest: Path, base_bid: Path, qual_sidecar: Path, tech_sidecar: Path
) -> None:
    data = _run_normalize(
        tmp_path, rfp_manifest,
        bid_glob=str(tmp_path / "bid_*.json"),
        qual_glob=str(tmp_path / "bid_*.qual.json"),
        tech_glob=str(tmp_path / "bid_*.tech.json"),
    )

    bids = data["bids"]
    assert len(bids) == 1
    bid = bids[0]

    # Base fields survived
    assert bid["bidder_id"] == "acme"
    assert bid["pricing"]["base_bid_cad"] == 500000

    # Gates merged from both sidecars
    assert set(bid["mandatory_gates"].keys()) == {"wsib_clearance", "cover_board"}

    # Scores merged from both sidecars
    assert bid["scores"]["experience_references"] == 60
    assert bid["scores"]["technical_approach"] == 65

    # Red flags concatenated
    categories = {f["category"] for f in bid["red_flags"]}
    assert categories == {"qualifications", "warranty"}


def test_merge_raises_on_duplicate_gate_key(
    tmp_path: Path, rfp_manifest: Path, base_bid: Path, qual_sidecar: Path
) -> None:
    # Tech sidecar collides with qual on wsib_clearance — illegal per SKILL ownership rules.
    bad_tech = tmp_path / "bid_acme.tech.json"
    _write_json(bad_tech, {
        "bidder_id": "acme",
        "mandatory_gates": {"wsib_clearance": {"result": "fail"}},
        "scores": {"technical_approach": 50, "warranty_materials": 50},
        "scoring_rationale": {},
        "red_flags": [],
    })

    result = subprocess.run(
        [
            sys.executable, str(NORMALIZE),
            "--rfp", str(rfp_manifest),
            "--bids", str(tmp_path / "bid_*.json"),
            "--qual-sidecars", str(tmp_path / "bid_*.qual.json"),
            "--tech-sidecars", str(tmp_path / "bid_*.tech.json"),
            "--out", str(tmp_path / "tender_manifest.json"),
        ],
        capture_output=True, text=True,
    )
    assert result.returncode != 0
    assert "wsib_clearance" in result.stderr
    assert "collision" in result.stderr.lower()


def test_merge_tolerates_missing_sidecars(
    tmp_path: Path, rfp_manifest: Path, base_bid: Path
) -> None:
    # Running without sidecars should still succeed — used for debugging + back-compat.
    data = _run_normalize(
        tmp_path, rfp_manifest,
        bid_glob=str(tmp_path / "bid_*.json"),
    )
    bids = data["bids"]
    assert len(bids) == 1
    assert bids[0]["bidder_id"] == "acme"
    # No sidecars means no gates/scores populated yet — that's fine, score.py fails later
    # with a clearer error. This test just asserts normalize itself doesn't crash.
    assert "mandatory_gates" not in bids[0] or bids[0].get("mandatory_gates") == {}
```

- [ ] **Step 2: Run the tests to verify they fail**

Run:
```bash
cd plugins/roof-replacement-review && python3 -m pytest tests/test_normalize_sidecar_merge.py -v
```

Expected: the two new-behavior tests (`test_merge_base_plus_qual_plus_tech_populates_all_sections`, `test_merge_raises_on_duplicate_gate_key`) fail with `unrecognized arguments: --qual-sidecars` — the argparse in `normalize.py` has not yet been extended. The third test (`test_merge_tolerates_missing_sidecars`) passes today because it only uses the existing `--rfp`/`--bids`/`--out` flags and asserts the no-sidecar path still works; it serves as a back-compat guard.

- [ ] **Step 3: Commit**

```bash
git add plugins/roof-replacement-review/tests/test_normalize_sidecar_merge.py
git commit -m "test(roof-review): failing tests for sidecar deep-merge in normalize"
```

---

## Task 2: Implement sidecar deep-merge in normalize.py

**Files:**
- Modify: `plugins/roof-replacement-review/scripts/normalize.py`

- [ ] **Step 1: Rewrite normalize.py to accept and merge sidecars**

Replace the current contents of `plugins/roof-replacement-review/scripts/normalize.py` with:

```python
#!/usr/bin/env python3
"""Merge an RFP manifest and N bid manifests (plus optional qual/tech sidecars)
into a single tender manifest.

Inputs are JSON files produced by the roof-rfp-extract, roof-bid-extract,
roof-qualification-check, and roof-technical-review skills. Output conforms
to templates/bid_schema.json.

Sidecar merge: when --qual-sidecars or --tech-sidecars globs are provided,
each sidecar is matched by bidder_id to its base bid manifest and deep-merged.
Collisions on mandatory_gates / scores / scoring_rationale keys are fatal —
the two review skills have disjoint output ownership by design (see the
ownership tables in skills/roof-qualification-check/SKILL.md and
skills/roof-technical-review/SKILL.md). A collision means a skill wrote
outside its lane.
"""
from __future__ import annotations

import argparse
import glob
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


DISJOINT_DICT_KEYS = ("mandatory_gates", "scores", "scoring_rationale")
CONCAT_LIST_KEYS = ("red_flags", "extraction_notes")


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def merge_sidecar(base: dict, sidecar: dict, sidecar_name: str) -> list[str]:
    """Merge sidecar into base in-place. Returns a list of collision errors;
    an empty list means the merge was clean."""
    errors: list[str] = []
    for key in DISJOINT_DICT_KEYS:
        incoming = sidecar.get(key) or {}
        if not incoming:
            continue
        existing = base.setdefault(key, {})
        for sub_key, sub_val in incoming.items():
            if sub_key in existing:
                errors.append(
                    f"collision on {key}.{sub_key} — already populated by earlier "
                    f"source; sidecar '{sidecar_name}' must not overwrite. "
                    "Check skill ownership boundaries."
                )
                continue
            existing[sub_key] = sub_val
    for key in CONCAT_LIST_KEYS:
        incoming = sidecar.get(key) or []
        if not incoming:
            continue
        base.setdefault(key, [])
        base[key].extend(incoming)
    return errors


def index_by_bidder(paths: list[Path]) -> dict[str, dict]:
    out: dict[str, dict] = {}
    for p in paths:
        data = load_json(p)
        bid_id = data.get("bidder_id")
        if not bid_id:
            raise ValueError(f"sidecar {p} missing bidder_id")
        if bid_id in out:
            raise ValueError(f"duplicate bidder_id '{bid_id}' across sidecars")
        out[bid_id] = data
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rfp", required=True, help="Path to rfp.json")
    ap.add_argument("--bids", required=True, help="Glob pattern for bid_*.json base manifests")
    ap.add_argument("--qual-sidecars", help="Glob for bid_*.qual.json files (optional)")
    ap.add_argument("--tech-sidecars", help="Glob for bid_*.tech.json files (optional)")
    ap.add_argument("--out", required=True, help="Path to write tender_manifest.json")
    args = ap.parse_args()

    rfp_path = Path(args.rfp)
    if not rfp_path.is_file():
        print(f"ERROR: RFP manifest not found: {rfp_path}", file=sys.stderr)
        return 1

    rfp_data = load_json(rfp_path)
    bid_paths = sorted(Path(p) for p in glob.glob(args.bids))
    if not bid_paths:
        print(f"ERROR: no bid manifests matched {args.bids}", file=sys.stderr)
        return 1

    bids = [load_json(p) for p in bid_paths]

    qual_index: dict[str, dict] = {}
    tech_index: dict[str, dict] = {}
    if args.qual_sidecars:
        qual_paths = sorted(Path(p) for p in glob.glob(args.qual_sidecars))
        qual_index = index_by_bidder(qual_paths)
    if args.tech_sidecars:
        tech_paths = sorted(Path(p) for p in glob.glob(args.tech_sidecars))
        tech_index = index_by_bidder(tech_paths)

    all_errors: list[str] = []
    for bid in bids:
        bid_id = bid.get("bidder_id")
        if not bid_id:
            all_errors.append(f"base bid manifest missing bidder_id")
            continue
        if bid_id in qual_index:
            all_errors.extend(merge_sidecar(bid, qual_index[bid_id], f"{bid_id}.qual"))
        elif args.qual_sidecars:
            print(
                f"WARNING: no qual sidecar found for bidder '{bid_id}' — "
                "score.py will fail unless this is intentional",
                file=sys.stderr,
            )
        if bid_id in tech_index:
            all_errors.extend(merge_sidecar(bid, tech_index[bid_id], f"{bid_id}.tech"))
        elif args.tech_sidecars:
            print(
                f"WARNING: no tech sidecar found for bidder '{bid_id}' — "
                "score.py will fail unless this is intentional",
                file=sys.stderr,
            )

    if all_errors:
        print("ERROR: sidecar merge failed:", file=sys.stderr)
        for line in all_errors:
            print(f"  - {line}", file=sys.stderr)
        return 1

    manifest = {
        "manifest_version": "1.0.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "project": rfp_data.get("project", {}),
        "rfp": rfp_data.get("rfp", {}),
        "bids": bids,
    }

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    print(f"Wrote tender manifest: {out_path}")
    print(f"  RFP: {rfp_path.name}")
    print(f"  Bids: {len(bids)}")
    if qual_index:
        print(f"  Qual sidecars merged: {len(qual_index)}")
    if tech_index:
        print(f"  Tech sidecars merged: {len(tech_index)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 2: Run the new tests to verify they pass**

Run:
```bash
cd plugins/roof-replacement-review && python3 -m pytest tests/test_normalize_sidecar_merge.py -v
```

Expected: all 3 tests PASS.

- [ ] **Step 3: Run the full existing test suite to verify no regression**

Run:
```bash
cd plugins/roof-replacement-review && python3 -m pytest -q
```

Expected: all 29 tests pass (26 existing + 3 new). `test_normalize_produces_three_bids` and the existing `test_score.py` tests continue to pass because the base-bid-only path (no sidecar globs) still works.

- [ ] **Step 4: Commit**

```bash
git add plugins/roof-replacement-review/scripts/normalize.py
git commit -m "feat(roof-review): normalize.py merges qual+tech sidecars with collision detection"
```

---

## Task 3: Add a backward-compat integration test using sample fixtures

**Files:**
- Test: `plugins/roof-replacement-review/tests/test_normalize_sidecar_merge.py` (extend)

This task guards against a subtle regression: the sample fixtures under `fixtures/sample_bids/` already contain merged `mandatory_gates` / `scores` / `red_flags` (from the legacy single-file pattern). We must confirm that feeding those as BASE bids (no sidecars) still produces the same tender manifest the existing `test_score.py` relies on.

- [ ] **Step 1: Add a test that re-runs normalize on legacy-shape fixtures**

Append to `plugins/roof-replacement-review/tests/test_normalize_sidecar_merge.py`:

```python
FIXTURES = PLUGIN_ROOT / "fixtures"


def test_legacy_fixture_shape_still_merges_cleanly(tmp_path: Path) -> None:
    """Regression guard: legacy fixtures (pre-sidecar) have qual+tech fields
    already merged into the base bid manifest. normalize must accept them
    unchanged when no sidecar globs are passed."""
    out = tmp_path / "tender_manifest.json"
    result = subprocess.run(
        [
            sys.executable, str(NORMALIZE),
            "--rfp", str(FIXTURES / "sample_rfp" / "rfp.json"),
            "--bids", str(FIXTURES / "sample_bids" / "bid_*.json"),
            "--out", str(out),
        ],
        capture_output=True, text=True, check=True,
    )
    assert "Qual sidecars merged" not in result.stdout
    data = json.loads(out.read_text())
    assert len(data["bids"]) == 3
    # Legacy fixtures carry these pre-populated — they must survive the pass-through.
    for bid in data["bids"]:
        assert "mandatory_gates" in bid
        assert "scores" in bid
```

- [ ] **Step 2: Run the tests**

Run:
```bash
cd plugins/roof-replacement-review && python3 -m pytest tests/test_normalize_sidecar_merge.py -v
```

Expected: all 4 tests pass.

- [ ] **Step 3: Commit**

```bash
git add plugins/roof-replacement-review/tests/test_normalize_sidecar_merge.py
git commit -m "test(roof-review): regression guard for legacy (no-sidecar) normalize path"
```

---

## Task 4: Update roof-qualification-check SKILL.md to write a sidecar

**Files:**
- Modify: `plugins/roof-replacement-review/skills/roof-qualification-check/SKILL.md`

No automated test fires here (SKILL.md is a prompt), but the downstream `/roof-review` end-to-end smoke test in Task 8 exercises this change.

- [ ] **Step 1: Update the Output section of SKILL.md**

Open `plugins/roof-replacement-review/skills/roof-qualification-check/SKILL.md`.

Find the `## Output per Gate` heading (around line 176). Immediately BEFORE that heading, insert a new section:

```markdown
## Sidecar Output File

Write your results to a **sidecar** JSON file so the technical-review skill can
run in parallel without clobbering your writes:

**Path:** `<rfp-dir>/roof-review-output/manifests/bid_<slug>.qual.json`

**Shape:**

```json
{
  "bidder_id": "<same as base bid manifest>",
  "mandatory_gates": { "<gate_name>": { "result": "...", "evidence": "...", "notes": "..." } },
  "scores": {
    "experience_references": <0-100>,
    "qualifications_certifications": <0-100>,
    "schedule": <0-100>
  },
  "scoring_rationale": {
    "experience_references": { "sub_factors": { "...": <points> } },
    "qualifications_certifications": { "sub_factors": { "...": <points> } },
    "schedule": { "sub_factors": { "...": <points> } }
  },
  "red_flags": [
    { "severity": "...", "category": "qualifications", "description": "...", ... }
  ]
}
```

**Do NOT** touch the base `bid_<slug>.json` — the technical-review skill is
writing `bid_<slug>.tech.json` concurrently and `scripts/normalize.py` will
merge all three files. A write to `bid_<slug>.json` from this skill is a bug.

Keys this sidecar MAY contain: `bidder_id`, `mandatory_gates`, `scores`,
`scoring_rationale`, `red_flags` (only `category: "qualifications"`).

Keys this sidecar MUST NOT contain: `scores.technical_approach`,
`scores.warranty_materials`, any `mandatory_gates` entry from the technical
table in `roof-technical-review` (scope_compliance, membrane_thickness,
cover_board, insulation_upgrade, warranty_type, warranty_duration,
completion_date, mobilization_date, fire_rating, wind_uplift), or any
`red_flags` with a category other than `qualifications`.
```

Then update the existing `## Output per Gate` section so it no longer says "Write each gate result to `bid.mandatory_gates.<gate_name>`" — change it to:

```markdown
## Output per Gate

Write each gate result into the sidecar file's `mandatory_gates.<gate_name>`:
```

(Rest of that section unchanged.)

- [ ] **Step 2: Add a fixture allowlist reminder**

Still in `skills/roof-qualification-check/SKILL.md`, find the `## Reference Material` block (around line 85-90). Replace it with:

```markdown
## Reference Material

**Read only these fixtures — do not load `01_ontario_roofing_codes.md` or `02_roofing_materials_warranties.md`, which are owned by `roof-technical-review`:**

- `fixtures/domain_knowledge/04_contractor_qualification.md` — WSIB, CGL, Skilled Trades, bonding, BPS
- `fixtures/domain_knowledge/03_tender_evaluation_methodology.md` §2 — mandatory vs rated split, Contract A/B doctrine (Ron Engineering 1981 SCC)
```

- [ ] **Step 3: Commit**

```bash
git add plugins/roof-replacement-review/skills/roof-qualification-check/SKILL.md
git commit -m "docs(roof-review): qual-check writes qual sidecar; allowlist to 2 fixtures"
```

---

## Task 5: Update roof-technical-review SKILL.md to write a sidecar

**Files:**
- Modify: `plugins/roof-replacement-review/skills/roof-technical-review/SKILL.md`

- [ ] **Step 1: Update the Output section of SKILL.md**

Open `plugins/roof-replacement-review/skills/roof-technical-review/SKILL.md`.

Find the `## Output` heading (around line 179). Replace the existing Output block with:

```markdown
## Sidecar Output File

Write your results to a **sidecar** JSON file so the qualification-check skill can
run in parallel without clobbering your writes:

**Path:** `<rfp-dir>/roof-review-output/manifests/bid_<slug>.tech.json`

**Shape:**

```json
{
  "bidder_id": "<same as base bid manifest>",
  "mandatory_gates": { "<technical_gate_name>": { "result": "...", "evidence": "..." } },
  "scores": {
    "technical_approach": <0-100>,
    "warranty_materials": <0-100>
  },
  "scoring_rationale": {
    "technical_approach": { "sub_factors": { "...": <points> } },
    "warranty_materials": { "sub_factors": { "...": <points> } }
  },
  "red_flags": [
    { "severity": "...", "category": "scope|materials|warranty|safety|substitutions", ... }
  ]
}
```

**Do NOT** touch the base `bid_<slug>.json` — the qualification-check skill is
writing `bid_<slug>.qual.json` concurrently and `scripts/normalize.py` will
merge all three files. A write to `bid_<slug>.json` from this skill is a bug.

Keys this sidecar MAY contain: `bidder_id`, `mandatory_gates` (only from the
technical gate table above), `scores.technical_approach`,
`scores.warranty_materials`, `scoring_rationale.technical_approach`,
`scoring_rationale.warranty_materials`, `red_flags` (categories `scope`,
`materials`, `warranty`, `safety`, `substitutions`).

Keys this sidecar MUST NOT contain: `scores.experience_references`,
`scores.qualifications_certifications`, `scores.schedule`, any administrative
`mandatory_gates` entry (`wsib_clearance`, `cgl_insurance`, `bid_bond`,
`working_at_heights`, `addenda`, `non_collusion`, `site_visit`,
`years_in_business`, `references`), or any `red_flags` with
`category: "qualifications"`.
```

- [ ] **Step 2: Update the Reference Material block**

Still in the same file, find `## Reference Material` (around line 52). Replace it with:

```markdown
## Reference Material

**Read only these fixtures — do not load `03_tender_evaluation_methodology.md` or `04_contractor_qualification.md`, which are owned by `roof-qualification-check`:**

Treat these as ground truth — cite section numbers in your findings:

- `fixtures/domain_knowledge/01_ontario_roofing_codes.md` — OBC Part 3 (commercial) and Part 9 (residential), wind uplift, SB-10/SB-12 R-values, ventilation ratios
- `fixtures/domain_knowledge/02_roofing_materials_warranties.md` — membrane/shingle specs, warranty taxonomy, certified installer programs, red flags catalogue
```

- [ ] **Step 3: Commit**

```bash
git add plugins/roof-replacement-review/skills/roof-technical-review/SKILL.md
git commit -m "docs(roof-review): tech-review writes tech sidecar; allowlist to 2 fixtures"
```

---

## Task 6: Clarify that roof-bid-extract does not require the RFP

**Files:**
- Modify: `plugins/roof-replacement-review/skills/roof-bid-extract/SKILL.md`

- [ ] **Step 1: Replace the Inputs block with an RFP-independent version**

Open `plugins/roof-replacement-review/skills/roof-bid-extract/SKILL.md`.

Find `## Inputs` (around line 17). Replace with:

```markdown
## Inputs

1. **Bid PDF** — the contractor's submission. This is the only input this skill
   needs. It extracts bid facts verbatim from the submission.

**This skill does NOT require the RFP manifest.** Comparison against the RFP
(mandatory-gate evaluation, warranty-tier match, spec compliance) is performed
by `roof-qualification-check` and `roof-technical-review` in the next pipeline
wave. Keeping bid-extract RFP-independent is what lets `/roof-review` dispatch
`roof-rfp-extract` and `roof-bid-extract` in parallel during wave 1.

If you feel you need to check a value against the RFP here, stop — record what
the bid says in `extraction_notes` and defer the comparison to the downstream
skills.
```

- [ ] **Step 2: Commit**

```bash
git add plugins/roof-replacement-review/skills/roof-bid-extract/SKILL.md
git commit -m "docs(roof-review): bid-extract is RFP-independent — authorizes wave-1 parallelism"
```

---

## Task 7: Rewrite /roof-review command for two-wave dispatch

**Files:**
- Modify: `plugins/roof-replacement-review/commands/roof-review.md`

- [ ] **Step 1: Replace steps 1–3 with the two-wave pattern**

Open `plugins/roof-replacement-review/commands/roof-review.md`.

Replace the entire `## Pipeline` section (currently steps 1–5) with:

```markdown
## Pipeline

1. **Wave 1 — extract everything in parallel.** Dispatch `N+1` subagents in a **single message**:
   - **One** subagent invokes the `roof-rfp-extract` skill on the RFP argument. It writes `<rfp-dir>/roof-review-output/manifests/rfp.json`.
   - **For each bid PDF argument**, one subagent invokes the `roof-bid-extract` skill. Each writes `<rfp-dir>/roof-review-output/manifests/bid_<slug>.json`.

   These are RFP-independent (see `skills/roof-bid-extract/SKILL.md` "Inputs") so they legitimately run concurrently. The main thread waits for all wave-1 subagents to return before proceeding.

   Per-bid wave-1 subagent prompt template (substitute `<BID_PATH>`, `<RFP_DIR>`, `<PLUGIN_ROOT>`):

   ```
   You are extracting one roofing bid for the roof-replacement-review pipeline.

   Plugin root: <PLUGIN_ROOT>    (also available as $CLAUDE_PLUGIN_ROOT)
   Bid PDF: <BID_PATH>
   Output directory: <RFP_DIR>/roof-review-output/manifests/

   Run the `roof-bid-extract` skill on this single bid. Write the base bid manifest
   to <RFP_DIR>/roof-review-output/manifests/bid_<slug>.json.

   Do NOT touch rfp.json or any other bid's manifest. Do NOT evaluate mandatory
   gates or sub-scores — that is wave 2's job.

   Return ONLY:
     - Bidder legal name
     - Bid manifest path
     - Base bid (and HST treatment)
     - Declared exclusions count
     - Any extraction_notes items that need owner follow-up
   ```

2. **Wave 2 — review each bid in parallel.** Once wave 1 completes, dispatch `2 × N` subagents in a **single message** (one qual + one tech per bid):
   - Each **qual subagent** invokes `roof-qualification-check` on one bid and writes `bid_<slug>.qual.json`.
   - Each **tech subagent** invokes `roof-technical-review` on the same bid and writes `bid_<slug>.tech.json`.

   Because the two skills write disjoint sidecar files and have disjoint output ownership (gate names, sub-scores, red-flag categories — see `skills/roof-qualification-check/SKILL.md` "Sidecar Output File" and `skills/roof-technical-review/SKILL.md" "Sidecar Output File"), they can run concurrently without conflict.

   Per-bid wave-2 qual subagent prompt template:

   ```
   You are running qualification review for one roofing bid.

   Plugin root: <PLUGIN_ROOT>
   RFP manifest: <RFP_DIR>/roof-review-output/manifests/rfp.json
   Base bid manifest: <RFP_DIR>/roof-review-output/manifests/bid_<slug>.json

   Run the `roof-qualification-check` skill. Write your output ONLY to:
     <RFP_DIR>/roof-review-output/manifests/bid_<slug>.qual.json

   Do NOT modify the base bid manifest or any other file.

   Return ONLY:
     - Bidder legal name
     - Gate pass / fail / needs-clarification counts
     - Sub-scores (experience_references, qualifications_certifications, schedule)
     - Critical qualification issues
   ```

   Per-bid wave-2 tech subagent prompt template:

   ```
   You are running technical review for one roofing bid.

   Plugin root: <PLUGIN_ROOT>
   RFP manifest: <RFP_DIR>/roof-review-output/manifests/rfp.json
   Base bid manifest: <RFP_DIR>/roof-review-output/manifests/bid_<slug>.json

   Run the `roof-technical-review` skill. Write your output ONLY to:
     <RFP_DIR>/roof-review-output/manifests/bid_<slug>.tech.json

   Do NOT modify the base bid manifest or any other file.

   Return ONLY:
     - Bidder legal name
     - Sub-scores (technical_approach, warranty_materials)
     - Critical/high red flag counts
     - Top 3 technical concerns
   ```

   The main thread waits for all `2 × N` subagents to return before proceeding.

3. **Merge manifests.** Run the merge script with both sidecar globs:

```bash
python3 "$CLAUDE_PLUGIN_ROOT/scripts/normalize.py" \
  --rfp "<rfp-output-dir>/manifests/rfp.json" \
  --bids "<rfp-output-dir>/manifests/bid_*.json" \
  --qual-sidecars "<rfp-output-dir>/manifests/bid_*.qual.json" \
  --tech-sidecars "<rfp-output-dir>/manifests/bid_*.tech.json" \
  --out "<rfp-output-dir>/manifests/tender_manifest.json"
```

The `--bids` glob picks up only `bid_<slug>.json` (base manifests); the sidecar globs match the `.qual.json` and `.tech.json` siblings. `normalize.py` will refuse to merge if the two sidecars collide on a gate/score/rationale key — that indicates a skill wrote outside its ownership boundary and must be fixed before scoring.

4. **Score.** Run the scoring engine. If the user passed `config=<path>` in the arguments, append `--config <path>` to override the RFP's weights and price scoring method:

```bash
python3 "$CLAUDE_PLUGIN_ROOT/scripts/score.py" \
  --manifest "<rfp-output-dir>/manifests/tender_manifest.json" \
  [--config <evaluation_config.yaml>]
```

`score.py` runs `reconcile_gates` (gate applicability + cross-bid symmetry) as its first action and refuses to score if a bidder has been failed on a gate the RFP never invoked, or if identical evidence has been treated asymmetrically across bidders. Fix the flagged bid sidecars by re-running the relevant wave-2 subagent on the offending bid(s), then re-run step 3 and step 4.

Example config at `templates/evaluation_config.yaml`. Common uses: occupied-building weighting (raise schedule + technical), BPS procurement (raise price, use `lowest_compliant` method), heritage/complex roof (raise technical).

5. **Render deliverables (deterministic fast path, then optional LLM polish).**

   Run all three renderer scripts **in parallel** — pure Python, no LLM, typically <1s total. Issue all three `Bash` tool calls in a single message so they execute concurrently (they only read the manifest and write disjoint output files, so there is no ordering or race risk):

```bash
python3 "$CLAUDE_PLUGIN_ROOT/scripts/render_matrix.py" \
  --manifest "<rfp-output-dir>/manifests/tender_manifest.json" \
  --out "<rfp-output-dir>/scoring_matrix.md"
```

```bash
python3 "$CLAUDE_PLUGIN_ROOT/scripts/redflags.py" \
  --manifest "<rfp-output-dir>/manifests/tender_manifest.json" \
  --out "<rfp-output-dir>/redflag_report.md"
```

```bash
python3 "$CLAUDE_PLUGIN_ROOT/scripts/render_memo.py" \
  --manifest "<rfp-output-dir>/manifests/tender_manifest.json" \
  --out "<rfp-output-dir>/recommendation_memo.md"
```

   Then invoke the skills **as refinement passes** over the generated files — not from-scratch regeneration. Issue both refinement subagent calls in a **single message** so they run concurrently:
   - `roof-score-matrix` — read `scoring_matrix.md`, refine wording only if the mechanical output reads awkwardly; leave numbers and structure alone.
   - `roof-recommendation-memo` — read `recommendation_memo.md`, polish §1 Recommendation prose and trim/reorder award conditions in §5 for owner tone; keep §3, §4, §6, §7, §8 as-is unless data is wrong.

   Skip the refinement passes entirely if the user asked for a fast/cheap run, or if the Python output already reads cleanly.
```

(Keep the `## Output` and `## Summary` sections at the bottom of the file unchanged.)

- [ ] **Step 2: Commit**

```bash
git add plugins/roof-replacement-review/commands/roof-review.md
git commit -m "feat(roof-review): two-wave parallel dispatch; ~50% wall-clock reduction target"
```

---

## Task 8: End-to-end smoke verification on sample fixtures

**Files:**
- Test: `plugins/roof-replacement-review/tests/test_normalize_sidecar_merge.py` (extend with end-to-end check)

No live LLM call — the smoke test uses synthesized sidecars to prove the Python pipeline from normalize → score → render still works under the new flag shape.

- [ ] **Step 1: Write the end-to-end test**

Append to `plugins/roof-replacement-review/tests/test_normalize_sidecar_merge.py`:

```python
SCORE = PLUGIN_ROOT / "scripts" / "score.py"
RENDER_MATRIX = PLUGIN_ROOT / "scripts" / "render_matrix.py"
RENDER_MEMO = PLUGIN_ROOT / "scripts" / "render_memo.py"
REDFLAGS = PLUGIN_ROOT / "scripts" / "redflags.py"


def test_end_to_end_with_synthetic_sidecars(tmp_path: Path, rfp_manifest: Path) -> None:
    """End-to-end: two base bids + their qual and tech sidecars must flow through
    normalize → score → all three renderers without error."""
    # Base bids
    for bid_id, price in [("alpha", 480000), ("beta", 520000)]:
        _write_json(tmp_path / f"bid_{bid_id}.json", {
            "bidder_id": bid_id,
            "bidder_name": f"{bid_id.title()} Roofing",
            "pricing": {"base_bid_cad": price, "hst_included": False},
            "red_flags": [],
            "extraction_notes": [],
        })
        _write_json(tmp_path / f"bid_{bid_id}.qual.json", {
            "bidder_id": bid_id,
            "mandatory_gates": {
                "wsib_clearance": {"result": "pass", "evidence": "p. 1"},
                "cgl_insurance": {"result": "pass", "evidence": "p. 2"},
            },
            "scores": {
                "experience_references": 60,
                "qualifications_certifications": 55,
                "schedule": 70,
            },
            "scoring_rationale": {},
            "red_flags": [],
        })
        _write_json(tmp_path / f"bid_{bid_id}.tech.json", {
            "bidder_id": bid_id,
            "mandatory_gates": {
                "cover_board": {"result": "pass", "evidence": "p. 10"},
            },
            "scores": {
                "technical_approach": 65,
                "warranty_materials": 70,
            },
            "scoring_rationale": {},
            "red_flags": [],
        })

    # RFP with weights
    _write_json(tmp_path / "rfp.json", {
        "project": {"name": "Smoke Test"},
        "rfp": {
            "mandatory_requirements": {},
            "submission_requirements": [],
            "evaluation_criteria": {
                "weighting": {
                    "price": 45, "technical_approach": 15, "experience_references": 15,
                    "warranty_materials": 10, "schedule": 5, "qualifications_certifications": 10,
                },
                "price_scoring_method": "formula_lowest_ratio",
            },
        },
    })

    manifest = tmp_path / "tender_manifest.json"
    subprocess.run([
        sys.executable, str(NORMALIZE),
        "--rfp", str(tmp_path / "rfp.json"),
        "--bids", str(tmp_path / "bid_*.json"),
        "--qual-sidecars", str(tmp_path / "bid_*.qual.json"),
        "--tech-sidecars", str(tmp_path / "bid_*.tech.json"),
        "--out", str(manifest),
    ], check=True)

    subprocess.run([sys.executable, str(SCORE), "--manifest", str(manifest)], check=True)

    scored = json.loads(manifest.read_text())
    assert scored["comparison"]["recommended_bidder_id"] in {"alpha", "beta"}
    ranked = [b for b in scored["bids"] if b["scores"].get("rank") == 1]
    assert len(ranked) == 1

    for script, out_name in [
        (RENDER_MATRIX, "scoring_matrix.md"),
        (RENDER_MEMO, "recommendation_memo.md"),
        (REDFLAGS, "redflag_report.md"),
    ]:
        out_path = tmp_path / out_name
        subprocess.run([
            sys.executable, str(script),
            "--manifest", str(manifest),
            "--out", str(out_path),
        ], check=True)
        assert out_path.is_file()
        assert out_path.stat().st_size > 0
```

- [ ] **Step 2: Run the test**

Run:
```bash
cd plugins/roof-replacement-review && python3 -m pytest tests/test_normalize_sidecar_merge.py::test_end_to_end_with_synthetic_sidecars -v
```

Expected: PASS. `scripts/score.py` accepts a manifest where gates/scores arrived via sidecar merge (it doesn't care how they got there). All three renderers produce non-empty output.

- [ ] **Step 3: Run the full test suite**

Run:
```bash
cd plugins/roof-replacement-review && python3 -m pytest -q
```

Expected: 30 passed (26 original + 4 new).

- [ ] **Step 4: Commit**

```bash
git add plugins/roof-replacement-review/tests/test_normalize_sidecar_merge.py
git commit -m "test(roof-review): end-to-end smoke test with sidecar-merged manifest"
```

---

## Task 9: Update plugin CHANGELOG

**Files:**
- Modify: `plugins/roof-replacement-review/CHANGELOG.md`

- [ ] **Step 1: Prepend a new release entry**

Read the current CHANGELOG.md, then prepend (above the most recent entry) a new block documenting this change:

```markdown
## [Unreleased]

### Changed
- `/roof-review` now dispatches subagents in two parallel waves instead of three serial steps:
  - **Wave 1:** `roof-rfp-extract` in parallel with N × `roof-bid-extract`. Authorized because `roof-bid-extract` is RFP-independent (extracts bid facts only, defers comparison).
  - **Wave 2:** N × (`roof-qualification-check` ∥ `roof-technical-review`). Each skill writes a disjoint sidecar (`bid_<slug>.qual.json`, `bid_<slug>.tech.json`); they are safe to run concurrently because their output ownership (gate names, sub-scores, red-flag categories) is disjoint by design.
  - Expected wall-clock reduction: ~45–55% on a 5-bid tender.
- `scripts/normalize.py` gains `--qual-sidecars` and `--tech-sidecars` flags and deep-merges sidecar files onto base bid manifests. Collisions on `mandatory_gates`, `scores`, or `scoring_rationale` keys are fatal — they indicate a skill wrote outside its ownership boundary.
- `roof-qualification-check` and `roof-technical-review` SKILL.md files now specify allowlisted fixture reads to reduce per-subagent context load.

### Migration notes
- Legacy base-bid manifests that already carry merged gates/scores still work when `normalize.py` is called without sidecar globs. Fixtures under `fixtures/sample_bids/` are unchanged.
- Any caller that ran `normalize.py` with the old two-flag shape is untouched; the two new flags are optional.
```

- [ ] **Step 2: Commit**

```bash
git add plugins/roof-replacement-review/CHANGELOG.md
git commit -m "docs(roof-review): changelog entry for two-wave parallel dispatch"
```

---

## Verification Checklist

After all tasks are committed, verify:

- [ ] `cd plugins/roof-replacement-review && python3 -m pytest -q` reports all tests passing (30 expected: 26 original + 4 new in `test_normalize_sidecar_merge.py`).
- [ ] `scripts/normalize.py --help` lists the two new flags (`--qual-sidecars`, `--tech-sidecars`).
- [ ] `commands/roof-review.md` contains the string "Wave 1" and "Wave 2".
- [ ] `skills/roof-qualification-check/SKILL.md` contains the string "bid_<slug>.qual.json".
- [ ] `skills/roof-technical-review/SKILL.md` contains the string "bid_<slug>.tech.json".
- [ ] `skills/roof-bid-extract/SKILL.md` contains the string "This skill does NOT require the RFP manifest".
- [ ] On a real 5-bid tender run, total wall-clock from `/roof-review` invocation to `recommendation_memo.md` write is materially shorter than baseline (target ≥40% reduction). Measure with `time` on both runs.

---

## Out of scope for this plan

Deliberately deferred, captured here so they don't get forgotten:

- Fusing `normalize.py` into `score.py` (saves ~100ms of interpreter startup — not worth the refactor risk right now).
- A `render_all.py` that unifies the three renderer scripts (minor savings; the three are already parallel-dispatched).
- Moving `reconcile_gates` to run immediately after wave 2 instead of at the start of `score.py` (shortens the failure-detection loop but doesn't change happy-path wall-clock).
- Inlining domain-fixture "hot anchors" into the SKILL.md files themselves (token savings per subagent, but requires careful audit of which fixture sections are the actual decision anchors).

If any of these become bottlenecks on larger tenders (>10 bids), revisit in a follow-up plan.
