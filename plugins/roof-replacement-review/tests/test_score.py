"""Tests for scripts/score.py against the Mississauga fixture."""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest


PLUGIN_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = PLUGIN_ROOT / "scripts" / "score.py"
NORMALIZE = PLUGIN_ROOT / "scripts" / "normalize.py"
FIXTURES = PLUGIN_ROOT / "fixtures"


@pytest.fixture
def built_manifest(tmp_path: Path) -> Path:
    """Build a merged tender manifest from the sample RFP and bids."""
    out = tmp_path / "tender_manifest.json"
    subprocess.run(
        [
            sys.executable,
            str(NORMALIZE),
            "--rfp", str(FIXTURES / "sample_rfp" / "rfp.json"),
            "--bids", str(FIXTURES / "sample_bids" / "bid_*.json"),
            "--out", str(out),
        ],
        check=True,
    )
    return out


def test_normalize_produces_three_bids(built_manifest: Path) -> None:
    data = json.loads(built_manifest.read_text())
    assert data["manifest_version"] == "1.0.0"
    assert len(data["bids"]) == 3
    bidder_ids = {b["bidder_id"] for b in data["bids"]}
    assert bidder_ids == {"apex", "meridian", "keystone"}


def test_score_ranks_apex_first(built_manifest: Path) -> None:
    subprocess.run([sys.executable, str(SCRIPT), "--manifest", str(built_manifest)], check=True)
    data = json.loads(built_manifest.read_text())

    bids = {b["bidder_id"]: b for b in data["bids"]}
    # Apex has strong sub-scores and a mid-range price; should beat Keystone on total
    assert bids["apex"]["scores"]["rank"] == 1
    assert bids["keystone"]["scores"]["rank"] == 2
    # Meridian fails mandatory gates (CGL, bonding, AOI, site visit, years, references) — excluded
    assert bids["meridian"]["scores"]["rank"] is None
    assert bids["meridian"]["scores"]["compliant"] is False


def test_price_score_formula(built_manifest: Path) -> None:
    subprocess.run([sys.executable, str(SCRIPT), "--manifest", str(built_manifest)], check=True)
    data = json.loads(built_manifest.read_text())
    bids = {b["bidder_id"]: b for b in data["bids"]}

    # Meridian excluded; price scores computed only across compliant bids.
    # Lowest compliant price is Apex $485,000 → score 100; Keystone $498,500.
    assert bids["apex"]["scores"]["price"] == 100.0
    expected_keystone = round(100.0 * 485000 / 498500, 2)
    assert bids["keystone"]["scores"]["price"] == expected_keystone


def test_weighted_total_math(built_manifest: Path) -> None:
    subprocess.run([sys.executable, str(SCRIPT), "--manifest", str(built_manifest)], check=True)
    data = json.loads(built_manifest.read_text())
    weights = data["rfp"]["evaluation_criteria"]["weighting"]
    bids = {b["bidder_id"]: b for b in data["bids"]}

    apex = bids["apex"]["scores"]
    # Recompute manually from sub-scores and compare
    manual = (
        apex["price"] * weights["price"]
        + apex["technical_approach"] * weights["technical_approach"]
        + apex["experience_references"] * weights["experience_references"]
        + apex["warranty_materials"] * weights["warranty_materials"]
        + apex["schedule"] * weights["schedule"]
        + apex["qualifications_certifications"] * weights["qualifications_certifications"]
    ) / 100.0
    assert abs(apex["weighted_total"] - round(manual, 2)) < 0.05


def test_comparison_populated(built_manifest: Path) -> None:
    subprocess.run([sys.executable, str(SCRIPT), "--manifest", str(built_manifest)], check=True)
    data = json.loads(built_manifest.read_text())
    comp = data["comparison"]
    assert comp["compliant_bidders_count"] == 2
    # Compliant-only range: Apex $485k (low) to Keystone $498.5k (high)
    assert comp["price_low_cad"] == 485000
    assert comp["price_high_cad"] == 498500
    # All-bids range includes non-compliant Meridian at $412k
    assert comp["all_bids_price_low_cad"] == 412000
    assert comp["all_bids_price_high_cad"] == 498500
    assert comp["recommended_bidder_id"] == "apex"
    # Compliant spread is ~2.8%, well under 15% — no spread warning
    assert comp["price_spread_percent"] < 5


def test_redflag_report_renders(built_manifest: Path, tmp_path: Path) -> None:
    subprocess.run([sys.executable, str(SCRIPT), "--manifest", str(built_manifest)], check=True)
    report = tmp_path / "redflag_report.md"
    subprocess.run(
        [
            sys.executable,
            str(PLUGIN_ROOT / "scripts" / "redflags.py"),
            "--manifest", str(built_manifest),
            "--out", str(report),
        ],
        check=True,
    )
    content = report.read_text()
    assert "Roof Replacement Tender — Red Flag Report" in content
    assert "Meridian Roofing Contractors" in content
    assert "NON-COMPLIANT" in content
    assert "Apex Commercial Roofing" in content
    assert "No red flags identified" in content  # Apex has zero red flags in fixture
