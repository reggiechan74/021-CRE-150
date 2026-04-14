# MCDA Sales Comparison Analysis

**Subject Property:** 2550 Industrial Parkway North, Hamilton, ON
**Property Type:** Industrial
**Valuation Date:** 2025-01-15
**Analysis Date:** 2025-12-16
**Weight Profile:** industrial_default

---

## Executive Summary

**Indicated Value:** $92.96/SF ($4,648,009 total)
**Value Range:** $87.69 – $98.53/SF ($4,415,609 – $4,880,410 total)

**Methodology:**
- MCDA Ordinal Ranking with Score-to-Price Mapping
- 5 comparable sales analyzed (0 excluded)
- Interpolation weight: 43%, Regression weight: 57%
- **Reconciliation rationale:** Small sample (n=5) favors interpolation; Strong model fit (R²=0.93) supports regression; Subject well-bracketed by comparables

---

## Subject Property

**Address:** 2550 Industrial Parkway North, Hamilton, ON
**Building SF:** 50,000 SF
**Composite Score:** 3.079 (lower = better)

---

## Comparable Sales Analysis

| Rank | ID | Address | Sale Date | Sale Price | PSF | Score |
|------|-----|---------|-----------|-----------|-----|-------|
| 1 | COMP_3 | 2320 Industrial Parkway North, Hamilton, ON | 2024-06-10 | $4,850,000 | $103.19 | 1.684 |
| 2 | COMP_1 | 2480 Industrial Parkway North, Hamilton, ON | 2024-09-15 | $4,650,000 | $95.88 | 2.895 |
| — | **SUBJECT** | **2550 Industrial Parkway North, Hamilton, ON** | — | **TBD** | **TBD** | **3.079** |
| 3 | COMP_4 | 1150 South Service Road, Stoney Creek, ON | 2024-08-05 | $4,400,000 | $88.00 | 3.605 |
| 4 | COMP_2 | 2650 Parkdale Avenue North, Hamilton, ON | 2024-07-22 | $4,100,000 | $78.85 | 4.211 |
| 5 | COMP_5 | 890 Kenora Avenue, Hamilton, ON | 2024-10-18 | $3,750,000 | $76.53 | 5.526 |

*Note: Composites scores are weighted rank sums — lower scores indicate superior overall quality relative to comparables. Subject is positioned between COMP_1 (score 2.895) and COMP_4 (score 3.605).*

---

## Score-to-Price Mapping

### Interpolation Method

| Parameter | Value |
|-----------|-------|
| Lower Bracket | COMP_1 — 2480 Industrial Parkway North (score 2.895, $95.88/SF) |
| Upper Bracket | COMP_4 — 1150 South Service Road (score 3.605, $88.00/SF) |
| Subject Score | 3.079 |
| Confidence | High |
| **Indicated PSF** | **$93.83/SF** |

The subject's score of 3.079 falls between COMP_1 (2.895) and COMP_4 (3.605), allowing linear interpolation within a well-defined bracket. High confidence reflects tight bracketing and minimal extrapolation.

### Regression Method

| Parameter | Value |
|-----------|-------|
| Method | Ordinary Least Squares (OLS) |
| R² | 0.928 |
| Slope (β) | −7.5519 $/SF per rank unit |
| **Indicated PSF** | **$92.30/SF** |

The strong R² of 0.928 indicates that composite score explains 92.8% of the variation in sale price per SF across the comparable set. The negative slope confirms the expected inverse relationship between score (lower = better) and price per SF.

### Reconciliation Table

| Method | Weight | Indicated PSF | Indicated Total Value |
|--------|--------|---------------|-----------------------|
| Interpolation | 43% | $93.83 | $4,691,500 |
| Regression (OLS) | 57% | $92.30 | $4,615,000 |
| **Reconciled** | **100%** | **$92.96** | **$4,648,009** |

*Weights reflect the analytical judgment that the strong regression fit (R²=0.928) warrants slight majority weighting, while interpolation's direct bracketing of the subject provides meaningful corroboration in a five-comparable sample.*

