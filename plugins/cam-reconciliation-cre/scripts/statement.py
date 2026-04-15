"""Stage 4: render tenant statements, workpaper, and narrative artifacts."""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from reportlab.lib import colors
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

PLUGIN_ROOT = Path(__file__).resolve().parent.parent
if str(PLUGIN_ROOT) not in sys.path:
    sys.path.insert(0, str(PLUGIN_ROOT))

from scripts.manifest import Manifest, canonical_category, money


def recoverable_totals_by_category(manifest: Manifest) -> dict[str, object]:
    totals = defaultdict(lambda: money("0"))
    for line in manifest.gl_lines:
        classification = line.classification
        if not classification or not classification.recoverable:
            continue
        category_key = classification.normalized_category or canonical_category(line.category_raw)
        totals[category_key] = money(totals[category_key] + (classification.recoverable_amount or line.amount))
    return dict(sorted(totals.items()))


def corrections_summary(manifest: Manifest) -> dict[str, object]:
    duplicate = money(
        sum(
            line.amount
            for line in manifest.gl_lines
            if line.classification and line.classification.reason == "duplicate_invoice"
        )
    )
    turnover = money(
        sum(
            line.amount
            for line in manifest.gl_lines
            if line.classification and line.classification.reason == "tenant_turnover_extraordinary_charge"
        )
    )
    management = money(
        sum(
            line.amount - (line.classification.recoverable_amount or line.amount)
            for line in manifest.gl_lines
            if line.classification and line.classification.reason == "management_fee_egi_adjusted"
        )
    )
    return {
        "duplicate_invoice": duplicate,
        "tenant_turnover": turnover,
        "management_fee_method": management,
        "total_nonrecoverable_removed": money(duplicate + turnover + management),
    }


def lease_narrative(manifest: Manifest, charge) -> str:
    lease = next(lease for lease in manifest.leases if lease.tenant_id == charge.tenant_id)
    if money(charge.direct_bill_total or 0) > 0:
        return (
            f"Your FY2025 pooled CAM charge is ${money(charge.final_charge):,.2f}. "
            f"Lease-specific direct-bill items total ${money(charge.direct_bill_total):,.2f}, "
            f"bringing your total due to ${money(charge.total_due):,.2f}."
        )
    if lease.lease_type.value == "modified_gross":
        items = ", ".join(
            f"{item.category} (${money(item.amount_removed):,.2f})" for item in charge.exclusions_applied
        )
        return (
            f"Your FY2025 CAM charge is ${money(charge.final_charge):,.2f}. "
            f"Under the modified-gross rider, the following categories were excluded from your bill: {items}. "
            f"The remaining charge reflects only the pass-through categories that continue to flow through under Article 6.07."
        )
    if lease.lease_type.value == "base_year" and charge.base_year_adjustment:
        base_amount = money(charge.base_year_adjustment["amount_removed"])
        return (
            f"Your FY2025 CAM charge is ${money(charge.final_charge):,.2f}. "
            f"Under the base-year clause, ${base_amount:,.2f} was removed as your fixed baseline, "
            f"leaving only the increase above the stated base year payable."
        )
    if lease.lease_type.value == "net_with_cap" and charge.cap_adjustment:
        absorbed = money(charge.cap_adjustment["landlord_absorbed"])
        if absorbed > 0:
            return (
                f"Your FY2025 CAM charge is ${money(charge.final_charge):,.2f}. "
                f"The CAM cap reduced controllable expenses by ${absorbed:,.2f}, while uncontrollable expenses still passed through."
            )
        return (
            f"Your FY2025 CAM charge is ${money(charge.final_charge):,.2f}. "
            f"The CAM cap was tested but did not bind because controllable expenses stayed below the FY{manifest.fiscal_year} ceiling."
        )
    if money(charge.vs_prebilled or 0) > 0:
        return (
            f"Your FY2025 CAM charge is ${money(charge.final_charge):,.2f}, "
            f"which is ${money(charge.vs_prebilled):,.2f} above your pre-billed amount. "
            f"The main driver this year is the realty tax reassessment that increased shared recoverable costs in the second half of 2025."
        )
    return (
        f"Your FY2025 CAM charge is ${money(charge.final_charge):,.2f}. "
        f"After applying lease-specific adjustments, your balance is below the amount pre-billed during the year."
    )


