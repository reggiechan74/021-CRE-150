#!/usr/bin/env python3
"""MCDA scoring engine for roof replacement tenders.

Reads a tender manifest, computes price scores via the configured method,
combines with skill-provided rated sub-scores, applies weights, ranks
compliant bidders, and writes back into the manifest.

Non-compliant bidders (any mandatory gate = fail) are excluded from ranking
but retained in the manifest with scores.rank = null and a note.
"""
from __future__ import annotations

import argparse
import json
import sys
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path


RATED_KEYS = (
    "technical_approach",
    "experience_references",
    "warranty_materials",
    "schedule",
    "qualifications_certifications",
)


def round2(x: float) -> float:
    return float(Decimal(str(x)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def is_compliant(bid: dict) -> bool:
    gates = bid.get("mandatory_gates") or {}
    if not gates:
        return False
    for gate in gates.values():
        if isinstance(gate, dict) and gate.get("result") == "fail":
            return False
    return True


def compute_price_scores(bids: list[dict], method: str) -> dict[str, float]:
    compliant_bids = [b for b in bids if is_compliant(b)]
    prices = [
        (b["bidder_id"], (b.get("pricing") or {}).get("base_bid_cad"))
        for b in compliant_bids
    ]
    valid_prices = [(bid_id, p) for bid_id, p in prices if isinstance(p, (int, float)) and p > 0]
    if not valid_prices:
        return {}

    lowest = min(p for _, p in valid_prices)
    if method == "formula_lowest_ratio":
        return {bid_id: round2(100.0 * lowest / p) for bid_id, p in valid_prices}
    if method == "linear_interpolation":
        highest = max(p for _, p in valid_prices)
        span = highest - lowest if highest > lowest else 1.0
        return {bid_id: round2(100.0 * (highest - p) / span) for bid_id, p in valid_prices}
    if method == "lowest_compliant":
        return {bid_id: (100.0 if p == lowest else 0.0) for bid_id, p in valid_prices}
    raise ValueError(f"Unknown price_scoring_method: {method}")


def compute_weighted_total(raw: dict, weights: dict) -> float:
    total = 0.0
    for key in ("price",) + RATED_KEYS:
        sub = raw.get(key)
        w = weights.get(key)
        if sub is None or w is None:
            continue
        total += (sub * w) / 100.0
    return round2(total)


def compute_spread_percent(prices: list[float]) -> float:
    if not prices:
        return 0.0
    low, high = min(prices), max(prices)
    if low <= 0:
        return 0.0
    return round2(100.0 * (high - low) / low)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", required=True)
    args = ap.parse_args()

    manifest_path = Path(args.manifest)
    with manifest_path.open("r", encoding="utf-8") as f:
        manifest = json.load(f)

    weights = (
        (manifest.get("rfp") or {}).get("evaluation_criteria", {}).get("weighting")
        or {}
    )
    method = (
        (manifest.get("rfp") or {}).get("evaluation_criteria", {}).get("price_scoring_method")
        or "formula_lowest_ratio"
    )
    bids = manifest.get("bids") or []

    price_scores = compute_price_scores(bids, method)

    all_prices = [
        (b.get("pricing") or {}).get("base_bid_cad")
        for b in bids
        if isinstance((b.get("pricing") or {}).get("base_bid_cad"), (int, float))
    ]
    compliant_prices = [
        (b.get("pricing") or {}).get("base_bid_cad")
        for b in bids
        if is_compliant(b) and isinstance((b.get("pricing") or {}).get("base_bid_cad"), (int, float))
    ]

    compliant_scored: list[tuple[str, float]] = []
    for bid in bids:
        bid.setdefault("scores", {})
        if not is_compliant(bid):
            bid["scores"] = {**bid["scores"], "rank": None, "weighted_total": None, "compliant": False}
            continue

        raw = {"price": price_scores.get(bid["bidder_id"], 0.0)}
        raw.update({k: bid["scores"].get(k, 0.0) for k in RATED_KEYS})
        total = compute_weighted_total(raw, weights)

        bid["scores"].update(raw)
        bid["scores"]["weighted_total"] = total
        bid["scores"]["compliant"] = True
        compliant_scored.append((bid["bidder_id"], total))

    compliant_scored.sort(key=lambda pair: pair[1], reverse=True)
    rank_by_id = {bid_id: idx + 1 for idx, (bid_id, _) in enumerate(compliant_scored)}
    for bid in bids:
        if bid.get("scores", {}).get("compliant"):
            bid["scores"]["rank"] = rank_by_id.get(bid["bidder_id"])

    manifest["comparison"] = {
        "price_low_cad": min(compliant_prices) if compliant_prices else None,
        "price_high_cad": max(compliant_prices) if compliant_prices else None,
        "price_spread_percent": compute_spread_percent(compliant_prices),
        "all_bids_price_low_cad": min(all_prices) if all_prices else None,
        "all_bids_price_high_cad": max(all_prices) if all_prices else None,
        "compliant_bidders_count": len(compliant_scored),
        "recommended_bidder_id": compliant_scored[0][0] if compliant_scored else None,
    }

    with manifest_path.open("w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    print(f"Scored {len(compliant_scored)} compliant bid(s) of {len(bids)} total")
    if compliant_scored:
        print(f"Leader: {compliant_scored[0][0]} — {compliant_scored[0][1]}/100")
    return 0


if __name__ == "__main__":
    sys.exit(main())
