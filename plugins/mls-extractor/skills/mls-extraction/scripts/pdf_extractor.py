#!/usr/bin/env python3
"""
MLS PDF → raw JSON extractor (pdfplumber table-based).

Stage 1 of the two-stage pipeline. Format-agnostic: works on both the
column-aligned TREB/Lennard format and the cleaner vertical `Field | Value`
sanitized format.

Strategy:
  1. pdfplumber.extract_tables() on every page
  2. Flatten every cell into (label, value) pairs — a cell may contain
     multiple `Label: Value` lines separated by `\n`, or be a single
     2-col row from a true label/value table
  3. Segment properties by MLS# occurrences
  4. Map labels to canonical fields via a synonym dictionary
  5. Emit per-property JSON with 34 fields + _raw_text + _gaps

Why pdfplumber tables (vs. pdftotext + regex): the table extractor handles
whitespace/column variation natively, so the same code works across broker
templates without retuning regex anchors.
"""
from __future__ import annotations

import json
import os
import re
import sys
import time
from datetime import datetime
from pathlib import Path

try:
    import pdfplumber  # type: ignore
except ImportError:
    print("error: pdfplumber not installed. Run: pip install pdfplumber --break-system-packages -q",
          file=sys.stderr)
    sys.exit(1)

CURRENT_YEAR = datetime.now().year

# ---------------------------------------------------------------------------
# Label → canonical field synonym map
# ---------------------------------------------------------------------------

# Keys are canonical field names; values are lists of label aliases (lowercase).
LABEL_MAP: dict[str, list[str]] = {
    "available_sf":       ["total area", "available sf", "available", "area"],
    "net_asking_rent":    ["list price", "net rent", "net asking rent", "list"],
    "price_unit":         ["price unit"],
    "tmi_raw":            ["taxes"],  # parse $X/YYYY/T.M.I.
    "clear_height_raw":   ["clear height"],
    "apx_age":            ["apx age", "year built", "age"],
    "pct_office_raw":     ["ofc/apt area", "% office", "office area"],
    "shipping_doors_tl":  ["truck level", "truck level doors", "tl doors"],
    "shipping_doors_di":  ["drive-in", "drive in", "drive-in doors", "di doors"],
    "grade_level_doors":  ["grade level", "grade level doors"],
    "power_amps":         ["amps"],
    "power_volts":        ["volts"],
    "bay_size_raw":       ["bay size"],
    "lot_raw":            ["lot/bldg/unit/dim", "lot size"],
    "zoning":             ["zoning"],
    "hvac_raw":           ["a/c", "hvac"],
    "sprinkler_raw":      ["sprinklers", "sprinkler"],
    "rail_raw":           ["rail"],
    "crane_raw":          ["crane"],
    "occupancy_raw":      ["occupancy", "occup"],
    "trailer_raw":        ["#trl spc", "trl spc", "trailer parking"],
    "out_storage":        ["out storage", "outside storage", "excess land"],
    "heat":               ["heat"],
    "availability_raw":   ["possession", "availability date", "availability"],
    "sellers":            ["sellers", "owner"],
}

# Known non-data labels to skip (noise in table extraction)
SKIP_LABELS = {"field", "value", "", "property specs", "listing summary",
               "showing requirements", "listing brokerage", "brokerage"}

# ---------------------------------------------------------------------------
# Text utilities
# ---------------------------------------------------------------------------

def _norm(s) -> str:
    if s is None:
        return ""
    return re.sub(r"\s+", " ", str(s)).strip()


def _lower(s) -> str:
    return _norm(s).lower().rstrip(":").strip()


def _to_int(v) -> int:
    if v is None:
        return 0
    try:
        return int(float(re.sub(r"[^\d.-]", "", str(v)) or 0))
    except (ValueError, TypeError):
        return 0


def _to_float(v) -> float:
    if v is None:
        return 0.0
    try:
        return float(re.sub(r"[^\d.-]", "", str(v)) or 0)
    except (ValueError, TypeError):
        return 0.0


def _yn(v) -> bool:
    return _norm(v).upper().startswith("Y")


