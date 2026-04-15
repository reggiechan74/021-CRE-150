"""Typed manifest models and shared domain helpers for CAM reconciliation."""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP
from enum import Enum
from pathlib import Path
from typing import Any, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field


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


class LeaseCitation(BaseModel):
    doc: str
    section: str
    quote: str


class CapConfig(BaseModel):
    base_year: int
    base_year_cam_psf: Decimal
    annual_increase_rate: Decimal
    uncontrollable_categories: list[str]


class BaseYearConfig(BaseModel):
    year: int
    cam_psf: Decimal
    gross_up_to_percent: Decimal = Decimal("1.0")


class Lease(BaseModel):
    tenant_id: str
    tenant_name: str
    unit_label: str
    rsf: int
    pool: PoolName
    pro_rata_of_pool: Decimal
    lease_type: LeaseType
    excluded_categories: list[str] = Field(default_factory=list)
    cap: Optional[CapConfig] = None
    base_year: Optional[BaseYearConfig] = None
    specific_exclusions: list[dict[str, Any]] = Field(default_factory=list)
    clause_refs: dict[str, LeaseCitation] = Field(default_factory=dict)
    annual_prebilled: Optional[Decimal] = None
    is_vacant: bool = False


class Pool(BaseModel):
    name: PoolName
    rsf: int
    share_of_total: Decimal


class Property(BaseModel):
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

    def pool_rsf(self, pool: PoolName) -> int:
        if pool == PoolName.OFFICE:
            return self.rsf_office
        if pool == PoolName.RETAIL:
            return self.rsf_retail
        return self.rsf_total


class Classification(BaseModel):
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


class GLLine(BaseModel):
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
    allocation: dict[str, Decimal] = Field(default_factory=dict)


class ExclusionApplied(BaseModel):
    category: str
    amount_removed: Decimal
    reason: str
    citation_ref: Optional[LeaseCitation] = None
    reallocated_to: list[str] = Field(default_factory=list)


class DirectBillApplied(BaseModel):
    category: str
    amount_billed: Decimal
    reason: str
    citation_ref: Optional[LeaseCitation] = None
    source_gl_ids: list[str] = Field(default_factory=list)


class TenantCharge(BaseModel):
    tenant_id: str
    gross_share_before_exclusions: Decimal
    exclusions_applied: list[ExclusionApplied] = Field(default_factory=list)
    direct_bills_applied: list[DirectBillApplied] = Field(default_factory=list)
    base_year_adjustment: Optional[dict[str, Any]] = None
    cap_adjustment: Optional[dict[str, Any]] = None
    final_charge: Decimal
    direct_bill_total: Decimal = Decimal("0")
    total_due: Decimal = Decimal("0")
    annual_prebilled: Optional[Decimal] = None
    vs_prebilled: Optional[Decimal] = None
    citations: list[dict[str, Any]] = Field(default_factory=list)
    math_trace: dict[str, Any] = Field(default_factory=dict)


class Provenance(BaseModel):
    plugin_version: str
    run_timestamp: datetime
    inputs_hash: str
    operator: Optional[str] = None


class Manifest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    property: Property
    fiscal_year: int
    budget: dict[str, Decimal]
    leases: list[Lease]
    gl_lines: list[GLLine]
    tenant_charges: list[TenantCharge] = Field(default_factory=list)
    landlord_absorbed_total: Decimal = Decimal("0")
    direct_billed_total: Decimal = Decimal("0")
    provenance: Provenance

    def save(self, path: str | Path) -> None:
        import json

        with open(path, "w", encoding="utf-8") as handle:
            json.dump(self.model_dump(mode="json"), handle, indent=2, default=str)

    @classmethod
    def load(cls, path: str | Path) -> "Manifest":
        import json

        with open(path, encoding="utf-8") as handle:
            return cls.model_validate(json.load(handle))


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
