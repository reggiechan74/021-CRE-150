---
name: mcda-sales-comparison
description: >
  Use when the user asks to run an MCDA sales comparison analysis, rank comparable sales
  using multi-criteria decision analysis, value a commercial property using ordinal ranking,
  produce an MCDA valuation report, or apply MCDA to a comparable sales dataset. Trigger
  phrases include: "MCDA analysis", "ordinal ranking valuation", "run MCDA", "value this
  property using comparables", "sales comparison using MCDA".
---

## Philosophy

The MCDA Sales Comparison method produces a defensible, auditable value indication. Unlike
traditional DCA with sequential dollar adjustments, ordinal ranking is more stable across
heterogeneous comparable sets. The output markdown report must be immediately
presentation-ready — complete ranking tables, score-to-price mapping, and a clear value
conclusion.

---

## Invocation

Triggered by messages such as:
- "Run MCDA sales comparison on inputs/hamilton_industrial.json"
- "Value 2550 Industrial Parkway using MCDA comps"
- "/mcda-sales-comparison inputs/data.json --profile industrial_logistics"

Parse the user's message for:
- An input JSON file path (required)
- An optional `--profile <weight-profile>` flag (industrial_default, industrial_logistics,
  industrial_manufacturing, office_default, retail_default)
- An optional `--output <report-path>` flag
- If no path given, scan the workspace for JSON files in an `inputs/` directory and ask

---

## Step 0 — Resolve paths (runs in primary context)

Before dispatching the subagent, resolve these values in the primary context.

**Plugin root** — run in Bash:
```bash
echo "${CLAUDE_PLUGIN_ROOT}"
```
If empty, find it:
```bash
find ~ -path "*/mcda-sales-comparison/skills/mcda-sales-comparison/SKILL.md" -maxdepth 8 2>/dev/null | head -1 | sed 's|/skills/mcda-sales-comparison/SKILL.md||'
```
If still empty, use: `/home/reggiechan/021-CRE-150/plugins/mcda-sales-comparison`

**Workspace path** — current working directory. Create `Reports/` if absent:
```bash
mkdir -p "$(pwd)/Reports"
```

**Timestamp** — run `TZ=America/Toronto date +%Y-%m-%d_%H%M%S`.

From the resolved plugin root, construct:
- `SCRIPTS_DIR` = `<plugin_root>/skills/mcda-sales-comparison/scripts`
- `CALCULATOR` = `<SCRIPTS_DIR>/mcda_sales_calculator.py`

Verify the calculator exists:
```bash
ls "<CALCULATOR>"
```
If missing, report the error and stop.

**Input JSON path** — resolve to absolute path. If the user provided a relative path,
resolve relative to workspace. Verify the file exists before dispatching.

**Weight profile** — use the `--profile` value if provided; otherwise use `"auto"` (the
calculator will auto-detect from property_type in the JSON).

---

## Step 1 — Dispatch analysis subagent

Use the **Agent tool** to dispatch a subagent. This offloads the calculator run and report
generation to a fresh 200k-token context window, keeping the primary context clean.

If the Agent tool is unavailable, execute Steps A through E directly in the current context.

Substitute the resolved values for `{{ }}` placeholders, then call the Agent tool with
`description: "MCDA sales comparison analysis"` and the prompt below:

--- BEGIN SUBAGENT PROMPT ---

You are an MCDA sales comparison analysis agent. Your sole job is to complete the analysis
pipeline below and return a structured summary. Do not ask questions — execute all steps
and report results.

## Parameters

- Input JSON: {{ INPUT_JSON_PATH }}
- Weight profile: {{ PROFILE }}
- Workspace: {{ WORKSPACE_PATH }}
- Reports folder: {{ WORKSPACE_PATH }}/Reports/
- Timestamp: {{ TIMESTAMP }}
- Scripts directory: {{ SCRIPTS_DIR }}
- Calculator: {{ CALCULATOR }}

## Step A — Validate input

Read the input JSON file using the Read tool:
- Read(file_path="{{ INPUT_JSON_PATH }}")

Confirm it contains:
- `subject_property` with `address` and `building_sf`
- `comparable_sales` array with at least 3 entries
- `valuation_date` at root or in `market_parameters`

