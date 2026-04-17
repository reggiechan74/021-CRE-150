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
