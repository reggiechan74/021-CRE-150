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

    gold_total = money(gold["corrected_recoverable_total"])
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
        "gold_corrected_recoverable_total": str(gold_total),
        "reported_total": str(reported_total) if reported_total is not None else None,
        "total_error": str(money((reported_total - gold_total) if reported_total is not None else Decimal("0"))) if reported_total is not None else None,
        "property_total_match": bool(reported_total == gold_total) if reported_total is not None else False,
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
    aggregate = {
        "cases_total": len(rows),
        "cases_scored": len(scored_rows),
        "property_total_exact_matches": sum(1 for row in scored_rows if row["property_total_match"]),
        "average_abs_total_error": str(
            money(
                sum(abs(Decimal(row["total_error"])) for row in scored_rows if row["total_error"] is not None)
                / Decimal(len(scored_rows))
            )
        ) if scored_rows else None,
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
        "| Case | Status | Gold Total | Reported Total | Error | Dup | Turnover | Mgmt |",
        "|------|--------|-----------:|---------------:|------:|:---:|:--------:|:----:|",
    ]
    for row in rows:
        if row["status"] == "missing_output":
            lines.append(f"| {row['case_id']} | missing | - | - | - | - | - | - |")
            continue
        if row["status"] == "parse_error":
            lines.append(f"| {row['case_id']} | parse_error | ${Decimal(row['gold_corrected_recoverable_total']):,.2f} | - | - | {'Y' if row['duplicate_detected'] else 'N'} | {'Y' if row['turnover_detected'] else 'N'} | {'Y' if row['management_fee_detected'] else 'N'} |")
            continue
        lines.append(
            f"| {row['case_id']} | scored | ${Decimal(row['gold_corrected_recoverable_total']):,.2f} | "
            f"${Decimal(row['reported_total']):,.2f} | ${Decimal(row['total_error']):,.2f} | "
            f"{'Y' if row['duplicate_detected'] else 'N'} | "
            f"{'Y' if row['turnover_detected'] else 'N'} | "
            f"{'Y' if row['management_fee_detected'] else 'N'} |"
        )
    if aggregate["average_abs_total_error"] is not None:
        lines.extend(
            [
                "",
                f"- Cases scored: {aggregate['cases_scored']} / {aggregate['cases_total']}",
                f"- Exact total matches: {aggregate['property_total_exact_matches']} / {aggregate['cases_total']}",
                f"- Average absolute total error: ${Decimal(aggregate['average_abs_total_error']):,.2f}",
                f"- Issue recall: {aggregate['issue_recall']:.2%}" if aggregate["issue_recall"] is not None else "- Issue recall: n/a",
            ]
        )
    report_path = ANTHROPIC_ROOT / "benchmark_score.md"
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"json": str(ANTHROPIC_ROOT / 'benchmark_score.json'), "markdown": str(report_path)}, indent=2))


if __name__ == "__main__":
    main()
