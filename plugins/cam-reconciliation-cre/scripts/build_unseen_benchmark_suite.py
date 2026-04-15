"""Build a 10-case unseen CAM benchmark suite for manual Anthropic runs and local plugin scoring."""

from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path
from typing import Any

import yaml

PLUGIN_ROOT = Path(__file__).resolve().parent.parent
SUITE_ROOT = PLUGIN_ROOT / "benchmarks" / "unseen_cam_suite"
CASES_ROOT = SUITE_ROOT / "cases"
GOLD_ROOT = SUITE_ROOT / "gold"
RESULTS_ROOT = SUITE_ROOT / "results"
PACKETS_ROOT = SUITE_ROOT / "anthropic_packets"


def money(value: Decimal | int | float | str) -> Decimal:
    return Decimal(str(value)).quantize(Decimal("0.01"))


def split_amount(total: Decimal, keys: list[str], weights: list[Decimal]) -> dict[str, Decimal]:
    total = money(total)
    total_cents = int(total * 100)
    weight_sum = sum(weights)
    if weight_sum == 0:
        return {key: Decimal("0.00") for key in keys}

    raw = [Decimal(total_cents) * weight / weight_sum for weight in weights]
    floors = [int(value) for value in raw]
    remainder = total_cents - sum(floors)
    ranked = sorted(
        ((raw[idx] - floors[idx], idx) for idx in range(len(keys))),
        key=lambda item: (-item[0], item[1]),
    )
    for _, idx in ranked[:remainder]:
        floors[idx] += 1
    return {key: Decimal(cents) / Decimal("100") for key, cents in zip(keys, floors)}


def normalize_weights(weights: dict[str, Decimal], total_rsf: int) -> dict[str, int]:
    raw = split_amount(Decimal(total_rsf), list(weights.keys()), list(weights.values()))
    return {key: int(value) for key, value in raw.items()}


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, default=str) + "\n", encoding="utf-8")


def write_yaml(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["Date", "Account", "Category", "Vendor", "Invoice Ref", "Memo", "Amount", "Pool"],
        )
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


@dataclass(frozen=True)
class CaseDefinition:
    case_id: str
    property_name: str
    address: str
    office_rsf: int
    retail_rsf: int
    tax_step_extra: Decimal
    duplicate_kind: str | None
    duplicate_amount: Decimal
    turnover_pool: str | None
    turnover_amount: Decimal
    management_fee_excess: Decimal
    include_cap: bool
    cap_binding: bool
    include_modified_gross: bool
    include_restaurant_exclusion: bool
    include_base_year_retail: bool
    include_base_year_office: bool
    include_vacancy: bool
    budget_multiplier: Decimal
    utility_legit_variance: Decimal
    repairs_legit_variance: Decimal
    janitorial_legit_variance: Decimal
    security_legit_variance: Decimal
    landscaping_legit_variance: Decimal
    snow_legit_variance: Decimal


CASE_DEFINITIONS: list[CaseDefinition] = [
    CaseDefinition("01_harborpoint_exchange", "Harborpoint Exchange", "177 Harbour Street West, Toronto, ON M5J 2L6", 36000, 18000, Decimal("54000"), "gas", Decimal("9300"), "Office", Decimal("11250"), Decimal("3600"), True, False, True, True, True, True, True, Decimal("0.96"), Decimal("4100"), Decimal("3200"), Decimal("1800"), Decimal("0"), Decimal("0"), Decimal("0")),
    CaseDefinition("02_kingsway_commons", "Kingsway Commons", "910 Kingsway Drive, Vancouver, BC V5V 3C5", 30000, 22000, Decimal("42000"), "security_patrol", Decimal("4200"), None, Decimal("0"), Decimal("2800"), True, True, True, False, True, False, False, Decimal("1.04"), Decimal("5200"), Decimal("6800"), Decimal("900"), Decimal("1700"), Decimal("600"), Decimal("0")),
    CaseDefinition("03_cedar_ridge_plaza", "Cedar Ridge Plaza", "245 Cedar Ridge Road, Ottawa, ON K2P 1A4", 26000, 24000, Decimal("30000"), None, Decimal("0"), "Retail", Decimal("9800"), Decimal("0"), True, False, False, True, True, True, False, Decimal("0.92"), Decimal("2600"), Decimal("2400"), Decimal("1400"), Decimal("0"), Decimal("400"), Decimal("0")),
    CaseDefinition("04_airport_north_hub", "Airport North Business Hub", "455 Jetstream Avenue, Mississauga, ON L5S 1X7", 41000, 16000, Decimal("25000"), "electric", Decimal("7600"), None, Decimal("0"), Decimal("5100"), True, True, True, False, False, True, True, Decimal("1.08"), Decimal("6100"), Decimal("5400"), Decimal("700"), Decimal("1200"), Decimal("0"), Decimal("0")),
    CaseDefinition("05_riverfront_market_centre", "Riverfront Market Centre", "88 Riverfront Lane, Calgary, AB T2P 3N4", 28000, 20000, Decimal("36000"), "janitorial_day_porter", Decimal("2400"), "Office", Decimal("13500"), Decimal("0"), False, False, True, True, False, True, True, Decimal("1.00"), Decimal("3000"), Decimal("1900"), Decimal("2200"), Decimal("0"), Decimal("500"), Decimal("0")),
    CaseDefinition("06_westmount_professional_campus", "Westmount Professional Campus", "1212 Westmount Boulevard, Montreal, QC H3Y 1Z8", 44000, 14000, Decimal("27000"), None, Decimal("0"), None, Decimal("0"), Decimal("4200"), True, False, False, False, True, True, False, Decimal("0.98"), Decimal("1800"), Decimal("2700"), Decimal("1100"), Decimal("300"), Decimal("0"), Decimal("0")),
    CaseDefinition("07_meadowvale_station_centre", "Meadowvale Station Centre", "75 Meadowvale Station Road, Mississauga, ON L5N 2R5", 32000, 21000, Decimal("48000"), "water", Decimal("5600"), "Retail", Decimal("8700"), Decimal("2200"), True, False, True, True, False, False, True, Decimal("1.02"), Decimal("3900"), Decimal("4600"), Decimal("1300"), Decimal("0"), Decimal("0"), Decimal("0")),
    CaseDefinition("08_lakeshore_atrium", "Lakeshore Atrium", "602 Lakeshore Avenue East, Toronto, ON M4M 1H2", 35000, 15000, Decimal("21000"), None, Decimal("0"), None, Decimal("0"), Decimal("0"), True, True, True, True, True, False, False, Decimal("1.06"), Decimal("2400"), Decimal("5100"), Decimal("600"), Decimal("900"), Decimal("700"), Decimal("300")),
    CaseDefinition("09_northline_commerce_court", "Northline Commerce Court", "1400 Northline Road, Edmonton, AB T5J 1A1", 38000, 19000, Decimal("39000"), "security_patrol", Decimal("3600"), None, Decimal("0"), Decimal("3900"), True, False, False, False, True, True, True, Decimal("0.94"), Decimal("2800"), Decimal("2100"), Decimal("1000"), Decimal("1400"), Decimal("0"), Decimal("0")),
    CaseDefinition("10_university_gate_centre", "University Gate Centre", "510 University Gate, Waterloo, ON N2L 3G1", 34000, 23000, Decimal("51000"), "gas", Decimal("8400"), "Office", Decimal("15400"), Decimal("4700"), True, True, True, True, True, True, True, Decimal("1.10"), Decimal("6300"), Decimal("7200"), Decimal("2500"), Decimal("1800"), Decimal("900"), Decimal("400")),
]