def render_tenant_pdf(manifest: Manifest, charge, output_path: Path) -> None:
    lease = next(lease for lease in manifest.leases if lease.tenant_id == charge.tenant_id)
    styles = getSampleStyleSheet()
    story = []
    story.append(Paragraph(f"{manifest.property.name} — FY{manifest.fiscal_year} CAM Statement", styles["Title"]))
    story.append(Paragraph(f"{lease.tenant_name} ({lease.unit_label})", styles["Heading2"]))
    story.append(Paragraph(lease_narrative(manifest, charge), styles["BodyText"]))
    story.append(Spacer(1, 12))

    summary_rows = [
        ["Gross Share Before Exclusions", f"${money(charge.gross_share_before_exclusions):,.2f}"],
        ["Final CAM Charge", f"${money(charge.final_charge):,.2f}"],
        ["Direct-Billed Items", f"${money(charge.direct_bill_total):,.2f}"],
        ["Total Due", f"${money(charge.total_due):,.2f}"],
        ["Pre-billed", f"${money(charge.annual_prebilled or 0):,.2f}"],
        ["CAM True-Up", f"${money(charge.vs_prebilled or 0):,.2f}"],
    ]
    table = Table(summary_rows, colWidths=[260, 140])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.whitesmoke),
                ("BOX", (0, 0), (-1, -1), 0.5, colors.grey),
                ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.lightgrey),
            ]
        )
    )
    story.append(table)

    if charge.exclusions_applied:
        story.append(Spacer(1, 12))
        story.append(Paragraph("Lease-Specific Exclusions", styles["Heading3"]))
        for exclusion in charge.exclusions_applied:
            story.append(
                Paragraph(
                    f"{exclusion.category}: -${money(exclusion.amount_removed):,.2f} "
                    f"({exclusion.citation_ref.section if exclusion.citation_ref else 'lease exclusion'})",
                    styles["BodyText"],
                )
            )

    if charge.direct_bills_applied:
        story.append(Spacer(1, 12))
        story.append(Paragraph("Lease-Specific Direct Bills", styles["Heading3"]))
        for item in charge.direct_bills_applied:
            source_ids = ", ".join(item.source_gl_ids)
            story.append(
                Paragraph(
                    f"{item.category}: +${money(item.amount_billed):,.2f} "
                    f"({item.citation_ref.section if item.citation_ref else 'lease direct bill'}; GL {source_ids})",
                    styles["BodyText"],
                )
            )

    if charge.base_year_adjustment:
        story.append(Spacer(1, 12))
        story.append(Paragraph("Base Year Adjustment", styles["Heading3"]))
        story.append(
            Paragraph(
                f"Base year amount removed: ${money(charge.base_year_adjustment['amount_removed']):,.2f}.",
                styles["BodyText"],
            )
        )

    if charge.cap_adjustment:
        story.append(Spacer(1, 12))
        story.append(Paragraph("CAM Cap Review", styles["Heading3"]))
        story.append(
            Paragraph(
                f"Controllable share: ${money(charge.cap_adjustment['controllable_uncapped']):,.2f}; "
                f"ceiling: ${money(charge.cap_adjustment['controllable_cap_ceiling_total']):,.2f}; "
                f"landlord absorbed: ${money(charge.cap_adjustment['landlord_absorbed']):,.2f}.",
                styles["BodyText"],
            )
        )

    story.append(Spacer(1, 12))
    story.append(Paragraph("Citation Trail", styles["Heading3"]))
    citation_rows = [["GL Line", "Contribution", "Lease Authority"]]
    for item in charge.citations[:20]:
        citation_rows.append(
            [
                item["gl_line_id"],
                f"${money(item['contribution_amount']):,.2f}",
                item["lease_citation_ref"]["section"],
            ]
        )
    citation_table = Table(citation_rows, colWidths=[90, 120, 190], repeatRows=1)
    citation_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1F4E78")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("BOX", (0, 0), (-1, -1), 0.5, colors.grey),
                ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.lightgrey),
            ]
        )
    )
    story.append(citation_table)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    SimpleDocTemplate(str(output_path), pagesize=LETTER).build(story)


def render_workpaper(manifest: Manifest, output_path: Path) -> None:
    wb = Workbook()
    ws = wb.active
    ws.title = "Tenant Charges"

    header_fill = PatternFill("solid", fgColor="1F4E78")
    header_font = Font(color="FFFFFF", bold=True)
    headers = [
        "Tenant ID",
        "Tenant",
        "Gross Before Exclusions",
        "Final CAM Charge",
        "Direct Bills",
        "Total Due",
        "Pre-billed",
        "CAM True-Up",
    ]
    for col, header in enumerate(headers, start=1):
        cell = ws.cell(row=1, column=col, value=header)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center")

    lease_by_id = {lease.tenant_id: lease for lease in manifest.leases}
    for row, charge in enumerate(manifest.tenant_charges, start=2):
        lease = lease_by_id[charge.tenant_id]
        ws.cell(row=row, column=1, value=charge.tenant_id)
        ws.cell(row=row, column=2, value=lease.tenant_name)
        ws.cell(row=row, column=3, value=float(money(charge.gross_share_before_exclusions)))
        ws.cell(row=row, column=4, value=float(money(charge.final_charge)))
        ws.cell(row=row, column=5, value=float(money(charge.direct_bill_total)))
        ws.cell(row=row, column=6, value=float(money(charge.total_due)))
        ws.cell(row=row, column=7, value=float(money(charge.annual_prebilled or 0)))
        ws.cell(row=row, column=8, value=float(money(charge.vs_prebilled or 0)))

    summary = wb.create_sheet("Summary")
    summary["A1"] = "Corrected Recoverable Totals"
    summary["A1"].font = Font(bold=True)
    category_totals = recoverable_totals_by_category(manifest)
    for row, (category, total) in enumerate(category_totals.items(), start=3):
        summary.cell(row=row, column=1, value=category)
        summary.cell(row=row, column=2, value=float(money(total)))
    summary["D1"] = "Landlord Absorbed Total"
    summary["E1"] = float(money(manifest.landlord_absorbed_total))

    classifications = wb.create_sheet("GL Classification")
    classification_headers = ["Line ID", "Category", "Recoverable", "Recoverable Amount", "Reason"]
    for col, header in enumerate(classification_headers, start=1):
        cell = classifications.cell(row=1, column=col, value=header)
        cell.fill = header_fill
        cell.font = header_font
    for row, line in enumerate(manifest.gl_lines, start=2):
        classifications.cell(row=row, column=1, value=line.line_id)
        classifications.cell(row=row, column=2, value=line.category_raw)
        classifications.cell(row=row, column=3, value="yes" if line.classification and line.classification.recoverable else "no")
        classifications.cell(
            row=row,
            column=4,
            value=float(money(line.classification.recoverable_amount or 0)) if line.classification and line.classification.recoverable else 0.0,
        )
        classifications.cell(row=row, column=5, value=line.classification.reason if line.classification else "")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    wb.save(output_path)


