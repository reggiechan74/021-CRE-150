#!/usr/bin/env python3
"""Render the scoring matrix markdown from a normalized tender manifest.

Mechanical assembly only: pulls scores, weights, compliance status, and
per-bid scoring_rationale strings that were written upstream by the
qualification-check and technical-review skills. No judgment added here.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


WEIGHT_LABELS = {
    "price": "Price",
    "technical_approach": "Technical Approach",
    "warranty_materials": "Warranty & Materials",
    "schedule": "Schedule",
    "experience_references": "Experience & References",
    "qualifications_certifications": "Qualifications & Certifications",
}

SUB_SCORE_KEYS = (
    "price",
    "technical_approach",
    "warranty_materials",
    "schedule",
    "experience_references",
    "qualifications_certifications",
)


def fmt_money(v) -> str:
    if v is None:
        return "—"
    try:
        return f"${int(round(float(v))):,}"
    except (TypeError, ValueError):
        return str(v)


def fmt_pct(v) -> str:
    if v is None:
        return "—"
    try:
        return f"{float(v):+.1f}%"
    except (TypeError, ValueError):
        return str(v)


def compliance_badge(bid: dict) -> str:
    gates = bid.get("mandatory_gates") or {}
    fails = [g for g, v in gates.items() if isinstance(v, dict) and v.get("result") == "fail"]
    clarifies = [g for g, v in gates.items() if isinstance(v, dict) and v.get("result") == "needs_clarification"]
    if fails:
        return f"❌ **Non-compliant** (failed: {', '.join(fails)}"  + (f"; {len(clarifies)} needs-clarification)" if clarifies else ")")
    if clarifies:
        return f"⚠️ **Needs clarification** ({len(clarifies)} gates: {', '.join(clarifies)})"
    return "✅ Compliant"


def render(manifest: dict) -> str:
    project = manifest.get("project", {})
    rfp = manifest.get("rfp", {})
    bids = manifest.get("bids", [])
    comparison = manifest.get("comparison", {})
    weights = (rfp.get("evaluation_criteria") or {}).get("weighting") or {}
    method = (rfp.get("evaluation_criteria") or {}).get("price_scoring_method") or "—"
    weighting_source = (rfp.get("evaluation_criteria") or {}).get("weighting_source") or "rfp_manifest"

    ranked = [b for b in bids if (b.get("scores") or {}).get("rank") is not None]
    ranked.sort(key=lambda b: b["scores"].get("rank", 9999))
    non_compliant = [b for b in bids if not (b.get("scores") or {}).get("compliant", False)]

    low_compliant = min(
        ((b.get("pricing") or {}).get("base_bid_cad") for b in ranked if (b.get("pricing") or {}).get("base_bid_cad") is not None),
        default=None,
    )

    lines = [
        "# Roof Replacement Tender — Scoring Matrix",
        "",
        f"**Project:** {project.get('property', '—')}",
        f"**Owner:** {project.get('owner', '—')}",
        f"**RFP:** {rfp.get('rfp_id', '—')} — issued {rfp.get('issued_date', '—')}",
        f"**Submissions received:** {len(bids)} total — "
        f"{comparison.get('fully_compliant_count', 0)} fully compliant, "
        f"{comparison.get('conditional_count', 0)} conditional, "
        f"{comparison.get('non_compliant_count', 0)} non-compliant",
        f"**Evaluation date:** {manifest.get('generated_at', '—')}",
        "",
        "---",
        "",
        "## Weighting Applied",
        "",
        "| Criterion | Weight |",
        "|---|---:|",
    ]
    total_w = 0
    for key in SUB_SCORE_KEYS:
        w = weights.get(key)
        if w is None:
            continue
        total_w += w
        lines.append(f"| {WEIGHT_LABELS[key]} | {w}% |")
    lines += [
        f"| **Total** | **{total_w}%** |",
        "",
        f"Price scoring method: `{method}`",
        "",
    ]

    source_label = {
        "rfp_manifest": "RFP manifest (§7 as issued)",
    }.get(weighting_source, weighting_source)
    lines.append(f"**Weighting source:** {source_label}")
    lines.append("")
    if weighting_source != "rfp_manifest":
        lines += [
            f"> ⚠️ **WARNING — weights and/or method overridden from the RFP.** "
            f"Source: `{weighting_source}`. The rated rubric above is not the one "
            f"published in the RFP. Evaluators must confirm the override was "
            f"authorized before circulating this matrix.",
            "",
        ]

    lines += [
        "---",
        "",
        "## Compliance Summary",
        "",
    ]
    for bid in sorted(bids, key=lambda b: b.get("bidder_name", "")):
        lines.append(f"- **{bid.get('bidder_name', bid.get('bidder_id', '?'))}** — {compliance_badge(bid)}")

    lines += [
        "",
        "*Non-compliant bids are excluded from rated scoring. Needs-clarification bids are scored but flagged as conditional pending gate resolution.*",
        "",
        "---",
        "",
        "## Rated Scoring (Compliant Bids Only)",
        "",
    ]

    header = "| Rank | Bidder |"
    sep = "|---:|---|"
    for key in SUB_SCORE_KEYS:
        w = weights.get(key, "")
        header += f" {WEIGHT_LABELS[key].split(' & ')[0]} (w={w}) |"
        sep += "---:|"
    header += " **Weighted Total** |"
    sep += "---:|"
    lines += [header, sep]

    for bid in ranked:
        s = bid.get("scores") or {}
        row = f"| {s.get('rank', '—')} | {bid.get('bidder_name', '?')} |"
        for key in SUB_SCORE_KEYS:
            v = s.get(key)
            row += f" {v if v is not None else '—'} |"
        wt = s.get("weighted_total")
        row += f" **{wt if wt is not None else '—'}** |"
        lines.append(row)

    lines += [
        "",
        "**Raw sub-scores are 0–100 per criterion; weighted total is the sum of (sub-score × weight/100).**",
        "",
        "---",
        "",
        "## Pricing Comparison (All Bids)",
        "",
        "| Bidder | Base Bid (CAD) | HST Incl? | Δ vs Low Compliant | Compliance |",
        "|---|---:|:-:|---:|:-:|",
    ]
    sorted_by_price = sorted(
        bids,
        key=lambda b: (b.get("pricing") or {}).get("base_bid_cad") or 0,
    )
    for bid in sorted_by_price:
        pricing = bid.get("pricing") or {}
        base = pricing.get("base_bid_cad")
        hst = "yes" if pricing.get("hst_included") else "no"
        delta = None
        if isinstance(base, (int, float)) and isinstance(low_compliant, (int, float)) and low_compliant:
            delta = (base - low_compliant) / low_compliant * 100
        comp = compliance_badge(bid)
        comp_short = "✅" if "Compliant" in comp and "Non" not in comp else ("⚠️" if "Needs" in comp else "❌")
        lines.append(
            f"| {bid.get('bidder_name', '?')} | {fmt_money(base)} | {hst} | {fmt_pct(delta)} | {comp_short} |"
        )

    spread = comparison.get("price_spread_percent")
    lines += [
        "",
        f"**Low compliant bid:** {fmt_money(low_compliant)}  ",
        f"**Low bid (all):** {fmt_money(comparison.get('all_bids_price_low_cad') or comparison.get('price_low_cad'))}  ",
        f"**High bid:** {fmt_money(comparison.get('all_bids_price_high_cad') or comparison.get('price_high_cad'))}  ",
        f"**Spread (compliant only):** {spread if spread is not None else '—'}%",
        "",
    ]
    if isinstance(spread, (int, float)) and spread > 15:
        lines += [
            "> ⚠️ **Spread exceeds 15%** — the CCA industry heuristic for bid outliers. Review the red-flag report for scope divergence before award.",
            "",
        ]

    lines += ["---", "", "## Scoring Rationale", ""]
    for bid in ranked:
        s = bid.get("scores") or {}
        rationale = bid.get("scoring_rationale") or {}
        lines += [
            f"### {s.get('rank', '—')}. {bid.get('bidder_name', '?')} — {s.get('weighted_total', '—')} pts",
            "",
        ]
        strengths = rationale.get("strengths") or []
        weaknesses = rationale.get("weaknesses") or []
        differentiator = rationale.get("differentiator") or ""
        if strengths:
            lines.append("**Strengths:** " + "; ".join(strengths))
        if weaknesses:
            lines.append("**Weaknesses:** " + "; ".join(weaknesses))
        if differentiator:
            lines.append(f"**Key differentiator:** {differentiator}")
        lines.append("")

    if non_compliant:
        lines += ["---", "", "## Non-Compliant Bids (Reference Only — Not Ranked)", ""]
        for bid in non_compliant:
            pricing = bid.get("pricing") or {}
            gates = bid.get("mandatory_gates") or {}
            failed = [g for g, v in gates.items() if isinstance(v, dict) and v.get("result") == "fail"]
            flags = bid.get("red_flags") or []
            crit = sum(1 for f in flags if f.get("severity") == "critical")
            high = sum(1 for f in flags if f.get("severity") == "high")
            lines.append(
                f"- **{bid.get('bidder_name', '?')}** ({fmt_money(pricing.get('base_bid_cad'))}) — failed: {', '.join(failed) or '—'}; {crit} critical / {high} high red flags"
            )
        lines.append("")

    lines += [
        "---",
        "",
        "*Scoring produced by `score.py`. Mandatory gate evaluation per `roof-qualification-check`. Technical evaluation per `roof-technical-review`.*",
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

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(render(manifest), encoding="utf-8")
    print(f"Wrote scoring matrix: {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