BASE_RATES = {
    "realty_tax": Decimal("6.55"),
    "utilities": Decimal("3.05"),
    "repairs_maintenance": Decimal("1.92"),
    "janitorial": Decimal("1.32"),
    "insurance": Decimal("0.88"),
    "security": Decimal("0.74"),
    "landscaping": Decimal("0.52"),
    "snow": Decimal("0.38"),
}


def build_budget(case: CaseDefinition) -> dict[str, Decimal]:
    total_rsf = case.office_rsf + case.retail_rsf
    budget = {key: money(rate * case.budget_multiplier * total_rsf) for key, rate in BASE_RATES.items()}
    projected_egi = money(Decimal(total_rsf) * case.budget_multiplier * Decimal("43.50"))
    budget["management_fee"] = money(projected_egi * Decimal("0.04"))
    return budget


def build_actual_totals(case: CaseDefinition, budget: dict[str, Decimal]) -> dict[str, Decimal]:
    actual = dict(budget)
    actual["realty_tax"] = money(actual["realty_tax"] + case.tax_step_extra)
    actual["utilities"] = money(actual["utilities"] + case.utility_legit_variance)
    actual["repairs_maintenance"] = money(actual["repairs_maintenance"] + case.repairs_legit_variance)
    actual["janitorial"] = money(actual["janitorial"] + case.janitorial_legit_variance)
    actual["security"] = money(actual["security"] + case.security_legit_variance)
    actual["landscaping"] = money(actual["landscaping"] + case.landscaping_legit_variance)
    actual["snow"] = money(actual["snow"] + case.snow_legit_variance)

    if case.duplicate_kind in {"gas", "electric", "water"}:
        actual["utilities"] = money(actual["utilities"] + case.duplicate_amount)
    elif case.duplicate_kind == "security_patrol":
        actual["security"] = money(actual["security"] + case.duplicate_amount)
    elif case.duplicate_kind == "janitorial_day_porter":
        actual["janitorial"] = money(actual["janitorial"] + case.duplicate_amount)

    if case.turnover_amount:
        actual["janitorial"] = money(actual["janitorial"] + case.turnover_amount)

    actual_egi = money((budget["management_fee"] + money(Decimal("1400.00"))) / Decimal("0.04"))
    actual["management_fee"] = money(actual_egi * Decimal("0.04") + case.management_fee_excess)
    actual["_effective_gross_income"] = actual_egi
    if case.management_fee_excess:
        actual["_gross_potential_income"] = money(actual_egi + (case.management_fee_excess / Decimal("0.04")))
        actual["_vacancy_loss"] = money(actual["_gross_potential_income"] - actual_egi - Decimal("20000.00"))
        actual["_credit_allowance"] = Decimal("20000.00")
    else:
        actual["_gross_potential_income"] = actual_egi
        actual["_vacancy_loss"] = Decimal("0.00")
        actual["_credit_allowance"] = Decimal("0.00")
    actual["_projected_effective_gross_income"] = money(budget["management_fee"] / Decimal("0.04"))
    return actual


