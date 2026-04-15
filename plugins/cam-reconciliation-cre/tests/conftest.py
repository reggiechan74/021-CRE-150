"""Shared pytest fixtures for cam-reconciliation-cre."""

from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path

import pytest

PLUGIN_ROOT = Path(__file__).resolve().parent.parent
if str(PLUGIN_ROOT) not in sys.path:
    sys.path.insert(0, str(PLUGIN_ROOT))

from scripts.allocate import allocate_manifest
from scripts.classify_validator import apply_decisions, generate_default_decisions
from scripts.ingest import build_manifest


@pytest.fixture
def plugin_root() -> Path:
    return PLUGIN_ROOT


@pytest.fixture
def fixtures_dir(plugin_root: Path) -> Path:
    return plugin_root / "fixtures"


@pytest.fixture
def matheson_dir(fixtures_dir: Path) -> Path:
    return fixtures_dir / "matheson"


@pytest.fixture
def raw_matheson_manifest(matheson_dir: Path):
    return build_manifest(
        property_dir=matheson_dir,
        plugin_version="0.1.0",
        fiscal_year=2025,
        run_timestamp=datetime(2026, 4, 15, 10, 50, 0),
        operator="pytest",
    )


@pytest.fixture
def classified_matheson_manifest(raw_matheson_manifest):
    decisions = generate_default_decisions(raw_matheson_manifest)
    return apply_decisions(raw_matheson_manifest, decisions)


@pytest.fixture
def allocated_matheson_manifest(classified_matheson_manifest):
    return allocate_manifest(classified_matheson_manifest)
