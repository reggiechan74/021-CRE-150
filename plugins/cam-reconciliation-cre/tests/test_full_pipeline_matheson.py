"""Full Matheson pipeline regression test."""

from __future__ import annotations

import json
from pathlib import Path

from scripts.manifest import Manifest
from scripts.validation import ManifestJSONEncoder


def _as_json(manifest: Manifest) -> dict:
    return json.loads(json.dumps(manifest, cls=ManifestJSONEncoder))


def test_full_pipeline_matches_expected_fixture(allocated_matheson_manifest, fixtures_dir: Path):
    expected_path = fixtures_dir / "matheson" / "expected_manifest.json"
    expected = Manifest.load(expected_path)
    assert _as_json(allocated_matheson_manifest) == _as_json(expected)