def build_tenants(case: CaseDefinition, budget_total: Decimal) -> list[dict[str, Any]]:
    retail_weights: dict[str, Decimal] = {
        "unit_101": Decimal("0.22") if case.include_cap else Decimal("0.24"),
        "unit_102": Decimal("0.12"),
        "unit_103": Decimal("0.16") if case.include_base_year_retail else Decimal("0.14"),
        "unit_104": Decimal("0.26") if case.include_modified_gross else Decimal("0.24"),
        "unit_105": Decimal("0.24") if case.include_restaurant_exclusion else Decimal("0.26"),
    }
    office_weights: dict[str, Decimal] = {
        "suite_200": Decimal("0.34"),
        "suite_300": Decimal("0.22"),
        "suite_310": Decimal("0.12") if case.include_base_year_office else Decimal("0.10"),
        "suite_320": Decimal("0.08") if case.include_vacancy else Decimal("0.06"),
        "suite_400": Decimal("0.24"),
    }
    retail_rsf = normalize_weights(retail_weights, case.retail_rsf)
    office_rsf = normalize_weights(office_weights, case.office_rsf)

    tenants: list[dict[str, Any]] = []
    clause_allocation_retail = {
        "doc": "Standard Form Lease",
        "section": "§6.02",
        "quote": "Tenant pays its Proportionate Share of Operating Expenses allocable to the Retail Pool.",
    }
    clause_allocation_office = {
        "doc": "Standard Form Lease",
        "section": "§6.02",
        "quote": "Tenant pays its Proportionate Share of Operating Expenses allocable to the Office Pool.",
    }

    def annual_prebill(pool: str, rsf: int, lease_type: str, cap_psf: Decimal | None = None) -> str:
        total_rsf = case.office_rsf + case.retail_rsf
        gross = money(budget_total * Decimal(rsf) / Decimal(total_rsf))
        if lease_type == "modified_gross":
            gross = money(gross * Decimal("0.74"))
        elif lease_type == "base_year":
            gross = money(gross * Decimal("0.24"))
        elif lease_type == "net_with_cap" and cap_psf is not None:
            gross = money(min(gross, cap_psf * Decimal(rsf)))
        return str(gross)

    cap_base_psf = Decimal("8.20") if case.cap_binding else Decimal("17.80")
    cap_ceiling_psf = money(cap_base_psf * (Decimal("1.04") ** 3))

    tenants.append(
        {
            "tenant_id": "unit_101",
            "tenant_name": "Harbor Federal Bank" if case.include_cap else "Anchor Pharmacy",
            "unit_label": "Unit 101",
            "rsf": retail_rsf["unit_101"],
            "pool": "retail",
            "pro_rata_of_pool": str(money(Decimal(retail_rsf["unit_101"]) / Decimal(case.retail_rsf))),
            "lease_type": "net_with_cap" if case.include_cap else "net",
            "cap": {
                "base_year": 2022,
                "base_year_cam_psf": str(cap_base_psf),
                "annual_increase_rate": "0.04",
                "uncontrollable_categories": ["realty_tax", "insurance", "utilities", "snow"],
            } if case.include_cap else None,
            "annual_prebilled": annual_prebill("retail", retail_rsf["unit_101"], "net_with_cap" if case.include_cap else "net", cap_ceiling_psf if case.include_cap else None),
            "clause_refs": {
                "allocation": clause_allocation_retail,
                "cap": {
                    "doc": "Retail Bank CAM Cap Rider",
                    "section": "§6.05",
                    "quote": "Controllable Operating Expenses are capped at 104% compounded annually over the 2022 Base Year CAM.",
                },
                "cap_uncontrollable": {
                    "doc": "Retail Bank CAM Cap Rider",
                    "section": "§6.05.1",
                    "quote": "Realty tax, insurance, utilities, and snow removal pass through without the cap.",
                },
            },
        }
    )
    tenants.append(
        {
            "tenant_id": "unit_102",
            "tenant_name": "Morning Roast Cafe",
            "unit_label": "Unit 102",
            "rsf": retail_rsf["unit_102"],
            "pool": "retail",
            "pro_rata_of_pool": str(money(Decimal(retail_rsf["unit_102"]) / Decimal(case.retail_rsf))),
            "lease_type": "net",
            "annual_prebilled": annual_prebill("retail", retail_rsf["unit_102"], "net"),
            "clause_refs": {"allocation": clause_allocation_retail},
        }
    )
    tenants.append(
        {
            "tenant_id": "unit_103",
            "tenant_name": "Harborview Dental" if case.include_base_year_retail else "Evergreen Medical",
            "unit_label": "Unit 103",
            "rsf": retail_rsf["unit_103"],
            "pool": "retail",
            "pro_rata_of_pool": str(money(Decimal(retail_rsf["unit_103"]) / Decimal(case.retail_rsf))),
            "lease_type": "base_year" if case.include_base_year_retail else "net",
            "base_year": {
                "year": 2024,
                "cam_psf": "15.60",
                "gross_up_to_percent": "1.0",
            } if case.include_base_year_retail else None,
            "annual_prebilled": annual_prebill("retail", retail_rsf["unit_103"], "base_year" if case.include_base_year_retail else "net"),
            "clause_refs": {
                "allocation": clause_allocation_retail,
                "base_year": {
                    "doc": "Medical Office Lease",
                    "section": "§6.06",
                    "quote": "Tenant pays only the increase in Operating Expenses above the 2024 Base Year CAM.",
                },
            },
        }
    )
    tenants.append(
        {
            "tenant_id": "unit_104",
            "tenant_name": "Summit Fitness Club" if case.include_modified_gross else "West End Apparel",
            "unit_label": "Unit 104",
            "rsf": retail_rsf["unit_104"],
            "pool": "retail",
            "pro_rata_of_pool": str(money(Decimal(retail_rsf["unit_104"]) / Decimal(case.retail_rsf))),
            "lease_type": "modified_gross" if case.include_modified_gross else "net",
            "excluded_categories": ["utilities", "repairs_maintenance"] if case.include_modified_gross else [],
            "annual_prebilled": annual_prebill("retail", retail_rsf["unit_104"], "modified_gross" if case.include_modified_gross else "net"),
            "clause_refs": {
                "allocation": clause_allocation_retail,
                "modified_gross_utilities": {
                    "doc": "Fitness Studio Lease",
                    "section": "§6.07(a)",
                    "quote": "All utility costs are excluded from the tenant's Operating Expense share.",
                },
                "modified_gross_repairs_maintenance": {
                    "doc": "Fitness Studio Lease",
                    "section": "§6.07(b)",
                    "quote": "All repair and maintenance expenses are excluded from the tenant's Operating Expense share.",
                },
            },
        }
    )
    tenants.append(
        {
            "tenant_id": "unit_105",
            "tenant_name": "Trattoria North" if case.include_restaurant_exclusion else "Urban Wellness Spa",
            "unit_label": "Unit 105",
            "rsf": retail_rsf["unit_105"],
            "pool": "retail",
            "pro_rata_of_pool": str(money(Decimal(retail_rsf["unit_105"]) / Decimal(case.retail_rsf))),
            "lease_type": "net_with_exclusions" if case.include_restaurant_exclusion else "net",
            "specific_exclusions": [
                {
                    "category": "repairs_maintenance",
                    "match_category_raw": "R&M - Grease Trap",
                    "reason": "schedule_c_grease_trap",
                    "citation": {
                        "doc": "Restaurant Exclusion Schedule",
                        "section": "Schedule C.1",
                        "quote": "Grease trap servicing and related compliance costs are excluded and billed directly to the tenant.",
                    },
                }
            ] if case.include_restaurant_exclusion else [],
            "annual_prebilled": annual_prebill("retail", retail_rsf["unit_105"], "net"),
            "clause_refs": {
                "allocation": clause_allocation_retail,
                "restaurant_exclusion": {
                    "doc": "Restaurant Exclusion Schedule",
                    "section": "Schedule C.1",
                    "quote": "Grease trap servicing and related compliance costs are excluded from the tenant's Operating Expense share.",
                },
            },
        }
    )

    tenants.append(
        {
            "tenant_id": "suite_200",
            "tenant_name": "Stonebridge Law LLP",
            "unit_label": "Suite 200",
            "rsf": office_rsf["suite_200"],
            "pool": "office",
            "pro_rata_of_pool": str(money(Decimal(office_rsf["suite_200"]) / Decimal(case.office_rsf))),
            "lease_type": "net",
            "annual_prebilled": annual_prebill("office", office_rsf["suite_200"], "net"),
            "clause_refs": {"allocation": clause_allocation_office},
        }
    )
    tenants.append(
        {
            "tenant_id": "suite_300",
            "tenant_name": "Vector Civil Engineering",
            "unit_label": "Suite 300",
            "rsf": office_rsf["suite_300"],
            "pool": "office",
            "pro_rata_of_pool": str(money(Decimal(office_rsf["suite_300"]) / Decimal(case.office_rsf))),
            "lease_type": "net",
            "annual_prebilled": annual_prebill("office", office_rsf["suite_300"], "net"),
            "clause_refs": {"allocation": clause_allocation_office},
        }
    )
    tenants.append(
        {
            "tenant_id": "suite_310",
            "tenant_name": "Covermark Insurance" if case.include_base_year_office else "Atlas Advisory Group",
            "unit_label": "Suite 310",
            "rsf": office_rsf["suite_310"],
            "pool": "office",
            "pro_rata_of_pool": str(money(Decimal(office_rsf["suite_310"]) / Decimal(case.office_rsf))),
            "lease_type": "base_year" if case.include_base_year_office else "net",
            "base_year": {
                "year": 2023,
                "cam_psf": "16.40",
                "gross_up_to_percent": "1.0",
            } if case.include_base_year_office else None,
            "annual_prebilled": annual_prebill("office", office_rsf["suite_310"], "base_year" if case.include_base_year_office else "net"),
            "clause_refs": {
                "allocation": clause_allocation_office,
                "base_year": {
                    "doc": "Office Insurance Lease",
                    "section": "§6.06",
                    "quote": "Tenant pays only the increase in Operating Expenses above the 2023 Base Year CAM.",
                },
            },
        }
    )
    tenants.append(
        {
            "tenant_id": "suite_320",
            "tenant_name": "VACANT (former tenant vacated 2024-12-31)" if case.include_vacancy else "North Shore Operations",
            "unit_label": "Suite 320",
            "rsf": office_rsf["suite_320"],
            "pool": "office",
            "pro_rata_of_pool": str(money(Decimal(office_rsf["suite_320"]) / Decimal(case.office_rsf))),
            "lease_type": "net",
            "annual_prebilled": "0.00" if case.include_vacancy else annual_prebill("office", office_rsf["suite_320"], "net"),
            "is_vacant": case.include_vacancy,
            "clause_refs": {"allocation": clause_allocation_office},
        }
    )
    tenants.append(
        {
            "tenant_id": "suite_400",
            "tenant_name": "Helix Data Systems",
            "unit_label": "Suite 400",
            "rsf": office_rsf["suite_400"],
            "pool": "office",
            "pro_rata_of_pool": str(money(Decimal(office_rsf["suite_400"]) / Decimal(case.office_rsf))),
            "lease_type": "net",
            "annual_prebilled": annual_prebill("office", office_rsf["suite_400"], "net"),
            "clause_refs": {"allocation": clause_allocation_office},
        }
    )

    cleaned: list[dict[str, Any]] = []
    for item in tenants:
        payload = {key: value for key, value in item.items() if value is not None}
        cleaned.append(payload)
    return cleaned


