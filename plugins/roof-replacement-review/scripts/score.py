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

ALL_WEIGHT_KEYS = ("price",) + RATED_KEYS

VALID_METHODS = ("formula_lowest_ratio", "linear_interpolation", "lowest_compliant")


def load_config_overrides(config_path: Path) -> dict:
    """Load evaluation_config.yaml. Returns dict with optional 'weighting' and
    'price_scoring_method' keys. Raises ValueError for malformed content."""
    try:
        import yaml
    except ImportError as exc:
        raise RuntimeError(
            "PyYAML is required to use --config. Install with: pip install pyyaml"
        ) from exc

    with config_path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}

    if not isinstance(data, dict):
        raise ValueError(f"{config_path}: top-level must be a mapping")

    result: dict = {}
    if "weighting" in data:
        w = data["weighting"]
        if not isinstance(w, dict):
            raise ValueError(f"{config_path}: 'weighting' must be a mapping")
        unknown = set(w.keys()) - set(ALL_WEIGHT_KEYS)
        if unknown:
            raise ValueError(f"{config_path}: unknown weighting keys {sorted(unknown)}; valid keys are {list(ALL_WEIGHT_KEYS)}")
        for k, v in w.items():
            if not isinstance(v, (int, float)):
                raise ValueError(f"{config_path}: weighting.{k} must be numeric, got {type(v).__name__}")
        result["weighting"] = {k: float(v) for k, v in w.items()}

    if "price_scoring_method" in data:
        m = data["price_scoring_method"]
        if m not in VALID_METHODS:
            raise ValueError(f"{config_path}: price_scoring_method must be one of {VALID_METHODS}, got {m!r}")
        result["price_scoring_method"] = m

    return result


def apply_overrides(manifest: dict, overrides: dict) -> tuple[dict, str, str]:
    """Merge config overrides into manifest weighting + method.
    Returns (final_weights, final_method, source_description).
    Validates that final weights sum to 100 (±0.01).
    """
    crit = manifest.setdefault("rfp", {}).setdefault("evaluation_criteria", {})
    base_weights = dict(crit.get("weighting") or {})
    base_method = crit.get("price_scoring_method") or "formula_lowest_ratio"

    if "weighting" in overrides:
        # Config weights REPLACE the RFP weights (not partial merge) — any key
        # omitted from the config is treated as 0 so the override is explicit.
        base_weights = overrides["weighting"]
    if "price_scoring_method" in overrides:
        base_method = overrides["price_scoring_method"]

    total = sum(base_weights.get(k, 0.0) for k in ALL_WEIGHT_KEYS)
    if abs(total - 100.0) > 0.01:
        raise ValueError(
            f"Weights must sum to 100, got {total}. Keys: "
            + ", ".join(f"{k}={base_weights.get(k, 0)}" for k in ALL_WEIGHT_KEYS)
        )

    source = "rfp_manifest"
    if "weighting" in overrides and "price_scoring_method" in overrides:
        source = "config_override (weights + method)"
    elif "weighting" in overrides:
        source = "config_override (weights only)"
    elif "price_scoring_method" in overrides:
        source = "config_override (method only)"

    return base_weights, base_method, source


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
    ap.add_argument(
        "--config",
        help="Optional evaluation_config.yaml to override RFP weights and price_scoring_method",
    )
    args = ap.parse_args()

    manifest_path = Path(args.manifest)
    with manifest_path.open("r", encoding="utf-8") as f:
        manifest = json.load(f)

    overrides: dict = {}
    if args.config:
        config_path = Path(args.config)
        if not config_path.is_file():
            print(f"ERROR: config file not found: {config_path}", file=sys.stderr)
            return 1
        try:
            overrides = load_config_overrides(config_path)
        except (ValueError, RuntimeError) as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
            return 1

    try:
        weights, method, source = apply_overrides(manifest, overrides)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    # Persist the effective values back into the manifest so downstream renderers
    # (scoring_matrix, memo) see what was actually used.
    crit = manifest.setdefault("rfp", {}).setdefault("evaluation_criteria", {})
    crit["weighting"] = weights
    crit["price_scoring_method"] = method
    crit["weighting_source"] = source

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
    print(f"Weights source: {source}")
    if compliant_scored:
        print(f"Leader: {compliant_scored[0][0]} — {compliant_scored[0][1]}/100")
    return 0


if __name__ == "__main__":
    sys.exit(main())
