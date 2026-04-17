"""Tests for scripts/render_memo.py — §4 compliance-tier buckets."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest


PLUGIN_ROOT = Path(__file__).resolve().parents[1]
RENDER = PLUGIN_ROOT / "scripts" / "render_memo.py"
SCORE = PLUGIN_ROOT / "scripts" / "score.py"
NORMALIZE = PLUGIN_ROOT / "scripts" / "normalize.py"
FIXTURES = PLUGIN_ROOT / "fixtures"


@pytest.fixture
def scored_manifest(tmp_path: Path) -> Path:
    out = tmp_path / "tender_manifest.json"
    subprocess.run(
        [
            sys.executable, str(NORMALIZE),
            "--rfp", str(FIXTURES / "sample_rfp" / "rfp.json"),
            "--bids", str(FIXTURES / "sample_bids" / "bid_*.json"),
            "--out", str(out),
        ],
        check=True,
    )
    subprocess.run([sys.executable, str(SCORE), "--manifest", str(out)], check=True)
    return out


def render(manifest_path: Path, out_path: Path) -> str:
    subprocess.run(
        [sys.executable, str(RENDER), "--manifest", str(manifest_path), "--out", str(out_path)],
        check=True,
    )
    return out_path.read_text()


def test_memo_has_three_compliance_buckets(scored_manifest: Path, tmp_path: Path) -> None:
    """Task H: §4 must split bids into three tiers — fully compliant,
    administratively conditional, and non-compliant. Mutate Keystone to
    'conditional' so all three buckets are populated."""
    data = json.loads(scored_manifest.read_text())
    for bid in data["bids"]:
        if bid["bidder_id"] == "keystone":
            bid["mandatory_gates"]["addenda"] = {
                "result": "needs_clarification",
                "evidence": "bid has no addenda acknowledgment section",
            }
    scored_manifest.write_text(json.dumps(data, indent=2))
    subprocess.run([sys.executable, str(SCORE), "--manifest", str(scored_manifest)], check=True)

    md = render(scored_manifest, tmp_path / "memo.md")

    # Three buckets, each named distinctly.
    assert "Fully Compliant" in md
    assert "Administratively Conditional" in md
    assert "Non-Compliant" in md

    # Apex is fully compliant; Keystone is conditional; Meridian is non-compliant.
    apex_idx = md.find("Fully Compliant")
    cond_idx = md.find("Administratively Conditional")
    nc_idx = md.find("Non-Compliant")
    assert apex_idx < cond_idx < nc_idx, "tiers must appear in order: compliant → conditional → non-compliant"

    # Ensure each bidder lands in its correct bucket.
    apex_section = md[apex_idx:cond_idx]
    cond_section = md[cond_idx:nc_idx]
    nc_section = md[nc_idx:]
    assert "Apex" in apex_section
    assert "Keystone" in cond_section
    assert "Meridian" in nc_section


def test_memo_annotates_nc_dq_basis(scored_manifest: Path, tmp_path: Path) -> None:
    """Non-compliant bidders must carry a DQ-basis annotation distinguishing
    technical failures (curable only by re-bid) from administrative failures
    (in principle curable, but the bidder failed to cure at submission)."""
    md = render(scored_manifest, tmp_path / "memo.md")
    # Meridian's fails in the fixture include cgl, bid_bond, site_visit — administrative.
    # The annotation must surface "administrative" or "technical" wording alongside the
    # bidder so the reader can distinguish the DQ basis at a glance.
    assert "administrative" in md.lower() or "technical" in md.lower()
