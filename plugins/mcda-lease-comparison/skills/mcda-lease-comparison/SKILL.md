---
name: mcda-lease-comparison
description: >
  Use when the user asks to run a competitive positioning analysis, rank a subject property
  against market comparables using MCDA, determine how competitive a listing is, calculate
  what rent reduction is needed to achieve Top 3 positioning, analyze a CoStar or broker
  package for competitive ranking, or generate a relative valuation report. Trigger phrases
  include: "relative valuation", "competitive positioning", "rank this property", "how
  competitive is this listing", "run relative valuation", "/mcda-lease-comparison".
---

# Relative Valuation: Competitive Positioning Analysis

**Automated PDF → JSON → Python → Report workflow for Multi-Criteria Decision Analysis (MCDA)**

You are executing the **/mcda-lease-comparison** skill. You are an expert in **Relative Valuation** and **Competitive Positioning Analysis** for commercial real estate, specializing in Multi-Criteria Decision Analysis (MCDA).

## Objective

Determine where the subject property ranks relative to market comparables and provide strategic pricing recommendations to achieve Top 3 competitive positioning (70-90% deal-winning probability).

## Core Methodology: MCDA Framework

### The Variable System: Core (9) + Optional (16) = Up to 25 Total

**Dynamic Weighting**: The system uses 9 core variables (always included) plus 16 optional variables (included only if sufficient data is available - 50% threshold for numeric fields, at least one True for boolean fields). When optional variables are missing, their weights are redistributed proportionally among available variables.

#### Full Variable Set (When All Data Available - 25 Variables)

| Variable | Weight | Type | Rationale |
|----------|--------|------|-----------|
| **Net Asking Rent** | 11% | Core | **Most critical** - Direct impact on tenant budget |
| **Parking Ratio** | 10% | Core | **Second most critical** - Often deal-breaker for industrial/office |
| **TMI** | 9% | Core | Affects total occupancy cost |
| **Clear Height** | 7% | Core | Critical for industrial operations |
| **% Office Space** | 7% | Core | Mix affects usability |
| **Distance** | 7% | Core | Location convenience |
| **Area Difference** | 7% | Core | Size match to tenant needs |
| **Building Age** | 4% | Core | Replaces Year Built - more intuitive condition proxy |
| **Class** | 5% | Core | A/B/C quality tier |
| **Bay Depth** | 5% | Optional | Racking efficiency, trailer access |
| **Shipping Doors (TL)** | 4% | Optional | Truck-level loading capacity |
| **Lot Size (Acres)** | 4% | Optional | Expansion potential, outdoor storage |
| **Shipping Doors (DI)** | 3% | Optional | Drive-in door access |
| **Power** | 3% | Optional | Electrical capacity (amps) |
| **HVAC Coverage** | 3% | Optional | Climate control for products/workers |
| **Sprinkler Type** | 3% | Optional | ESFR = insurance savings + high-piled storage |
| **Trailer Parking** | 2% | Optional | Trailer storage availability |
| **Rail Access** | 2% | Optional | Deal-breaker for bulk commodities |
| **Crane** | 2% | Optional | Heavy manufacturing essential |
| **Occupancy Status** | 0% | Optional | Vacant = immediate occupancy (low priority) |
| **Grade Level Doors** | 2% | Optional | Courier vans, small truck access |
| **Days on Market** | 2% | Optional | Landlord motivation indicator |
| **Zoning** | 2% | Optional | Permitted use restrictions |
| **Secure Shipping** | 0% | Optional | Secure loading areas (rarely available) |
| **Excess Land** | 0% | Optional | Expansion/outdoor storage (rarely available) |

### Competitive Tiers

| Rank | Status | Win Probability | Action Required |
|------|--------|----------------|-----------------|
| **#1-3** | ✅ Highly Competitive | 70-90% | Maintain position |
| **#4-10** | ⚠️ Moderately Competitive | 50-70% | Consider adjustments |
| **#11+** | ❌ Not Competitive | <50% | **Urgent** price reduction needed |

**The "Top 3 Rule"**: Must be Rank #1, #2, or #3 to win deals consistently.

### Ranking Rules

**Ascending (Lower = Rank 1):** Net Asking Rent, TMI, Distance, Class (A=1 beats C=3), Area Difference

