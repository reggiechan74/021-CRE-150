"""Classification-stage tests."""

from __future__ import annotations

from decimal import Decimal


def test_generated_decisions_cover_every_gl_line(raw_matheson_manifest):
    from scripts.classify_validator import generate_default_decisions

    decisions = generate_default_decisions(raw_matheson_manifest)
    assert len(decisions) == len(raw_matheson_manifest.gl_lines)


def test_duplicate_invoice_flagged(classified_matheson_manifest):
    duplicate = next(
        line
        for line in classified_matheson_manifest.gl_lines
        if line.invoice_ref == "GA-2025-12-4471" and "re-entered" in line.memo
    )
    assert duplicate.classification.reason == "duplicate_invoice"
    assert duplicate.classification.recoverable is False


def test_turnover_deep_clean_flagged(classified_matheson_manifest):
    deep_clean = next(
        line
        for line in classified_matheson_manifest.gl_lines
        if line.invoice_ref == "CPS-SPECIAL-2025-1018"
    )
    assert deep_clean.classification.reason == "tenant_turnover_extraordinary_charge"
    assert deep_clean.classification.recoverable is False


def test_management_fee_reduced_to_egi_basis(classified_matheson_manifest):
    recoverable_total = sum(
        line.classification.recoverable_amount
        for line in classified_matheson_manifest.gl_lines
        if line.category_raw == "Management Fee"
    )
    assert recoverable_total == Decimal("110800.00")