def periodic_amounts(total: Decimal, labels: list[str], weights: list[Decimal]) -> dict[str, Decimal]:
    return split_amount(total, labels, weights)


def build_gl_rows(case: CaseDefinition, actual: dict[str, Decimal], include_restaurant: bool) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    months = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]

    def add(date: str, account: str, category: str, vendor: str, invoice_ref: str, memo: str, amount: Decimal, pool: str) -> None:
        rows.append(
            {
                "Date": date,
                "Account": account,
                "Category": category,
                "Vendor": vendor,
                "Invoice Ref": invoice_ref,
                "Memo": memo,
                "Amount": f"{money(amount):.2f}",
                "Pool": pool,
            }
        )

    # Realty tax with mid-year step change.
    base_h1 = money((actual["realty_tax"] - case.tax_step_extra) / Decimal("12"))
    h2_increment = money(case.tax_step_extra / Decimal("6")) if case.tax_step_extra else Decimal("0.00")
    for idx, month in enumerate(months, start=1):
        amount = base_h1 if idx <= 6 else money(base_h1 + h2_increment)
        if idx == 12:
            posted = sum(Decimal(row["Amount"]) for row in rows if row["Category"] == "Realty Tax")
            amount = money(actual["realty_tax"] - posted)
        add(f"2025-{idx:02d}-15", "6100", "Realty Tax", "Municipal Tax Authority", f"TAX-2025-{month}", "Interim billing" if idx <= 6 else "Post-reassessment billing", amount, "Shared")

    # Insurance annual.
    add("2025-01-12", "6200", "Insurance", "Marsh Canada Ltd.", "INS-2025-ANNUAL", "Annual property and liability premium", actual["insurance"], "Shared")

    # Utilities.
    duplicate_remaining = case.duplicate_amount if case.duplicate_kind in {"gas", "electric", "water"} else Decimal("0.00")
    utility_base = money(actual["utilities"] - duplicate_remaining)
    water_total = money(utility_base * Decimal("0.15"))
    remaining_after_water = money(utility_base - water_total)
    electric_total = money(remaining_after_water * Decimal("0.63"))
    gas_total = money(utility_base - water_total - electric_total)

    electric_weights = [Decimal(x) for x in ("1.00", "0.96", "0.93", "0.90", "0.88", "0.92", "1.02", "1.06", "1.04", "1.00", "1.01", "1.08")]
    gas_weights = [Decimal(x) for x in ("1.25", "1.12", "0.98", "0.84", "0.70", "0.62", "0.58", "0.60", "0.66", "0.82", "1.00", "1.28")]
    water_weights = [Decimal("1"), Decimal("1"), Decimal("1"), Decimal("1")]

    electric_map = periodic_amounts(electric_total, months, electric_weights)
    gas_map = periodic_amounts(gas_total, months, gas_weights)
    water_map = periodic_amounts(water_total, ["Q1", "Q2", "Q3", "Q4"], water_weights)

    if case.duplicate_kind == "electric":
        electric_map["DEC"] = case.duplicate_amount
        posted_else = sum(value for key, value in electric_map.items() if key != "DEC")
        if posted_else != electric_total - case.duplicate_amount:
            rebalance = split_amount(electric_total - case.duplicate_amount, [key for key in months if key != "DEC"], [electric_weights[idx] for idx in range(11)])
            for key, value in rebalance.items():
                electric_map[key] = value
    if case.duplicate_kind == "gas":
        gas_map["DEC"] = case.duplicate_amount
        rebalance = split_amount(gas_total - case.duplicate_amount, [key for key in months if key != "DEC"], [gas_weights[idx] for idx in range(11)])
        for key, value in rebalance.items():
            gas_map[key] = value
    if case.duplicate_kind == "water":
        water_map["Q4"] = case.duplicate_amount
        rebalance = split_amount(water_total - case.duplicate_amount, ["Q1", "Q2", "Q3"], [Decimal("1"), Decimal("1"), Decimal("1")])
        for key, value in rebalance.items():
            water_map[key] = value

    for idx, month in enumerate(months, start=1):
        add(f"2025-{idx:02d}-20", "6310", "Utilities - Electric", "Alectra Utilities", f"ALT-2025-{month}", f"Base building electric — {month}", electric_map[month], "Shared")
        gas_invoice = f"ENB-2025-{month}"
        gas_memo = f"Base building gas — {month}"
        if case.duplicate_kind == "gas" and month == "DEC":
            gas_invoice = f"GA-2025-{case.case_id[-2:]}-4471"
            gas_memo = "December gas — original posting"
        add(f"2025-{idx:02d}-22", "6320", "Utilities - Gas", "Enbridge Gas Inc.", gas_invoice, gas_memo, gas_map[month], "Shared")
    for quarter, month_num in zip(["Q1", "Q2", "Q3", "Q4"], [3, 6, 9, 12]):
        water_invoice = f"WTR-2025-{quarter}"
        water_memo = f"{quarter} water and sewer"
        if case.duplicate_kind == "water" and quarter == "Q4":
            water_invoice = f"ROP-{case.case_id[-2:]}-DUP"
            water_memo = "Q4 water and sewer — original posting"
        add(f"2025-{month_num:02d}-27", "6330", "Utilities - Water", "Regional Water Services", water_invoice, water_memo, water_map[quarter], "Shared")

    if case.duplicate_kind == "electric":
        add("2025-12-28", "6310", "Utilities - Electric", "Alectra Utilities", "ALT-2025-DEC", "December electric re-entered in year-end close (duplicate)", case.duplicate_amount, "Shared")
    if case.duplicate_kind == "gas":
        add("2025-12-29", "6320", "Utilities - Gas", "Enbridge Gas Inc.", f"GA-2025-{case.case_id[-2:]}-4471", "December gas re-entered in year-end close (duplicate)", case.duplicate_amount, "Shared")
    if case.duplicate_kind == "water":
        add("2025-12-30", "6330", "Utilities - Water", "Regional Water Services", f"ROP-{case.case_id[-2:]}-DUP", "Q4 water re-entered in close (duplicate)", case.duplicate_amount, "Shared")

    # Repairs and maintenance.
    r_and_m_total = actual["repairs_maintenance"]
    grease_total = money(r_and_m_total * Decimal("0.04")) if include_restaurant else Decimal("0.00")
    storefront_total = money(r_and_m_total * Decimal("0.05"))
    elevator_total = money(r_and_m_total * Decimal("0.18"))
    hvac_total = money(r_and_m_total * Decimal("0.22"))
    pest_total = money(r_and_m_total * Decimal("0.05"))
    roof_total = money(r_and_m_total * Decimal("0.08"))
    general_total = money(r_and_m_total - grease_total - storefront_total - elevator_total - hvac_total - pest_total - roof_total)

    elevator_map = periodic_amounts(elevator_total, months, [Decimal("1")] * 12)
    for idx, month in enumerate(months, start=1):
        add(f"2025-{idx:02d}-05", "6410", "R&M - Elevator", "Kone Elevator Canada", f"KONE-2025-{month}", "Monthly elevator service contract", elevator_map[month], "Office")

    hvac_map = periodic_amounts(hvac_total, ["Q1", "Q2", "Q3", "Q4"], [Decimal("1")] * 4)
    for quarter, month_num in zip(["Q1", "Q2", "Q3", "Q4"], [3, 6, 9, 12]):
        add(f"2025-{month_num:02d}-12", "6420", "R&M - HVAC", "Mechanical Systems Inc.", f"MSI-2025-{quarter}", f"{quarter} HVAC preventive maintenance", hvac_map[quarter], "Shared")

    general_keys = ["A", "B", "C", "D", "E", "F"]
    general_map = periodic_amounts(general_total, general_keys, [Decimal("1.1"), Decimal("1.4"), Decimal("0.8"), Decimal("1.0"), Decimal("0.9"), Decimal("1.2")])
    general_rows = [
        ("2025-02-14", "MRO-2025-0214", "Plumbing repair to common washroom"),
        ("2025-03-22", "MRO-2025-0322", "LED retrofit to garage fixtures"),
        ("2025-05-08", "MRO-2025-0508", "Electrical panel maintenance"),
        ("2025-07-11", "MRO-2025-0711", "Lobby carpentry and millwork repair"),
        ("2025-09-25", "MRO-2025-0925", "Asphalt crack sealing and line touch-up"),
        ("2025-11-18", "MRO-2025-1118", "Backflow test and certification"),
    ]
    for key, (date, ref, memo_text) in zip(general_keys, general_rows):
        add(date, "6430", "R&M - General", "Metro Building Services", ref, memo_text, general_map[key], "Shared")

    pest_map = periodic_amounts(pest_total, ["Q1", "Q2", "Q3", "Q4"], [Decimal("1")] * 4)
    for quarter, month_num in zip(["Q1", "Q2", "Q3", "Q4"], [3, 6, 9, 12]):
        add(f"2025-{month_num:02d}-19", "6440", "R&M - Pest Control", "Orkin Canada", f"ORK-2025-{quarter}", f"{quarter} pest control", pest_map[quarter], "Shared")

    if include_restaurant:
        grease_map = periodic_amounts(grease_total, ["Q1", "Q2", "Q3", "Q4"], [Decimal("1")] * 4)
        for quarter, month_num in zip(["Q1", "Q2", "Q3", "Q4"], [3, 6, 9, 12]):
            add(f"2025-{month_num:02d}-14", "6450", "R&M - Grease Trap", "Drain Pro Services", f"DPS-2025-{quarter}", f"{quarter} grease trap service", grease_map[quarter], "Retail")

    storefront_map = periodic_amounts(storefront_total, ["JAN", "MAR", "MAY", "JUL", "SEP", "NOV"], [Decimal("1")] * 6)
    for month, month_num in zip(["JAN", "MAR", "MAY", "JUL", "SEP", "NOV"], [1, 3, 5, 7, 9, 11]):
        add(f"2025-{month_num:02d}-10", "6460", "R&M - Storefront Glass", "Crystal Clear Window Co.", f"CCW-2025-{month}", "Retail storefront glass cleaning", storefront_map[month], "Retail")

    roof_map = periodic_amounts(roof_total, ["SPRING", "FALL"], [Decimal("1"), Decimal("1")])
    add("2025-05-09", "6470", "R&M - Roof", "Flynn Canada Roofing", "FLN-2025-SPRING", "Spring roof inspection and repair", roof_map["SPRING"], "Shared")
    add("2025-11-07", "6470", "R&M - Roof", "Flynn Canada Roofing", "FLN-2025-FALL", "Fall roof inspection and flashing repair", roof_map["FALL"], "Shared")

    # Management fee.
    mgmt_total = actual["management_fee"]
    mgmt_map = periodic_amounts(mgmt_total, months, [Decimal("1.0"), Decimal("1.0"), Decimal("1.0"), Decimal("1.0"), Decimal("1.0"), Decimal("1.02"), Decimal("1.03"), Decimal("1.04"), Decimal("1.03"), Decimal("1.02"), Decimal("1.01"), Decimal("1.0")])
    for idx, month in enumerate(months, start=1):
        add(f"2025-{idx:02d}-28", "6500", "Management Fee", "Harborline Property Management", f"HPM-MF-2025-{month}", f"Management fee — 4% of {month} gross revenue", mgmt_map[month], "Shared")

    # Janitorial.
    duplicate_janitorial = case.duplicate_amount if case.duplicate_kind == "janitorial_day_porter" else Decimal("0.00")
    janitorial_base = money(actual["janitorial"] - case.turnover_amount - duplicate_janitorial)
    contract_total = money(janitorial_base * Decimal("0.58"))
    porter_total = money(janitorial_base * Decimal("0.26"))
    supplies_total = money(janitorial_base * Decimal("0.09"))
    window_total = money(janitorial_base - contract_total - porter_total - supplies_total)
    contract_map = periodic_amounts(contract_total, months, [Decimal("1")] * 12)
    porter_map = periodic_amounts(porter_total, months, [Decimal("1")] * 12)
    if case.duplicate_kind == "janitorial_day_porter":
        porter_map["DEC"] = case.duplicate_amount
        rebalance = split_amount(porter_total - case.duplicate_amount, [key for key in months if key != "DEC"], [Decimal("1")] * 11)
        for key, value in rebalance.items():
            porter_map[key] = value
    for idx, month in enumerate(months, start=1):
        add(f"2025-{idx:02d}-02", "6600", "Janitorial - Contract", "Clean Pro Services Ltd.", f"CPS-2025-{month}", "Monthly janitorial contract", contract_map[month], "Shared")
        porter_invoice = f"CPS-DP-2025-{month}"
        porter_memo = "Retail concourse day porter"
        if case.duplicate_kind == "janitorial_day_porter" and month == "DEC":
            porter_invoice = f"CPS-DP-{case.case_id[-2:]}-DUP"
            porter_memo = "December day porter — original posting"
        add(f"2025-{idx:02d}-03", "6610", "Janitorial - Day Porter", "Clean Pro Services Ltd.", porter_invoice, porter_memo, porter_map[month], "Retail")
    supplies_map = periodic_amounts(supplies_total, ["Q1", "Q2", "Q3", "Q4"], [Decimal("1")] * 4)
    for quarter, month_num in zip(["Q1", "Q2", "Q3", "Q4"], [3, 6, 9, 12]):
        add(f"2025-{month_num:02d}-16", "6620", "Janitorial - Supplies", "Swish Maintenance", f"SWM-2025-{quarter}", f"{quarter} janitorial supplies", supplies_map[quarter], "Shared")
    window_map = periodic_amounts(window_total, ["SPRING", "FALL"], [Decimal("1"), Decimal("1")])
    add("2025-05-22", "6630", "Janitorial - Window", "Crystal Clear Window Co.", "CCW-INT-2025-SPRING", "Spring interior window cleaning", window_map["SPRING"], "Shared")
    add("2025-10-22", "6630", "Janitorial - Window", "Crystal Clear Window Co.", "CCW-INT-2025-FALL", "Fall interior window cleaning", window_map["FALL"], "Shared")

    if case.turnover_amount:
        memo = "Suite turnover move-out deep clean, patch-paint, and restoration before remarketing"
        pool = case.turnover_pool or "Office"
        add("2025-10-18", "6600", "Janitorial - Contract", "Northview Restoration", f"TURN-{case.case_id[-2:]}-1018", memo, case.turnover_amount, pool)
    if case.duplicate_kind == "janitorial_day_porter":
        add("2025-12-29", "6610", "Janitorial - Day Porter", "Clean Pro Services Ltd.", f"CPS-DP-{case.case_id[-2:]}-DUP", "December day porter re-entered in close (duplicate)", case.duplicate_amount, "Retail")

    # Security.
    duplicate_security = case.duplicate_amount if case.duplicate_kind == "security_patrol" else Decimal("0.00")
    security_base = money(actual["security"] - duplicate_security)
    patrol_total = money(security_base * Decimal("0.82"))
    alarm_total = money(security_base * Decimal("0.10"))
    access_total = money(security_base - patrol_total - alarm_total)
    patrol_map = periodic_amounts(patrol_total, months, [Decimal("1")] * 12)
    if case.duplicate_kind == "security_patrol":
        patrol_map["NOV"] = case.duplicate_amount
        rebalance = split_amount(patrol_total - case.duplicate_amount, [key for key in months if key != "NOV"], [Decimal("1")] * 11)
        for key, value in rebalance.items():
            patrol_map[key] = value
    alarm_map = periodic_amounts(alarm_total, months, [Decimal("1")] * 12)
    access_map = periodic_amounts(access_total, ["Q1", "Q2", "Q3", "Q4"], [Decimal("1")] * 4)
    for idx, month in enumerate(months, start=1):
        patrol_invoice = f"GW-2025-{month}"
        patrol_memo = "Nightly mobile patrol"
        if case.duplicate_kind == "security_patrol" and month == "NOV":
            patrol_invoice = f"GW-{case.case_id[-2:]}-DUP"
            patrol_memo = "November mobile patrol — original posting"
        add(f"2025-{idx:02d}-05", "6700", "Security - Patrol", "GardaWorld", patrol_invoice, patrol_memo, patrol_map[month], "Shared")
        add(f"2025-{idx:02d}-12", "6710", "Security - Alarm", "ADT Commercial", f"ADT-2025-{month}", "Monitored alarm", alarm_map[month], "Shared")
    for quarter, month_num in zip(["Q1", "Q2", "Q3", "Q4"], [3, 6, 9, 12]):
        add(f"2025-{month_num:02d}-18", "6720", "Security - Access Control", "SecureTech Inc.", f"ST-2025-{quarter}", f"{quarter} access control maintenance", access_map[quarter], "Shared")
    if case.duplicate_kind == "security_patrol":
        add("2025-11-29", "6700", "Security - Patrol", "GardaWorld", f"GW-{case.case_id[-2:]}-DUP", "November mobile patrol re-entered in close (duplicate)", case.duplicate_amount, "Shared")

    # Landscaping.
    landscaping_total = actual["landscaping"]
    maintenance_total = money(landscaping_total * Decimal("0.63"))
    seasonal_total = money(landscaping_total * Decimal("0.23"))
    irrigation_total = money(landscaping_total * Decimal("0.08"))
    tree_total = money(landscaping_total - maintenance_total - seasonal_total - irrigation_total)
    maintenance_map = periodic_amounts(maintenance_total, ["APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV"], [Decimal("1")] * 8)
    for month, month_num in zip(["APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV"], [4, 5, 6, 7, 8, 9, 10, 11]):
        add(f"2025-{month_num:02d}-30", "6800", "Landscaping - Maintenance", "GreenScape Contractors", f"GSC-2025-{month}", "Monthly landscaping maintenance", maintenance_map[month], "Shared")
    seasonal_map = periodic_amounts(seasonal_total, ["SPRING", "FALL"], [Decimal("1"), Decimal("1")])
    add("2025-05-15", "6810", "Landscaping - Seasonal", "GreenScape Contractors", "GSC-SPRING-2025", "Spring seasonal plantings", seasonal_map["SPRING"], "Shared")
    add("2025-09-25", "6810", "Landscaping - Seasonal", "GreenScape Contractors", "GSC-FALL-2025", "Fall seasonal plantings", seasonal_map["FALL"], "Shared")
    add("2025-04-10", "6820", "Landscaping - Irrigation", "GreenScape Contractors", "GSC-IRR-2025", "Annual irrigation maintenance", irrigation_total, "Shared")
    add("2025-03-18", "6830", "Landscaping - Tree Pruning", "ArborCare Ltd.", "ARB-2025-SPRING", "Spring tree pruning", tree_total, "Shared")

    # Snow.
    snow_total = actual["snow"]
    snow_map = periodic_amounts(snow_total, ["JAN", "FEB", "MAR", "NOV", "DEC"], [Decimal("1.4"), Decimal("1.1"), Decimal("0.7"), Decimal("0.8"), Decimal("2.0")])
    for month, month_num in zip(["JAN", "FEB", "MAR", "NOV", "DEC"], [1, 2, 3, 11, 12]):
        add(f"2025-{month_num:02d}-28", "6900", "Snow & Ice", "Snowman Contracting", f"SNOW-2025-{month}", "Snow plowing and salting", snow_map[month], "Shared")

    return sorted(rows, key=lambda row: (row["Date"], row["Account"], row["Invoice Ref"]))


