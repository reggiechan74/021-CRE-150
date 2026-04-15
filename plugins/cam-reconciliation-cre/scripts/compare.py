"""Stage 5: compare corrected CAM output against the Anthropic finance workflow."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

PLUGIN_ROOT = Path(__file__).resolve().parent.parent
if str(PLUGIN_ROOT) not in sys.path:
    sys.path.insert(0, str(PLUGIN_ROOT))

from scripts.manifest import Manifest, money
from scripts.statement import corrections_summary


TOTAL_RECONCILIATION_RE = re.compile(
    r"TOTAL\s+\$\s*([0-9,]+)\s+\$\s*([0-9,]+)\s+\$\s*([+\-]?[0-9,]+)",
    re.MULTILINE,
)
TOTAL_EXPENSES_RE = re.compile(
    r"TOTAL OPERATING EXPENSES\s+([0-9,]+)\s+([0-9,]+)\s+([+\-]?[0-9,]+)",
    re.MULTILINE,
)
MONEY_RE = re.compile(r"\$?\s*([0-9]{1,3}(?:,[0-9]{3})+(?:\.[0-9]{2})|[0-9]+\.[0-9]{2})")


def _is_corrected_header(line: str) -> bool:
    stripped = line.strip().lower()
    header_prefix_re = re.compile(r"^(?:[#*\-\s]+|[a-z]\.\d+\s+|step\s+\d+\.?\s+)?corrected\b")
    if not header_prefix_re.match(stripped):
        return False
    return any(token in stripped for token in ("recoverable", "opex", "operating expense"))


def _extract_corrected_total(text: str) -> Decimal | None:
    lines = text.splitlines()
    candidates: list[str] = []
    for idx, line in enumerate(lines):
        if not _is_corrected_header(line):
            continue

        line_amounts = MONEY_RE.findall(line)
        if line_amounts:
            candidates.append(line_amounts[-1])
            continue

        window: list[tuple[str, list[str]]] = []
        for next_line in lines[idx + 1 : idx + 7]:
            if not next_line.strip():
                if window:
                    break
                continue
            next_amounts = MONEY_RE.findall(next_line)
            if next_amounts:
                window.append((next_line, next_amounts))
        if not window:
            continue

        corrected_window = [
            amounts[-1]
            for candidate_line, amounts in window
            if _is_corrected_header(candidate_line)
        ]
        if corrected_window:
            candidates.append(corrected_window[-1])
            continue

        first_line, first_amounts = window[0]
        if len(first_amounts) == 1 and "raw" not in first_line.lower():
            candidates.append(first_amounts[0])
            continue

        equals_window = [
            amounts[-1]
            for candidate_line, amounts in window
            if "=" in candidate_line
        ]
        if equals_window:
            candidates.append(equals_window[-1])
            continue

        candidates.append(window[-1][1][-1])

    if not candidates:
        return None
    return money(candidates[-1].replace(",", ""))


def extract_anthropic_totals(text: str) -> dict[str, object]:
    corrected_total = _extract_corrected_total(text)
    if corrected_total is not None:
        return {
            "budget_total": None,
            "reported_total": corrected_total,
            "reported_variance": None,
        }

    match = TOTAL_RECONCILIATION_RE.search(text)
    if not match:
        match = TOTAL_EXPENSES_RE.search(text)
    if not match:
        raise ValueError("Could not extract Anthropic totals from comparison source.")
    budget, actual, variance = match.groups()
    return {
        "budget_total": money(budget.replace(",", "")),
        "reported_total": money(actual.replace(",", "")),
        "reported_variance": money(variance.replace(",", "").replace("+", "")),
    }


def compare_against_anthropic(manifest: Manifest, anthropic_text: str) -> str:
    theirs = extract_anthropic_totals(anthropic_text)
    ours_total = money(
        sum(
            line.classification.recoverable_amount or 0
            for line in manifest.gl_lines
            if line.classification and line.classification.recoverable
        )
    )
    corrections = corrections_summary(manifest)
    avoided = money(theirs["reported_total"] - ours_total)

    lines = [
        "# CAM Reconciliation Comparison",
        "",
        f"- Property: {manifest.property.name}",
        f"- Anthropic-reported recoverable opex: ${money(theirs['reported_total']):,.2f}",
        f"- CAM-native corrected recoverable opex: ${ours_total:,.2f}",
        f"- Tenant overbilling avoided: ${avoided:,.2f}",
        "",
        "## Side-by-Side",
        "",
        "| Metric | Anthropic Finance Workflow | cam-reconciliation-cre | Delta |",
        "|--------|---------------------------:|-----------------------:|------:|",
        f"| Recoverable operating expenses | ${money(theirs['reported_total']):,.2f} | ${ours_total:,.2f} | ${avoided:,.2f} |",
        f"| Duplicate invoice removed | $0.00 | ${money(corrections['duplicate_invoice']):,.2f} | ${money(corrections['duplicate_invoice']):,.2f} |",
        f"| Turnover cleaning removed | $0.00 | ${money(corrections['tenant_turnover']):,.2f} | ${money(corrections['tenant_turnover']):,.2f} |",
        f"| Management fee methodology correction | $0.00 | ${money(corrections['management_fee_method']):,.2f} | ${money(corrections['management_fee_method']):,.2f} |",
        "",
        "## Payoff Chart",
        "",
        f"- Anthropic draft:      ${money(theirs['reported_total']):,.2f}",
        f"- Corrected recoverable:${ours_total:,.2f}",
        f"- Avoided overbilling:  ${avoided:,.2f}",
    ]
    return "\n".join(lines) + "\n"


def default_output_path(allocated_manifest_path: Path) -> Path:
    return allocated_manifest_path.parents[1] / "compare_report.md"


def main() -> None:
    parser = argparse.ArgumentParser(description="Compare corrected CAM output against Anthropic output text.")
    parser.add_argument("--manifest", type=Path, required=True, help="Path to allocated_manifest.json.")
    parser.add_argument("--anthropic", type=Path, required=True, help="Path to Anthropic output text.")
    parser.add_argument("--output", type=Path, help="Path to compare_report.md.")
    args = parser.parse_args()

    manifest = Manifest.load(args.manifest)
    report = compare_against_anthropic(manifest, args.anthropic.read_text(encoding="utf-8"))
    output = args.output or default_output_path(args.manifest)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(report, encoding="utf-8")
    print(json.dumps({"compare_report": str(output)}, indent=2))


if __name__ == "__main__":
    main()