**Descending (Higher = Rank 1):** Clear Height, Parking Ratio, Year Built, % Office Space

**Tie handling:** Average rank method — (5 + 6 + 7) / 3 = 6.0 for a three-way tie at ranks 5-7.

### Strategic Recommendations by Rank Tier

| Tier | Strategy |
|------|----------|
| **Rank #1-3** | Defend pricing, highlight value proposition, weekly comp monitoring |
| **Rank #4-10** | Calculate exact pricing to reach Rank #3, evaluate TI/free rent alternatives |
| **Rank #11+** | Urgent repositioning — immediate rent reduction, consider below-market deal to secure tenant |

### Sensitivity Analysis

Calculate rent/TMI reduction to achieve Rank #3:
- **Scenario 1**: Rent only — lower net asking rent, TMI unchanged
- **Scenario 2**: TMI only — lower operating costs, rent unchanged
- **Scenario 3**: Combined — adjust both rent and TMI

Formula: `Points gap = Subject Score − Rank #3 Score` → convert to required rent/TMI changes using variable weights.

### Non-Price Levers (When Price Reduction Not Feasible)

TI allowance (+$10-20/SF effective rent reduction), free rent (3-6 months), TMI escalation caps (2-3%/year), lease flexibility (termination/expansion rights).

### Key Communication Language

**To Landlord:**
- Rank #1-3: "Highly competitive at 70-90% deal-winning probability"
- Rank #4-10: "Moderately competitive — specific adjustments to reach Top 3"
- Rank #11+: "Not competitive — immediate price correction required"

**To Tenant Rep:**
- Rank #1-3: "Excellent value — proceed with negotiations"
- Rank #4-10: "Decent but not optimal — use analysis to negotiate rent reduction"
- Rank #11+: "Overpriced — pursue Top 3 or negotiate aggressively"

### Red Flags

1. Ignoring the Top 3 Rule ("we're Rank #5, close enough")
2. Focusing only on rent — parking (10%) is nearly as important
3. Using stale comps — re-run monthly during active leasing
4. Over-relying on model — qualitative factors always supplement the output

---

## Step 0 — Resolve plugin paths (runs in primary context before subagent dispatch)

**Plugin root** — run in Bash:
```bash
echo "${CLAUDE_PLUGIN_ROOT}"
```
If empty, find it:
```bash
find ~ -path "*/mcda-lease-comparison/skills/mcda-lease-comparison/SKILL.md" -maxdepth 8 2>/dev/null | head -1 | sed 's|/skills/mcda-lease-comparison/SKILL.md||'
```
If still empty, use: `/home/reggiechan/021-CRE-150/plugins/mcda-lease-comparison`

**Workspace** — current working directory. Create `Reports/` if absent:
```bash
mkdir -p "$(pwd)/Reports"
```

**Timestamp** — run `TZ=America/Toronto date +%Y-%m-%d_%H%M%S`.

From the resolved plugin root, construct absolute paths:
- `SCRIPTS_DIR` = `<plugin_root>/skills/mcda-lease-comparison/scripts`
- `REFERENCES_DIR` = `<plugin_root>/skills/mcda-lease-comparison/references`
- `INPUTS_DIR` = `<plugin_root>/skills/mcda-lease-comparison/inputs`
- `CALCULATOR` = `<SCRIPTS_DIR>/relative_valuation_calculator.py`
- `DISTANCE_CALCULATOR` = `<SCRIPTS_DIR>/calculate_distances.py`
- `PDF_STYLE` = `<REFERENCES_DIR>/pdf_style.css`
- `SCHEMA_TEMPLATE` = `<INPUTS_DIR>/schema_template.json`

Verify the calculator exists:
```bash
ls "<CALCULATOR>"
```
If missing, report the error and stop.

**Parse user arguments:**
- Input path (PDF or JSON) — resolve to absolute path, verify it exists
- `--full` flag (show all competitors vs. top 10 only)
- `--stats` flag (append statistical analysis)
- `--persona <name>` (default, 3pl, manufacturing, office) — default: `default`

---

## Step 1 — Dispatch analysis subagent

Use the **Agent tool** to dispatch a subagent. This offloads vision reads, data extraction, and report generation to a fresh 200k context window, keeping the primary context clean.

If the Agent tool is unavailable, execute Steps A through G directly in the current context.

