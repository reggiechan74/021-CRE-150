"""Classification-stage tests."""

from __future__ import annotations

import json
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


def test_decision_record_roundtrip(raw_matheson_manifest):
    from scripts.classify_validator import DecisionRecord, generate_default_decisions
    from scripts.validation import ManifestJSONEncoder

    decisions = generate_default_decisions(raw_matheson_manifest)
    payload = json.loads(json.dumps(decisions, cls=ManifestJSONEncoder))
    rebuilt = [DecisionRecord.from_dict(item) for item in payload]

    assert len(rebuilt) == len(decisions)
    for original, restored in zip(decisions, rebuilt):
        assert original.line_id == restored.line_id
        assert original.classification.recoverable == restored.classification.recoverable
        assert original.classification.reason == restored.classification.reason
        assert original.classification.recoverable_amount == restored.classification.recoverable_amount
