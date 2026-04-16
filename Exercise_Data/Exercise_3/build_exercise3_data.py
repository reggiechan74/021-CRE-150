#!/usr/bin/env python3
"""Build Exercise 3 sample data files: xlsx rent roll, xlsx+csv GL extract, PDF lease excerpts."""

import csv
from pathlib import Path
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
)
from reportlab.lib import colors

OUT = Path("/home/reggiechan/reggie-life-plan/01_FINANCIAL/1_TENEBRUS_CAPITAL/Services/Training/Curriculum/CRE/CRE-150/04-materials/Exercise_Data/Exercise_3")
OUT.mkdir(parents=True, exist_ok=True)

# ============================================================================
# 1. RENT ROLL (xlsx)
# ============================================================================

def build_rent_roll():
    wb = Workbook()
    ws = wb.active
    ws.title = "Rent Roll FY2025"

    hdr_fill = PatternFill("solid", fgColor="1F4E78")
    hdr_font = Font(bold=True, color="FFFFFF", size=11)
    bold = Font(bold=True)
    money = '"$"#,##0.00'
    pct = '0.00%'
    thin = Side(style='thin', color='CCCCCC')
    border = Border(left=thin, right=thin, top=thin, bottom=thin)

    # Title
    ws["A1"] = "MATHESON GATEWAY CENTRE — FY2025 RENT ROLL"
    ws["A1"].font = Font(bold=True, size=14)
    ws.merge_cells("A1:M1")
    ws["A2"] = "2450 Matheson Blvd East, Mississauga, ON  |  As of December 31, 2025"
    ws["A2"].font = Font(italic=True, size=10, color="555555")
    ws.merge_cells("A2:M2")

    headers = [
        "Unit/Suite", "Tenant", "Use", "RSF", "Pool",
        "Lease Type", "Lease Start", "Lease End",
        "Base Rent PSF", "Annual Base Rent",
        "Pro-Rata % (of pool)", "CAM Treatment", "Notes"
    ]
    for col, h in enumerate(headers, 1):
        c = ws.cell(row=4, column=col, value=h)
        c.font = hdr_font
        c.fill = hdr_fill
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        c.border = border

    rows = [
        # Retail
        ("101", "CanadaFirst Bank", "Retail branch", 4500, "Retail",
         "Net w/ CAM cap", "2021-01-01", "2030-12-31",
         38.00, 171000, 0.2250, "Full pass-through, 4% annual cap over BY 2022 ($11.40)", "Cap ceiling FY2025: $12.82 PSF"),
        ("102", "Brewhouse Coffee Co.", "QSR / café", 1800, "Retail",
         "Net", "2022-06-01", "2027-05-31",
         42.00, 75600, 0.0900, "Full pass-through, no cap", ""),
        ("103", "Matheson Family Dental", "Medical retail", 2500, "Retail",
         "Base Year 2024", "2024-03-01", "2034-02-28",
         32.00, 80000, 0.1250, "Pays FY2025 increases over BY 2024 baseline only", "BY CAM: $15.40 PSF"),
        ("104", "Peak Fitness Studio", "Fitness", 6200, "Retail",
         "Modified gross", "2023-09-01", "2028-08-31",
         22.00, 136400, 0.3100, "EXCLUDED from utilities & R&M allocations", "Pays tax/ins/land/sec/snow/mgmt only"),
        ("105", "Pronto Italian Kitchen", "Full-service restaurant", 5000, "Retail",
         "Net w/ exclusions", "2022-11-01", "2032-10-31",
         34.00, 170000, 0.2500, "Excluded from grease trap, hood cleaning, vent maint.", "Tenant self-performs kitchen-specific R&M"),
        # Office
        ("200", "Harrington & Kline LLP", "Law firm (full floor)", 14000, "Office",
         "Net", "2021-07-01", "2031-06-30",
         28.00, 392000, 0.3333, "Full pass-through", ""),
        ("300", "Meridian Civil Engineering", "Professional services", 8500, "Office",
         "Net", "2023-01-01", "2028-12-31",
         26.00, 221000, 0.2024, "Full pass-through", ""),
        ("310", "Coverpoint Insurance Brokers", "Professional services", 3500, "Office",
         "Base Year 2023", "2023-04-01", "2028-03-31",
         24.00, 84000, 0.0833, "Pays FY2025 increases over BY 2023 baseline only", "BY CAM: $16.10 PSF"),
        ("320", "VACANT (predecessor Apex Consulting Group, lease exp. 2024-12-31)", "Office", 2000, "Office",
         "—", "—", "—",
         0, 0, 0.0476, "Vacant full year 2025 — landlord absorbs share", "Marketing with CBRE; quoted rent $25 PSF net"),
        ("400", "Helix AI Labs", "Technology (full floor)", 14000, "Office",
         "Net", "2024-02-01", "2029-01-31",
         27.00, 378000, 0.3333, "Full pass-through", ""),
    ]

    for r_idx, row in enumerate(rows, start=5):
        for c_idx, val in enumerate(row, start=1):
            c = ws.cell(row=r_idx, column=c_idx, value=val)
            c.border = border
            c.alignment = Alignment(vertical="top", wrap_text=True)
            if c_idx == 4:
                c.number_format = '#,##0'
            elif c_idx == 9:
                c.number_format = money
            elif c_idx == 10:
                c.number_format = money
            elif c_idx == 11:
                c.number_format = pct

    # Totals row
    total_row = len(rows) + 5
    ws.cell(row=total_row, column=1, value="TOTALS").font = bold
    ws.cell(row=total_row, column=4, value=sum(r[3] for r in rows)).font = bold
    ws.cell(row=total_row, column=4).number_format = '#,##0'
    ws.cell(row=total_row, column=10, value=sum(r[9] for r in rows)).font = bold
    ws.cell(row=total_row, column=10).number_format = money
    for c_idx in range(1, 14):
        ws.cell(row=total_row, column=c_idx).fill = PatternFill("solid", fgColor="E8EEF4")
        ws.cell(row=total_row, column=c_idx).border = border

    # Occupancy summary
    summary_row = total_row + 3
    ws.cell(row=summary_row, column=1, value="Occupancy Summary").font = Font(bold=True, size=12)
    ws.cell(row=summary_row+1, column=1, value="Total RSF")
    ws.cell(row=summary_row+1, column=2, value=62000).number_format = '#,##0'
    ws.cell(row=summary_row+2, column=1, value="Leased RSF")
    ws.cell(row=summary_row+2, column=2, value=60000).number_format = '#,##0'
    ws.cell(row=summary_row+3, column=1, value="Vacant RSF (Suite 320 full year)")
    ws.cell(row=summary_row+3, column=2, value=2000).number_format = '#,##0'
    ws.cell(row=summary_row+4, column=1, value="Occupancy %")
    ws.cell(row=summary_row+4, column=2, value=0.9677).number_format = pct

    # Column widths
    widths = [12, 32, 22, 10, 10, 20, 13, 13, 13, 15, 18, 40, 40]
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w

    ws.row_dimensions[4].height = 30
    for r in range(5, total_row):
        ws.row_dimensions[r].height = 32

    wb.save(OUT / "2025_Rent_Roll.xlsx")
    print(f"Wrote {OUT/'2025_Rent_Roll.xlsx'}")