---

## Value Indication

**Indicated Value Per SF:** $92.96
**Indicated Total Value:** $4,648,009
**Value Range:** $4,415,609 – $4,880,410 (±5%)
**Confidence:** High / R² = 0.928

---

## Methodology Notes

### MCDA vs Traditional DCA

Traditional direct comparison analysis (DCA) applies dollar adjustments to each comparable for differences in location, condition, size, and market conditions, then reconciles the adjusted sale prices to a value conclusion. While intuitive, DCA adjustments are often subjectively estimated and difficult to support empirically in thin markets. The MCDA (Multi-Criteria Decision Analysis) ordinal ranking approach instead scores each property across weighted criteria without requiring dollar-quantified adjustments. By mapping composite ordinal scores to observed sale prices using interpolation and regression, MCDA provides a systematic, auditable, and statistically grounded alternative that is particularly well-suited to industrial markets where paired-sales data for discrete adjustments is limited.

### Weight Profile: industrial_default

The `industrial_default` profile weights variables according to their typical influence on industrial property value in the Greater Hamilton market. Key weighted variables include:

| Variable | Direction | Rationale |
|----------|-----------|-----------|
| location_score | Higher = better (lower rank score) | Proximity to highway interchange, labour pool, and logistics infrastructure |
| clear_height_feet | Higher = better | Modern logistics and e-commerce tenants require 28'+ clear heights |
| condition | Better condition = lower rank score | Physical condition directly affects lease-up risk and capital expenditure |
| effective_age_years | Lower age = lower rank score | Newer buildings command rent and value premiums |
| loading_docks_total | More = better | Dock-loading capacity is a primary functional utility driver |
| highway_frontage | Yes = better | Visibility and direct access reduce tenant logistics costs |
| lot_size_acres | Larger = better | Land coverage ratios affect expansion options and trailer staging |
| office_finish_pct | Lower = better (for industrial) | Excess office reduces warehouse efficiency and tenant appeal |

### Limitations

1. **Sample size:** Five comparables represent a small dataset. While sufficient for interpolation with good bracketing, additional sales would improve statistical reliability.
2. **Time adjustments not applied:** Warnings in the analysis flag four comparables with sales 4–7 months prior to the valuation date. A 3.5% annual appreciation rate implies adjustments of 1.2%–2.2% that have not been incorporated into the reported values. Appraisers should consider applying time-trending adjustments in a formal appraisal report.
3. **Geographic scope:** COMP_4 (Stoney Creek) is located outside the primary Hamilton industrial node, which may introduce location heterogeneity beyond what the location score variable fully captures.
4. **Model assumptions:** OLS regression assumes a linear relationship between composite score and price per SF. With only five data points, the model is sensitive to individual observations, and the regression results should be interpreted alongside the interpolation method rather than in isolation.

---

## Warnings

The following time adjustment warnings were flagged by the analysis engine. No time adjustments have been applied to the sale prices used in this analysis. In a formal appraisal, consideration should be given to adjusting these comparables to the valuation date of 2025-01-15 using the market appreciation rate of 3.5% per annum.

| Comparable | Sale Date | Months Prior to Valuation Date | Implied Time Adjustment |
|------------|-----------|-------------------------------|------------------------|
| COMP_1 — 2480 Industrial Parkway North | 2024-09-15 | ~4.0 months | ~1.2% |
| COMP_2 — 2650 Parkdale Avenue North | 2024-07-22 | ~5.8 months | ~1.7% |
| COMP_3 — 2320 Industrial Parkway North | 2024-06-10 | ~7.2 months | ~2.2% |
| COMP_4 — 1150 South Service Road | 2024-08-05 | ~5.4 months | ~1.6% |

*COMP_5 (sale date 2024-10-18) was closest to the valuation date and required no time adjustment flag.*

---

**Report Generated By:** Claude Code — MCDA Sales Comparison Plugin
**Analysis Date:** 2025-12-16
**Framework:** MCDA Ordinal Ranking with Score-to-Price Mapping
