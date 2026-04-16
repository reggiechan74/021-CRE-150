# Roof Replacement Tender — Scoring Matrix

**Project:** 2550 Argentia Road, Mississauga, ON
**Owner:** Tenebrus Capital
**RFP:** TC-ROOF-2026-001 — issued 2026-03-15
**Submissions received:** 3 compliant of 5 total
**Evaluation date:** 2026-04-15

---

## Weighting Applied (RFP §7, normalized to 6-criterion schema)

| Criterion | Weight | RFP Source |
|---|---:|---|
| Price | 35% | RFP §7 "Total Price" |
| Technical Approach (Materials + VE) | 23% | RFP §7 "Materials" 20 + "VE" 3 |
| Experience / References | 10% | RFP §7 "Qualifications/References" |
| Warranty & Materials | 15% | RFP §7 "Warranty Terms" |
| Schedule & Phasing | 12% | RFP §7 "Schedule & Phasing Plan" |
| Qualifications / Certifications (Safety) | 5% | RFP §7 "Safety Record/Program" |
| **Total** | **100%** | |

Price scoring method: `formula_lowest_ratio` — compliant-pool basis.

---

## Compliance Summary

| Bidder | Stage 1 Mandatory Gates | Result |
|---|---|---|
| Lakeside Roofing Inc. | 45 mil membrane (spec 60 min); single-layer insulation (spec two-layer); 15-yr warranty (min 20); no cover board; no manufacturer certification; denies ponding correction | ❌ Non-compliant |
| Summit Contracting Ltd. | All gates pass; exceeds spec on membrane, insulation, warranty | ✅ Compliant |
| Pinnacle Roofing Corp. | All gates pass; meets spec | ✅ Compliant |
| Metro Building Solutions Inc. | 25+ exclusions; 1-yr workmanship (min 2); no cover board; single-layer insulation; no manufacturer certification; denies ponding correction; WSIB rate 1.12 (above industry avg) | ❌ Non-compliant |
| Heritage Construction Group | All gates pass; meets spec with VE options available | ✅ Compliant |

---

## Rated Scoring (Compliant Bids)

| Rank | Bidder | Price (35) | Technical (23) | Experience (10) | Warranty (15) | Schedule (12) | Qualifications (5) | **Weighted Total** |
|---:|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | Heritage Construction Group | 100.0 | 88 | 92 | 82 | 88 | 90 | **91.80** |
| 2 | Summit Contracting Ltd. | 77.9 | 95 | 95 | 98 | 92 | 95 | **89.10** |
| 3 | Pinnacle Roofing Corp. | 94.44 | 80 | 85 | 82 | 82 | 78 | **85.99** |

---

## Pricing Comparison

| Bidder | Base Bid (ex HST) | HST @ 13% | Grand Total | Status |
|---|---:|---:|---:|---|
| Metro Building Solutions | $468,000 | $60,840 | $528,840 | Excluded (non-compliant) |
| Lakeside Roofing | $487,500 | $63,375 | $550,875 | Excluded (non-compliant) |
| **Heritage Construction** | **$578,000** | **$75,140** | **$653,140** | ✅ Compliant low |
| Pinnacle Roofing | $612,000 | $79,560 | $691,560 | ✅ Compliant |
| Summit Contracting | $742,000 | $96,460 | $838,460 | ✅ Compliant |

**Low compliant bid:** $578,000 (Heritage)
**High compliant bid:** $742,000 (Summit)
**Compliant-pool spread:** 28.4%

> ⚠️ Spread exceeds 15% — Summit's 28% premium over Heritage reflects upgraded specification (80 mil, R-38, 30-yr NDL) rather than scope divergence. See red flag report for analysis.

---

## Scoring Rationale

### 1. Heritage Construction Group — 91.80 pts

**Strengths:** Lowest compliant price (100 on price formula); GAF Master Elite + COR + WSIB 0.81; Apotex pharmaceutical reference directly analogous to Tenebrus tenant profile; transparent VE analysis demonstrates integrity (explicitly recommends AGAINST VE Option 2 single-layer insulation on honest energy analysis).
**Weaknesses:** 2-year workmanship matches RFP minimum but lags Summit (5yr) and Pinnacle (3yr); base bid leaves only 1-day margin before July 31 LD trigger.
**Key differentiator:** Best price among compliant bids + Apotex pharma experience + VE flexibility gives owner optionality.

### 2. Summit Contracting Ltd. — 89.10 pts

**Strengths:** Highest technical/warranty/qualification sub-scores of any bidder; 30-yr NDL + 5-yr workmanship + 10-yr ponding warranty; GAF Master Elite + COR + WSIB 0.72 (best of all); Pfizer + Shoppers pharma references; 25 years in business; temperature-monitoring protocol detailed.
**Weaknesses:** 28% price premium over Heritage; spec exceeds RFP minimums without owner having explicitly requested upgrade (80 mil vs 60, R-38 vs R-30).
**Key differentiator:** The "insurance policy" bid — buys highest-confidence execution but at a cost that only makes sense if owner prioritizes long-term hold or cannot tolerate any tenant disruption risk.

### 3. Pinnacle Roofing Corp. — 85.99 pts

**Strengths:** Matches RFP spec exactly without gold-plating; 20-yr NDL + 3-yr workmanship + 5-yr ponding warranty; Tim Hortons cold storage reference directly comparable; 18 years in business.
**Weaknesses:** Smaller crew relative to 85,000 sqft scope; no dedicated pharma reference (cold storage is adjacent but not identical); permits excluded ($4.5-6k owner cost).
**Key differentiator:** The "safe middle" bid — meets every requirement without exceeding any. $34k more expensive than Heritage without the differentiating VE analysis or pharma reference.

---

*Scoring produced by `roof-score-matrix` skill via `scripts/score.py`. Mandatory gate evaluation per `roof-qualification-check`. Technical evaluation per `roof-technical-review` against `fixtures/domain_knowledge/`.*
