"""Score saved Anthropic finance-plugin outputs against the unseen benchmark gold totals."""

from __future__ import annotations

import json
import re
import sys
from decimal import Decimal
from pathlib import Path

PLUGIN_ROOT = Path(__file__).resolve().parent.parent
if str(PLUGIN_ROOT) not in sys.path:
    sys.path.insert(0, str(PLUGIN_ROOT))

from scripts.compare import extract_anthropic_totals
from scripts.manifest import money


SUITE_ROOT = PLUGIN_ROOT / "benchmarks" / "unseen_cam_suite"
GOLD_ROOT = SUITE_ROOT / "gold"
ANTHROPIC_ROOT = SUITE_ROOT / "results" / "anthropic"


def gold_property_total(gold: dict[str, object]) -> Decimal:
    return money(gold.get("property_level_recoverable_total") or gold["corrected_recoverable_total"])


def gold_direct_bill_total(gold: dict[str, object]) -> Decimal:
    return money(gold.get("direct_bill_total", "0.00"))


def gold_pooled_cam_total(gold: dict[str, object]) -> Decimal:
    explicit_total = gold.get("pooled_cam_total_after_direct_bills")
    if explicit_total is not None:
        return money(explicit_total)
    return money(gold_property_total(gold) - gold_direct_bill_total(gold))


def alignment_label(reported_total: Decimal, property_total: Decimal, pooled_total: Decimal) -> str:
    if reported_total == property_total and reported_total == pooled_total:
        return "both"
    if reported_total == property_total:
        return "property"
    if reported_total == pooled_total:
        return "pooled"
    return "neither"


def detect_issue(text: str, meta: dict[str, object] | None) -> bool | None:
    if not meta:
        return None
    lowered = text.lower()
    invoice_ref = str(meta.get("invoice_ref", "")).lower()
    if invoice_ref and invoice_ref in lowered:
        return True
    keywords = [str(item).lower() for item in meta.get("keywords", [])]
    if not keywords:
        return False
    hits = sum(1 for keyword in keywords if keyword in lowered)
    return hits >= 2 or ("duplicate" in lowered and hits >= 1)