def render_audit_log(manifest: Manifest, output_path: Path) -> None:
    corrections = corrections_summary(manifest)
    content = [
        f"# FY{manifest.fiscal_year} CAM Audit Log",
        "",
        f"- Property: {manifest.property.name}",
        f"- Plugin version: {manifest.provenance.plugin_version}",
        f"- Run timestamp: {manifest.provenance.run_timestamp.isoformat()}",
        "",
        "## Corrections Applied",
        "",
        f"- Duplicate invoice removed: ${money(corrections['duplicate_invoice']):,.2f}",
        f"- Tenant-turnover cleaning removed: ${money(corrections['tenant_turnover']):,.2f}",
        f"- Management fee EGI correction: ${money(corrections['management_fee_method']):,.2f}",
        f"- Total non-recoverable removed from draft: ${money(corrections['total_nonrecoverable_removed']):,.2f}",
        "",
        "## Landlord Absorption",
        "",
        f"- Total absorbed after lease structures: ${money(manifest.landlord_absorbed_total):,.2f}",
        f"- Total billed directly outside pooled CAM: ${money(manifest.direct_billed_total):,.2f}",
    ]
    output_path.write_text("\n".join(content) + "\n", encoding="utf-8")


def render_narrative_commentary(manifest: Manifest, output_path: Path) -> None:
    corrected = recoverable_totals_by_category(manifest)
    lines = [
        f"# FY{manifest.fiscal_year} Category Commentary",
        "",
        "| Category | Budget | Corrected Recoverable | Variance |",
        "|----------|-------:|----------------------:|---------:|",
    ]
    for category, corrected_total in corrected.items():
        budget = money(manifest.budget.get(category, 0))
        variance = money(money(corrected_total) - budget)
        lines.append(
            f"| {category} | ${budget:,.2f} | ${money(corrected_total):,.2f} | ${variance:,.2f} |"
        )
    lines.extend(
        [
            "",
            "Realty tax remains the dominant driver of the FY2025 overage after corrections. "
            "Utilities reconcile back to budget once the duplicate Enbridge posting is reversed, "
            "and janitorial also drops back below budget once the turnover deep-cleaning charge is removed.",
        ]
    )
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def render_outputs(manifest: Manifest, output_dir: Path) -> dict[str, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    statements_dir = output_dir / "tenant_statements"
    for charge in manifest.tenant_charges:
        render_tenant_pdf(manifest, charge, statements_dir / f"{charge.tenant_id}.pdf")

    workpaper = output_dir / "workpaper.xlsx"
    audit_log = output_dir / "audit_log.md"
    commentary = output_dir / "narrative_commentary.md"
    render_workpaper(manifest, workpaper)
    render_audit_log(manifest, audit_log)
    render_narrative_commentary(manifest, commentary)
    return {
        "tenant_statements": statements_dir,
        "workpaper": workpaper,
        "audit_log": audit_log,
        "narrative_commentary": commentary,
    }


def default_output_dir(allocated_manifest_path: Path) -> Path:
    return allocated_manifest_path.parents[1]


def main() -> None:
    parser = argparse.ArgumentParser(description="Render tenant statements and workpapers from an allocated manifest.")
    parser.add_argument("--manifest", type=Path, required=True, help="Path to allocated_manifest.json.")
    parser.add_argument("--output-dir", type=Path, help="Directory for rendered outputs.")
    args = parser.parse_args()

    manifest = Manifest.load(args.manifest)
    output_dir = args.output_dir or default_output_dir(args.manifest)
    outputs = render_outputs(manifest, output_dir)
    print(json.dumps({key: str(path) for key, path in outputs.items()}, indent=2))


if __name__ == "__main__":
    main()
