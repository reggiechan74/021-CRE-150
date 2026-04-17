"""Typed manifest models and shared domain helpers for CAM reconciliation.

Models are stdlib ``@dataclass`` classes with explicit ``from_dict``
classmethods and per-field coercion in ``__post_init__``. No pydantic.
See ``scripts/validation.py`` for ``ValidationError`` and
``ManifestJSONEncoder``; see plan-rewrite-cam-reconciliation-cre.md
Step 2 for why we do not ship a generic coercion engine.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field, fields
from datetime import date, datetime
from decimal import Decimal, ROUND_HALF_UP
from enum import Enum
from pathlib import Path
from typing import Any, Literal, Optional

from scripts.validation import (
    ManifestJSONEncoder,
    ValidationError,
    check_unknown_keys,
)


MONEY_PLACES = Decimal("0.01")


def money(value: Decimal | int | float | str) -> Decimal:
    """Round a value to currency precision using standard commercial rounding."""
    return Decimal(str(value)).quantize(MONEY_PLACES, rounding=ROUND_HALF_UP)


def slugify(value: str) -> str:
    cleaned = []
    for char in value.lower():
        if char.isalnum():
            cleaned.append(char)
        else:
            cleaned.append("_")
    slug = "".join(cleaned)
    while "__" in slug:
        slug = slug.replace("__", "_")
    return slug.strip("_")


# --- helpers for per-model coercion -----------------------------------------


def _to_decimal(value: Any) -> Decimal:
    if isinstance(value, Decimal):
        return value
    return Decimal(str(value))


def _to_optional_decimal(value: Any) -> Optional[Decimal]:
    if value is None:
        return None
    return _to_decimal(value)


def _to_datetime(value: Any) -> datetime:
    if isinstance(value, datetime):
        return value
    return datetime.fromisoformat(value)


def _coerce_any_decimals(obj: Any, decimal_keys: set[str]) -> Any:
    """Walk ``obj`` (dict or list) and coerce named keys to Decimal in place.

    Used for ``dict[str, Any]`` fields such as ``base_year_adjustment`` and
    ``cap_adjustment`` that carry embedded money values through JSON as
    strings. Any key listed in ``decimal_keys`` gets wrapped with Decimal.
    """
    if isinstance(obj, dict):
        for key, value in list(obj.items()):
            if key in decimal_keys and value is not None and not isinstance(value, Decimal):
                obj[key] = _to_decimal(value)
            elif isinstance(value, (dict, list)):
                _coerce_any_decimals(value, decimal_keys)
    elif isinstance(obj, list):
        for item in obj:
            _coerce_any_decimals(item, decimal_keys)
    return obj


# --- enums ------------------------------------------------------------------


class LeaseType(str, Enum):
    NET = "net"
    NET_WITH_CAP = "net_with_cap"
    BASE_YEAR = "base_year"
    MODIFIED_GROSS = "modified_gross"
    NET_WITH_EXCLUSIONS = "net_with_exclusions"


class PoolName(str, Enum):
    OFFICE = "office"
    RETAIL = "retail"
    SHARED = "shared"


# --- models -----------------------------------------------------------------


@dataclass
class LeaseCitation:
    doc: str
    section: str
    quote: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "LeaseCitation":
        return cls(doc=data["doc"], section=data["section"], quote=data["quote"])


@dataclass
class CapConfig:
    base_year: int
    base_year_cam_psf: Decimal
    annual_increase_rate: Decimal
    uncontrollable_categories: list[str]

    def __post_init__(self) -> None:
        self.base_year_cam_psf = _to_decimal(self.base_year_cam_psf)
        self.annual_increase_rate = _to_decimal(self.annual_increase_rate)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "CapConfig":
        return cls(
            base_year=int(data["base_year"]),
            base_year_cam_psf=_to_decimal(data["base_year_cam_psf"]),
            annual_increase_rate=_to_decimal(data["annual_increase_rate"]),
            uncontrollable_categories=list(data.get("uncontrollable_categories", [])),
        )


@dataclass
class BaseYearConfig:
    year: int
    cam_psf: Decimal
    gross_up_to_percent: Decimal = Decimal("1.0")

    def __post_init__(self) -> None:
        self.cam_psf = _to_decimal(self.cam_psf)
        self.gross_up_to_percent = _to_decimal(self.gross_up_to_percent)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "BaseYearConfig":
        return cls(
            year=int(data["year"]),
            cam_psf=_to_decimal(data["cam_psf"]),
            gross_up_to_percent=_to_decimal(data.get("gross_up_to_percent", "1.0")),
        )


@dataclass
class Lease:
    tenant_id: str
    tenant_name: str
    unit_label: str
    rsf: int
    pool: PoolName
    pro_rata_of_pool: Decimal
    lease_type: LeaseType
    excluded_categories: list[str] = field(default_factory=list)
    cap: Optional[CapConfig] = None
    base_year: Optional[BaseYearConfig] = None
    specific_exclusions: list[dict[str, Any]] = field(default_factory=list)
    clause_refs: dict[str, LeaseCitation] = field(default_factory=dict)
    annual_prebilled: Optional[Decimal] = None
    is_vacant: bool = False

    def __post_init__(self) -> None:
        if not isinstance(self.pool, PoolName):
            self.pool = PoolName(self.pool)
        if not isinstance(self.lease_type, LeaseType):
            self.lease_type = LeaseType(self.lease_type)
        self.pro_rata_of_pool = _to_decimal(self.pro_rata_of_pool)
        self.annual_prebilled = _to_optional_decimal(self.annual_prebilled)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Lease":
        cap = data.get("cap")
        base_year = data.get("base_year")
        clause_refs_raw = data.get("clause_refs") or {}
        return cls(
            tenant_id=data["tenant_id"],
            tenant_name=data["tenant_name"],
            unit_label=data["unit_label"],
            rsf=int(data["rsf"]),
            pool=PoolName(data["pool"]),
            pro_rata_of_pool=_to_decimal(data["pro_rata_of_pool"]),
            lease_type=LeaseType(data["lease_type"]),
            excluded_categories=list(data.get("excluded_categories", [])),
            cap=CapConfig.from_dict(cap) if cap else None,
            base_year=BaseYearConfig.from_dict(base_year) if base_year else None,
            specific_exclusions=[dict(rule) for rule in data.get("specific_exclusions", [])],
            clause_refs={key: LeaseCitation.from_dict(value) for key, value in clause_refs_raw.items()},
            annual_prebilled=_to_optional_decimal(data.get("annual_prebilled")),
            is_vacant=bool(data.get("is_vacant", False)),
        )


@dataclass
class Pool:
    name: PoolName
    rsf: int
    share_of_total: Decimal

    def __post_init__(self) -> None:
        if not isinstance(self.name, PoolName):
            self.name = PoolName(self.name)
        self.share_of_total = _to_decimal(self.share_of_total)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Pool":
        return cls(
            name=PoolName(data["name"]),
            rsf=int(data["rsf"]),
            share_of_total=_to_decimal(data["share_of_total"]),
        )


@dataclass
class Property:
    id: str
    name: str
    address: str
    rsf_total: int
    rsf_retail: int
    rsf_office: int
    pools: list[Pool]
    gross_potential_income: Optional[Decimal] = None
    effective_gross_income: Optional[Decimal] = None
    projected_effective_gross_income: Optional[Decimal] = None
    vacancy_loss: Optional[Decimal] = None
    credit_allowance: Optional[Decimal] = None

    def __post_init__(self) -> None:
        self.gross_potential_income = _to_optional_decimal(self.gross_potential_income)
        self.effective_gross_income = _to_optional_decimal(self.effective_gross_income)
        self.projected_effective_gross_income = _to_optional_decimal(self.projected_effective_gross_income)
        self.vacancy_loss = _to_optional_decimal(self.vacancy_loss)
        self.credit_allowance = _to_optional_decimal(self.credit_allowance)

    def pool_rsf(self, pool: PoolName) -> int:
        if pool == PoolName.OFFICE:
            return self.rsf_office
        if pool == PoolName.RETAIL:
            return self.rsf_retail
        return self.rsf_total

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Property":
        return cls(
            id=data["id"],
            name=data["name"],
            address=data["address"],
            rsf_total=int(data["rsf_total"]),
            rsf_retail=int(data["rsf_retail"]),
            rsf_office=int(data["rsf_office"]),
            pools=[Pool.from_dict(item) for item in data.get("pools", [])],
            gross_potential_income=_to_optional_decimal(data.get("gross_potential_income")),
            effective_gross_income=_to_optional_decimal(data.get("effective_gross_income")),
            projected_effective_gross_income=_to_optional_decimal(data.get("projected_effective_gross_income")),
            vacancy_loss=_to_optional_decimal(data.get("vacancy_loss")),
            credit_allowance=_to_optional_decimal(data.get("credit_allowance")),
        )


_ALLOWED_CONFIDENCE = {"high", "medium", "low"}


@dataclass
class Classification:
    recoverable: bool
    reason: str
    lease_citation: Optional[LeaseCitation] = None
    pool: Optional[PoolName] = None
    pool_specific: bool = False
    confidence: Literal["high", "medium", "low"] = "high"
    human_review_flag: bool = False
    matched_against: Optional[str] = None
    normalized_category: Optional[str] = None
    recoverable_amount: Optional[Decimal] = None

    def __post_init__(self) -> None:
        if self.pool is not None and not isinstance(self.pool, PoolName):
            self.pool = PoolName(self.pool)
        self.recoverable_amount = _to_optional_decimal(self.recoverable_amount)
        if self.confidence not in _ALLOWED_CONFIDENCE:
            raise ValidationError(
                f"Classification.confidence must be one of {sorted(_ALLOWED_CONFIDENCE)}, got {self.confidence!r}"
            )

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Classification":
        lease_citation = data.get("lease_citation")
        return cls(
            recoverable=bool(data["recoverable"]),
            reason=data["reason"],
            lease_citation=LeaseCitation.from_dict(lease_citation) if lease_citation else None,
            pool=PoolName(data["pool"]) if data.get("pool") else None,
            pool_specific=bool(data.get("pool_specific", False)),
            confidence=data.get("confidence", "high"),
            human_review_flag=bool(data.get("human_review_flag", False)),
            matched_against=data.get("matched_against"),
            normalized_category=data.get("normalized_category"),
            recoverable_amount=_to_optional_decimal(data.get("recoverable_amount")),
        )


@dataclass
class GLLine:
    line_id: str
    date: str
    account: str
    category_raw: str
    vendor: str
    invoice_ref: str
    memo: str
    amount: Decimal
    pool_hint: str
    classification: Optional[Classification] = None
    allocation: dict[str, Decimal] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.amount = _to_decimal(self.amount)
        self.allocation = {key: _to_decimal(value) for key, value in self.allocation.items()}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "GLLine":
        classification = data.get("classification")
        allocation = data.get("allocation") or {}
        return cls(
            line_id=data["line_id"],
            date=data["date"],
            account=data["account"],
            category_raw=data["category_raw"],
            vendor=data["vendor"],
            invoice_ref=data["invoice_ref"],
            memo=data["memo"],
            amount=_to_decimal(data["amount"]),
            pool_hint=data["pool_hint"],
            classification=Classification.from_dict(classification) if classification else None,
            allocation={key: _to_decimal(value) for key, value in allocation.items()},
        )


@dataclass
class ExclusionApplied:
    category: str
    amount_removed: Decimal
    reason: str
    citation_ref: Optional[LeaseCitation] = None
    reallocated_to: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.amount_removed = _to_decimal(self.amount_removed)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ExclusionApplied":
        citation = data.get("citation_ref")
        return cls(
            category=data["category"],
            amount_removed=_to_decimal(data["amount_removed"]),
            reason=data["reason"],
            citation_ref=LeaseCitation.from_dict(citation) if citation else None,
            reallocated_to=list(data.get("reallocated_to", [])),
        )


@dataclass
class DirectBillApplied:
    category: str
    amount_billed: Decimal
    reason: str
    citation_ref: Optional[LeaseCitation] = None
    source_gl_ids: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.amount_billed = _to_decimal(self.amount_billed)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "DirectBillApplied":
        citation = data.get("citation_ref")
        return cls(
            category=data["category"],
            amount_billed=_to_decimal(data["amount_billed"]),
            reason=data["reason"],
            citation_ref=LeaseCitation.from_dict(citation) if citation else None,
            source_gl_ids=list(data.get("source_gl_ids", [])),
        )


# Keys that carry Decimal values inside the opaque ``dict[str, Any]`` fields
# below. JSON stores them as strings; we rehydrate on load so arithmetic at
# read sites (allocate.py, statement.py, tests) sees real Decimals.
_BASE_YEAR_DECIMAL_KEYS = {"base_amount", "amount_removed"}
_CAP_DECIMAL_KEYS = {
    "controllable_uncapped",
    "uncontrollable_uncapped",
    "controllable_cap_ceiling_psf",
    "controllable_cap_ceiling_total",
    "landlord_absorbed",
}
_CITATION_DECIMAL_KEYS = {"contribution_amount"}
_MATH_TRACE_DECIMAL_KEYS = {"direct_bill_total"}


def _coerce_math_trace(trace: dict[str, Any]) -> dict[str, Any]:
    if "direct_bill_total" in trace and trace["direct_bill_total"] is not None:
        trace["direct_bill_total"] = _to_decimal(trace["direct_bill_total"])
    cat_totals = trace.get("category_totals_before_base_or_cap")
    if isinstance(cat_totals, dict):
        trace["category_totals_before_base_or_cap"] = {
            key: _to_decimal(value) for key, value in cat_totals.items()
        }
    return trace


@dataclass
class TenantCharge:
    tenant_id: str
    gross_share_before_exclusions: Decimal
    exclusions_applied: list[ExclusionApplied] = field(default_factory=list)
    direct_bills_applied: list[DirectBillApplied] = field(default_factory=list)
    base_year_adjustment: Optional[dict[str, Any]] = None
    cap_adjustment: Optional[dict[str, Any]] = None
    final_charge: Decimal = Decimal("0")
    direct_bill_total: Decimal = Decimal("0")
    total_due: Decimal = Decimal("0")
    annual_prebilled: Optional[Decimal] = None
    vs_prebilled: Optional[Decimal] = None
    citations: list[dict[str, Any]] = field(default_factory=list)
    math_trace: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.gross_share_before_exclusions = _to_decimal(self.gross_share_before_exclusions)
        self.final_charge = _to_decimal(self.final_charge)
        self.direct_bill_total = _to_decimal(self.direct_bill_total)
        self.total_due = _to_decimal(self.total_due)
        self.annual_prebilled = _to_optional_decimal(self.annual_prebilled)
        self.vs_prebilled = _to_optional_decimal(self.vs_prebilled)
        if self.base_year_adjustment is not None:
            _coerce_any_decimals(self.base_year_adjustment, _BASE_YEAR_DECIMAL_KEYS)
        if self.cap_adjustment is not None:
            _coerce_any_decimals(self.cap_adjustment, _CAP_DECIMAL_KEYS)
        for citation in self.citations:
            _coerce_any_decimals(citation, _CITATION_DECIMAL_KEYS)
        if self.math_trace:
            _coerce_math_trace(self.math_trace)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "TenantCharge":
        return cls(
            tenant_id=data["tenant_id"],
            gross_share_before_exclusions=_to_decimal(data["gross_share_before_exclusions"]),
            exclusions_applied=[ExclusionApplied.from_dict(item) for item in data.get("exclusions_applied", [])],
            direct_bills_applied=[DirectBillApplied.from_dict(item) for item in data.get("direct_bills_applied", [])],
            base_year_adjustment=dict(data["base_year_adjustment"]) if data.get("base_year_adjustment") else None,
            cap_adjustment=dict(data["cap_adjustment"]) if data.get("cap_adjustment") else None,
            final_charge=_to_decimal(data.get("final_charge", 0)),
            direct_bill_total=_to_decimal(data.get("direct_bill_total", 0)),
            total_due=_to_decimal(data.get("total_due", 0)),
            annual_prebilled=_to_optional_decimal(data.get("annual_prebilled")),
            vs_prebilled=_to_optional_decimal(data.get("vs_prebilled")),
            citations=[dict(item) for item in data.get("citations", [])],
            math_trace=dict(data.get("math_trace", {})),
        )


@dataclass
class Provenance:
    plugin_version: str
    run_timestamp: datetime
    inputs_hash: str
    operator: Optional[str] = None

    def __post_init__(self) -> None:
        self.run_timestamp = _to_datetime(self.run_timestamp)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Provenance":
        return cls(
            plugin_version=data["plugin_version"],
            run_timestamp=_to_datetime(data["run_timestamp"]),
            inputs_hash=data["inputs_hash"],
            operator=data.get("operator"),
        )


_MANIFEST_FIELDS = {
    "property",
    "fiscal_year",
    "budget",
    "leases",
    "gl_lines",
    "tenant_charges",
    "landlord_absorbed_total",
    "direct_billed_total",
    "provenance",
}


@dataclass
class Manifest:
    property: Property
    fiscal_year: int
    budget: dict[str, Decimal]
    leases: list[Lease]
    gl_lines: list[GLLine]
    provenance: Provenance
    tenant_charges: list[TenantCharge] = field(default_factory=list)
    landlord_absorbed_total: Decimal = Decimal("0")
    direct_billed_total: Decimal = Decimal("0")

    def __post_init__(self) -> None:
        self.budget = {key: _to_decimal(value) for key, value in self.budget.items()}
        self.landlord_absorbed_total = _to_decimal(self.landlord_absorbed_total)
        self.direct_billed_total = _to_decimal(self.direct_billed_total)

    def save(self, path: str | Path) -> None:
        with open(path, "w", encoding="utf-8") as handle:
            json.dump(self, handle, cls=ManifestJSONEncoder, indent=2)

    @classmethod
    def load(cls, path: str | Path) -> "Manifest":
        with open(path, encoding="utf-8") as handle:
            return cls.from_dict(json.load(handle))

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Manifest":
        check_unknown_keys(cls, data, _MANIFEST_FIELDS)
        return cls(
            property=Property.from_dict(data["property"]),
            fiscal_year=int(data["fiscal_year"]),
            budget={key: _to_decimal(value) for key, value in data.get("budget", {}).items()},
            leases=[Lease.from_dict(item) for item in data.get("leases", [])],
            gl_lines=[GLLine.from_dict(item) for item in data.get("gl_lines", [])],
            tenant_charges=[TenantCharge.from_dict(item) for item in data.get("tenant_charges", [])],
            landlord_absorbed_total=_to_decimal(data.get("landlord_absorbed_total", 0)),
            direct_billed_total=_to_decimal(data.get("direct_billed_total", 0)),
            provenance=Provenance.from_dict(data["provenance"]),
        )


# --- canonical citations and category maps ----------------------------------


STANDARD_FORM_ALLOCATION = LeaseCitation(
    doc="Standard Form Lease",
    section="§6.02",
    quote="The Tenant shall pay the Tenant's Proportionate Share of Operating Expenses allocable to the applicable Pool.",
)
STANDARD_FORM_OPERATING = LeaseCitation(
    doc="Standard Form Lease",
    section="§6.01",
    quote="Operating Expenses means the total reasonable costs incurred in operating, maintaining, and administering the Building.",
)
STANDARD_FORM_TURNOVER = LeaseCitation(
    doc="Standard Form Lease",
    section="§6.03(c)",
    quote="One-time extraordinary charges arising from tenant turnover, including move-out deep cleaning, are excluded.",
)
STANDARD_FORM_DUPLICATE = LeaseCitation(
    doc="Standard Form Lease",
    section="§6.03(g)",
    quote="Amounts posted to the general ledger in error, including duplicate invoices, are excluded.",
)
MANAGEMENT_FEE_BASIS = LeaseCitation(
    doc="Management Agreement",
    section="§4.1",
    quote="Owner shall pay a management fee equal to four percent of Effective Gross Income.",
)
MANAGEMENT_FEE_NONRECOVERABLE = LeaseCitation(
    doc="Management Agreement",
    section="§4.1.2",
    quote="No portion of any fee paid in excess of the correct EGI-based amount is recoverable from tenants.",
)
CANADAFIRST_CAP = LeaseCitation(
    doc="CanadaFirst Bank Lease",
    section="§6.05",
    quote="Operating Expenses for the tenant are capped at 104% compounded annually over the 2022 Base Year CAM.",
)
CANADAFIRST_UNCONTROLLABLE = LeaseCitation(
    doc="CanadaFirst Bank Lease",
    section="§6.05.1",
    quote="Realty tax, insurance, utilities, and snow removal pass through without the cap.",
)
BASE_YEAR_CITATION = LeaseCitation(
    doc="Matheson Family Dental Lease",
    section="§6.06",
    quote="The tenant pays only the amount by which current-year Operating Expenses exceed the Base Year CAM.",
)
PEAK_UTILITIES_CITATION = LeaseCitation(
    doc="Peak Fitness Studio Lease",
    section="§6.07(a)",
    quote="All utility costs are excluded from the tenant's Proportionate Share of Operating Expenses.",
)
PEAK_RM_CITATION = LeaseCitation(
    doc="Peak Fitness Studio Lease",
    section="§6.07(b)",
    quote="All repair and maintenance expenses are excluded from the tenant's Proportionate Share of Operating Expenses.",
)
PRONTO_GREASE_TRAP_CITATION = LeaseCitation(
    doc="Pronto Italian Kitchen Lease",
    section="Schedule C.1",
    quote="Grease trap servicing and associated compliance costs are excluded and billed directly to the tenant.",
)


CANONICAL_CATEGORY_MAP = {
    "realty tax": "realty_tax",
    "utilities - electric": "utilities",
    "utilities - gas": "utilities",
    "utilities - water": "utilities",
    "r&m - elevator": "repairs_maintenance",
    "r&m - hvac": "repairs_maintenance",
    "r&m - general": "repairs_maintenance",
    "r&m - pest control": "repairs_maintenance",
    "r&m - grease trap": "repairs_maintenance",
    "r&m - storefront glass": "repairs_maintenance",
    "r&m - roof": "repairs_maintenance",
    "management fee": "management_fee",
    "janitorial - contract": "janitorial",
    "janitorial - day porter": "janitorial",
    "janitorial - supplies": "janitorial",
    "janitorial - window": "janitorial",
    "insurance": "insurance",
    "security - patrol": "security",
    "security - alarm": "security",
    "security - access control": "security",
    "landscaping - maintenance": "landscaping",
    "landscaping - seasonal": "landscaping",
    "landscaping - irrigation": "landscaping",
    "landscaping - tree pruning": "landscaping",
    "snow & ice": "snow",
}


def canonical_category(raw_category: str) -> str:
    key = raw_category.strip().lower()
    if key in CANONICAL_CATEGORY_MAP:
        return CANONICAL_CATEGORY_MAP[key]
    raise KeyError(f"Unsupported GL category: {raw_category}")