# ============================================================================
# 2. GL EXTRACT (xlsx + csv)
# ============================================================================

# Monthly GL data — every line gets date, account, category, memo, amount, pool
# Discrepancies embedded:
#   (1) Property tax: Jan-Jun @ $35,000/mo, Jul-Dec @ $47,600/mo (+18% full year = +$75,600)
#   (2) Utilities: Enbridge invoice #GA-2025-08-4471 $8,340 posted Aug 22 AND Sep 3 (double post)
#   (3) Janitorial: Oct 18, 2025 Clean Pro one-time deep clean $14,500 — Suite 320 move-out restoration
#   (4) Mgmt fee: 4% applied to GPI $2,870,000 not EGI $2,770,000 → posted $114,800 vs correct $110,800

MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

def gl_rows():
    rows = []  # (date, account_code, category, vendor, invoice_ref, memo, amount, pool)

    # Realty Tax — Jan-Jun $35,000/mo, Jul-Dec $47,600/mo
    for i, m in enumerate(MONTHS):
        month_num = i + 1
        amt = 35000 if i < 6 else 47600
        memo = "Interim billing" if i < 6 else "Post-reassessment billing (MPAC Notice 2025-07-01)"
        rows.append((f"2025-{month_num:02d}-15", "6100", "Realty Tax", "City of Mississauga",
                     f"TAX-2025-{m.upper()}", memo, amt, "Shared"))

    # Insurance — annual, posted Jan 15 $55,000
    rows.append(("2025-01-15", "6200", "Insurance", "Marsh Canada Ltd.",
                 "INS-2025-ANNUAL", "FY2025 annual premium (property + GL + B&M + env.)", 55000, "Shared"))

    # Utilities — Electric (Alectra) monthly ~$9,583
    alectra = [9200, 8800, 8400, 7900, 7600, 8100, 10800, 11400, 10900, 9700, 9900, 12300]
    for i, amt in enumerate(alectra):
        rows.append((f"2025-{i+1:02d}-20", "6310", "Utilities - Electric", "Alectra Utilities",
                     f"ALT-2025-{MONTHS[i].upper()}", f"Common area + base building electric — {MONTHS[i]} 2025", amt, "Shared"))

    # Utilities — Gas (Enbridge) monthly — DOUBLE POST of Dec invoice
    enbridge = [9800, 8400, 6100, 4200, 2800, 2100, 1900, 2000, 2400, 4600, 7800, 9900]
    for i, amt in enumerate(enbridge):
        rows.append((f"2025-{i+1:02d}-22", "6320", "Utilities - Gas", "Enbridge Gas Inc.",
                     f"ENB-2025-{MONTHS[i].upper()}", f"Common area + base building gas — {MONTHS[i]} 2025", amt, "Shared"))
    # Relabel the Dec Enbridge row to the actual invoice number
    for idx, r in enumerate(rows):
        if r[3] == "Enbridge Gas Inc." and r[4] == "ENB-2025-DEC":
            rows[idx] = ("2025-12-22", "6320", "Utilities - Gas", "Enbridge Gas Inc.",
                         "GA-2025-12-4471", "Dec 2025 gas — common area + base building", 9900, "Shared")
            break
    # *** PLANTED DISCREPANCY #4: Double-post of Dec Enbridge invoice ***
    rows.append(("2025-12-29", "6320", "Utilities - Gas", "Enbridge Gas Inc.",
                 "GA-2025-12-4471", "Dec 2025 gas — invoice re-entered in year-end close (DUPLICATE OF 2025-12-22 POSTING)", 9900, "Shared"))

    # Utilities — Water (Region of Peel) quarterly ~$4,500
    for q, month in enumerate([3, 6, 9, 12]):
        rows.append((f"2025-{month:02d}-28", "6330", "Utilities - Water", "Region of Peel",
                     f"ROP-2025-Q{q+1}", f"Q{q+1} 2025 water & sewer", 4500, "Shared"))

    # R&M — Elevator (Kone) monthly ~$1,833 — office pool only
    for i in range(12):
        rows.append((f"2025-{i+1:02d}-05", "6410", "R&M - Elevator", "Kone Elevator Canada",
                     f"KONE-2025-{MONTHS[i].upper()}", f"Monthly elevator service contract — {MONTHS[i]} 2025", 1833, "Office"))

    # R&M — HVAC preventive (quarterly)
    for q, month in enumerate([3, 6, 9, 12]):
        rows.append((f"2025-{month:02d}-12", "6420", "R&M - HVAC", "Mechanical Systems Inc.",
                     f"MSI-2025-Q{q+1}", f"Q{q+1} 2025 HVAC PM (rooftop units, office VAV, retail splits)", 7000, "Shared"))

    # R&M — General (plumbing, electrical, carpentry) — irregular
    rnm_general = [
        ("2025-02-14", "MRO-2025-0214", "Plumbing leak repair - 3rd floor men's washroom", 2400),
        ("2025-03-22", "MRO-2025-0322", "LED retrofit, parking garage fixtures (42 units)", 8900),
        ("2025-04-18", "MRO-2025-0418", "Roof drain flush & membrane inspection", 3100),
        ("2025-05-07", "MRO-2025-0507", "Electrical panel re-termination, Suite 300", 1800),
        ("2025-06-11", "MRO-2025-0611", "Carpentry — lobby millwork repair", 2200),
        ("2025-07-09", "MRO-2025-0709", "HVAC after-hours call — Suite 400 server room cooling", 1650),
        ("2025-08-16", "MRO-2025-0816", "Plumbing — main lobby drinking fountain replacement", 1400),
        ("2025-09-28", "MRO-2025-0928", "Asphalt crack sealing, parking lot (pre-winter)", 6800),
        ("2025-10-30", "MRO-2025-1030", "Electrical — emergency exit sign battery replacement (property-wide)", 2100),
        ("2025-11-18", "MRO-2025-1118", "Plumbing — backflow preventer annual test & certification", 1200),
        ("2025-12-09", "MRO-2025-1209", "Door closer & hardware — various common area doors", 1850),
    ]
    for date, ref, memo, amt in rnm_general:
        rows.append((date, "6430", "R&M - General", "Metro Building Services",
                     ref, memo, amt, "Shared"))

    # R&M — Pest control (quarterly)
    for q, month in enumerate([3, 6, 9, 12]):
        rows.append((f"2025-{month:02d}-20", "6440", "R&M - Pest Control", "Orkin Canada",
                     f"ORK-2025-Q{q+1}", f"Q{q+1} 2025 IPM service — retail + common areas", 1000, "Shared"))

    # R&M — Grease trap (retail pool only)
    for q, month in enumerate([3, 6, 9, 12]):
        rows.append((f"2025-{month:02d}-14", "6450", "R&M - Grease Trap", "Drain Pro Services",
                     f"DPS-2025-Q{q+1}", f"Q{q+1} 2025 grease trap pump-out & inspection (Pronto line excluded per lease)", 1125, "Retail"))

    # R&M — Storefront glass (retail pool only, bi-monthly)
    for i in range(6):
        month = (i * 2) + 1
        rows.append((f"2025-{month:02d}-10", "6460", "R&M - Storefront Glass", "Crystal Clear Window Co.",
                     f"CCW-2025-{MONTHS[month-1].upper()}", f"Bi-monthly retail storefront cleaning — {MONTHS[month-1]} 2025", 1000, "Retail"))

    # R&M - Roof inspection (semi-annual)
    for i, month in enumerate([5, 11]):
        rows.append((f"2025-{month:02d}-08", "6470", "R&M - Roof", "Flynn Canada Roofing",
                     f"FLN-2025-{'SPRING' if i == 0 else 'FALL'}", f"{'Spring' if i == 0 else 'Fall'} roof inspection + minor flashing repair", 3500, "Shared"))

    # Management Fee — monthly, 4% of revenue. Posted on GPI, should be on EGI.
    # FY2025 GPI = $2,870,000 → monthly avg $239,167 → fee @ 4% = $9,566.67
    # But FY2025 EGI = $2,770,000 → should be $230,833/mo → fee $9,233.33
    # Let's vary monthly to look natural but total = $114,800 (GPI basis, error)
    mgmt_monthly_gpi = [
        9520, 9520, 9520, 9520, 9520,  # Jan-May flat
        9566, 9620, 9650, 9620, 9620, 9620, 9504  # Jun-Dec (minor variation)
    ]
    # ensure sum = 114,800
    target = 114800
    diff = target - sum(mgmt_monthly_gpi)
    mgmt_monthly_gpi[-1] += diff
    for i, amt in enumerate(mgmt_monthly_gpi):
        rows.append((f"2025-{i+1:02d}-28", "6500", "Management Fee", "Gateway Property Management Inc.",
                     f"GPM-MF-2025-{MONTHS[i].upper()}", f"Mgmt fee — 4% of {MONTHS[i]} 2025 gross revenue (see calc schedule)", amt, "Shared"))

    # Janitorial — Clean Pro Services monthly contract $4,200
    for i in range(12):
        rows.append((f"2025-{i+1:02d}-02", "6600", "Janitorial - Contract", "Clean Pro Services Ltd.",
                     f"CPS-2025-{MONTHS[i].upper()}", f"Monthly janitorial contract — common areas + office suites (excl. Peak Fitness) — {MONTHS[i]} 2025", 4200, "Shared"))

    # Janitorial — Day porter (retail pool) $2,083/mo
    for i in range(12):
        rows.append((f"2025-{i+1:02d}-02", "6610", "Janitorial - Day Porter", "Clean Pro Services Ltd.",
                     f"CPS-DP-2025-{MONTHS[i].upper()}", f"Day porter — retail concourse — {MONTHS[i]} 2025", 2083, "Retail"))

    # Janitorial — Supplies
    for i, month in enumerate([3, 6, 9, 12]):
        rows.append((f"2025-{month:02d}-15", "6620", "Janitorial - Supplies", "Swish Maintenance",
                     f"SWM-2025-Q{i+1}", f"Q{i+1} 2025 paper products, soap, cleaning supplies", 1500, "Shared"))

    # Janitorial — Window cleaning (semi-annual, interior)
    for i, month in enumerate([5, 10]):
        rows.append((f"2025-{month:02d}-22", "6630", "Janitorial - Window", "Crystal Clear Window Co.",
                     f"CCW-INT-2025-{'SPRING' if i == 0 else 'FALL'}", f"{'Spring' if i == 0 else 'Fall'} interior window cleaning — all floors", 1800, "Shared"))

    # *** JANITORIAL DEEP CLEAN — PLANTED DISCREPANCY #3 ***
    rows.append(("2025-10-18", "6600", "Janitorial - Contract", "Clean Pro Services Ltd.",
                 "CPS-SPECIAL-2025-1018",
                 "Suite 320 move-out deep clean & restoration (predecessor Apex Consulting) — post-vacate cleaning, carpet extraction, wall spot-paint, kitchenette degrease",
                 14500, "Office"))

    # Security — GardaWorld monthly $3,000
    for i in range(12):
        rows.append((f"2025-{i+1:02d}-05", "6700", "Security - Patrol", "GardaWorld",
                     f"GW-2025-{MONTHS[i].upper()}", f"Monthly mobile patrol (3 visits/night) — {MONTHS[i]} 2025", 3000, "Shared"))

    # Security — ADT monitored alarm monthly $500
    for i in range(12):
        rows.append((f"2025-{i+1:02d}-12", "6710", "Security - Alarm", "ADT Commercial",
                     f"ADT-2025-{MONTHS[i].upper()}", f"Monitored alarm — {MONTHS[i]} 2025", 500, "Shared"))

    # Security — Card access maintenance (quarterly)
    for q, month in enumerate([3, 6, 9, 12]):
        rows.append((f"2025-{month:02d}-18", "6720", "Security - Access Control", "SecureTech Inc.",
                     f"ST-2025-Q{q+1}", f"Q{q+1} 2025 card access system maintenance", 750, "Shared"))

    # Landscaping — Apr-Nov weekly @ $687.50 (rough)
    landscaping_months = [4, 5, 6, 7, 8, 9, 10, 11]
    for m in landscaping_months:
        rows.append((f"2025-{m:02d}-30", "6800", "Landscaping - Maintenance", "GreenScape Contractors",
                     f"GSC-2025-{MONTHS[m-1].upper()}", f"Monthly landscaping maintenance — {MONTHS[m-1]} 2025", 2750, "Shared"))
    # Seasonal plantings (spring + fall)
    rows.append(("2025-05-15", "6810", "Landscaping - Seasonal", "GreenScape Contractors",
                 "GSC-SPRING-2025", "Spring seasonal planting installation", 4000, "Shared"))
    rows.append(("2025-09-25", "6810", "Landscaping - Seasonal", "GreenScape Contractors",
                 "GSC-FALL-2025", "Fall seasonal planting installation", 4000, "Shared"))
    # Irrigation + tree pruning
    rows.append(("2025-04-10", "6820", "Landscaping - Irrigation", "GreenScape Contractors",
                 "GSC-IRR-2025", "Annual irrigation start-up & maintenance", 3000, "Shared"))
    rows.append(("2025-03-18", "6830", "Landscaping - Tree Pruning", "ArborCare Ltd.",
                 "ARB-SPRING-2025", "Spring tree pruning + deadwood removal", 2000, "Shared"))

    # Snow & Ice — Dec 2024 season carries Jan-Mar + Nov-Dec 2025
    for date_str, ref, memo, amt in [
        ("2025-01-31", "SNOW-2025-JAN", "January 2025 snow plowing + salting (8 events)", 4800),
        ("2025-02-28", "SNOW-2025-FEB", "February 2025 snow plowing + salting (6 events)", 3600),
        ("2025-03-31", "SNOW-2025-MAR", "March 2025 snow + ice management (3 events)", 1800),
        ("2025-11-30", "SNOW-2025-NOV", "November 2025 snow pre-season + early events (2 events)", 2400),
        ("2025-12-31", "SNOW-2025-DEC", "December 2025 snow plowing + salting (7 events)", 11400),
    ]:
        rows.append((date_str, "6900", "Snow & Ice", "Snowman Contracting",
                     ref, memo, amt, "Shared"))

    return rows


