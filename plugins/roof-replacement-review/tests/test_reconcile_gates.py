"""Tests for scripts/reconcile_gates.py — uniform gate treatment across bidders."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest


PLUGIN_ROOT = Path(__file__).resolve().parents[1]
RECONCILE = PLUGIN_ROOT / "scripts" / "reconcile_gates.py"
NORMALIZE = PLUGIN_ROOT / "scripts" / "normalize.py"
FIXTURES = PLUGIN_ROOT / "fixtures"


@pytest.fixture
def built_manifest(tmp_path: Path) -> Path:
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


def test_uniform_gates_pass(built_manifest: Path) -> None:
    """Fixture bids already apply gates uniformly — reconciliation passes clean."""
    result = subprocess.run(
        [sys.executable, str(RECONCILE), "--manifest", str(built_manifest)],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr


def test_asymmetric_gate_treatment_errors(built_manifest: Path) -> None:
    """Task C: If gate X is 'fail' for bidder A but 'needs_clarification' for
    bidder B, that is the exact Heritage-vs-Summit inconsistency observed in
    the Exercise 6 roof review output — reconciliation must flag it."""
    data = json.loads(built_manifest.read_text())
    for bid in data["bids"]:
        if bid["bidder_id"] == "apex":
            # Apex currently passes bid_bond; demote to needs_clarification.
            bid["mandatory_gates"]["bid_bond"] = {
                "result": "needs_clarification",
                "evidence": "bond attachment unclear",
            }
    built_manifest.write_text(json.dumps(data, indent=2))

    result = subprocess.run(
        [sys.executable, str(RECONCILE), "--manifest", str(built_manifest)],
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0, "asymmetric gate result should fail reconciliation"
    assert "bid_bond" in result.stderr
    # Meridian has bid_bond=fail in the fixture; we changed Apex to needs_clarification.
    assert "meridian" in result.stderr.lower()
    assert "apex" in result.stderr.lower()


def test_inapplicable_gate_failure_errors(built_manifest: Path) -> None:
    """Tasks A+C: if a bidder is failed on a gate the RFP does not invoke,
    reconciliation flags it. Fixture RFP silent on bid_bond — so a bid_bond
    fail is illegitimate regardless of uniform treatment."""
    data = json.loads(built_manifest.read_text())
    # Strip both bid_bond_percent and any submission_requirements mention so the
    # gate is demonstrably inapplicable.
    data["rfp"]["mandatory_requirements"].pop("bid_bond_percent", None)
    data["rfp"]["submission_requirements"] = ["Form of Tender signed in ink"]
    # Force every bidder's bid_bond gate to 'fail' so asymmetry isn't the signal.
    for bid in data["bids"]:
        bid["mandatory_gates"]["bid_bond"] = {
            "result": "fail",
            "evidence": "bond not attached",
        }
    built_manifest.write_text(json.dumps(data, indent=2))

    result = subprocess.run(
        [sys.executable, str(RECONCILE), "--manifest", str(built_manifest)],
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
    assert "bid_bond" in result.stderr
    assert "not applicable" in result.stderr.lower() or "inapplicable" in result.stderr.lower()


def test_reconcile_writes_nothing(built_manifest: Path) -> None:
    """Reconciliation is a check, not a mutator — manifest bytes unchanged."""
    before = built_manifest.read_bytes()
    subprocess.run(
        [sys.executable, str(RECONCILE), "--manifest", str(built_manifest)],
        check=True,
    )
    after = built_manifest.read_bytes()
    assert before == after
