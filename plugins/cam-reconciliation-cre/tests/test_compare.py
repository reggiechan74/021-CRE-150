"""Anthropic comparison tests."""

from __future__ import annotations

from decimal import Decimal


def test_compare_report_contains_payoff(matheson_dir, allocated_matheson_manifest):
    from scripts.compare import compare_against_anthropic

    anthropic_text = (matheson_dir / "anthropic_output.txt").read_text(encoding="utf-8")
    report = compare_against_anthropic(allocated_matheson_manifest, anthropic_text)
    assert "$28,400.00" in report
    assert "$1,178,692.00" in report
    assert "$1,150,292.00" in report


def test_extract_anthropic_totals_handles_narrative_benchmark_format():
    from scripts.compare import extract_anthropic_totals

    anthropic_text = """
### Corrected FY2025 recoverable operating expense total

Raw GL total .................................. $1,172,170.00
Less: Turnover restoration (TURN-re-1018) .....    (15,400.00)
Less: Duplicate Dec gas (GA-2025-re-4471) .....     (8,400.00)
Less: Mgmt fee overage above 4% EGI cap .......     (4,700.00)
                                                 --------------
**Corrected recoverable OpEx total ............  $1,143,670.00**
"""
    parsed = extract_anthropic_totals(anthropic_text)
    assert parsed["reported_total"] == 1143670


def test_extract_anthropic_totals_prefers_immediate_total_under_header():
    from scripts.compare import extract_anthropic_totals

    anthropic_text = """
Corrected FY2025 recoverable operating expense total:

    $946,854.69

    If another assumption were used, the corrected recoverable becomes $945,454.69.
"""
    parsed = extract_anthropic_totals(anthropic_text)
    assert parsed["reported_total"] == Decimal("946854.69")


def test_extract_anthropic_totals_uses_equals_line_when_first_line_is_raw():
    from scripts.compare import extract_anthropic_totals

    anthropic_text = """
B.3 Corrected FY2025 recoverable operating expense total
--------------------------------------------------------
$971,418.00 (raw)
−  $3,600.00 (duplicate)
−  $3,900.00 (management fee excess)
= **$963,918.00**
"""
    parsed = extract_anthropic_totals(anthropic_text)
    assert parsed["reported_total"] == 963918