# ---------------------------------------------------------------------------
# Table → (label, value) pair extraction
# ---------------------------------------------------------------------------

PAIR_INLINE_RE = re.compile(r"([A-Za-z#/%][^:\n]{0,40}?):\s*([^\n]*)")


def pairs_from_cell(cell: str | None) -> list[tuple[str, str]]:
    """A cell may contain multiple `Label: Value` lines (TREB format).

    Split on newlines; for each line, match `Label: Value` and collect.
    Also handles lines without colons by ignoring them (prose).
    """
    if not cell:
        return []
    pairs: list[tuple[str, str]] = []
    for line in cell.split("\n"):
        line = line.strip()
        if not line or ":" not in line:
            continue
        # A single line can contain multiple "Label: Value" pairs in TREB format
        # e.g. "Occup: Vacant Lse Term Mnths: 60/180"
        # Strategy: split on runs of 2+ spaces, then re-match each segment.
        segments = re.split(r"\s{2,}", line) if "  " in line else [line]
        for seg in segments:
            m = re.match(r"^([A-Za-z#/%][^:]{0,40}?):\s*(.*)$", seg)
            if m:
                label, value = m.group(1), m.group(2)
                pairs.append((label.strip(), value.strip()))
    return pairs


def pairs_from_row(row: list) -> list[tuple[str, str]]:
    """A table row of cells. If it's a clean 2-col `[label, value]`, return
    that directly. Otherwise, extract pairs from each cell's multi-line text.
    """
    cells = [c for c in row if c is not None]
    pairs: list[tuple[str, str]] = []

    if len(cells) == 2:
        label, value = _norm(cells[0]), _norm(cells[1])
        if label and value and ":" not in label and len(label) < 50:
            # Clean label/value row (sanitized format)
            pairs.append((label, value))
            return pairs

    # Multi-line cells — walk each
    for cell in cells:
        pairs.extend(pairs_from_cell(cell if isinstance(cell, str) else None))
    return pairs


# ---------------------------------------------------------------------------
# PDF → property records
# ---------------------------------------------------------------------------

MLS_RE = re.compile(r"MLS#[:\s]+([A-Z]\d{6,})", re.IGNORECASE)
DOM_RE = re.compile(r"DOM[:\s|]+(\d+)", re.IGNORECASE)


def extract_properties(pdf_path: str) -> list[dict]:
    """Walk all pages, collect (label, value) pairs + prose, segment by MLS#."""
    page_records: list[dict] = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables() or []
            text = page.extract_text() or ""
            pairs: list[tuple[str, str]] = []
            for tbl in tables:
                for row in tbl:
                    pairs.extend(pairs_from_row(row))
            # Also parse inline pairs from raw text (catches text outside tables)
            pairs.extend(pairs_from_cell(text))
            page_records.append({"text": text, "pairs": pairs})

    # Segment: find MLS# occurrences across concatenated text
    full_text = "\n==PAGE==\n".join(r["text"] for r in page_records)
    mls_hits = [(m.group(1), m.start()) for m in MLS_RE.finditer(full_text)]
    if not mls_hits:
        return []

    # Determine which page each MLS# starts on
    # We'll accumulate pairs per property by walking pages and switching on MLS# change.
    # Simpler: group pairs by MLS# using page-level MLS# assignment.
    pages_per_mls: dict[str, list[int]] = {}
    current_mls = None
    for pi, rec in enumerate(page_records):
        m = MLS_RE.search(rec["text"])
        if m:
            current_mls = m.group(1)
        if current_mls:
            pages_per_mls.setdefault(current_mls, []).append(pi)

    # Preserve order of first occurrence
    seen: list[str] = []
    for mls, _ in mls_hits:
        if mls not in seen:
            seen.append(mls)

    properties: list[dict] = []
    for mls in seen:
        pidxs = pages_per_mls.get(mls, [])
        all_pairs: list[tuple[str, str]] = []
        all_text_parts: list[str] = []
        for pi in pidxs:
            all_pairs.extend(page_records[pi]["pairs"])
            all_text_parts.append(page_records[pi]["text"])
        properties.append({
            "mls_number": mls,
            "pairs": all_pairs,
            "raw_text": "\n".join(all_text_parts),
        })
    return properties