def build_budget_md(case: CaseDefinition, budget: dict[str, Decimal], leases: list[dict[str, Any]]) -> str:
    total_budget = sum(budget[key] for key in ("realty_tax", "utilities", "repairs_maintenance", "management_fee", "janitorial", "insurance", "security", "landscaping", "snow"))
    lines = [
        f"# {case.property_name} — FY2025 CAM Budget",
        "",
        "| Category | FY2025 Budget |",
        "|----------|--------------:|",
        f"| Realty Tax | ${budget['realty_tax']:,.2f} |",
        f"| Utilities (electric, gas, water) | ${budget['utilities']:,.2f} |",
        f"| R&M (building systems, elevators, general) | ${budget['repairs_maintenance']:,.2f} |",
        f"| Management Fee (4% of projected EGI ${budget['management_fee'] / Decimal('0.04'):,.2f}) | ${budget['management_fee']:,.2f} |",
        f"| Janitorial (common areas + tenant suites per lease) | ${budget['janitorial']:,.2f} |",
        f"| Insurance (property + liability) | ${budget['insurance']:,.2f} |",
        f"| Security (monitored alarm + patrol) | ${budget['security']:,.2f} |",
        f"| Landscaping (maintenance + seasonal refresh) | ${budget['landscaping']:,.2f} |",
        f"| Snow & Ice Management | ${budget['snow']:,.2f} |",
        f"| **Total Recoverable Budget** | **${total_budget:,.2f}** |",
        "",
        "## Tenant Annual CAM Pre-Bills",
        "",
        "| Unit/Suite | Tenant | Lease Type | Annual CAM Pre-Bill | Monthly CAM Pre-Bill |",
        "|------------|--------|------------|--------------------:|---------------------:|",
    ]
    for lease in leases:
        annual = money(lease.get("annual_prebilled", "0"))
        lines.append(
            f"| {lease['unit_label']} | {lease['tenant_name']} | {lease['lease_type']} | ${annual:,.2f} | ${money(annual / Decimal('12')):,.2f} |"
        )
    lines.extend(
        [
            "",
            "This budget is the basis for tenant pre-bills and the benchmark for the FY2025 reconciliation.",
        ]
    )
    return "\n".join(lines) + "\n"