def load_gold_cases() -> list[dict[str, object]]:
    cases: list[dict[str, object]] = []
    for path in sorted(GOLD_ROOT.glob("*.json")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(payload, dict) and "case_id" in payload:
            cases.append(payload)
    return cases


def score_case(gold: dict[str, object]) -> dict[str, object]:
    case_id = str(gold["case_id"])
    output_path = ANTHROPIC_ROOT / case_id / "anthropic_output.txt"
    if not output_path.exists():
        return {
            "case_id": case_id,
            "status": "missing_output",
        }

    text = output_path.read_text(encoding="utf-8")
    try:
        parsed = extract_anthropic_totals(text)
        reported_total = money(parsed["reported_total"])
    except Exception:
        reported_total = None

    property_total = gold_property_total(gold)
    direct_bill_total = gold_direct_bill_total(gold)
    pooled_total = gold_pooled_cam_total(gold)
    issues = gold.get("issues", {})
    duplicate_hit = detect_issue(text, issues.get("duplicate"))
    turnover_hit = detect_issue(text, issues.get("turnover"))
    mgmt_hit = detect_issue(text, issues.get("management_fee"))

    expected_issue_count = sum(1 for key in ("duplicate", "turnover", "management_fee") if issues.get(key))
    hit_count = sum(
        1
        for value in (duplicate_hit, turnover_hit, mgmt_hit)
        if value is True
    )

    result = {
        "case_id": case_id,
        "status": "scored" if reported_total is not None else "parse_error",
        "property_level_recoverable_total": str(property_total),
        "corrected_recoverable_total": str(property_total),
        "direct_bill_total": str(direct_bill_total),
        "pooled_cam_total_after_direct_bills": str(pooled_total),
        "reported_total": str(reported_total) if reported_total is not None else None,
        "property_total_error": str(money((reported_total - property_total) if reported_total is not None else Decimal("0"))) if reported_total is not None else None,
        "pooled_cam_total_error": str(money((reported_total - pooled_total) if reported_total is not None else Decimal("0"))) if reported_total is not None else None,
        "property_total_match": bool(reported_total == property_total) if reported_total is not None else False,
        "pooled_cam_total_match": bool(reported_total == pooled_total) if reported_total is not None else False,
        "alignment": alignment_label(reported_total, property_total, pooled_total) if reported_total is not None else None,
        "duplicate_detected": duplicate_hit,
        "turnover_detected": turnover_hit,
        "management_fee_detected": mgmt_hit,
        "issue_hits": hit_count,
        "issue_expected": expected_issue_count,
    }
    return result


def main() -> None:
    rows = [score_case(gold) for gold in load_gold_cases()]
    scored_rows = [row for row in rows if row["status"] == "scored"]
    direct_bill_rows = [row for row in scored_rows if Decimal(row["direct_bill_total"]) > 0]
    pooled_only_rows = [
        row for row in direct_bill_rows if row["pooled_cam_total_match"] and not row["property_total_match"]
    ]
    missed_both_rows = [
        row for row in scored_rows if not row["property_total_match"] and not row["pooled_cam_total_match"]
    ]
    aggregate = {
        "cases_total": len(rows),
        "cases_scored": len(scored_rows),
        "property_total_exact_matches": sum(1 for row in scored_rows if row["property_total_match"]),
        "pooled_cam_total_exact_matches": sum(1 for row in scored_rows if row["pooled_cam_total_match"]),
        "average_abs_property_total_error": str(
            money(
                sum(abs(Decimal(row["property_total_error"])) for row in scored_rows if row["property_total_error"] is not None)
                / Decimal(len(scored_rows))
            )
        ) if scored_rows else None,
        "average_abs_pooled_cam_total_error": str(
            money(
                sum(abs(Decimal(row["pooled_cam_total_error"])) for row in scored_rows if row["pooled_cam_total_error"] is not None)
                / Decimal(len(scored_rows))
            )
        ) if scored_rows else None,
        "direct_bill_case_count": len(direct_bill_rows),
        "direct_bill_case_pooled_matches": sum(1 for row in direct_bill_rows if row["pooled_cam_total_match"]),
        "direct_bill_case_property_matches": sum(1 for row in direct_bill_rows if row["property_total_match"]),
        "direct_bill_case_pooled_only_matches": len(pooled_only_rows),
        "missed_both_case_count": len(missed_both_rows),
        "missed_both_cases": [row["case_id"] for row in missed_both_rows],
        "issue_recall": (
            float(sum(row["issue_hits"] for row in scored_rows) / sum(row["issue_expected"] for row in scored_rows if row["issue_expected"]))
            if scored_rows and sum(row["issue_expected"] for row in scored_rows if row["issue_expected"])
            else None
        ),
        "results_dir": str(ANTHROPIC_ROOT),
        "cases": rows,
    }
    ANTHROPIC_ROOT.mkdir(parents=True, exist_ok=True)
    (ANTHROPIC_ROOT / "benchmark_score.json").write_text(json.dumps(aggregate, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# Anthropic Benchmark Score",
        "",
        "| Case | Status | Property Gold | Pooled Gold | Reported | Property Err | Pooled Err | Align | Dup | Turnover | Mgmt |",
        "|------|--------|--------------:|------------:|---------:|-------------:|-----------:|-------|:---:|:--------:|:----:|",
    ]
    for row in rows:
        if row["status"] == "missing_output":
            lines.append(f"| {row['case_id']} | missing | - | - | - | - | - | - | - | - | - |")
            continue
        if row["status"] == "parse_error":
            lines.append(
                f"| {row['case_id']} | parse_error | ${Decimal(row['property_level_recoverable_total']):,.2f} | "
                f"${Decimal(row['pooled_cam_total_after_direct_bills']):,.2f} | - | - | - | - | "
                f"{'Y' if row['duplicate_detected'] else 'N'} | {'Y' if row['turnover_detected'] else 'N'} | "
                f"{'Y' if row['management_fee_detected'] else 'N'} |"
            )
            continue
        lines.append(
            f"| {row['case_id']} | scored | ${Decimal(row['property_level_recoverable_total']):,.2f} | "
            f"${Decimal(row['pooled_cam_total_after_direct_bills']):,.2f} | "
            f"${Decimal(row['reported_total']):,.2f} | ${Decimal(row['property_total_error']):,.2f} | "
            f"${Decimal(row['pooled_cam_total_error']):,.2f} | {row['alignment']} | "
            f"{'Y' if row['duplicate_detected'] else 'N'} | "
            f"{'Y' if row['turnover_detected'] else 'N'} | "
            f"{'Y' if row['management_fee_detected'] else 'N'} |"
        )
    if aggregate["average_abs_property_total_error"] is not None:
        lines.extend(
            [
                "",
                f"- Cases scored: {aggregate['cases_scored']} / {aggregate['cases_total']}",
                f"- Exact property-level matches: {aggregate['property_total_exact_matches']} / {aggregate['cases_total']}",
                f"- Exact pooled-CAM matches: {aggregate['pooled_cam_total_exact_matches']} / {aggregate['cases_total']}",
                f"- Average absolute property-level error: ${Decimal(aggregate['average_abs_property_total_error']):,.2f}",
                f"- Average absolute pooled-CAM error: ${Decimal(aggregate['average_abs_pooled_cam_total_error']):,.2f}",
                f"- Direct-bill cases matching pooled CAM exactly: {aggregate['direct_bill_case_pooled_matches']} / {aggregate['direct_bill_case_count']}",
                f"- Issue recall: {aggregate['issue_recall']:.2%}" if aggregate["issue_recall"] is not None else "- Issue recall: n/a",
            ]
        )
        lines.extend(
            [
                "",
                "Interpretation",
                "  Two benchmark totals are tracked separately:",
                "  - Property total: corrected building-level recoverable OpEx after property-level removals.",
                "  - Pooled CAM total: the shared CAM pool after removing lease-specific direct bills.",
                "",
                f"  Anthropic matched the pooled CAM total exactly in {aggregate['direct_bill_case_pooled_only_matches']} direct-bill cases where it did not match the broader property total.",
                f"  It matched the property total in {aggregate['property_total_exact_matches']} cases and the pooled CAM total in {aggregate['pooled_cam_total_exact_matches']} cases overall.",
            ]
        )
        if aggregate["missed_both_case_count"] == 1:
            missed_case = missed_both_rows[0]
            lines.append(
                f"  The only case that missed both totals was {missed_case['case_id']}, where the reported total was "
                f"${Decimal(missed_case['property_total_error']):,.2f} below the property total and "
                f"${Decimal(missed_case['pooled_cam_total_error']):,.2f} below the pooled CAM total."
            )
        elif aggregate["missed_both_case_count"] > 1:
            lines.append(
                "  Cases missing both totals: " + ", ".join(str(case_id) for case_id in aggregate["missed_both_cases"]) + "."
            )
    report_path = ANTHROPIC_ROOT / "benchmark_score.md"
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"json": str(ANTHROPIC_ROOT / 'benchmark_score.json'), "markdown": str(report_path)}, indent=2))


if __name__ == "__main__":
    main()
