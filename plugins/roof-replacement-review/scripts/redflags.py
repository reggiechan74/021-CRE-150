#!/usr/bin/env python3
"""Consolidate red flags and mandatory gate results into the redflag report markdown."""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path


SEVERITY_ORDER = ("critical", "high", "medium", "low")


def gate_symbol(result: str) -> str:
    return {"pass": "✅ pass", "fail": "❌ fail", "needs_clarification": "⚠️ clarify"}.get(
        result, f"? {result}"
    )


def render(manifest: dict) -> str:
    project = manifest.get("project", {})
    rfp = manifest.get("rfp", {})
    bids = manifest.get("bids", [])
    comparison = manifest.get("comparison", {})

    all_flags = [f for b in bids for f in (b.get("red_flags") or [])]
    flag_counts = Counter(f.get("severity", "unknown") for f in all_flags)

    lines = [
        "# Roof Replacement Tender — Red Flag Report",
        "",
        f"**Project:** {project.get('property', '—')}",
        f"**Owner:** {project.get('owner', '—')}",
        f"**RFP:** {rfp.get('rfp_id', '—')}",
        f"**Report date:** {manifest.get('generated_at', '—')}",
        "",
        "---",
        "",
        "## Executive Summary",
        "",
        f"- Bids received: {len(bids)}",
        f"- Fully compliant: {comparison.get('fully_compliant_count', 0)}",
        f"- Conditional (scored, pending pre-contract clarifications): {comparison.get('conditional_count', 0)}",
        f"- Non-compliant (excluded from ranking): {comparison.get('non_compliant_count', 0)}",
        f"- Critical red flags: {flag_counts.get('critical', 0)}",
        f"- High-severity red flags: {flag_counts.get('high', 0)}",
        f"- Medium / low: {flag_counts.get('medium', 0)} / {flag_counts.get('low', 0)}",
        "",
        "---",
        "",
        "## Stage 1 — Mandatory Gate Results",
        "",
    ]

    for bid in bids:
        name = bid.get("bidder_name", bid.get("bidder_id", "Unknown"))
        gates = bid.get("mandatory_gates") or {}
        lines += [f"### {name}", ""]
        if not gates:
            lines += ["_No gate results recorded — run roof-qualification-check._", ""]
            continue
        lines += ["| Gate | Result | Evidence |", "|---|:---:|---|"]
        for gate_name, g in gates.items():
            if not isinstance(g, dict):
                continue
            lines.append(
                f"| {gate_name.replace('_', ' ').title()} | {gate_symbol(g.get('result', '?'))} | {g.get('evidence', '—')} |"
            )
        compliant = bid.get("scores", {}).get("compliant")
        status = "COMPLIANT — advances to rated scoring" if compliant else "NON-COMPLIANT — excluded"
        lines += ["", f"**Stage 1 status:** {status}", ""]

    lines += ["---", "", "## Stage 2 — Qualitative Red Flags", ""]

    for bid in bids:
        name = bid.get("bidder_name", bid.get("bidder_id", "Unknown"))
        flags = bid.get("red_flags") or []
        lines += [f"### {name}", ""]
        if not flags:
            lines += ["_No red flags identified._", ""]
            continue
        flags_sorted = sorted(
            flags, key=lambda f: SEVERITY_ORDER.index(f.get("severity", "low")) if f.get("severity") in SEVERITY_ORDER else 99
        )
        for f in flags_sorted:
            sev = (f.get("severity") or "low").upper()
            cat = (f.get("category") or "general").title()
            lines += [
                f"**[{sev}] {cat} — {f.get('description', '')}**",
                f"- Citation: {f.get('citation', '—')}",
                f"- Evidence: {f.get('evidence', '—')}",
                f"- Recommended action: {f.get('recommendation', '—')}",
                "",
            ]

    lines += ["---", "", "## Cross-Bid Patterns", ""]
    spread = comparison.get("price_spread_percent")
    if isinstance(spread, (int, float)) and spread > 15:
        lines.append(
            f"- **Price spread {spread}%** — exceeds 15%. Review whether scope is equivalent across bids or one is a low-bid outlier."
        )
    lines += [
        "",
        "## Severity Definitions",
        "",
        "| Severity | Meaning | Default owner action |",
        "|---|---|---|",
        "| Critical | Non-compliant, voids warranty, or safety risk | Reject or cure before award |",
        "| High | Material deviation from RFP or industry standard | Negotiate or reject |",
        "| Medium | Ambiguity or moderate risk | Request written clarification |",
        "| Low | Minor note | Accept, note for contract admin |",
        "",
        "_Red flags identified by `roof-technical-review` and `roof-qualification-check` against `fixtures/domain_knowledge/`._",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    with Path(args.manifest).open("r", encoding="utf-8") as f:
        manifest = json.load(f)

    report = render(manifest)
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(report, encoding="utf-8")
    print(f"Wrote red flag report: {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