def build_property_fact_sheet(case: CaseDefinition, actual: dict[str, Decimal], leases: list[dict[str, Any]]) -> str:
    lines = [
        f"# {case.property_name} — Property Fact Sheet",
        "",
        "| Field | Value |",
        "|-------|-------|",
        f"| Address | {case.address} |",
        f"| Total RSF | {case.office_rsf + case.retail_rsf:,} |",
        f"| Office RSF | {case.office_rsf:,} |",
        f"| Retail RSF | {case.retail_rsf:,} |",
        f"| Gross Potential Income | ${actual['_gross_potential_income']:,.2f} |",
        f"| Effective Gross Income | ${actual['_effective_gross_income']:,.2f} |",
        f"| Projected Effective Gross Income | ${actual['_projected_effective_gross_income']:,.2f} |",
        "",
        "## Tenant Roster",
        "",
        "| Unit/Suite | Tenant | Pool | RSF | Lease Type |",
        "|------------|--------|------|----:|------------|",
    ]
    for lease in leases:
        lines.append(
            f"| {lease['unit_label']} | {lease['tenant_name']} | {lease['pool']} | {lease['rsf']:,} | {lease['lease_type']} |"
        )
    lines.extend(
        [
            "",
            "The benchmark packet includes the GL extract, budget, and lease excerpts required to assess recoverability.",
        ]
    )
    return "\n".join(lines) + "\n"


