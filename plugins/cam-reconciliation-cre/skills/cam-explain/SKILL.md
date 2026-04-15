---
name: cam-explain
description: >
  Use when the user asks why a tenant was charged a particular amount, how a specific GL
  line flowed through the reconciliation, or wants a drill-in explanation from an allocated
  manifest using the citation graph.
---

# CAM Explain

Use the allocated manifest as the source of truth.

## Tenant Drill-In

When given a `tenant_id`:

1. Report final charge, pre-billed amount, and true-up.
2. Walk `math_trace.steps` in order.
3. For each `exclusions_applied`, explain the clause and the amount removed.
4. If present, explain `base_year_adjustment` and `cap_adjustment`.
5. Close by naming the governing lease sections.

## GL Line Drill-In

When given a `line_id`:

1. Report date, vendor, amount, memo, and classification result.
2. If non-recoverable, explain why and cite the exclusion.
3. If recoverable, show which tenant charges reference that `line_id` in `citations[]`.

## Tone

- Be specific.
- Keep the math visible.
- Use clause sections exactly as stored in the manifest.