Substitute the resolved values for `{{ }}` placeholders, then call the Agent tool with `description: "Relative valuation competitive positioning analysis"` and the prompt below:

--- BEGIN SUBAGENT PROMPT ---

You are a relative valuation competitive positioning analysis agent for commercial real estate. Your job is to execute the full analysis pipeline below and return a structured result. Do not ask questions — execute all steps and report results.

## Parameters

- Input: {{ INPUT_PATH }}
- Workspace: {{ WORKSPACE }}
- Reports folder: {{ WORKSPACE }}/Reports/
- Timestamp: {{ TIMESTAMP }}
- Scripts directory: {{ SCRIPTS_DIR }}
- Calculator: {{ CALCULATOR }}
- Distance calculator: {{ DISTANCE_CALCULATOR }}
- PDF style: {{ PDF_STYLE }}
- Schema template: {{ SCHEMA_TEMPLATE }}
- Flags: {{ FLAGS }}  (e.g., --full --stats --persona 3pl)

## Extraction Reference Tables

### 25 Variables — Field Names, Encodings, and Direction

**Core variables (always included):**

| Field | Encoding | Rank Direction |
|-------|----------|----------------|
| `net_asking_rent` | $/SF/year (decimal) | Ascending (lower = better) |
| `parking_ratio` | spaces per 1,000 SF (decimal) | Descending (higher = better) |
| `tmi` | $/SF/year (decimal) | Ascending (lower = better) |
| `clear_height_ft` | feet (decimal) | Descending (higher = better) |
| `pct_office_space` | **DECIMAL 0–1** (e.g., 0.11 not 11.0) | Descending (higher = better) |
| `distance_km` | km from subject (0.0 for subject) | Ascending (lower = better) |
| `area_difference` | abs(available_sf − subject_sf) / subject_sf | Ascending (lower = better) |
| `year_built` / `building_age_years` | year integer / age auto-calculated | Descending year = better |
| `class` | 1=A, 2=B, 3=C | Ascending (1=A is best) |

**Optional variables (included if ≥50% of properties have data):**

| Field | Encoding | Rank Direction |
|-------|----------|----------------|
| `bay_depth_ft` | feet (decimal) | Descending |
| `shipping_doors_tl` | integer count (truck-level) | Descending |
| `lot_size_acres` | acres (decimal) | Descending |
| `shipping_doors_di` | integer count (drive-in) | Descending |
| `power_amps` | amps (integer) | Descending |
| `hvac_coverage` | 1=Full, 2=Partial, 3=None | Ascending (1 is best) |
| `sprinkler_type` | 1=ESFR, 2=Standard, 3=None | Ascending (1 is best) |
| `trailer_parking` | boolean true/false | Descending (true is better) |
| `rail_access` | boolean true/false | Descending |
| `crane` | boolean true/false | Descending |
| `occupancy_status` | 1=Vacant, 2=Tenant occupied | Ascending (1=Vacant is better) |
| `grade_level_doors` | integer count | Descending |
| `days_on_market` | integer | Ascending (lower = better) |
| `zoning` | string (e.g., "M1") | No ranking (filter only) |
| `secure_shipping` | boolean | Descending |
| `excess_land` | boolean | Descending |

### Critical Extraction Rules

**Address format (REQUIRED for distance API):**
```
"Street Address, City, Province PostalCode, Country"
"2550 Stanfield Rd, Mississauga, ON L4Y 1S2, Canada"
```
- Province: two-letter code (ON not Ontario)
- Postal code: space inside (L4Y 1S2 not L4Y1S2)
- Unit stored in `unit` field, NOT appended to address

**pct_office_space conversion (CRITICAL):**
- PDF shows % Warehouse Space, NOT % Office Space
- Formula: `pct_office_space = (100 − warehouse_pct) / 100`
- Example: 89% warehouse → (100−89)/100 = **0.11** (NOT 11.0)

**Shipping doors:** PDF format "X TL Y DI"
- X → `shipping_doors_tl`, Y → `shipping_doors_di`

**Bay depth:** Parse from "Bay Size" field (e.g., "55 x 52" → take first number: 55.0)

**Lot size:** Convert to acres (from sq ft: ÷ 43,560; from hectares: × 2.471)

**Subject property:** Must have `is_subject: true`, `distance_km: 0.0`

**All comparables:** Must have `is_subject: false`

