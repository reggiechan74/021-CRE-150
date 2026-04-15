"""Stage 2: validate or deterministically generate recoverability decisions."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from decimal import Decimal, ROUND_FLOOR
import sys
from pathlib import Path

from pydantic import BaseModel

PLUGIN_ROOT = Path(__file__).resolve().parent.parent
if str(PLUGIN_ROOT) not in sys.path:
    sys.path.insert(0, str(PLUGIN_ROOT))

from scripts.manifest import (
    Classification,
    MANAGEMENT_FEE_BASIS,
    MANAGEMENT_FEE_NONRECOVERABLE,
    Manifest,
    PoolName,
    STANDARD_FORM_DUPLICATE,
    STANDARD_FORM_OPERATING,
    STANDARD_FORM_TURNOVER,
    canonical_category,
    money,
)


class DecisionRecord(BaseModel):
    line_id: str
    classification: Classification


def split_amount(total: Decimal, weighted_items: list[tuple[str, Decimal]]) -> dict[str, Decimal]:
    if not weighted_items:
        return {}
    total_weight = sum(weight for _, weight in weighted_items)
    if total_weight == 0:
        return {key: Decimal("0.00") for key, _ in weighted_items}

    total_cents = int((money(total) * 100).to_integral_value())
    raw_cents = {
        key: Decimal(total_cents) * weight / total_weight for key, weight in weighted_items
    }
    floor_cents = {
        key: int(value.to_integral_value(rounding=ROUND_FLOOR))
        for key, value in raw_cents.items()
    }
    remaining = total_cents - sum(floor_cents.values())
    remainders = sorted(
        ((raw_cents[key] - floor_cents[key], key) for key in raw_cents),
        key=lambda item: (-item[0], item[1]),
    )
    for _, key in remainders[:remaining]:
        floor_cents[key] += 1
    return {key: Decimal(cents) / Decimal("100") for key, cents in floor_cents.items()}


def _pool_name(raw_pool: str) -> PoolName:
    return PoolName(raw_pool.strip().lower())


def _duplicate_map(manifest: Manifest) -> dict[str, str]:
    seen: dict[tuple[str, str, Decimal], str] = {}
    duplicates: dict[str, str] = {}
    for line in manifest.gl_lines:
        key = (line.vendor, line.invoice_ref, line.amount)
        if key in seen:
            duplicates[line.line_id] = seen[key]
        else:
            seen[key] = line.line_id
    return duplicates


def _management_fee_splits(manifest: Manifest) -> dict[str, Decimal]:
    management_lines = [line for line in manifest.gl_lines if line.category_raw == "Management Fee"]
    if not management_lines:
        return {}
    gpi = manifest.property.gross_potential_income
    egi = manifest.property.effective_gross_income
    if not gpi or not egi:
        return {line.line_id: line.amount for line in management_lines}
    target_total = money(sum(line.amount for line in management_lines) * egi / gpi)
    weighted_items = [(line.line_id, line.amount) for line in management_lines]
    return split_amount(target_total, weighted_items)


def generate_default_decisions(manifest: Manifest) -> list[DecisionRecord]:
    duplicates = _duplicate_map(manifest)
    management_splits = _management_fee_splits(manifest)
    decisions: list[DecisionRecord] = []

    for line in manifest.gl_lines:
        normalized_category = canonical_category(line.category_raw)
        pool = _pool_name(line.pool_hint)

        if line.line_id in duplicates:
            decisions.append(
                DecisionRecord(
                    line_id=line.line_id,
                    classification=Classification(
                        recoverable=False,
                        reason="duplicate_invoice",
                        lease_citation=STANDARD_FORM_DUPLICATE,
                        pool=pool,
                        pool_specific=(pool != PoolName.SHARED),
                        matched_against=duplicates[line.line_id],
                        normalized_category=normalized_category,
                    ),
                )
            )
            continue

        if "move-out" in line.memo.lower() or "turnover" in line.memo.lower():
            decisions.append(
                DecisionRecord(
                    line_id=line.line_id,
                    classification=Classification(
                        recoverable=False,
                        reason="tenant_turnover_extraordinary_charge",
                        lease_citation=STANDARD_FORM_TURNOVER,
                        pool=pool,
                        pool_specific=(pool != PoolName.SHARED),
                        normalized_category=normalized_category,
                    ),
                )
            )
            continue

        if line.category_raw == "Management Fee":
            decisions.append(
                DecisionRecord(
                    line_id=line.line_id,
                    classification=Classification(
                        recoverable=True,
                        reason="management_fee_egi_adjusted",
                        lease_citation=MANAGEMENT_FEE_BASIS,
                        pool=pool,
                        pool_specific=False,
                        normalized_category=normalized_category,
                        recoverable_amount=management_splits[line.line_id],
                    ),
                )
            )
            continue

        decisions.append(
            DecisionRecord(
                line_id=line.line_id,
                classification=Classification(
                    recoverable=True,
                    reason="standard_recoverable_operating_expense",
                    lease_citation=STANDARD_FORM_OPERATING,
                    pool=pool,
                    pool_specific=(pool != PoolName.SHARED),
                    normalized_category=normalized_category,
                    recoverable_amount=line.amount,
                ),
            )
        )

    return decisions


def load_decisions(path: Path) -> list[DecisionRecord]:
    data = json.loads(path.read_text(encoding="utf-8"))
    return [DecisionRecord.model_validate(item) for item in data]


def apply_decisions(manifest: Manifest, decisions: list[DecisionRecord]) -> Manifest:
    decision_map = {item.line_id: item.classification for item in decisions}
    if len(decision_map) != len(manifest.gl_lines):
        missing = {line.line_id for line in manifest.gl_lines} - set(decision_map)
        extra = set(decision_map) - {line.line_id for line in manifest.gl_lines}
        raise ValueError(f"Decision file mismatch. Missing={sorted(missing)} extra={sorted(extra)}")

    updated_lines = []
    for line in manifest.gl_lines:
        updated_lines.append(line.model_copy(update={"classification": decision_map[line.line_id]}))
    return manifest.model_copy(update={"gl_lines": updated_lines})


def decisions_output_path(raw_manifest_path: Path) -> Path:
    return raw_manifest_path.parent / "classification_decisions.json"


def classified_output_path(raw_manifest_path: Path) -> Path:
    return raw_manifest_path.parent / "classified_manifest.json"


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate or generate classification decisions for a raw manifest.")
    parser.add_argument("--manifest", type=Path, required=True, help="Path to raw_manifest.json.")
    parser.add_argument("--output", type=Path, help="Path to classified_manifest.json.")
    parser.add_argument("--decisions", type=Path, help="Optional JSON decisions file to validate and apply.")
    parser.add_argument("--decisions-output", type=Path, help="Write generated or validated decisions here.")
    args = parser.parse_args()

    manifest = Manifest.load(args.manifest)
    decisions = load_decisions(args.decisions) if args.decisions else generate_default_decisions(manifest)
    classified = apply_decisions(manifest, decisions)

    decisions_path = args.decisions_output or decisions_output_path(args.manifest)
    decisions_path.parent.mkdir(parents=True, exist_ok=True)
    decisions_payload = [item.model_dump(mode="json") for item in decisions]
    decisions_path.write_text(json.dumps(decisions_payload, indent=2, default=str), encoding="utf-8")

    output = args.output or classified_output_path(args.manifest)
    output.parent.mkdir(parents=True, exist_ok=True)
    classified.save(output)

    mgmt_total = money(
        sum(
            line.classification.recoverable_amount or Decimal("0")
            for line in classified.gl_lines
            if line.category_raw == "Management Fee"
        )
    )
    print(
        json.dumps(
            {
                "classified_manifest": str(output),
                "decisions": str(decisions_path),
                "management_fee_recoverable_total": str(mgmt_total),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
