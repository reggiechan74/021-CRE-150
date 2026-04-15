#!/usr/bin/env python3
"""Bootstrap script for roof-replacement-review.

Creates the output directory structure beside an RFP and verifies Python
dependencies are available. Idempotent — safe to re-run.
"""
from __future__ import annotations

import sys
from pathlib import Path


REQUIRED_DIRS = [
    "roof-review-output",
    "roof-review-output/manifests",
]


def ensure_dirs(rfp_dir: Path) -> None:
    for sub in REQUIRED_DIRS:
        (rfp_dir / sub).mkdir(parents=True, exist_ok=True)


def check_deps() -> list[str]:
    missing: list[str] = []
    for mod in ("json", "argparse", "pathlib", "decimal"):
        try:
            __import__(mod)
        except ImportError:
            missing.append(mod)
    return missing


def main() -> int:
    if len(sys.argv) > 1:
        rfp_dir = Path(sys.argv[1]).resolve()
        if not rfp_dir.is_dir():
            print(f"ERROR: {rfp_dir} is not a directory", file=sys.stderr)
            return 1
        ensure_dirs(rfp_dir)
        print(f"Output dirs ready under {rfp_dir / 'roof-review-output'}")

    missing = check_deps()
    if missing:
        print(f"Missing stdlib modules: {missing}", file=sys.stderr)
        return 2
    print("Python stdlib dependencies: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