If validation fails, stop and report the specific missing fields.

## Step B — Run MCDA calculator

Run the following in Bash. Note: `cd` to the scripts directory first — the calculator uses
sibling imports (validation, score_to_price, weight_profiles) that resolve relative to CWD.

If weight profile is "auto":
```bash
cd "{{ SCRIPTS_DIR }}" && python3 mcda_sales_calculator.py \
  "{{ INPUT_JSON_PATH }}" \
  --output /tmp/mcda_results.json \
  --verbose
```

If weight profile is specified:
```bash
cd "{{ SCRIPTS_DIR }}" && python3 mcda_sales_calculator.py \
  "{{ INPUT_JSON_PATH }}" \
  --output /tmp/mcda_results.json \
  --profile {{ PROFILE }} \
  --verbose
```

Capture stdout/stderr. If the command exits non-zero, report the error and stop.

## Step C — Verify results JSON

Read the results file: Read(file_path="/tmp/mcda_results.json")

Verify ALL of the following before proceeding to report generation:
1. `value_indication.indicated_value_psf` is present, non-null, and positive (> 0)
2. `value_indication.indicated_value_total` is present, non-null, and positive
3. `comparable_analysis` array has at least 3 entries
4. `subject_property.composite_score` is present and numeric
5. `analysis_summary.comparables_used` equals len(comparable_analysis)
6. `value_indication.regression.r_squared` is present and between 0 and 1

If ANY check fails:
- Report which check failed and the actual value found
- Set errors field in the ANALYSIS_RESULT return block
- Still proceed to Step D — generate the report with a warning section noting the issue

## Step D — Generate markdown report

Using the results from /tmp/mcda_results.json, write a complete markdown report to:
`{{ WORKSPACE_PATH }}/Reports/{{ TIMESTAMP }}_mcda_sales_comparison.md`

Use this template, filling every placeholder with real values from the results JSON:

```markdown
# MCDA Sales Comparison Analysis

**Subject Property:** {subject_property.address}
**Property Type:** {analysis_summary.property_type}
**Valuation Date:** {analysis_summary.valuation_date}
**Analysis Date:** {analysis_summary.analysis_date}
**Weight Profile:** {analysis_summary.weights_profile}

---

## Executive Summary

**Indicated Value:** ${value_indication.indicated_value_psf:.2f}/SF (${value_indication.indicated_value_total:,.0f} total)
**Value Range:** ${value_indication.value_range_psf[0]:.2f} – ${value_indication.value_range_psf[1]:.2f}/SF

**Methodology:**
- MCDA Ordinal Ranking with Score-to-Price Mapping
- {analysis_summary.comparables_used} comparable sales analyzed
  ({analysis_summary.comparables_excluded} excluded — non-arm's length or data issues)
- Interpolation weight: {value_indication.reconciliation.method_weights.interpolation:.0%},
  Regression weight: {value_indication.reconciliation.method_weights.regression:.0%}
- **Reconciliation rationale:** {value_indication.reconciliation.rationale}

---

## Subject Property

**Address:** {subject_property.address}
**Building SF:** {subject_property.building_sf:,}
**Composite Score:** {subject_property.composite_score:.3f} (lower = better)

---

## Comparable Sales Analysis

| # | ID | Address | Sale Date | Price | PSF | Score | Rank |
|---|----|---------|-----------|-------|-----|-------|------|
[For each entry in comparable_analysis, sorted by composite_score ascending:]
| {rank} | {id} | {address} | {sale_date} | ${sale_price:,.0f} | ${price_psf:.2f} | {composite_score:.3f} | {rank} |
| **Subject** | — | {subject_property.address} | — | TBD | TBD | {subject_property.composite_score:.3f} | {subject_rank} |

---

## Score-to-Price Mapping

### Interpolation Method

**Lower Bracket:** {value_indication.interpolation.lower_bracket} (Score: X.XX, $XX.XX/SF)
**Upper Bracket:** {value_indication.interpolation.upper_bracket} (Score: X.XX, $XX.XX/SF)
**Confidence:** {value_indication.interpolation.confidence}

**Indicated Value (Interpolation):** ${value_indication.interpolation.indicated_psf:.2f}/SF

### Regression Method

**Method:** {value_indication.regression.method}
**R²:** {value_indication.regression.r_squared:.3f}
**Slope (β):** ${value_indication.regression.beta:.4f}/score point

**Indicated Value (Regression):** ${value_indication.regression.indicated_psf:.2f}/SF

### Reconciliation

| Method | Weight | Indicated Value |
|--------|--------|-----------------|
| Interpolation | {value_indication.reconciliation.method_weights.interpolation:.0%} | ${value_indication.interpolation.indicated_psf:.2f}/SF |
| Regression | {value_indication.reconciliation.method_weights.regression:.0%} | ${value_indication.regression.indicated_psf:.2f}/SF |
| **Reconciled** | **100%** | **${value_indication.indicated_value_psf:.2f}/SF** |

**Rationale:** {value_indication.reconciliation.rationale}

---

## Value Indication

**Indicated Value Per SF:** ${value_indication.indicated_value_psf:.2f}
**Indicated Total Value:** ${value_indication.indicated_value_total:,.0f}
**Value Range:** ${value_indication.value_range_total[0]:,.0f} – ${value_indication.value_range_total[1]:,.0f} (±5%)

**Confidence:** {value_indication.interpolation.confidence} / R² = {value_indication.regression.r_squared:.3f}

---

## Methodology Notes

### MCDA vs Traditional DCA

**Traditional DCA** requires paired sales data and applies sequential dollar adjustments — errors
compound and adjustment order matters. **MCDA Ordinal Ranking** ranks all properties on each
characteristic; relative rankings are more stable than dollar estimates. Score-to-price mapping
via interpolation and regression provides a model-based value check on the interpolation result.

### Weight Profile: {analysis_summary.weights_profile}

[Enumerate the top variables from the results and their directional meaning.]

### Limitations

1. Ordinal ranking captures relative position, not magnitude of differences
2. Requires minimum 3 comparables for meaningful analysis
3. Score-to-price assumes monotonicity (better score → higher price)
4. Extrapolation beyond comparable range carries lower confidence

---

[If analysis_summary.warnings is non-empty:]
## Warnings

{For each warning in analysis_summary.warnings, format as a bullet point}

---

**Report Generated By:** Claude Code — MCDA Sales Comparison Plugin
**Analysis Date:** {analysis_summary.analysis_date}
**Framework:** MCDA Ordinal Ranking with Score-to-Price Mapping
```

Compute `subject_rank` by counting how many comparables have a lower composite_score than
the subject (lower = better), then adding 1.

Write the completed report to the Reports/ path using the Write tool.

Copy the results JSON for reproducibility:
```bash
cp /tmp/mcda_results.json \
   "{{ WORKSPACE_PATH }}/Reports/{{ TIMESTAMP }}_mcda_sales_comparison.json"
```

## Step E — Verify outputs

Confirm:
- Report file exists and has size > 0: `ls -lh "{{ WORKSPACE_PATH }}/Reports/{{ TIMESTAMP }}_mcda_sales_comparison.md"`
- JSON copy exists: `ls -lh "{{ WORKSPACE_PATH }}/Reports/{{ TIMESTAMP }}_mcda_sales_comparison.json"`

## Return format

Return ONLY this block — no other commentary:

ANALYSIS_RESULT
subject: <subject_property.address>
indicated_value_psf: $<XX.XX>
indicated_value_total: $<X,XXX,XXX>
value_range: $<X,XXX,XXX> – $<X,XXX,XXX>
comparables_used: <N>
regression_r2: <X.XXX>
regression_method: <ols|monotone|theil_sen>
report: Reports/<filename>.md
json: Reports/<filename>.json
errors: <none, or description of any issues encountered>

--- END SUBAGENT PROMPT ---

---

## Step 2 — Relay result to user

When the subagent returns, parse the `ANALYSIS_RESULT` block and report:

```
✅ MCDA analysis complete — {comparables_used} comparables
💰 Indicated Value: {indicated_value_psf}/SF ({indicated_value_total})
📊 Value Range: {value_range}
📈 R² ({regression_method}): {regression_r2}
📄 Report: {report}
📋 JSON: {json}
```

If `errors` is not "none":
> ⚠️ Issues encountered: {errors}
