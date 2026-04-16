---
title: Exercise 3 — Instructor Key & File Inventory
date: 2026-04-15
keywords: [cre-150, exercise-3, instructor-key, answer-key, cam-reconciliation]
lastUpdated: 2026-04-15
category: Training
documentType: Instructor Reference
status: Active
shareable: false
---

# Exercise 3 — "The Numbers" — Instructor Key

**DO NOT distribute to participants.** This file contains the answer key and planted-discrepancy details.

---

## File Inventory (distributed to participants)

| # | File | Purpose | Size |
|---|------|---------|------|
| 1 | `Property_Fact_Sheet.md` | Building specs, ownership, tenant roster, lease summary, FY2025 revenue | ~5 KB |
| 2 | `2025_CAM_Budget.md` | FY2025 budget (basis for tenant pre-bills), pool allocation methodology, monthly CAM pre-bills by tenant | ~7 KB |
| 3 | `2025_Rent_Roll.xlsx` | 10-row rent roll with RSF, pro-rata shares, lease type, CAM treatment per tenant | ~7 KB |
| 4 | `2025_GL_Extract.xlsx` | 3 sheets: Summary (budget vs actual by category), GL Detail (~180 line-item transactions), Pool Allocation | ~20 KB |
| 5 | `2025_GL_Extract.csv` | Flat CSV version of GL Detail sheet — for plugin ingestion fallback | ~18 KB |
| 6 | `Lease_Excerpts_CAM_Clauses.pdf` | 6 lease/agreement excerpts: Standard Form Article 6, CanadaFirst cap, Matheson Dental base year, Peak Fitness modified gross, Pronto restaurant exclusions, Management Agreement §4.1 | ~10 pages |

---

## Answer Key — The Four Planted Discrepancies

### Headline: Draft reconciliation shows $96,692 over budget
**Reconciled correct over-budget: $68,296 (all recoverable)**
**Non-recoverable errors requiring reversal: $28,396**

---

### Discrepancy #1 — Property Tax Reassessment

- **Where:** GL Detail sheet, account 6100, monthly entries
- **What:** Jan–Jun 2025 billed at $35,000/month (pre-reassessment). Jul–Dec 2025 billed at $47,600/month (post-reassessment MPAC Notice dated 2025-07-01).
- **Variance:** +$75,600 vs budget
- **Classification:** **Legitimate variance — fully recoverable from tenants**
- **Lease basis:** Standard Form §6.01 includes realty tax in Operating Expenses; CanadaFirst cap §6.05.1 explicitly carves out realty tax as Uncontrollable (passes through without cap).
- **Plugin should:** Identify as variance, classify as legitimate, decompose driver (reassessment event, not rate change), confirm recoverability.
- **Tenant billing implication:** Tenants on net leases pay pro-rata. Base-year tenants (Unit 103, Suite 310) pay only the increase over their base year.

### Discrepancy #2 — Utility Double-Post

- **Where:** GL Detail sheet, account 6320 — two Enbridge entries with same invoice #
  - 2025-12-22, Enbridge Gas Inc., invoice **GA-2025-12-4471**, $9,900
  - 2025-12-29, Enbridge Gas Inc., invoice **GA-2025-12-4471**, $9,900 (memo: "invoice re-entered in year-end close")
- **Variance contribution:** +$9,900
- **Classification:** **Accounting error — duplicate posting. NOT recoverable.**
- **Lease basis:** Standard Form §6.03(g) — amounts posted in error, including duplicate invoices, are explicitly excluded from Operating Expenses.
- **Plugin should:** Match invoice numbers across the GL, flag the duplicate, recommend reversal.
- **Action:** Reverse $9,900 from FY2025 opex. Do not bill tenants.

### Discrepancy #3 — Janitorial One-Time Deep Clean (Tenant Turnover)

- **Where:** GL Detail sheet, 2025-10-18, account 6600, Clean Pro Services Ltd., reference CPS-SPECIAL-2025-1018, $14,500
- **Memo:** "Suite 320 move-out deep clean & restoration (predecessor Apex Consulting) — post-vacate cleaning, carpet extraction, wall spot-paint, kitchenette degrease"
- **Variance contribution:** +$14,500 (entire overage in janitorial line)
- **Classification:** **Classification error — not a recoverable operating expense.**
- **Lease basis:** Standard Form §6.03(c) — *"one-time extraordinary charges arising from tenant turnover, including without limitation move-out deep cleaning, suite restoration works, demising wall construction, or carpet replacement attributable to a specific prior tenant, all of which shall be recoverable, if at all, solely from the applicable outgoing or incoming tenant."*
- **Plugin should:** Decompose the janitorial variance into recurring contract ($4,200/mo × 12 = $50,400) + day porter ($2,083/mo × 12 = $25,000) + supplies/window cleaning ($9,600) + one-time $14,500. Flag the one-time item as outlier/anomaly; match to lease exclusion language.
- **Action:** Reclassify the $14,500 out of CAM pool. Recover from Apex Consulting's security deposit (landlord-side collection, not tenant-billed).

### Discrepancy #4 — Management Fee Methodology Error

- **Where:** GL Detail sheet, account 6500, monthly entries totalling **$114,800**
- **Calculation:** Posted as 4% × Gross Potential Income ($2,870,000). Correct basis per Management Agreement §4.1 is 4% × Effective Gross Income ($2,770,000) = **$110,800**.
- **Error component:** $4,000 (methodology)
- **Legitimate component:** $2,800 (EGI came in $70,000 above projected, so fee is that much higher than budgeted — recoverable)
- **Total budget variance:** +$6,800
- **Classification:**
  - $2,800 legitimate variance — recoverable
  - $4,000 calculation error — **NOT recoverable**