def build_lease_excerpts(case: CaseDefinition, leases: list[dict[str, Any]]) -> str:
    lines = [
        f"# {case.property_name} — Lease Excerpts",
        "",
        "## Standard Form Lease — Operating Expenses",
        "",
        "**§6.01 Definitions.** Operating Expenses include reasonable costs incurred in ownership, operation, maintenance, repair, insurance, supervision, and administration of the Building.",
        "",
        "**§6.02 Tenant's Proportionate Share.** Tenant pays its Proportionate Share of Operating Expenses allocable to the applicable Pool.",
        "",
        "**§6.03 Exclusions.** Operating Expenses do not include:",
        "- one-time extraordinary charges arising from tenant turnover, including move-out deep cleaning, suite restoration, and demising work;",
        "- amounts posted to the general ledger in error, including duplicate invoices or unsupported entries;",
        "",
    ]
    if case.include_cap:
        lines.extend(
            [
                "## Retail Bank CAM Cap Rider",
                "",
                "**§6.05.** Controllable Operating Expenses are capped at 104% compounded annually over the 2022 Base Year CAM.",
                "",
                "**§6.05.1.** Realty tax, insurance, utilities, and snow removal pass through without the cap.",
                "",
            ]
        )
    if case.include_base_year_retail or case.include_base_year_office:
        lines.extend(
            [
                "## Base Year Rider",
                "",
                "**§6.06.** Tenant pays only the increase in Operating Expenses above the stated Base Year CAM.",
                "",
            ]
        )
    if case.include_modified_gross:
        lines.extend(
            [
                "## Modified Gross Fitness Rider",
                "",
                "**§6.07(a).** All utility costs are excluded from the tenant's Operating Expense share.",
                "",
                "**§6.07(b).** All repair and maintenance expenses are excluded from the tenant's Operating Expense share.",
                "",
            ]
        )
    if case.include_restaurant_exclusion:
        lines.extend(
            [
                "## Restaurant Exclusion Schedule",
                "",
                "**Schedule C.1.** Grease trap servicing and associated compliance costs are billed directly to the restaurant tenant and excluded from CAM recovery.",
                "",
            ]
        )
    if case.management_fee_excess:
        lines.extend(
            [
                "## Management Agreement §4.1",
                "",
                "Management fee equals 4.0% of Effective Gross Income, not Gross Potential Income.",
                "",
                "Any amount paid above the EGI-based fee is not recoverable from tenants.",
                "",
            ]
        )
    return "\n".join(lines)


def corrected_total(actual: dict[str, Decimal], case: CaseDefinition) -> Decimal:
    raw_total = sum(actual[key] for key in ("realty_tax", "utilities", "repairs_maintenance", "management_fee", "janitorial", "insurance", "security", "landscaping", "snow"))
    return money(raw_total - case.duplicate_amount - case.turnover_amount - case.management_fee_excess)


def issue_metadata(case: CaseDefinition) -> dict[str, Any]:
    duplicate_meta = None
    if case.duplicate_kind == "gas":
        duplicate_meta = {"category": "utilities", "invoice_ref": f"GA-2025-{case.case_id[-2:]}-4471", "keywords": ["duplicate", "gas", "re-entered"]}
    elif case.duplicate_kind == "electric":
        duplicate_meta = {"category": "utilities", "invoice_ref": "ALT-2025-DEC", "keywords": ["duplicate", "electric", "re-entered"]}
    elif case.duplicate_kind == "water":
        duplicate_meta = {"category": "utilities", "invoice_ref": f"ROP-{case.case_id[-2:]}-DUP", "keywords": ["duplicate", "water", "re-entered"]}
    elif case.duplicate_kind == "security_patrol":
        duplicate_meta = {"category": "security", "invoice_ref": f"GW-{case.case_id[-2:]}-DUP", "keywords": ["duplicate", "patrol", "re-entered"]}
    elif case.duplicate_kind == "janitorial_day_porter":
        duplicate_meta = {"category": "janitorial", "invoice_ref": f"CPS-DP-{case.case_id[-2:]}-DUP", "keywords": ["duplicate", "day porter", "re-entered"]}

    turnover_meta = None
    if case.turnover_amount:
        turnover_meta = {
            "invoice_ref": f"TURN-{case.case_id[-2:]}-1018",
            "keywords": ["turnover", "move-out", "deep clean"],
        }

    management_meta = None
    if case.management_fee_excess:
        management_meta = {
            "keywords": ["effective gross income", "gross potential income", "management fee", "EGI"],
        }

    return {
        "duplicate": duplicate_meta,
        "turnover": turnover_meta,
        "management_fee": management_meta,
    }