# ---------------------------------------------------------------------------
# Pair → canonical field mapping
# ---------------------------------------------------------------------------

def build_label_index() -> dict[str, str]:
    """alias → canonical field. Longer aliases first to prevent collisions."""
    idx: dict[str, str] = {}
    for canonical, aliases in LABEL_MAP.items():
        for a in aliases:
            idx[a.lower()] = canonical
    return idx


LABEL_INDEX = build_label_index()


def pairs_to_dict(pairs: list[tuple[str, str]]) -> dict:
    """Collapse duplicate labels by keeping the first non-empty value."""
    out: dict = {}
    for label, value in pairs:
        key = _lower(label)
        if key in SKIP_LABELS:
            continue
        canonical = LABEL_INDEX.get(key)
        if not canonical:
            continue
        if canonical not in out and value:
            out[canonical] = value
    return out


# ---------------------------------------------------------------------------
# Canonical-field computation
# ---------------------------------------------------------------------------

def parse_clear_height(raw: str) -> float:
    """e.g. `36 0` → 36.0 (ft + in), `40 0` → 40.0, `36.5` → 36.5."""
    if not raw:
        return 0.0
    m = re.match(r"\s*(\d+(?:\.\d+)?)\s*(\d+)?", raw.strip())
    if not m:
        return 0.0
    ft = float(m.group(1))
    inches = float(m.group(2)) if m.group(2) else 0.0
    return round(ft + inches / 12.0, 2)


def parse_bay_depth(raw: str) -> float:
    m = re.match(r"\s*(\d+(?:\.\d+)?)\s*x", raw.strip(), re.IGNORECASE)
    return float(m.group(1)) if m else 0.0


def parse_tmi(raw: str) -> float:
    """`$4/2025/T.M.I.` or `$3.87/2025/T.M.I.` → first dollar amount."""
    m = re.search(r"\$?([\d.,]+)\s*/\s*\d{4}\s*/\s*T\.?M\.?I\.?", raw, re.IGNORECASE)
    if m:
        return _to_float(m.group(1))
    return _to_float(raw)


def parse_pct_office(raw: str) -> float:
    """`3 %` or `3%` → 0.03."""
    v = _to_float(raw)
    return round(v / 100.0, 4) if v else 0.0


def parse_lot_acres(raw: str) -> float:
    m = re.search(r"([\d.,]+)\s*(acres|Sq\s*Ft)?", raw, re.IGNORECASE)
    if not m:
        return 0.0
    v = _to_float(m.group(1))
    unit = (m.group(2) or "").lower()
    if "sq" in unit:
        return round(v / 43560.0, 2)
    return v


AGE_BAND_RE = re.compile(r"(\d+)\s*-\s*(\d+)")


def parse_year_built(raw: str) -> int:
    if not raw:
        return 0
    s = raw.strip().lower()
    if "new" in s:
        return CURRENT_YEAR
    m = AGE_BAND_RE.match(s)
    if m:
        mid = (int(m.group(1)) + int(m.group(2))) // 2
        return CURRENT_YEAR - mid
    m = re.match(r"(\d{4})", s)
    if m:
        return int(m.group(1))
    return 0


def parse_hvac(raw: str) -> int:
    s = raw.strip().upper()
    if s.startswith("Y") or "100" in s:
        return 1
    if s.startswith("PART") or "50" in s:
        return 2
    if s.startswith("N") or "0" in s:
        return 3
    return 0


def parse_sprinkler(raw: str, remarks: str) -> int:
    if re.search(r"\bESFR\b", remarks, re.IGNORECASE):
        return 1
    s = raw.strip().upper()
    if s.startswith("Y"):
        return 2
    if s.startswith("N"):
        return 3
    return 0


def parse_occupancy(raw: str) -> int:
    s = raw.strip().lower()
    if "vacant" in s:
        return 1
    if "occup" in s or "lease" in s or "tenant" in s:
        return 2
    return 0


