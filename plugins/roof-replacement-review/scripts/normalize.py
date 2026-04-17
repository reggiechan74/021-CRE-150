#!/usr/bin/env python3
"""Merge an RFP manifest and N bid manifests (plus optional qual/tech sidecars)
into a single tender manifest.

Inputs are JSON files produced by the roof-rfp-extract, roof-bid-extract,
roof-qualification-check, and roof-technical-review skills. Output conforms
to templates/bid_schema.json.

Sidecar merge: when --qual-sidecars or --tech-sidecars globs are provided,
each sidecar is matched by bidder_id to its base bid manifest and deep-merged.
Collisions on mandatory_gates / scores / scoring_rationale keys are fatal —
the two review skills have disjoint output ownership by design (see the
ownership tables in skills/roof-qualification-check/SKILL.md and
skills/roof-technical-review/SKILL.md). A collision means a skill wrote
outside its lane. Base bid manifests are distinguished from sidecars purely
by filename suffix — the --bids glob automatically filters out *.qual.json
and *.tech.json so a single manifests/ directory can hold all three file
classes safely.
"""
from __future__ import annotations

import argparse
import glob
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


DISJOINT_DICT_KEYS = ("mandatory_gates", "scores", "scoring_rationale")
CONCAT_LIST_KEYS = ("red_flags", "extraction_notes")


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def merge_sidecar(base: dict, sidecar: dict, sidecar_name: str) -> list[str]:
    """Merge sidecar into base in-place. Returns a list of collision errors;
    an empty list means the merge was clean."""
    errors: list[str] = []
    for key in DISJOINT_DICT_KEYS:
        incoming = sidecar.get(key) or {}
        if not incoming:
            continue
        existing = base.setdefault(key, {})
        for sub_key, sub_val in incoming.items():
            if sub_key in existing:
                errors.append(
                    f"collision on {key}.{sub_key} — already populated by earlier "
                    f"source; sidecar '{sidecar_name}' must not overwrite. "
                    "Check skill ownership boundaries."
                )
                continue
            existing[sub_key] = sub_val
    for key in CONCAT_LIST_KEYS:
        incoming = sidecar.get(key) or []
        if not incoming:
            continue
        base.setdefault(key, [])
        base[key].extend(incoming)
    return errors


def index_by_bidder(paths: list[Path]) -> dict[str, dict]:
    out: dict[str, dict] = {}
    for p in paths:
        data = load_json(p)
        bid_id = data.get("bidder_id")
        if not bid_id:
            raise ValueError(f"sidecar {p} missing bidder_id")
        if bid_id in out:
            raise ValueError(f"duplicate bidder_id '{bid_id}' across sidecars")
        out[bid_id] = data
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rfp", required=True, help="Path to rfp.json")
    ap.add_argument("--bids", required=True, help="Glob pattern for bid_*.json base manifests")
    ap.add_argument("--qual-sidecars", help="Glob for bid_*.qual.json files (optional)")
    ap.add_argument("--tech-sidecars", help="Glob for bid_*.tech.json files (optional)")
    ap.add_argument("--out", required=True, help="Path to write tender_manifest.json")
    args = ap.parse_args()

    rfp_path = Path(args.rfp)
    if not rfp_path.is_file():
        print(f"ERROR: RFP manifest not found: {rfp_path}", file=sys.stderr)
        return 1

    rfp_data = load_json(rfp_path)
    bid_paths = sorted(
        Path(p) for p in glob.glob(args.bids)
        if not p.endswith(".qual.json") and not p.endswith(".tech.json")
    )
    if not bid_paths:
        print(f"ERROR: no bid manifests matched {args.bids}", file=sys.stderr)
        return 1

    bids = [load_json(p) for p in bid_paths]

    qual_index: dict[str, dict] = {}
    tech_index: dict[str, dict] = {}
    if args.qual_sidecars:
        qual_paths = sorted(Path(p) for p in glob.glob(args.qual_sidecars))
        qual_index = index_by_bidder(qual_paths)
    if args.tech_sidecars:
        tech_paths = sorted(Path(p) for p in glob.glob(args.tech_sidecars))
        tech_index = index_by_bidder(tech_paths)

    all_errors: list[str] = []
    for bid in bids:
        bid_id = bid.get("bidder_id")
        if not bid_id:
            all_errors.append("base bid manifest missing bidder_id")
            continue
        if bid_id in qual_index:
            all_errors.extend(merge_sidecar(bid, qual_index[bid_id], f"{bid_id}.qual"))
        elif args.qual_sidecars:
            print(
                f"WARNING: no qual sidecar found for bidder '{bid_id}' — "
                "score.py will fail unless this is intentional",
                file=sys.stderr,
            )
        if bid_id in tech_index:
            all_errors.extend(merge_sidecar(bid, tech_index[bid_id], f"{bid_id}.tech"))
        elif args.tech_sidecars:
            print(
                f"WARNING: no tech sidecar found for bidder '{bid_id}' — "
                "score.py will fail unless this is intentional",
                file=sys.stderr,
            )

    bid_ids = {bid.get("bidder_id") for bid in bids}
    orphan_quals = sorted(set(qual_index) - bid_ids)
    orphan_techs = sorted(set(tech_index) - bid_ids)
    for orphan in orphan_quals:
        print(
            f"WARNING: qual sidecar for bidder '{orphan}' has no matching base bid "
            "manifest — likely a bidder_id typo; sidecar contents will be dropped",
            file=sys.stderr,
        )
    for orphan in orphan_techs:
        print(
            f"WARNING: tech sidecar for bidder '{orphan}' has no matching base bid "
            "manifest — likely a bidder_id typo; sidecar contents will be dropped",
            file=sys.stderr,
        )

    if all_errors:
        print("ERROR: sidecar merge failed:", file=sys.stderr)
        for line in all_errors:
            print(f"  - {line}", file=sys.stderr)
        return 1

    manifest = {
        "manifest_version": "1.0.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "project": rfp_data.get("project", {}),
        "rfp": rfp_data.get("rfp", {}),
        "bids": bids,
    }

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    print(f"Wrote tender manifest: {out_path}")
    print(f"  RFP: {rfp_path.name}")
    print(f"  Bids: {len(bids)}")
    if qual_index:
        print(f"  Qual sidecars merged: {len(qual_index)}")
    if tech_index:
        print(f"  Tech sidecars merged: {len(tech_index)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
