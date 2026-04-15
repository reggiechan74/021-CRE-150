#!/usr/bin/env python3
"""Merge an RFP manifest and N bid manifests into a single tender manifest.

Inputs are JSON files produced by the roof-rfp-extract and roof-bid-extract
skills. Output conforms to templates/bid_schema.json.
"""
from __future__ import annotations

import argparse
import glob
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rfp", required=True, help="Path to rfp.json")
    ap.add_argument("--bids", required=True, help="Glob pattern for bid_*.json files")
    ap.add_argument("--out", required=True, help="Path to write tender_manifest.json")
    args = ap.parse_args()

    rfp_path = Path(args.rfp)
    if not rfp_path.is_file():
        print(f"ERROR: RFP manifest not found: {rfp_path}", file=sys.stderr)
        return 1

    rfp_data = load_json(rfp_path)
    bid_paths = sorted(Path(p) for p in glob.glob(args.bids))
    if not bid_paths:
        print(f"ERROR: no bid manifests matched {args.bids}", file=sys.stderr)
        return 1

    bids = [load_json(p) for p in bid_paths]

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
    return 0


if __name__ == "__main__":
    sys.exit(main())