def infer_class(clear_ft: float, sprinkler: int, remarks: str) -> int:
    """A/B/C inference when the PDF doesn't state it explicitly."""
    rem = (remarks or "").lower()
    modern = any(k in rem for k in [
        "state of the art", "state-of-the-art", "zero carbon",
        "leed", "net carbon", "newest", "modern precast", "prestigious",
    ])
    if clear_ft >= 32 and (sprinkler == 1 or modern):
        return 1
    if clear_ft >= 28:
        return 2
    if clear_ft >= 24:
        return 2
    return 3


# ---------------------------------------------------------------------------
# Address, remarks, broker extraction (still text-based — labels are too varied)
# ---------------------------------------------------------------------------

ADDRESS_TREB_RE = re.compile(
    r"([\d][^\n]{3,80}?)\s+List:\s*\$[\d.,]+\s*\n[^\n]*?"
    r"([A-Z][a-z]+\s+Ontario\s+[A-Z]\d[A-Z]\s?\d[A-Z]\d)",
)
ADDRESS_SANITIZED_RE = re.compile(
    r"Location:\s*-\s*([^\-\n]+?)\s*-\s*([A-Z][a-z]+\s+Ontario\s+[A-Z]\d[A-Z]\s?\d[A-Z]\d)",
)
PROPERTY_HEADER_RE = re.compile(r"Property\s+\d+:\s*([^\n]+)")


def extract_address(raw_text: str) -> str:
    m = ADDRESS_SANITIZED_RE.search(raw_text)
    if m:
        return f"{m.group(1).strip()}, {m.group(2).strip()}, Canada"
    m = ADDRESS_TREB_RE.search(raw_text)
    if m:
        street = re.sub(r"\s+", " ", m.group(1)).strip()
        return f"{street}, {m.group(2).strip()}, Canada"
    m = PROPERTY_HEADER_RE.search(raw_text)
    return m.group(1).strip() if m else ""


REMARKS_RE = re.compile(
    r"Client\s+Remarks?:?\s*\n?(.+?)(?=(?:Extras:|Brokerage\s+Remarks?:|Brkage\s+Remks?:|"
    r"Inclusions:|Showing\s+Requirements:|Listing\s+Brokerage:|Page\s+\d+|$))",
    re.DOTALL | re.IGNORECASE,
)


def extract_remarks(raw_text: str) -> str:
    m = REMARKS_RE.search(raw_text)
    if not m:
        return ""
    return _norm(m.group(1))[:500]


BROKER_RE = re.compile(
    r"(?:Brokerage:\s*|Prepared\s+By:\s*)([A-Z][A-Z0-9 .,'&-]{4,80}?)(?:,\s*Salesperson|\s*$|\n)",
)


def extract_broker(raw_text: str) -> str:
    m = BROKER_RE.search(raw_text)
    return _norm(m.group(1)) if m else ""


def extract_unit(raw_text: str, address: str) -> str:
    # Prefer explicit "Unit: X" labels; else blank
    m = re.search(r"\bUnit\s*[:#]\s*([A-Za-z0-9-]+)", raw_text)
    return m.group(1) if m else ""


DOM_HEADER_RE = re.compile(r"DOM[:\s|]+(\d+)", re.IGNORECASE)


# ---------------------------------------------------------------------------
# Assembly
# ---------------------------------------------------------------------------

CRITICAL = [
    "address", "available_sf", "net_asking_rent", "tmi", "year_built",
    "clear_height_ft", "pct_office_space", "class",
]