def build_gl_xlsx(rows):
    wb = Workbook()

    # Sheet 1: Summary
    ws = wb.active
    ws.title = "Summary"
    ws["A1"] = "MATHESON GATEWAY CENTRE — FY2025 GL EXTRACT (RECOVERABLE OPEX)"
    ws["A1"].font = Font(bold=True, size=14)
    ws.merge_cells("A1:F1")
    ws["A2"] = "General ledger extract — FY2025 (Jan 1 – Dec 31, 2025)"
    ws["A2"].font = Font(italic=True, size=10, color="555555")
    ws.merge_cells("A2:F2")
    ws["A3"] = "Prepared by: Gateway Property Management Inc.  |  For: Tenebrus Asset Management review, April 2026"
    ws["A3"].font = Font(italic=True, size=10, color="555555")
    ws.merge_cells("A3:F3")

    # Summary by category
    cat_totals = {}
    for r in rows:
        cat = r[2].split(" - ")[0] if " - " in r[2] else r[2]
        cat_totals[cat] = cat_totals.get(cat, 0) + r[6]

    # Budget comparison
    budget = {
        "Realty Tax": 420000,
        "Insurance": 55000,
        "Utilities": 195000,
        "R&M": 115000,
        "Management Fee": 108000,
        "Janitorial": 85000,
        "Security": 45000,
        "Landscaping": 35000,
        "Snow & Ice": 24000,
    }

    # Combine cat_totals into rollups matching budget keys
    actual = {
        "Realty Tax": cat_totals.get("Realty Tax", 0),
        "Insurance": cat_totals.get("Insurance", 0),
        "Utilities": sum(v for k, v in cat_totals.items() if k == "Utilities"),
        "R&M": sum(v for k, v in cat_totals.items() if k == "R&M"),
        "Management Fee": cat_totals.get("Management Fee", 0),
        "Janitorial": sum(v for k, v in cat_totals.items() if k == "Janitorial"),
        "Security": sum(v for k, v in cat_totals.items() if k == "Security"),
        "Landscaping": sum(v for k, v in cat_totals.items() if k == "Landscaping"),
        "Snow & Ice": cat_totals.get("Snow & Ice", 0),
    }

    hdr_fill = PatternFill("solid", fgColor="1F4E78")
    hdr_font = Font(bold=True, color="FFFFFF", size=11)
    money = '"$"#,##0'

    headers = ["Category", "FY2025 Budget", "FY2025 Actual", "Variance ($)", "Variance (%)", "Notes"]
    for c, h in enumerate(headers, 1):
        cell = ws.cell(row=5, column=c, value=h)
        cell.font = hdr_font
        cell.fill = hdr_fill
        cell.alignment = Alignment(horizontal="center")

    r = 6
    totals_b, totals_a = 0, 0
    for cat in ["Realty Tax", "Utilities", "R&M", "Management Fee", "Janitorial",
                "Insurance", "Security", "Landscaping", "Snow & Ice"]:
        b = budget[cat]
        a = actual[cat]
        v = a - b
        vp = v / b if b else 0
        totals_b += b
        totals_a += a
        ws.cell(row=r, column=1, value=cat)
        ws.cell(row=r, column=2, value=b).number_format = money
        ws.cell(row=r, column=3, value=a).number_format = money
        ws.cell(row=r, column=4, value=v).number_format = money
        ws.cell(row=r, column=5, value=vp).number_format = '0.0%'
        r += 1

    # Total
    ws.cell(row=r, column=1, value="TOTAL").font = Font(bold=True)
    ws.cell(row=r, column=2, value=totals_b).number_format = money
    ws.cell(row=r, column=2).font = Font(bold=True)
    ws.cell(row=r, column=3, value=totals_a).number_format = money
    ws.cell(row=r, column=3).font = Font(bold=True)
    ws.cell(row=r, column=4, value=totals_a - totals_b).number_format = money
    ws.cell(row=r, column=4).font = Font(bold=True)
    ws.cell(row=r, column=5, value=(totals_a - totals_b) / totals_b).number_format = '0.0%'
    ws.cell(row=r, column=5).font = Font(bold=True)
    for c in range(1, 7):
        ws.cell(row=r, column=c).fill = PatternFill("solid", fgColor="E8EEF4")

    # Column widths
    widths = [22, 16, 16, 16, 14, 50]
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w

    # Sheet 2: GL Detail
    ws2 = wb.create_sheet("GL Detail")
    ws2["A1"] = "FY2025 GL — DETAILED TRANSACTION LINES"
    ws2["A1"].font = Font(bold=True, size=12)
    ws2.merge_cells("A1:H1")

    detail_headers = ["Date", "Account", "Category", "Vendor", "Invoice Ref", "Memo", "Amount", "Pool"]
    for c, h in enumerate(detail_headers, 1):
        cell = ws2.cell(row=3, column=c, value=h)
        cell.font = hdr_font
        cell.fill = hdr_fill
        cell.alignment = Alignment(horizontal="center")

    # Sort by date
    sorted_rows = sorted(rows, key=lambda x: x[0])
    for i, row in enumerate(sorted_rows, start=4):
        for c, val in enumerate(row, 1):
            cell = ws2.cell(row=i, column=c, value=val)
            if c == 7:
                cell.number_format = money
            cell.alignment = Alignment(vertical="top", wrap_text=True)

    # Column widths
    widths2 = [12, 10, 22, 30, 24, 60, 12, 10]
    for i, w in enumerate(widths2, 1):
        ws2.column_dimensions[get_column_letter(i)].width = w

    # Sheet 3: Pool Allocation
    ws3 = wb.create_sheet("Pool Allocation")
    ws3["A1"] = "FY2025 ACTUAL OPEX — POOL ALLOCATION"
    ws3["A1"].font = Font(bold=True, size=12)
    ws3.merge_cells("A1:E1")

    office_total = sum(r[6] for r in rows if r[7] == "Office")
    retail_total = sum(r[6] for r in rows if r[7] == "Retail")
    shared_total = sum(r[6] for r in rows if r[7] == "Shared")
    office_share = shared_total * 0.6774
    retail_share = shared_total * 0.3226

    pool_headers = ["Pool Assignment", "Direct Pool ($)", "Shared Allocation ($)", "Pool Total ($)", "% of Actual"]
    for c, h in enumerate(pool_headers, 1):
        cell = ws3.cell(row=3, column=c, value=h)
        cell.font = hdr_font
        cell.fill = hdr_fill
        cell.alignment = Alignment(horizontal="center")

    ws3.cell(row=4, column=1, value="Office Pool (67.74% of shared)")
    ws3.cell(row=4, column=2, value=office_total).number_format = money
    ws3.cell(row=4, column=3, value=office_share).number_format = money
    ws3.cell(row=4, column=4, value=office_total + office_share).number_format = money
    ws3.cell(row=4, column=5, value=(office_total + office_share) / (office_total + retail_total + shared_total)).number_format = '0.0%'

    ws3.cell(row=5, column=1, value="Retail Pool (32.26% of shared)")
    ws3.cell(row=5, column=2, value=retail_total).number_format = money
    ws3.cell(row=5, column=3, value=retail_share).number_format = money
    ws3.cell(row=5, column=4, value=retail_total + retail_share).number_format = money
    ws3.cell(row=5, column=5, value=(retail_total + retail_share) / (office_total + retail_total + shared_total)).number_format = '0.0%'

    ws3.cell(row=7, column=1, value="Shared pool total (pre-allocation)")
    ws3.cell(row=7, column=2, value=shared_total).number_format = money

    ws3.cell(row=9, column=1, value="GRAND TOTAL").font = Font(bold=True)
    ws3.cell(row=9, column=4, value=office_total + retail_total + shared_total).number_format = money
    ws3.cell(row=9, column=4).font = Font(bold=True)

    for i, w in enumerate([36, 18, 22, 18, 14], 1):
        ws3.column_dimensions[get_column_letter(i)].width = w

    wb.save(OUT / "2025_GL_Extract.xlsx")
    print(f"Wrote {OUT/'2025_GL_Extract.xlsx'}")

    # Also write flat CSV of GL Detail
    with open(OUT / "2025_GL_Extract.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(detail_headers)
        for row in sorted_rows:
            w.writerow(row)
    print(f"Wrote {OUT/'2025_GL_Extract.csv'}")

    # Print totals for verification
    print(f"\n-- VERIFICATION --")
    print(f"Total actual opex: ${totals_a:,.0f}")
    print(f"Total budget:      ${totals_b:,.0f}")
    print(f"Variance:          ${totals_a - totals_b:,.0f}")
    print(f"\nBy category:")
    for cat in ["Realty Tax", "Utilities", "R&M", "Management Fee", "Janitorial",
                "Insurance", "Security", "Landscaping", "Snow & Ice"]:
        print(f"  {cat:20s} budget ${budget[cat]:>9,.0f}  actual ${actual[cat]:>9,.0f}  var ${actual[cat]-budget[cat]:>+9,.0f}")


# ============================================================================
# 3. LEASE EXCERPTS PDF
# ============================================================================

def build_lease_pdf():
    doc = SimpleDocTemplate(
        str(OUT / "Lease_Excerpts_CAM_Clauses.pdf"),
        pagesize=LETTER,
        leftMargin=0.9*inch, rightMargin=0.9*inch,
        topMargin=0.8*inch, bottomMargin=0.8*inch,
    )
    styles = getSampleStyleSheet()
    h1 = ParagraphStyle("h1", parent=styles["Heading1"], fontSize=14, spaceAfter=10, textColor=colors.HexColor("#1F4E78"))
    h2 = ParagraphStyle("h2", parent=styles["Heading2"], fontSize=11, spaceAfter=6, textColor=colors.HexColor("#1F4E78"))
    body = ParagraphStyle("body", parent=styles["BodyText"], fontSize=9.5, leading=13, alignment=TA_JUSTIFY, spaceAfter=6)
    lease_body = ParagraphStyle("lease", parent=body, fontName="Times-Roman", leftIndent=16, rightIndent=16, fontSize=9.5)
    caption = ParagraphStyle("cap", parent=styles["BodyText"], fontSize=8, textColor=colors.HexColor("#666666"), alignment=TA_CENTER)
    note = ParagraphStyle("note", parent=body, fontSize=8.5, textColor=colors.HexColor("#555555"), backColor=colors.HexColor("#F4F6F8"),
                         borderPadding=6, leftIndent=4, rightIndent=4)
    story = []

    story.append(Paragraph("Matheson Gateway Centre — Lease Excerpts<br/>CAM / Operating Expense Clauses (Redacted)", h1))
    story.append(Paragraph(
        "Prepared for CRE-150 Exercise 3. Excerpts are taken from four live leases at the property plus the "
        "Management Agreement between Tenebrus Core Income Fund LP and Gateway Property Management Inc. "
        "Tenant-specific financial terms and proprietary clauses have been redacted. All figures are illustrative.",
        caption))
    story.append(Spacer(1, 16))

    story.append(Paragraph(
        "<b>Document Index</b><br/>"
        "1. Standard Form Lease — Article 6 (Operating Expenses) [applies to Suites 200, 300, 400; Units 102, 105]<br/>"
        "2. CanadaFirst Bank Lease — Article 6.05 (CAM Cap) [Unit 101]<br/>"
        "3. Matheson Family Dental Lease — Article 6.06 (Base Year Gross-Up) [Unit 103]<br/>"
        "4. Peak Fitness Studio Lease — Article 6.07 (Modified Gross — Exclusions) [Unit 104]<br/>"
        "5. Pronto Italian Kitchen Lease — Schedule C (Restaurant Exclusions) [Unit 105]<br/>"
        "6. Management Agreement §4.1 — Management Fee Basis",
        body))
    story.append(PageBreak())

    # Document 1: Standard Form Lease Article 6
    story.append(Paragraph("1. Standard Form Lease — Article 6: Operating Expenses", h1))
    story.append(Paragraph("<i>Applies to Suites 200 (Harrington &amp; Kline), 300 (Meridian Civil), 400 (Helix AI) and Units 102 (Brewhouse), 105 (Pronto — subject to Schedule C).</i>", caption))
    story.append(Spacer(1, 8))

    story.append(Paragraph("<b>6.01 Definitions.</b>", h2))
    story.append(Paragraph(
        "In this Article, \"<b>Operating Expenses</b>\" means the total, without duplication, of all reasonable costs, "
        "expenses and disbursements of every kind and nature incurred or accrued by the Landlord in each calendar "
        "year in connection with the ownership, operation, management, maintenance, repair, insurance, supervision "
        "and administration of the Building and the Lands, calculated as if the Building were one hundred percent "
        "(100%) occupied, and including without limitation the categories enumerated in Schedule B.",
        lease_body))

    story.append(Paragraph("<b>6.02 Tenant's Proportionate Share.</b>", h2))
    story.append(Paragraph(
        "The Tenant shall pay to the Landlord, as Additional Rent, the Tenant's Proportionate Share of Operating "
        "Expenses allocable to the Pool in which the Premises are situated. Proportionate Share is determined by "
        "dividing the Rentable Area of the Premises by the total Rentable Area of the applicable Pool. The Landlord "
        "shall allocate Operating Expenses between the Office Pool and the Retail Pool in a fair and equitable "
        "manner consistent with generally accepted property management practice.",
        lease_body))

    story.append(Paragraph("<b>6.03 Exclusions from Operating Expenses.</b>", h2))
    story.append(Paragraph(
        "Notwithstanding anything in this Article to the contrary, Operating Expenses shall <b>not</b> include:",
        lease_body))
    for item in [
        "(a) capital expenditures of a nature that, in accordance with generally accepted accounting principles, would be capitalized, save as expressly permitted under Section 6.04;",
        "(b) leasing commissions, marketing costs, tenant inducement payments, tenant improvement allowances, or any legal fees incurred in connection with the negotiation or enforcement of leases;",
        "(c) <b>one-time extraordinary charges arising from tenant turnover, including without limitation move-out deep cleaning, suite restoration works, demising wall construction, or carpet replacement attributable to a specific prior tenant, all of which shall be recoverable, if at all, solely from the applicable outgoing or incoming tenant;</b>",
        "(d) legal fees, accounting fees, or consulting fees incurred in connection with ownership disputes, financing, refinancing, sale, or leasing of the Property;",
        "(e) income taxes, capital taxes, transfer taxes, land transfer tax, or goods and services taxes (except where GST/HST forms part of a recoverable invoice and cannot be claimed as input tax credit);",
        "(f) any expense for which the Landlord has been reimbursed by insurance proceeds, warranty recovery, or payment from any third party;",
        "(g) <b>amounts posted to the general ledger in error, including without limitation duplicate invoices, transposition errors, accounting misclassifications, or any accounting entry not supported by a valid third-party invoice or receipt.</b>",
        "(h) the cost of correcting defects in the original construction of the Building, latent defects, or any repair covered under warranty;",
        "(i) expenses of any specialty or premium service provided to another tenant but not available to the Tenant on equivalent terms.",
    ]:
        story.append(Paragraph(item, lease_body))

    story.append(Paragraph("<b>6.04 Amortization of Certain Capital Expenditures.</b>", h2))
    story.append(Paragraph(
        "Capital expenditures required (i) by applicable law enacted after the date of this Lease, or (ii) to "
        "reduce Operating Expenses on a demonstrable basis, may be amortized over the useful life of the asset "
        "determined in accordance with generally accepted accounting principles, together with interest on the "
        "unamortized balance at the Landlord's cost of borrowing, and the annual amortization amount only shall "
        "be included in Operating Expenses.",
        lease_body))

    story.append(PageBreak())

    # Document 2: CanadaFirst Bank CAM Cap
    story.append(Paragraph("2. CanadaFirst Bank Lease — Article 6.05 (CAM Cap Rider)", h1))
    story.append(Paragraph("<i>Applies to Unit 101. Negotiated rider to the Standard Form Lease.</i>", caption))
    story.append(Spacer(1, 8))

    story.append(Paragraph("<b>6.05 Annual Cap on Operating Expenses.</b>", h2))
    story.append(Paragraph(
        "Notwithstanding Section 6.02, the Tenant's Proportionate Share of Operating Expenses payable in respect "
        "of any calendar year shall not exceed one hundred four percent (104%) of the Tenant's Proportionate "
        "Share of Operating Expenses paid in the immediately preceding calendar year, compounded annually. For "
        "the purposes of this Section, the base year shall be the 2022 calendar year, during which the Tenant's "
        "Proportionate Share of Operating Expenses was $11.40 per square foot of the Rentable Area of the "
        "Premises (the \"<b>Base Year CAM</b>\").",
        lease_body))
    story.append(Paragraph(
        "<b>6.05.1</b> The cap imposed by this Section does <b>not</b> apply to realty tax, insurance premiums, "
        "utility costs, or snow removal (collectively, the \"<b>Uncontrollable Expenses</b>\"), which pass through "
        "to the Tenant without limit on annual increase.",
        lease_body))
    story.append(Paragraph(
        "<b>6.05.2</b> The Landlord shall calculate the cap ceiling for each calendar year and reflect it on the "
        "annual CAM reconciliation statement delivered under Section 6.08. For greater certainty, the FY2025 cap "
        "ceiling is $12.82 per square foot for Controllable Operating Expenses.",
        lease_body))

    story.append(Spacer(1, 12))
    story.append(Paragraph(
        "<b>EXERCISE NOTE</b> — The cap applies only to Controllable expenses. For FY2025 reconciliation, the Uncontrollable Expenses "
        "(realty tax, insurance, utilities, snow) pass through without the cap. The cap matters only for the Controllable bucket.",
        note))

    story.append(PageBreak())

    # Document 3: Matheson Family Dental Base Year
    story.append(Paragraph("3. Matheson Family Dental Lease — Article 6.06 (Base Year)", h1))
    story.append(Paragraph("<i>Applies to Unit 103. Also applies in substance to Coverpoint Insurance (Suite 310, BY 2023).</i>", caption))
    story.append(Spacer(1, 8))

    story.append(Paragraph("<b>6.06 Base Year Gross-Up.</b>", h2))
    story.append(Paragraph(
        "In substitution for the full pass-through contemplated by Section 6.02, the Tenant shall pay as Additional "
        "Rent only the amount by which the Tenant's Proportionate Share of Operating Expenses in each calendar "
        "year exceeds the Tenant's Proportionate Share of Operating Expenses for the <b>Base Year</b>, being the "
        "2024 calendar year (\"<b>Base Year CAM</b>\" = $15.40 per square foot).",
        lease_body))
    story.append(Paragraph(
        "For the purposes of this calculation, Operating Expenses for each of the Base Year and subsequent years "
        "shall be <b>grossed up</b> to reflect the cost that would have been incurred had the Building been fully "
        "occupied for the full calendar year, consistent with the definition of Operating Expenses in Section 6.01.",
        lease_body))

    story.append(Spacer(1, 12))
    story.append(Paragraph(
        "<b>EXERCISE NOTE</b> — Base-year tenants (Unit 103, Suite 310) pay only the <i>increase</i> over their base year. "
        "Their pro-rata share of FY2025 opex is calculated normally; then the base-year dollar amount is subtracted. "
        "This is a rate calculation, not a reconciliation discrepancy — no planted error here.",
        note))

    story.append(PageBreak())

    # Document 4: Peak Fitness Modified Gross
    story.append(Paragraph("4. Peak Fitness Studio Lease — Article 6.07 (Modified Gross — Exclusions)", h1))
    story.append(Paragraph("<i>Applies to Unit 104.</i>", caption))
    story.append(Spacer(1, 8))

    story.append(Paragraph("<b>6.07 Modified Gross Structure — Excluded Categories.</b>", h2))
    story.append(Paragraph(
        "Section 6.02 is modified to the extent that, in each calendar year, the Tenant's Proportionate Share of "
        "Operating Expenses shall be calculated <b>excluding</b> the following categories, which shall be borne by "
        "the Landlord without recovery from the Tenant:",
        lease_body))
    for item in [
        "(a) all utility costs of every nature, including without limitation electric, gas, water, sewer, and telecommunications backbone (Landlord acknowledging that the Tenant's premises is separately metered for electric and gas, with the Tenant paying such charges directly to the utility);",
        "(b) all repair and maintenance expenses, whether relating to the base building, mechanical systems, roof, or common areas.",
    ]:
        story.append(Paragraph(item, lease_body))
    story.append(Paragraph(
        "All other Operating Expense categories, including realty tax, insurance, landscaping, security, snow and "
        "ice management, and management fee, shall flow through to the Tenant on the same basis as in Section 6.02, "
        "subject to the Tenant's Proportionate Share of the Retail Pool.",
        lease_body))

    story.append(Spacer(1, 12))
    story.append(Paragraph(
        "<b>EXERCISE NOTE</b> — Peak Fitness is excluded from the Utilities line ($203,340 actual) and the R&amp;M "
        "line ($115,658 actual) for recovery purposes. The plugin's reconciliation must strip Peak Fitness's "
        "pro-rata share of those two lines from their chargeable total.",
        note))

    story.append(PageBreak())

    # Document 5: Pronto Restaurant exclusions
    story.append(Paragraph("5. Pronto Italian Kitchen Lease — Schedule C (Restaurant Exclusions)", h1))
    story.append(Paragraph("<i>Applies to Unit 105.</i>", caption))
    story.append(Spacer(1, 8))

    story.append(Paragraph("<b>Schedule C — Restaurant-Specific Operating Expense Exclusions.</b>", h2))
    story.append(Paragraph(
        "The parties acknowledge that the Tenant operates a full-service restaurant and that certain categories of "
        "Operating Expense primarily benefit the Tenant (or, conversely, arise primarily from the Tenant's "
        "operations). Accordingly, notwithstanding Section 6.02, the following categories shall be <b>excluded</b> "
        "from the calculation of the Tenant's Proportionate Share of Operating Expenses:",
        lease_body))
    for item in [
        "C.1 Grease trap servicing, pump-out, inspection, and any regulatory compliance cost associated with the kitchen grease interceptor serving the Premises, all of which shall be billed directly to the Tenant;",
        "C.2 Kitchen exhaust hood cleaning, duct cleaning, and fire-suppression system inspection for the Premises' ventilation system (Tenant self-performs through a licensed third-party contractor);",
        "C.3 Any increase in building insurance premium directly attributable to the Tenant's restaurant operations, as certified by the Landlord's broker.",
    ]:
        story.append(Paragraph(item, lease_body))

    story.append(Spacer(1, 12))
    story.append(Paragraph(
        "<b>EXERCISE NOTE</b> — The grease trap line (account 6450, $4,500 actual) is in the Retail Pool but Pronto is "
        "excluded from it. The reconciliation must reallocate that $4,500 across the other retail tenants, not across "
        "all five retail tenants including Pronto.",
        note))

    story.append(PageBreak())

    # Document 6: Management Agreement §4.1
    story.append(Paragraph("6. Management Agreement §4.1 — Management Fee Basis", h1))
    story.append(Paragraph("<i>Between Tenebrus Core Income Fund LP (\"Owner\") and Gateway Property Management Inc. (\"Manager\"), executed January 1, 2024.</i>", caption))
    story.append(Spacer(1, 8))

    story.append(Paragraph("<b>§4.1 Management Fee.</b>", h2))
    story.append(Paragraph(
        "As compensation for services rendered hereunder, Owner shall pay Manager a monthly management fee equal "
        "to <b>four percent (4.0%) of the Effective Gross Income</b> of the Property for such month.",
        lease_body))
    story.append(Paragraph(
        "For the purposes of this Section, \"<b>Effective Gross Income</b>\" (\"<b>EGI</b>\") means the sum of all "
        "rental income, additional rent, parking revenue, and other miscellaneous income <b>actually billed</b> in "
        "respect of the Property, <b>less</b>:",
        lease_body))
    for item in [
        "(i) <b>vacancy loss</b> attributable to unleased rentable area at the Property during such month; and",
        "(ii) an <b>allowance for credit losses and uncollected rent</b>, determined in accordance with generally accepted property management practice and reviewed annually by Owner.",
    ]:
        story.append(Paragraph(item, lease_body))

    story.append(Paragraph("<b>§4.1.1 Distinction from Gross Potential Income.</b>", h2))
    story.append(Paragraph(
        "For the avoidance of doubt, the Management Fee shall <b>not</b> be calculated on the basis of Gross "
        "Potential Income (being the income that would be received if the Property were fully leased and all rent "
        "were collected in full), nor on the basis of billed income before deduction of vacancy and credit losses. "
        "Any fee paid on an incorrect basis shall be reconciled at year-end and the difference credited or debited "
        "to the Manager's next monthly payment.",
        lease_body))

    story.append(Paragraph("<b>§4.1.2 Non-Recoverability from Tenants.</b>", h2))
    story.append(Paragraph(
        "The Management Fee is recoverable from tenants as an Operating Expense only to the extent of the fee "
        "actually payable by Owner under this Section — i.e., <b>four percent (4.0%) of Effective Gross Income</b>. "
        "No portion of any fee paid in excess of that amount, whether due to calculation error or otherwise, shall "
        "form part of Operating Expenses recoverable from tenants under Article 6 of the Standard Form Lease or "
        "any equivalent provision of a tenant lease.",
        lease_body))

    story.append(Spacer(1, 12))
    story.append(Paragraph(
        "<b>EXERCISE NOTE — CRITICAL</b> — The FY2025 GL shows monthly management fee postings totaling $114,800, "
        "calculated as 4% of Gross Potential Income ($2,870,000). The correct basis is EGI ($2,770,000), which "
        "yields a fee of $110,800. The $4,000 overstatement is both (a) not recoverable from tenants per §4.1.2, "
        "and (b) creates a credit owed by the Manager to the Owner per §4.1.1. The plugin must flag both the "
        "calculation method and the allocation error.",
        note))

    doc.build(story)
    print(f"Wrote {OUT/'Lease_Excerpts_CAM_Clauses.pdf'}")


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    build_rent_roll()
    rows = gl_rows()
    build_gl_xlsx(rows)
    build_lease_pdf()
    print("\nAll files generated.")
