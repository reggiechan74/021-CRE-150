"""Statement rendering smoke tests."""

from __future__ import annotations


def test_statement_renderer_outputs_expected_files(tmp_path, allocated_matheson_manifest):
    from scripts.statement import render_outputs

    outputs = render_outputs(allocated_matheson_manifest, tmp_path)
    statement_files = sorted(outputs["tenant_statements"].glob("*.md"))
    assert len(statement_files) == 9
    assert outputs["workpaper"].exists()
    assert outputs["audit_log"].exists()
    assert outputs["narrative_commentary"].exists()
    assert "$28,400.00" in outputs["audit_log"].read_text(encoding="utf-8")


def test_tenant_statement_includes_summary_and_citations(tmp_path, allocated_matheson_manifest):
    from scripts.statement import render_outputs

    outputs = render_outputs(allocated_matheson_manifest, tmp_path)
    # Pick a tenant with a CAM cap so we exercise the cap section.
    cap_statement = (outputs["tenant_statements"] / "unit_101.md").read_text(encoding="utf-8")
    assert "## Summary" in cap_statement
    assert "## Citation Trail" in cap_statement
    assert "## CAM Cap Review" in cap_statement

    # Pick a tenant with modified-gross exclusions.
    mg_statement = (outputs["tenant_statements"] / "unit_104.md").read_text(encoding="utf-8")
    assert "## Lease-Specific Exclusions" in mg_statement
    assert "utilities" in mg_statement
    assert "repairs_maintenance" in mg_statement
