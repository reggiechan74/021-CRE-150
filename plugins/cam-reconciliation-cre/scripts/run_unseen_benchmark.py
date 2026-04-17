"""Run cam-reconciliation-cre across the unseen benchmark suite."""

from __future__ import annotations

import json
import sys
from pathlib import Path

PLUGIN_ROOT = Path(__file__).resolve().parent.parent
if str(PLUGIN_ROOT) not in sys.path:
    sys.path.insert(0, str(PLUGIN_ROOT))

from scripts.allocate import allocate_manifest
from scripts.classify_validator import apply_decisions, generate_default_decisions
from scripts.ingest import build_manifest
from scripts.manifest import money
from scripts.validation import ManifestJSONEncoder


SUITE_ROOT = PLUGIN_ROOT / "benchmarks" / "unseen_cam_suite"
CASES_ROOT = SUITE_ROOT / "cases"
GOLD_ROOT = SUITE_ROOT / "gold"
OURS_ROOT = SUITE_ROOT / "results" / "ours"


def run_case(case_dir: Path) -> dict[str, object]:
    manifest = build_manifest(case_dir, plugin_version="0.1.0-benchmark", fiscal_year=2025)
    classified = apply_decisions(manifest, generate_default_decisions(manifest))
    allocated = allocate_manifest(classified)

    property_level_recoverable_total = money(
        sum(
            line.classification.recoverable_amount or 0
            for line in allocated.gl_lines
            if line.classification and line.classification.recoverable
        )
    )
    direct_bill_total = money(allocated.direct_billed_total)
    pooled_cam_total_after_direct_bills = money(property_level_recoverable_total - direct_bill_total)
    tenant_charges = [
        {
            "tenant_id": charge.tenant_id,
            "final_charge": str(money(charge.final_charge)),
        }
        for charge in allocated.tenant_charges
    ]
    summary = {
        "case_id": case_dir.name,
        "property_level_recoverable_total": str(property_level_recoverable_total),
        "corrected_recoverable_total": str(property_level_recoverable_total),
        "direct_bill_total": str(direct_bill_total),
        "pooled_cam_total_after_direct_bills": str(pooled_cam_total_after_direct_bills),
        "landlord_absorbed_total": str(money(allocated.landlord_absorbed_total)),
        "tenant_charges": tenant_charges,
    }
    output_dir = OURS_ROOT / case_dir.name
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "allocated_manifest.json").write_text(
        json.dumps(allocated, cls=ManifestJSONEncoder, indent=2) + "\n",
        encoding="utf-8",
    )
    (output_dir / "submission.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    return summary


def main() -> None:
    cases = sorted(path for path in CASES_ROOT.iterdir() if path.is_dir())
    rows: list[dict[str, object]] = []
    for case_dir in cases:
        summary = run_case(case_dir)
        gold = json.loads((GOLD_ROOT / f"{case_dir.name}.json").read_text(encoding="utf-8"))
        gold_property_total = str(gold.get("property_level_recoverable_total", gold["corrected_recoverable_total"]))
        gold_pooled_total = str(
            gold.get(
                "pooled_cam_total_after_direct_bills",
                money(money(gold_property_total) - money(gold.get("direct_bill_total", "0.00"))),
            )
        )
        summary["gold_property_level_recoverable_total"] = gold_property_total
        summary["gold_pooled_cam_total_after_direct_bills"] = gold_pooled_total
        summary["property_total_match"] = summary["property_level_recoverable_total"] == gold_property_total
        summary["pooled_cam_total_match"] = summary["pooled_cam_total_after_direct_bills"] == gold_pooled_total
        rows.append(summary)

    aggregate = {
        "cases_run": len(rows),
        "property_total_exact_matches": sum(1 for row in rows if row["property_total_match"]),
        "pooled_cam_total_exact_matches": sum(1 for row in rows if row["pooled_cam_total_match"]),
        "results_dir": str(OURS_ROOT),
        "cases": rows,
    }
    OURS_ROOT.mkdir(parents=True, exist_ok=True)
    (OURS_ROOT / "benchmark_summary.json").write_text(json.dumps(aggregate, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(aggregate, indent=2))


if __name__ == "__main__":
    main()
