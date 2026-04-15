"""Full Matheson pipeline regression test."""

from __future__ import annotations

from pathlib import Path

from scripts.manifest import Manifest


def test_full_pipeline_matches_expected_fixture(allocated_matheson_manifest, fixtures_dir: Path):
    expected_path = fixtures_dir / "matheson" / "expected_manifest.json"
    expected = Manifest.load(expected_path)
    assert allocated_matheson_manifest.model_dump(mode="json") == expected.model_dump(mode="json")