def build_property(rec: dict, source_pdf: str) -> dict:
    raw_text = rec["raw_text"]
    d = pairs_to_dict(rec["pairs"])

    address = extract_address(raw_text)
    remarks = extract_remarks(raw_text)
    broker = extract_broker(raw_text)

    net_rent = _to_float(d.get("net_asking_rent", ""))
    tmi = parse_tmi(d.get("tmi_raw", ""))
    clear_ft = parse_clear_height(d.get("clear_height_raw", ""))
    year_built = parse_year_built(d.get("apx_age", ""))
    pct_office = parse_pct_office(d.get("pct_office_raw", ""))
    sprinkler = parse_sprinkler(d.get("sprinkler_raw", ""), remarks + " " + raw_text)

    dom_m = DOM_HEADER_RE.search(raw_text)
    dom = int(dom_m.group(1)) if dom_m else 0

    f = {
        "address": address,
        "unit": extract_unit(raw_text, address),
        "available_sf": _to_int(d.get("available_sf", "")),
        "net_asking_rent": net_rent,
        "tmi": tmi,
        "year_built": year_built,
        "clear_height_ft": clear_ft,
        "pct_office_space": pct_office,
        "parking_ratio": 0.0,
        "class": 0,  # inferred below
        "shipping_doors_tl": _to_int(d.get("shipping_doors_tl", "")),
        "shipping_doors_di": _to_int(d.get("shipping_doors_di", "")),
        "power_amps": _to_int(d.get("power_amps", "")),
        "bay_depth_ft": parse_bay_depth(d.get("bay_size_raw", "")),
        "lot_size_acres": parse_lot_acres(d.get("lot_raw", "")),
        "hvac_coverage": parse_hvac(d.get("hvac_raw", "")),
        "sprinkler_type": sprinkler,
        "rail_access": _yn(d.get("rail_raw", "")),
        "crane": _yn(d.get("crane_raw", "")),
        "occupancy_status": parse_occupancy(d.get("occupancy_raw", "")),
        "trailer_parking": bool(_to_int(d.get("trailer_raw", ""))),
        "secure_shipping": bool(re.search(r"secure\s+shipping|fenced\s+yard", raw_text, re.IGNORECASE)),
        "excess_land": _yn(d.get("out_storage", ""))
            or bool(re.search(r"excess\s+land", raw_text, re.IGNORECASE)),
        "grade_level_doors": _to_int(d.get("grade_level_doors", "")),
        "days_on_market": dom,
        "zoning": _norm(d.get("zoning", "")),
        "availability_date": _norm(d.get("availability_raw", "")).replace("Other Remarks: ", "").replace("Remarks: ", ""),
        "mls_number": rec["mls_number"],
        "broker_name": broker,
        "client_remarks": remarks,
        "is_subject": False,
        "reported_market": "",
        "report_generated_at": datetime.now().strftime("%Y-%m-%d"),
        "source_pdf": source_pdf,
    }
    f["class"] = infer_class(clear_ft, sprinkler, remarks)
    f["gross_rent"] = round(f["net_asking_rent"] + f["tmi"], 2)
    f["building_age_years"] = (CURRENT_YEAR - f["year_built"]) if f["year_built"] else 0

    gaps = [k for k in CRITICAL if not f.get(k)]
    if f["net_asking_rent"] in (0.0, 1.0):
        gaps.append("net_asking_rent_suspicious")
    f["_gaps"] = gaps
    f["_raw_text"] = raw_text
    return f


def extract(pdf_path: str) -> dict:
    t0 = time.time()
    records = extract_properties(pdf_path)
    source_pdf = os.path.basename(pdf_path)
    properties = [build_property(r, source_pdf) for r in records]
    return {
        "source_pdf": source_pdf,
        "total_properties": len(properties),
        "extraction_method": "pdfplumber-tables",
        "elapsed_sec": round(time.time() - t0, 2),
        "extraction_date": datetime.now().strftime("%Y-%m-%d"),
        "properties": properties,
    }


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: pdf_extractor.py <pdf_path> [output.json]", file=sys.stderr)
        return 2
    pdf = sys.argv[1]
    if not Path(pdf).is_file():
        print(f"error: file not found: {pdf}", file=sys.stderr)
        return 1
    result = extract(pdf)
    out = sys.argv[2] if len(sys.argv) > 2 else None
    payload = json.dumps(result, indent=2, ensure_ascii=False)
    if out:
        Path(out).write_text(payload, encoding="utf-8")
        print(
            f"[pdf_extractor] {result['total_properties']} properties "
            f"via {result['extraction_method']} in {result['elapsed_sec']}s → {out}",
            file=sys.stderr,
        )
    else:
        print(payload)
    return 0


if __name__ == "__main__":
    sys.exit(main())