### Tenant Personas (for --persona flag)

| Persona | Key emphasis |
|---------|-------------|
| `default` | Balanced — general industrial |
| `3pl` | Bay depth 7%, clear height 10%, shipping doors TL 6%, trailer parking 4% |
| `manufacturing` | Clear height 9%, power 5%, crane 5%, rail access 4%, bay depth 6% |
| `office` | Office space 12%, parking 12%, rent 13%, HVAC 6%, class 8%, distance 10% |

### Competitive Tiers (for result interpretation)

| Rank | Status | Win Probability |
|------|--------|----------------|
| #1-3 | Highly Competitive | 70-90% |
| #4-10 | Moderately Competitive | 50-70% |
| #11+ | Not Competitive | <50% |

## Step A — Extract data from PDF (if input is a PDF)

If the input file is a JSON file (`.json`), skip to Step C.

Read the PDF using vision. For large PDFs (>5 pages), read in batches of 20 pages to stay within context limits.

Extract all properties — subject + comparables — using the extraction rules above. Capture all available optional fields in addition to the 9 core fields.

Identify the subject property: it is typically highlighted, listed first, or described as the "subject" or "availability" being analyzed. Set `is_subject: true`, `distance_km: 0.0`.

## Step B — Create input JSON

Build the input JSON following this structure:

```json
{
  "analysis_date": "YYYY-MM-DD",
  "market": "Market Name - Property Type",
  "subject_property": {
    "address": "Complete geocodable address",
    "unit": "",
    "year_built": 2005,
    "clear_height_ft": 32.0,
    "pct_office_space": 0.11,
    "parking_ratio": 2.0,
    "available_sf": 50000,
    "distance_km": 0.0,
    "net_asking_rent": 9.50,
    "tmi": 4.75,
    "class": 2,
    "is_subject": true,
    "landlord": ""
  },
  "comparables": [
    { /* same structure as subject_property with is_subject: false */ }
  ],
  "filters": {},
  "weights": {}
}
```

Save to: `{{ WORKSPACE }}/Reports/{{ TIMESTAMP }}_mcda_lease_comparison_input.json`

## Step C — Validate input JSON before running calculator

**Verify the JSON before proceeding** — the calculator cannot self-correct if the input is malformed. Run:

```bash
python3 - << 'PYEOF'
import json, sys

with open("{{ WORKSPACE }}/Reports/{{ TIMESTAMP }}_mcda_lease_comparison_input.json") as f:
    data = json.load(f)

errors = []

if "subject_property" not in data:
    errors.append("Missing 'subject_property'")
if not data.get("comparables"):
    errors.append("Missing or empty 'comparables' array")
if "analysis_date" not in data:
    errors.append("Missing 'analysis_date'")

sp = data.get("subject_property", {})
if not sp.get("is_subject"):
    errors.append("subject_property.is_subject must be true")
if sp.get("distance_km", -1) != 0.0:
    errors.append("subject_property.distance_km must be 0.0")

# Catch common pct_office_space mistake
for prop in [sp] + data.get("comparables", []):
    pct = prop.get("pct_office_space", 0)
    if pct > 1.0:
        errors.append(f"{prop.get('address','unknown')}: pct_office_space={pct} — must be decimal (0.11 not 11.0)")

if errors:
    print("VALIDATION FAILED:")
    for e in errors:
        print(f"  - {e}")
    sys.exit(1)
else:
    print(f"Validation passed — {len(data.get('comparables', []))} comparables, subject: {sp.get('address','?')}")
PYEOF
```

If validation fails, correct the JSON errors and re-validate before proceeding to Step D.

## Step D — Calculate distances (if API key available)

```bash
if [ -z "$DISTANCEMATRIX_API_KEY" ]; then
  echo "WARNING: DISTANCEMATRIX_API_KEY not set. Skipping distance calculations."
  echo "Set API key: export DISTANCEMATRIX_API_KEY=your_key_here"
else
  python3 "{{ DISTANCE_CALCULATOR }}" \
    --input "{{ WORKSPACE }}/Reports/{{ TIMESTAMP }}_mcda_lease_comparison_input.json" \
    --output "{{ WORKSPACE }}/Reports/{{ TIMESTAMP }}_mcda_lease_comparison_input.json" \
    --verbose
fi
```

## Step E — Run Python calculator

