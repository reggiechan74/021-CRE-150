---
name: cam-classify
description: >
  Use when the user asks to classify CAM line items for recoverability, determine whether
  a GL posting belongs in the office or retail pool, evaluate duplicate invoices, check
  turnover-related janitorial charges, or validate whether a management fee is recoverable
  on an EGI basis.
---

# CAM Classification

You are classifying GL lines for CAM recoverability in a CRE reconciliation workflow.

## Decision Order

1. Check for accounting errors.
2. Check for explicit lease or management-agreement exclusions.
3. Determine the correct pool (`office`, `retail`, or `shared`).
4. Return a normalized reason code and a citation.

## Priority Rules

### Duplicate postings

- If the same `(vendor, invoice_ref, amount)` appears more than once, keep the earliest posting and mark later duplicates non-recoverable.
- Citation: Standard Form Lease `§6.03(g)`.

### Tenant-turnover charges

- If the memo describes move-out cleaning, suite restoration, demising work, or other tenant-turnover activity, mark it non-recoverable from CAM.
- Citation: Standard Form Lease `§6.03(c)`.

### Management fee basis

- Management fee is recoverable only to the extent it equals `4% × EGI`.
- Any excess over the EGI-based amount is non-recoverable from tenants.
- Citation: Management Agreement `§4.1` and `§4.1.2`.

### Modified gross and specific exclusions

- Peak Fitness excludes `utilities` and `repairs_maintenance`.
- Pronto excludes grease-trap servicing under Schedule C.
- Base-year and cap structures do not change recoverability at the line level; they affect tenant charging later in allocation.

## Output Shape

Return one decision per `line_id` with:

- `recoverable`
- `reason`
- `lease_citation`
- `pool`
- `normalized_category`
- `recoverable_amount` when partial recoverability applies
