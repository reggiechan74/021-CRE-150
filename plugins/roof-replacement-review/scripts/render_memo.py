#!/usr/bin/env python3
"""Render the owner-facing recommendation memo from a normalized tender manifest.

Assembles the memo mechanically from manifest data:
- Recommendation and why-not-low-bid from scoring + pricing
- Award conditions derived from needs_clarification gates + medium/high red flags
  on the recommended bid, plus standard conditions
- Risk table seeded with standard roofing-project risks
- Contract form chosen from OBC classification + project value

For deeper contextual synthesis (per-risk mitigation nuance, project-specific
rationale prose), use the `roof-recommendation-memo` skill — that wraps this
script's output with LLM judgment. This renderer is the fast deterministic path.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def fmt_money(v) -> str:
    if v is None:
        return "—"
    try:
        return f"${int(round(float(v))):,}"
    except (TypeError, ValueError):
        return str(v)


def compliance_status(bid: dict) -> tuple[str, list[str], list[str]]:
    gates = bid.get("mandatory_gates") or {}
    fails = [g for g, v in gates.items() if isinstance(v, dict) and v.get("result") == "fail"]
    clarifies = [g for g, v in gates.items() if isinstance(v, dict) and v.get("result") == "needs_clarification"]
    if fails:
        return "non_compliant", fails, clarifies
    if clarifies:
        return "needs_clarification", fails, clarifies
    return "compliant", fails, clarifies


def gate_to_award_condition(gate_name: str, gate: dict) -> str:
    """Translate a needs_clarification gate into an award-condition sentence."""
    ev = gate.get("evidence") or ""
    mapping = {
        "wsib_clearance": "Produce a current WSIB clearance certificate within the active validity window with 'in good standing' wording.",
        "cgl_insurance": "Produce a Certificate of Insurance naming the owner as additional insured, with the required completed-operations tail in writing from the insurer.",
        "bonding": "Produce consent of surety for the performance and labour-and-material bonds at the RFP-specified percentages.",
        "working_at_heights": "Confirm in writing that all on-site workers have current O. Reg. 297/13 Working-at-Heights training.",
        "addenda_acknowledgment": "Provide signed acknowledgment of all RFP addenda on the Form of Tender.",
        "non_collusion_declaration": "Provide a signed and dated non-collusion declaration.",
        "site_visit": "Confirm attendance at the mandatory pre-bid site meeting.",
        "similar_project_references": "Provide written verification that reference projects are comparable in size, scope, and recency per the RFP.",
        "minimum_years_in_business": "Provide documentary evidence of minimum years in continuous business operation.",
    }
    base = mapping.get(gate_name, f"Resolve the clarification on {gate_name.replace('_', ' ')}.")
    return f"{base}" + (f" (Evidence note: {ev})" if ev else "")


def flag_to_condition(flag: dict) -> str:
    desc = flag.get("description") or ""
    rec = flag.get("recommendation") or "clarify"
    cite = flag.get("citation") or ""
    action_map = {
        "clarify": "Clarify in writing",
        "negotiate": "Negotiate",
        "accept-with-condition": "Accept with written condition",
        "reject": "Reject",
    }
    action = action_map.get(rec, "Clarify")
    return f"{action}: {desc}" + (f" (per {cite})" if cite else "")


STANDARD_CONDITIONS = [
    "WSIB clearance re-verification at clearances.wsib.ca within 7 days of contract signing; record the verification reference number in the contract file.",
    "10% statutory holdback under Ontario Construction Act; monthly progress certification.",
    "Substantial performance declaration at 97% per Construction Act s. 2, with publication per s. 32.",
    "Manufacturer inspection within 30 days of substantial performance; inspector's sign-off is a condition of final warranty issuance.",
]


def contract_form_recommendation(project: dict, recommended_price: float | None) -> str:
    classification = (project.get("building_classification") or "").lower()
    if classification.startswith("obc_part_9"):
        return "Simple stipulated-price contract (OBC Part 9 residential)"
    if recommended_price is not None and recommended_price <= 500_000:
        return "CCA-1 stipulated price (2021) — OBC Part 3, value ≤ $500K"
    return "CCDC 2 (2020) stipulated-price contract — OBC Part 3, value > $500K"


STANDARD_RISKS = [
    ("Weather delay during tear-off phase", "Med", "Med", "Phased staging plan with daily dry-in protocol; watertight at end of each work day; schedule float between substantial and final completion."),
    ("Deck replacement exceeds allowance", "Med", "Med", "Unit prices carried in bid; owner's rep photographs and signs off each replacement quantity; cap via allowance."),
    ("Concealed conditions (ACM, lead, wet insulation) discovered during tear-off", "Med", "High", "Transition-era safety protocol in bid; owner-borne abatement cost with schedule contingency; HEPA dust protocols."),
    ("Change orders from undocumented prior repairs", "Med", "Med", "10% owner contingency retained separately; owner's rep reviews each change before issuance; documented pricing formula in RFP."),
    ("Tenant disruption on occupied building", "Med", "High", "72-hour HVAC coordination; max-exposure phasing cap per RFP; weekend watertight protection; daily tenant communication protocol."),
    ("Contractor insolvency during project", "Low", "High", "Performance bond + L&M bond at RFP-specified percentages; statutory holdback; monthly progress certification."),
]


def render(manifest: dict) -> str:
    project = manifest.get("project", {})
    rfp = manifest.get("rfp", {})
    bids = manifest.get("bids", [])
    comparison = manifest.get("comparison", {})
    recommended_id = comparison.get("recommended_bidder_id")

    by_id = {b.get("bidder_id"): b for b in bids}
    recommended = by_id.get(recommended_id) if recommended_id else None
    if recommended is None:
        ranked = [b for b in bids if (b.get("scores") or {}).get("rank") == 1]
        if ranked:
            recommended = ranked[0]

    if recommended is None:
        return "# Recommendation Memo\n\n_Cannot render: no recommended bidder found in manifest.comparison.recommended_bidder_id and no bid has rank=1._\n"

    rec_name = recommended.get("bidder_name", "?")
    rec_pricing = recommended.get("pricing") or {}
    rec_base = rec_pricing.get("base_bid_cad")
    rec_hst_incl = rec_pricing.get("hst_included")
    rec_all_in = rec_base * 1.13 if isinstance(rec_base, (int, float)) and not rec_hst_incl else rec_base
    rec_scores = recommended.get("scores") or {}
    rec_weighted = rec_scores.get("weighted_total")

    ranked = sorted(
        [b for b in bids if (b.get("scores") or {}).get("rank") is not None],
        key=lambda b: b["scores"].get("rank", 9999),
    )
    non_compliant = [b for b in bids if not (b.get("scores") or {}).get("compliant", False)]

    compliant_prices = [
        (b.get("pricing") or {}).get("base_bid_cad") for b in ranked if (b.get("pricing") or {}).get("base_bid_cad") is not None
    ]
    low_compliant = min(compliant_prices) if compliant_prices else None
    low_compliant_bid = next(
        (b for b in ranked if (b.get("pricing") or {}).get("base_bid_cad") == low_compliant), None
    ) if low_compliant is not None else None
    is_rec_low_compliant = (
        low_compliant_bid is not None and recommended.get("bidder_id") == low_compliant_bid.get("bidder_id")
    )
    all_low = comparison.get("all_bids_price_low_cad") or comparison.get("price_low_cad")

    lines = [
        "# RECOMMENDATION MEMO — Award of Roof Replacement Contract",
        "",
        f"**To:** {project.get('owner', '—')} — Executive / Property Management",
        "**From:** Roof Replacement Evaluation Team",
        f"**Re:** RFP {rfp.get('rfp_id', '—')} — {project.get('property', '—')}",
        f"**Date:** {manifest.get('generated_at', '—')[:10]}",
        "",
        "---",
        "",
        "## 1. Recommendation",
        "",
    ]
    hst_note = (
        f" (excluding HST); with 13% HST, the all-in contract value is **{fmt_money(rec_all_in)}**"
        if isinstance(rec_base, (int, float)) and not rec_hst_incl
        else " (HST included)"
    )
    lines.append(
        f"We recommend award of the roof replacement contract to **{rec_name}** for a base bid of **{fmt_money(rec_base)} CAD**{hst_note}."
    )
    lines.append("")
    second = ranked[1] if len(ranked) > 1 else None
    if second is not None and rec_weighted is not None:
        second_weighted = (second.get("scores") or {}).get("weighted_total")
        if second_weighted is not None:
            lines.append(
                f"{rec_name} achieved the highest weighted score of {rec_weighted}/100 against the RFP evaluation criteria, leading the second-ranked compliant bid ({second.get('bidder_name', '—')} at {second_weighted}/100) by {round(rec_weighted - second_weighted, 2)} points. Of the {len(bids)} submissions received, {comparison.get('compliant_bidders_count', '—')} are compliant and {len(non_compliant)} are non-compliant on material grounds (see §4)."
            )
            lines.append("")
    lines += [
        "Award is conditional on the owner resolving the clarifications enumerated in §5 before contract execution.",
        "",
        "---",
        "",
        "## 2. Why Not the Low Bid",
        "",
    ]
    if non_compliant and isinstance(all_low, (int, float)) and isinstance(low_compliant, (int, float)) and all_low < low_compliant:
        nc_names = [b.get("bidder_name", "?") for b in non_compliant]
        lines.append(
            f"The lowest-priced submissions — {', '.join(nc_names)} — are disqualified as non-compliant (see §4). Their apparent savings are engineered by deleting RFP scope items or failing mandatory gates, and would expose the owner to uninsured warranty failure or safety/regulatory risk."
        )
        lines.append("")
    if is_rec_low_compliant:
        lines.append(
            f"Among compliant bids, {rec_name} is in fact the **low compliant bid** at {fmt_money(rec_base)}. The recommendation therefore does not carry a compliant-bid price premium."
        )
    elif low_compliant_bid is not None and isinstance(rec_base, (int, float)) and isinstance(low_compliant, (int, float)):
        premium_pct = (rec_base - low_compliant) / low_compliant * 100 if low_compliant else 0
        lines.append(
            f"Among compliant bids, the low compliant price is {fmt_money(low_compliant)} from {low_compliant_bid.get('bidder_name', '—')}. The recommended bid carries a {premium_pct:+.1f}% premium, justified by the scoring differential in §3 and the qualification differentiators captured in §4."
        )
    lines += [
        "",
        "---",
        "",
        "## 3. Rated Scoring Summary (Compliant Bids)",
        "",
        "| Rank | Bidder | Base Bid | Tech | Warranty | Schedule | Exp | Qual | **Weighted Total** |",
        "|---:|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for b in ranked:
        s = b.get("scores") or {}
        p = (b.get("pricing") or {}).get("base_bid_cad")
        lines.append(
            f"| {s.get('rank', '—')} | {b.get('bidder_name', '?')} | {fmt_money(p)} | {s.get('technical_approach', '—')} | {s.get('warranty_materials', '—')} | {s.get('schedule', '—')} | {s.get('experience_references', '—')} | {s.get('qualifications_certifications', '—')} | **{s.get('weighted_total', '—')}** |"
        )
    weights = (rfp.get("evaluation_criteria") or {}).get("weighting") or {}
    lines += [
        "",
        f"Weighting applied: Price {weights.get('price', '—')}%, Technical {weights.get('technical_approach', '—')}%, Warranty {weights.get('warranty_materials', '—')}%, Schedule {weights.get('schedule', '—')}%, Experience {weights.get('experience_references', '—')}%, Qualifications {weights.get('qualifications_certifications', '—')}% (100% total, per RFP §7).",
        "",
        "---",
        "",
        "## 4. Compliance Findings",
        "",
        "**Compliant (ranked):**",
    ]
    for b in ranked:
        status, fails, clarifies = compliance_status(b)
        note = f"all mandatory gates pass/fail satisfied; {len(clarifies)} gate(s) need documentary clarification before contract execution" if clarifies else "all mandatory gates satisfied"
        lines.append(f"- **{b.get('bidder_name', '?')}** — {note}")
    if non_compliant:
        lines += ["", "**Non-compliant (excluded from rated scoring):**"]
        for b in non_compliant:
            _, fails, _ = compliance_status(b)
            flags = b.get("red_flags") or []
            crit = sum(1 for f in flags if f.get("severity") == "critical")
            high = sum(1 for f in flags if f.get("severity") == "high")
            lines.append(
                f"- **{b.get('bidder_name', '?')}** — failed gates: {', '.join(fails) or '—'}; also carries {crit} critical and {high} high red flags. Non-compliance is not curable by clarification."
            )
    lines += [
        "",
        "---",
        "",
        "## 5. Award Conditions",
        "",
        f"Prior to contract execution, {rec_name} must provide or satisfy the following:",
        "",
    ]
    conditions: list[str] = []
    gates = recommended.get("mandatory_gates") or {}
    for gate_name, gate in gates.items():
        if isinstance(gate, dict) and gate.get("result") == "needs_clarification":
            conditions.append(gate_to_award_condition(gate_name, gate))
    for flag in (recommended.get("red_flags") or []):
        sev = flag.get("severity")
        if sev in ("high", "medium"):
            conditions.append(flag_to_condition(flag))
    for i, c in enumerate(conditions, start=1):
        lines.append(f"{i}. {c}")
    lines += ["", "**Standard conditions (applied to every award):**"]
    for c in STANDARD_CONDITIONS:
        lines.append(f"- {c}")

    lines += [
        "",
        "---",
        "",
        "## 6. Risk Assessment",
        "",
        "| Risk | Likelihood | Impact | Mitigation |",
        "|---|:-:|:-:|---|",
    ]
    for desc, like, impact, mit in STANDARD_RISKS:
        if desc == "Tenant disruption on occupied building" and not project.get("occupied_during_work"):
            continue
        lines.append(f"| {desc} | {like} | {impact} | {mit} |")

    contract_form = contract_form_recommendation(project, rec_base)
    lines += [
        "",
        "---",
        "",
        "## 7. Contract Form",
        "",
        f"Recommend **{contract_form}**.",
        "",
        "Supplementary conditions should reference the Ontario Construction Act holdback and lien provisions (s. 26, s. 32, s. 34), OBC compliance for the insulation upgrade, RFP phasing requirements, and RFP closeout deliverables (as-builts, warranty documents, maintenance manual, lien waivers).",
        "",
        "---",
        "",
        "## 8. Next Steps",
        "",
        f"1. Issue conditional award letter to {rec_name} citing §5 conditions with a 10-business-day response window.",
        "2. Parallel track: notify remaining compliant bidders that their bids remain on file as alternates pending conditions satisfaction.",
        "3. Issue notice of non-compliance to non-compliant bidders with a right of response (Contract A disclosure per Ron Engineering doctrine).",
        "4. Upon conditions satisfied, execute the recommended contract form; coordinate mobilization per RFP schedule.",
        "5. Retain these manifests, scoring matrix, and red flag report in the procurement file as the evaluation record defensible against any bid protest.",
        "",
        "---",
        "",
        "*Prepared from the normalized tender manifest at `manifests/tender_manifest.json`. Supporting detail: `scoring_matrix.md`, `redflag_report.md`.*",
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
    print(f"Wrote recommendation memo: {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
