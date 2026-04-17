"""Tests for scripts/render_matrix.py — weighting source, compliance tiers."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest


PLUGIN_ROOT = Path(__file__).resolve().parents[1]
RENDER = PLUGIN_ROOT / "scripts" / "render_matrix.py"
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


def test_weighting_source_shown_rfp(scored_manifest: Path, tmp_path: Path) -> None:
    """Task G: matrix must state the source of weights — RFP manifest vs config override."""
    md = render(scored_manifest, tmp_path / "matrix.md")
    assert "Weighting source:" in md
    assert "RFP manifest" in md or "rfp_manifest" in md


def test_weighting_source_warns_on_override(scored_manifest: Path, tmp_path: Path) -> None:
    """When evaluation_config.yaml overrides the RFP weights, the matrix must surface
    a visible warning so evaluators know the rubric changed."""
    config = tmp_path / "eval.yaml"
    config.write_text(
        """
weighting:
  price: 60
  technical_approach: 10
  experience_references: 10
  warranty_materials: 10
  schedule: 5
  qualifications_certifications: 5
price_scoring_method: lowest_compliant
""".strip(),
        encoding="utf-8",
    )
    subprocess.run(
        [sys.executable, str(SCORE), "--manifest", str(scored_manifest), "--config", str(config)],
        check=True,
    )
    md = render(scored_manifest, tmp_path / "matrix.md")
    assert "config_override" in md or "Config override" in md
    # Must be visibly called out — not buried in a footnote.
    assert "⚠️" in md or "WARNING" in md.upper()
    # Should cite both changed dimensions so the evaluator can audit.
    assert "weights" in md.lower()
