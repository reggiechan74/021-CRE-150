"""Statement rendering smoke tests."""

from __future__ import annotations


def test_statement_renderer_outputs_expected_files(tmp_path, allocated_matheson_manifest):
    from scripts.statement import render_outputs

    outputs = render_outputs(allocated_matheson_manifest, tmp_path)
    statement_files = sorted(outputs["tenant_statements"].glob("*.pdf"))
    assert len(statement_files) == 9
    assert outputs["workpaper"].exists()
    assert outputs["audit_log"].exists()
    assert outputs["narrative_commentary"].exists()
    assert "$28,400.00" in outputs["audit_log"].read_text(encoding="utf-8")