def build_case(case: CaseDefinition) -> dict[str, Any]:
    budget = build_budget(case)
    budget_total = sum(budget[key] for key in ("realty_tax", "utilities", "repairs_maintenance", "management_fee", "janitorial", "insurance", "security", "landscaping", "snow"))
    leases = build_tenants(case, budget_total)
    actual = build_actual_totals(case, budget)
    gl_rows = build_gl_rows(case, actual, include_restaurant=case.include_restaurant_exclusion)

    property_payload = {
        "id": case.case_id,
        "name": case.property_name,
        "address": case.address,
        "rsf_total": case.office_rsf + case.retail_rsf,
        "rsf_retail": case.retail_rsf,
        "rsf_office": case.office_rsf,
        "gross_potential_income": str(actual["_gross_potential_income"]),
        "effective_gross_income": str(actual["_effective_gross_income"]),
        "projected_effective_gross_income": str(actual["_projected_effective_gross_income"]),
        "vacancy_loss": str(actual["_vacancy_loss"]),
        "credit_allowance": str(actual["_credit_allowance"]),
        "pools": [
            {"name": "office", "rsf": case.office_rsf, "share_of_total": float(money(Decimal(case.office_rsf) / Decimal(case.office_rsf + case.retail_rsf)))},
            {"name": "retail", "rsf": case.retail_rsf, "share_of_total": float(money(Decimal(case.retail_rsf) / Decimal(case.office_rsf + case.retail_rsf)))},
        ],
    }

    case_dir = CASES_ROOT / case.case_id
    case_dir.mkdir(parents=True, exist_ok=True)
    write_yaml(case_dir / "property.yaml", property_payload)
    write_json(case_dir / "leases.json", leases)
    budget_md = build_budget_md(case, budget, leases)
    (case_dir / "budget.md").write_text(budget_md, encoding="utf-8")
    (case_dir / "2025_CAM_Budget.md").write_text(budget_md, encoding="utf-8")
    property_md = build_property_fact_sheet(case, actual, leases)
    (case_dir / "Property_Fact_Sheet.md").write_text(property_md, encoding="utf-8")
    lease_md = build_lease_excerpts(case, leases)
    (case_dir / "Lease_Excerpts_CAM_Clauses.md").write_text(lease_md, encoding="utf-8")
    write_csv(case_dir / "gl.csv", gl_rows)
    write_csv(case_dir / "2025_GL_Extract.csv", gl_rows)
    readme_case = "\n".join(
        [
            f"# {case.property_name} — Benchmark Case",
            "",
            "Manual Anthropic run packet:",
            "- `Property_Fact_Sheet.md`",
            "- `2025_CAM_Budget.md`",
            "- `2025_GL_Extract.csv`",
            "- `Lease_Excerpts_CAM_Clauses.md`",
            "",
            "Plugin input files for `cam-reconciliation-cre`:",
            "- `property.yaml`",
            "- `leases.json`",
            "- `gl.csv`",
            "- `budget.md`",
        ]
    ) + "\n"
    (case_dir / "README_CASE.md").write_text(readme_case, encoding="utf-8")

    packet_dir = PACKETS_ROOT / case.case_id
    packet_dir.mkdir(parents=True, exist_ok=True)
    (packet_dir / "Property_Fact_Sheet.md").write_text(property_md, encoding="utf-8")
    (packet_dir / "2025_CAM_Budget.md").write_text(budget_md, encoding="utf-8")
    write_csv(packet_dir / "2025_GL_Extract.csv", gl_rows)
    (packet_dir / "Lease_Excerpts_CAM_Clauses.md").write_text(lease_md, encoding="utf-8")
    (packet_dir / "README.md").write_text(
        "\n".join(
            [
                f"# {case.property_name} — Anthropic Packet",
                "",
                "This directory contains only the materials needed for a manual reconciliation review.",
                "",
                "Suggested Claude workflow:",
                "1. `/reconciliation opex 2025`",
                "2. `/variance-analysis opex 2025 vs budget`",
                "3. `/income-statement annual 2025`",
                "4. Ask: `Based on the lease excerpts, what is the corrected FY2025 recoverable operating expense total after removing non-recoverable items?`",
                "",
                "Save the combined answer outside this packet as:",
                f"`plugins/cam-reconciliation-cre/benchmarks/unseen_cam_suite/results/anthropic/{case.case_id}/anthropic_output.txt`",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    raw_total = money(sum(actual[key] for key in ("realty_tax", "utilities", "repairs_maintenance", "management_fee", "janitorial", "insurance", "security", "landscaping", "snow")))
    corrected = corrected_total(actual, case)
    gold_payload = {
        "case_id": case.case_id,
        "property_name": case.property_name,
        "budget_total": str(money(budget_total)),
        "raw_actual_total": str(raw_total),
        "corrected_recoverable_total": str(corrected),
        "duplicate_amount": str(case.duplicate_amount),
        "turnover_amount": str(case.turnover_amount),
        "management_fee_excess": str(case.management_fee_excess),
        "scenario_flags": {
            "include_cap": case.include_cap,
            "cap_binding": case.cap_binding,
            "include_modified_gross": case.include_modified_gross,
            "include_restaurant_exclusion": case.include_restaurant_exclusion,
            "include_base_year_retail": case.include_base_year_retail,
            "include_base_year_office": case.include_base_year_office,
            "include_vacancy": case.include_vacancy,
        },
        "issues": issue_metadata(case),
    }
    write_json(GOLD_ROOT / f"{case.case_id}.json", gold_payload)
    return gold_payload


def write_suite_readme(manifest: list[dict[str, Any]]) -> None:
    lines = [
        "# Unseen CAM Benchmark Suite",
        "",
        "Ten unseen benchmark properties for comparing Anthropic's finance plugin workflow against `cam-reconciliation-cre`.",
        "",
        "## Layout",
        "",
        "- `cases/<case_id>/` contains the manual review packet and plugin input files.",
        "- `anthropic_packets/<case_id>/` contains only the user-facing review materials for a cleaner Claude run.",
        "- `gold/<case_id>.json` contains hidden expected totals and scenario metadata.",
        "- `results/ours/` is populated by the local benchmark harness.",
        "- `results/anthropic/` is where you should place Claude Code finance-plugin outputs for scoring.",
        "",
        "## Manual Anthropic Procedure",
        "",
        "For each packet directory, open Claude Code in `anthropic_packets/<case_id>/` and run:",
        "",
        "1. `/reconciliation opex 2025`",
        "2. `/variance-analysis opex 2025 vs budget`",
        "3. `/income-statement annual 2025`",
        "4. A follow-up prompt: `Based on the lease excerpts, what is the corrected FY2025 recoverable operating expense total after removing non-recoverable items?`",
        "",
        "Save the combined output as:",
        "",
        "`plugins/cam-reconciliation-cre/benchmarks/unseen_cam_suite/results/anthropic/<case_id>/anthropic_output.txt`",
        "",
        "Then run:",
        "",
        "```bash",
        "python3 plugins/cam-reconciliation-cre/scripts/score_anthropic_benchmark.py",
        "```",
        "",
        "## Cases",
        "",
        "| Case | Property | Notes |",
        "|------|----------|-------|",
    ]
    for item in manifest:
        flags = item["scenario_flags"]
        notes: list[str] = []
        if item["duplicate_amount"] != "0":
            notes.append("duplicate")
        if item["turnover_amount"] != "0":
            notes.append("turnover")
        if item["management_fee_excess"] != "0":
            notes.append("mgmt fee")
        if flags["include_cap"]:
            notes.append("cap")
        if flags["include_base_year_retail"] or flags["include_base_year_office"]:
            notes.append("base year")
        if flags["include_modified_gross"]:
            notes.append("modified gross")
        if flags["include_restaurant_exclusion"]:
            notes.append("specific exclusion")
        if flags["include_vacancy"]:
            notes.append("vacancy")
        lines.append(f"| {item['case_id']} | {item['property_name']} | {', '.join(notes)} |")
    (SUITE_ROOT / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def public_manifest_item(item: dict[str, Any]) -> dict[str, Any]:
    return {
        "case_id": item["case_id"],
        "property_name": item["property_name"],
        "scenario_flags": item["scenario_flags"],
    }


def main() -> None:
    CASES_ROOT.mkdir(parents=True, exist_ok=True)
    GOLD_ROOT.mkdir(parents=True, exist_ok=True)
    RESULTS_ROOT.mkdir(parents=True, exist_ok=True)
    PACKETS_ROOT.mkdir(parents=True, exist_ok=True)

    manifest = [build_case(case) for case in CASE_DEFINITIONS]
    write_json(SUITE_ROOT / "benchmark_manifest.json", [public_manifest_item(item) for item in manifest])
    write_json(GOLD_ROOT / "benchmark_manifest.json", manifest)
    write_suite_readme(manifest)
    print(json.dumps({"cases_built": len(manifest), "suite_root": str(SUITE_ROOT)}, indent=2))


if __name__ == "__main__":
    main()