Note: `cd` to the scripts directory first — the calculator uses sibling imports (statistics_module, weights_loader) that resolve relative to CWD.

Build the command based on flags:

```bash
cd "{{ SCRIPTS_DIR }}" && python3 relative_valuation_calculator.py \
  --input "{{ WORKSPACE }}/Reports/{{ TIMESTAMP }}_mcda_lease_comparison_input.json" \
  --output "{{ WORKSPACE }}/Reports/{{ TIMESTAMP }}_mcda_lease_comparison_report.md" \
  --output-json "{{ WORKSPACE }}/Reports/{{ TIMESTAMP }}_mcda_lease_comparison_output.json" \
  {{ FLAGS }}
```

Where `{{ FLAGS }}` may include `--full`, `--stats`, `--persona 3pl`, etc.

Capture stdout/stderr. If the command exits non-zero, report the error and stop.

## Step F — Interpret results and generate executive summary

Read the output JSON from `{{ WORKSPACE }}/Reports/{{ TIMESTAMP }}_mcda_lease_comparison_output.json` and the markdown report. Identify:

1. **Subject rank** — #X out of Y (lower score = better)
2. **Competitive tier** — Highly Competitive (#1-3), Moderately Competitive (#4-10), Not Competitive (#11+)
3. **Key strengths** — variables where subject ranks in Top 5
4. **Key weaknesses** — variables where subject ranks in Bottom 5, especially high-weight ones (rent, parking, TMI)
5. **Sensitivity analysis** — estimate rent/TMI changes needed to reach Rank #3 if not already there
6. **Statistical insights** (if `--stats` was used) — R², regression coefficients, outliers

Append the executive summary to the markdown report OR present inline. Format:

```markdown
## EXECUTIVE SUMMARY: COMPETITIVE POSITIONING

**Subject Property**: [Address]
**Analysis Date**: [Date]
**Market**: [Market Name]

### Current Position
- **Rank**: #X out of Y properties
- **Score**: XX.XX (lower is better)
- **Status**: [Highly/Moderately/Not] Competitive
- **Deal-Winning Probability**: XX-XX%

### Key Findings
1. [Top strength]
2. [Key weakness]
3. [Critical insight]

### Strategic Recommendation
[Action-oriented recommendation for the rank tier]

### Next Steps
1. [Immediate action]
2. [Secondary action]
3. [Long-term]
```

## Step G — Generate PDF report (landscape format)

```bash
pandoc "{{ WORKSPACE }}/Reports/{{ TIMESTAMP }}_mcda_lease_comparison_report.md" \
  -o "{{ WORKSPACE }}/Reports/{{ TIMESTAMP }}_mcda_lease_comparison_report.pdf" \
  --css "{{ PDF_STYLE }}" \
  --pdf-engine=wkhtmltopdf \
  --pdf-engine-opt=--orientation --pdf-engine-opt=Landscape \
  --pdf-engine-opt=--margin-top --pdf-engine-opt=5mm \
  --pdf-engine-opt=--margin-bottom --pdf-engine-opt=5mm \
  --pdf-engine-opt=--margin-left --pdf-engine-opt=8mm \
  --pdf-engine-opt=--margin-right --pdf-engine-opt=8mm
```

Landscape orientation is required — the competitor table has 13 columns. If wkhtmltopdf is unavailable, note in the return block and skip.

## Return format

Return ONLY this block — no other commentary:

ANALYSIS_RESULT
subject: <subject property address>
rank: #X out of Y properties
score: <composite score>
tier: <Highly Competitive / Moderately Competitive / Not Competitive>
win_probability: <XX-XX%>
report: Reports/<filename>.md
json: Reports/<filename>.json
pdf: Reports/<filename>.pdf (or "not generated — wkhtmltopdf unavailable")
errors: <none, or description of issues>

--- END SUBAGENT PROMPT ---

---

## Step 2 — Relay result to user

When the subagent returns, parse the `ANALYSIS_RESULT` block and report:

```
✅ Relative valuation complete
📍 Subject: {subject}
🏆 Rank: {rank}
📊 Score: {score} (lower is better)
🎯 Status: {tier} ({win_probability})
📄 Report: {report}
📋 JSON: {json}
📑 PDF: {pdf}
```

If `errors` is not "none":
> ⚠️ Issues encountered: {errors}
