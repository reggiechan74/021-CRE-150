"""Stage 1: parse property inputs into the typed reconciliation manifest."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
from datetime import datetime
from pathlib import Path

import yaml

PLUGIN_ROOT = Path(__file__).resolve().parent.parent
if str(PLUGIN_ROOT) not in sys.path:
    sys.path.insert(0, str(PLUGIN_ROOT))

from scripts.manifest import GLLine, Lease, Manifest, Property, Provenance, canonical_category


BUDGET_ROW_RE = re.compile(r"^\|\s*(?P<label>[^|]+?)\s*\|\s*\$(?P<amount>[0-9,]+(?:\.[0-9]{2})?)\s*\|")


BUDGET_CATEGORY_MAP = {
    "realty tax": "realty_tax",
    "utilities (electric, gas, water)": "utilities",
    "r&m (building systems, elevators, general)": "repairs_maintenance",
    "management fee (4% of projected egi $2,700,000)": "management_fee",
    "janitorial (common areas + tenant suites per lease)": "janitorial",
    "insurance (property + liability)": "insurance",
    "security (monitored alarm + patrol)": "security",
    "landscaping (maintenance + seasonal refresh)": "landscaping",
    "snow & ice management": "snow",
}


def _hash_files(paths: list[Path]) -> str:
    digest = hashlib.sha256()
    for path in sorted(paths):
        digest.update(path.name.encode("utf-8"))
        digest.update(path.read_bytes())
    return f"sha256:{digest.hexdigest()}"


def _read_budget(path: Path) -> dict[str, str]:
    if path.suffix.lower() == ".json":
        data = json.loads(path.read_text(encoding="utf-8"))
        return {str(k): str(v) for k, v in data.items()}

    budget: dict[str, str] = {}
    in_summary_table = False
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if line.startswith("| Category | FY2025 Budget |"):
            in_summary_table = True
            continue
        if in_summary_table and (not line.startswith("|") or line.startswith("| **Office Pool") or line.startswith("| **Retail Pool")):
            break
        if not in_summary_table:
            continue
        match = BUDGET_ROW_RE.match(line)
        if not match:
            continue
        label = match.group("label").strip().lower()
        if label.startswith("**total") or label == "category":
            break
        canonical = BUDGET_CATEGORY_MAP.get(label)
        if canonical:
            budget[canonical] = match.group("amount").replace(",", "")
    if not budget:
        raise ValueError(f"Could not parse budget rows from {path}")
    return budget


def _read_property(path: Path) -> Property:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return Property.model_validate(data)


def _read_leases(path: Path) -> list[Lease]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, dict) and "leases" in data:
        data = data["leases"]
    return [Lease.model_validate(item) for item in data]


def _read_gl(path: Path) -> list[GLLine]:
    gl_lines: list[GLLine] = []
    with open(path, newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for idx, row in enumerate(reader, start=1):
            raw_category = row["Category"].strip()
            canonical_category(raw_category)
            gl_lines.append(
                GLLine(
                    line_id=f"gl_{idx:04d}",
                    date=row["Date"].strip(),
                    account=row["Account"].strip(),
                    category_raw=raw_category,
                    vendor=row["Vendor"].strip(),
                    invoice_ref=row["Invoice Ref"].strip(),
                    memo=row["Memo"].strip(),
                    amount=row["Amount"].strip(),
                    pool_hint=row["Pool"].strip(),
                )
            )
    return gl_lines


def build_manifest(
    property_dir: Path,
    plugin_version: str = "0.1.0",
    fiscal_year: int = 2025,
    run_timestamp: datetime | None = None,
    operator: str | None = None,
) -> Manifest:
    property_dir = property_dir.resolve()
    property_path = property_dir / "property.yaml"
    leases_path = property_dir / "leases.json"
    gl_path = property_dir / "gl.csv"
    budget_path = property_dir / "budget.md"
    if not budget_path.exists():
        budget_path = property_dir / "budget.json"

    source_paths = [property_path, leases_path, gl_path, budget_path]
    manifest = Manifest(
        property=_read_property(property_path),
        fiscal_year=fiscal_year,
        budget=_read_budget(budget_path),
        leases=_read_leases(leases_path),
        gl_lines=_read_gl(gl_path),
        provenance=Provenance(
            plugin_version=plugin_version,
            run_timestamp=run_timestamp or datetime.utcnow(),
            inputs_hash=_hash_files(source_paths),
            operator=operator,
        ),
    )
    return manifest


def output_path_for(property_dir: Path) -> Path:
    return property_dir / "reconciliation-output" / "manifests" / "raw_manifest.json"


def main() -> None:
    parser = argparse.ArgumentParser(description="Build a raw reconciliation manifest from property inputs.")
    parser.add_argument("--property-dir", type=Path, required=True, help="Directory containing property.yaml, leases.json, gl.csv, and budget.md/json.")
    parser.add_argument("--output", type=Path, help="Output path for raw_manifest.json.")
    parser.add_argument("--plugin-version", default="0.1.0")
    parser.add_argument("--fiscal-year", type=int, default=2025)
    parser.add_argument("--operator")
    parser.add_argument("--run-timestamp", help="ISO timestamp override for deterministic tests.")
    args = parser.parse_args()

    timestamp = datetime.fromisoformat(args.run_timestamp) if args.run_timestamp else None
    manifest = build_manifest(
        property_dir=args.property_dir,
        plugin_version=args.plugin_version,
        fiscal_year=args.fiscal_year,
        run_timestamp=timestamp,
        operator=args.operator,
    )
    output = args.output or output_path_for(args.property_dir.resolve())
    output.parent.mkdir(parents=True, exist_ok=True)
    manifest.save(output)
    print(json.dumps({"output": str(output), "gl_lines": len(manifest.gl_lines), "leases": len(manifest.leases)}, indent=2))


if __name__ == "__main__":
    main()
