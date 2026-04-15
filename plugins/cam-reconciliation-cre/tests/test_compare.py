"""Anthropic comparison tests."""

from __future__ import annotations


def test_compare_report_contains_payoff(matheson_dir, allocated_matheson_manifest):
    from scripts.compare import compare_against_anthropic

    anthropic_text = (matheson_dir / "anthropic_output.txt").read_text(encoding="utf-8")
    report = compare_against_anthropic(allocated_matheson_manifest, anthropic_text)
    assert "$28,400.00" in report
    assert "$1,178,692.00" in report
    assert "$1,150,292.00" in report
