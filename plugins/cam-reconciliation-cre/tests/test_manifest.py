"""Manifest model and serialization tests."""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal

import pytest

from scripts.manifest import (
    BaseYearConfig,
    CapConfig,
    GLLine,
    Lease,
    LeaseType,
    Manifest,
    Pool,
    PoolName,
    Property,
    Provenance,
)
from scripts.validation import ManifestJSONEncoder, ValidationError


def minimal_manifest() -> Manifest:
    return Manifest(
        property=Property(
            id="matheson",
            name="Matheson Gateway Centre",
            address="2450 Matheson Blvd East, Mississauga, ON",
            rsf_total=62000,
            rsf_retail=20000,
            rsf_office=42000,
            pools=[
                Pool(name=PoolName.OFFICE, rsf=42000, share_of_total=Decimal("0.6774")),
                Pool(name=PoolName.RETAIL, rsf=20000, share_of_total=Decimal("0.3226")),
            ],
            gross_potential_income=Decimal("2870000"),
            effective_gross_income=Decimal("2770000"),
        ),
        fiscal_year=2025,
        budget={"realty_tax": Decimal("420000")},
        leases=[
            Lease(
                tenant_id="unit_102",
                tenant_name="Brewhouse Coffee Co.",
                unit_label="Unit 102",
                rsf=1800,
                pool=PoolName.RETAIL,
                pro_rata_of_pool=Decimal("0.09"),
                lease_type=LeaseType.NET,
                annual_prebilled=Decimal("32058"),
            )
        ],
        gl_lines=[
            GLLine(
                line_id="gl_0001",
                date="2025-01-15",
                account="6100",
                category_raw="Realty Tax",
                vendor="City of Mississauga",
                invoice_ref="TAX-2025-JAN",
                memo="Interim billing",
                amount=Decimal("35000"),
                pool_hint="Shared",
            )
        ],
        provenance=Provenance(
            plugin_version="0.1.0",
            run_timestamp=datetime(2026, 4, 15, 10, 50),
            inputs_hash="sha256:abc",
        ),
    )


def test_manifest_round_trip(tmp_path):
    manifest = minimal_manifest()
    path = tmp_path / "manifest.json"
    manifest.save(path)
    loaded = Manifest.load(path)
    assert loaded.property.name == manifest.property.name
    assert loaded.leases[0].tenant_id == "unit_102"
    assert loaded.gl_lines[0].amount == Decimal("35000")


def test_manifest_rejects_unknown_root_field():
    import json

    data = json.loads(json.dumps(minimal_manifest(), cls=ManifestJSONEncoder))
    data["unknown_field"] = "oops"
    with pytest.raises(ValidationError):
        Manifest.from_dict(data)


def test_lease_cap_config():
    cap = CapConfig(
        base_year=2022,
        base_year_cam_psf=Decimal("11.40"),
        annual_increase_rate=Decimal("0.04"),
        uncontrollable_categories=["realty_tax", "insurance", "utilities", "snow"],
    )
    assert cap.annual_increase_rate == Decimal("0.04")


def test_base_year_config():
    base_year = BaseYearConfig(year=2024, cam_psf=Decimal("15.40"))
    assert base_year.cam_psf == Decimal("15.40")
    assert base_year.gross_up_to_percent == Decimal("1.0")