- **Lease basis:** Management Agreement §4.1 defines fee as 4% of EGI, where EGI = GPI less vacancy loss less credit allowance. §4.1.2 explicitly states that any fee paid in excess of the correct amount is *not* recoverable from tenants as an Operating Expense.
- **Plugin should:** Recalculate the fee on EGI basis ($2,770,000 × 4% = $110,800), flag the $4,000 over-calculation, cite §4.1 and §4.1.2.
- **Critical pedagogical note:** The **plugin catches this** — it reads the Management Agreement definition and recalculates. Before AI, a human property accountant had to (a) remember the EGI distinction, (b) pull the revenue breakdown, (c) recalculate manually, (d) separate methodology error from legitimate variance. The plugin does all four in seconds.
- **Action:** Gateway PM owes Owner a $4,000 credit (per §4.1.1). Tenant CAM calculation uses $110,800 as the recoverable fee.

---

## Reconciled FY2025 Recoverable Opex (Corrected)

| Category | Budget | Posted Actual | Corrections | Recoverable | vs Budget |
|----------|-------:|--------------:|------------:|------------:|----------:|
| Realty Tax | $420,000 | $495,600 | — | $495,600 | +$75,600 |
| Utilities | $195,000 | $204,900 | ($9,900) duplicate | $195,000 | +$0 |
| R&M | $115,000 | $104,896 | — | $104,896 | ($10,104) |
| Management Fee | $108,000 | $114,800 | ($4,000) method error | $110,800 | +$2,800 |
| Janitorial | $85,000 | $99,496 | ($14,500) turnover exclusion | $84,996 | ($4) |
| Insurance | $55,000 | $55,000 | — | $55,000 | +$0 |
| Security | $45,000 | $45,000 | — | $45,000 | +$0 |
| Landscaping | $35,000 | $35,000 | — | $35,000 | +$0 |
| Snow & Ice | $24,000 | $24,000 | — | $24,000 | +$0 |
| **TOTAL** | **$1,082,000** | **$1,178,692** | **($28,400)** | **$1,150,292** | **+$68,292** |

**Tenants chargeable recoverable opex: $1,150,292** — net $68,292 over budget, driven almost entirely by the MPAC tax reassessment (uncontrollable expense per lease). All other line items reconcile to budget or below after corrections.

---

## The "Before AI / After AI" Pedagogical Arc

**Before the Finance plugin** (how a human analyst does this):

1. Export GL to Excel (~1 hour)
2. Manually match to budget line-by-line (~2 hours)
3. Investigate each variance: email AP for invoice copies, eyeball for duplicates, cross-reference vendor files (~4–8 hours)
4. Read every affected lease and the Management Agreement to determine recoverability (~3–4 hours)
5. Recalculate management fee manually (~30 min)
6. Prepare tenant statements (~2 hours)
7. **Total: 12–17 hours of skilled property accountant time.**

**After the Finance plugin** (`/reconciliation`, `/variance-analysis`, `/income-statement`):

1. Ingest GL + budget + lease PDFs (~2 min setup)
2. Plugin identifies all four discrepancies, classifies each, cites the lease clause (~2–3 min)
3. Human reviews, verifies lease citations are correct, approves corrections (~30 min)
4. Plugin regenerates tenant-level reconciliation statements (~1 min)
5. **Total: 35–45 minutes of senior judgment time. Zero manual spreadsheet work.**

**Productivity delta: ~20×.** More importantly, the judgment work (Is the lease citation correct? Is this variance fair to recover?) is now the *only* work the human does — everything else is automated.

This is the demonstration: AI does not replace the property accountant. It replaces the 15 hours of mechanical reconciliation that stood between the accountant and the decision.

---

## Facilitation Notes

- **Time budget:** 30 minutes total. Plan: plugin install (2 min) → `/reconciliation` (5 min) → `/variance-analysis` (5 min) → `/income-statement` (5 min) → review/discuss (13 min).
- **Expected participant reactions:**
  - Surprise that the plugin catches the duplicate Enbridge invoice on invoice-number match.
  - Some will push back on the management fee calculation — "the PM always does it that way." That's the teaching moment: the *lease* says EGI, not "how it's always been done."
  - The turnover-cleaning exclusion is the most lease-specific finding. Have participants read §6.03(c) aloud.
- **Common participant errors:**
  - Trying to recover the $14,500 anyway because "it's still a cleaning expense." Refer to the lease.
  - Missing the distinction between the $4,000 methodology error (not recoverable) and the $2,800 legitimate variance (recoverable). The plugin should separate these cleanly.
- **Bridge to Exercise 4:** "The plugin applied Article 6 clauses. But who *reviews* whether Article 6 is drafted correctly — whether the exclusions are complete, whether the management fee clause has escape hatches, whether the cap language is enforceable? That's the Legal plugin's job."

---

## Data Regeneration

All binary files are generated by `/tmp/build_exercise3_data.py`. To regenerate (e.g., after editing budget or tenant data):

```bash
python3 /tmp/build_exercise3_data.py
```

The script prints a verification block showing budget vs actual by category. Confirm the four discrepancies reconcile to expected values before distributing.
