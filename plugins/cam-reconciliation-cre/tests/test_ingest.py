"""Ingest-stage tests against the Matheson fixture set."""

from __future__ import annotations

from decimal import Decimal


def test_build_manifest_loads_matheson_fixture(raw_matheson_manifest):
    assert raw_matheson_manifest.property.name == "Matheson Gateway Centre"
    assert raw_matheson_manifest.fiscal_year == 2025
    assert len(raw_matheson_manifest.gl_lines) == 173
    assert len(raw_matheson_manifest.leases) == 10
    assert raw_matheson_manifest.budget["realty_tax"] == Decimal("420000")
    assert raw_matheson_manifest.budget["management_fee"] == Decimal("108000")


def test_gl_line_ids_are_stable(raw_matheson_manifest):
    assert raw_matheson_manifest.gl_lines[0].line_id == "gl_0001"
    assert raw_matheson_manifest.gl_lines[-1].line_id == "gl_0173"
