# Lease Abstraction Skill — Guide for CRE Practitioners

**Author:** Reggie Chan  
**Specification:** REIXS-LA-NA-001  
**Version:** 1.0.0  

---

## What This Skill Does

This skill reads a commercial lease (Office or Industrial) and produces a **5–10 page summary** that captures all the important business terms: parties, rent, dates, obligations, and risks.

Think of it as **automated lease abstraction** — the kind of work a paralegal would normally do in 2–4 hours.

---

## Why This Skill Was Built

### The Problem

- Commercial leases are 50–100+ pages of dense legal language
- Critical deadlines (like renewal notices) are buried in different sections
- Manual abstraction is slow, expensive, and people make mistakes
- Different people abstracting the same lease produce inconsistent results

### The Solution

This skill applies a **standardized method** (REIXS-LA-NA-001) that:
- Extracts the same 258 fields every time
- Tags every term with its source (page number, clause reference, exact quote)
- Says "not found" instead of guessing when something's missing
- Flags contradictions instead of silently picking one

---

## Why Not Just Ask a Chatbot to "Summarize This Lease"?

You could paste your lease into a chatbot and get a summary in 30 seconds. So why use this skill instead?

| Concern | Chatbot Summary | This Skill |
|---------|-----------------|------------|
| **Completeness** | Summarizes what seems important — may miss critical terms buried in exhibits or schedules | Extracts all 258 defined fields across 25 sections — nothing skipped |
| **Auditability** | No source references — you can't verify where a summarized term came from | Every fact includes page number, clause reference, and verbatim quote |
| **Consistency** | Different runs may produce different summaries — no standardization | Same 258 fields, same structure, same rules every time |
| **Missing terms** | May not tell you what's absent — silence looks like confirmation | Explicitly marks missing fields as "Not specified" — you know what's not there |
| **Contradictions** | May silently pick one version when clauses conflict | Flags both conflicting values for your review — no silent resolution |
| **Financial accuracy** | May paraphrase or round numbers | Extracts verbatim text first, then provides normalized numeric form separately |
| **Currency** | May assume or misidentify currency | Determines currency from document context — never assumes |
| **Schedule G overrides** | Typically misses special provisions that override main body | Detects and flags all Schedule G overrides that contradict main lease terms |
| **Critical dates** | May capture a few obvious dates | Systematically extracts dates across 10 categories with priority rankings and reminder schedules |
| **Output structure** | Free-form narrative — hard to compare across leases or import into systems | Structured Markdown or JSON — consistent format for comparison, analysis, and system integration |
| **Quality gates** | No validation — errors pass through silently | AutoFail conditions catch critical errors (parties swapped, fabricated terms, wrong currency) before output is delivered |
| **Use case fit** | Good for quick orientation — "What's this lease about?" | Built for business-critical work — audits, transactions, portfolio analysis, compliance |

### When a Chatbot Summary Is Enough

- You're doing initial due diligence and need a quick overview
- You want to understand the general structure of an unfamiliar lease type
- You're preparing for a first meeting and need talking points

### When You Need This Skill

- **Transaction support** — Buying, selling, or assigning lease interests
- **Lease audit** — Verifying obligations, rent calculations, or compliance
- **Portfolio analysis** — Comparing terms across multiple leases
- **Renewal planning** — Identifying all notice deadlines and option rights
- **Legal review preparation** — Flagging issues for counsel before negotiation
- **Data migration** — Importing lease data into management systems
- **Compliance documentation** — Proving what the lease says with full audit trail

### The Bottom Line

> A chatbot gives you a **quick overview**. This skill gives you an **auditable, structured abstract** you can rely on for business-critical decisions.

**Time investment:**
- Chatbot: 30 seconds to generate, unknown time to verify and fill gaps
- This skill: Several minutes to run, output ready for professional use

**Risk:**
- Chatbot: You're trusting the summary — errors may not surface until there's a problem
- This skill: Every fact is traceable — you can verify, audit, and defend the extraction

**Analogy:** A chatbot summary is like a Zillow estimate — useful for a quick sense of value. This skill is like a professional appraisal — documented, defensible, and built for transactions.

---

## Why a Domain Data Dictionary (DDD) Is Required

You might wonder: why not let the AI extract and define terms based on what it sees in each lease? The answer is **data consistency and consolidation**.

### The Problem: Every Lease Defines Terms Differently

Leases are legal documents, not database schemas. Each one defines its own terminology:

| Lease A | Lease B | Lease C | What They All Mean |
|---------|---------|---------|-------------------|
| `Net Rentable Area` | `Net Leasable Area` | `Rentable Square Footage` | The same thing: tenant's rentable space |
| `Base Rent` | `Minimum Rent` | `Contract Rent` | The same thing: guaranteed rent payment |
| `Operating Costs` | `CAM Charges` | `Common Area Expenses` | The same thing: shared building costs |

**If the AI followed each lease's definitions:**
- Lease A → extracts `net_rentable_area` = 100,000 sf
- Lease B → extracts `net_leasable_area` = 100,000 sf  
- Lease C → extracts `rentable_square_footage` = 100,000 sf

**Result:** Three different field names for the same concept. Your database now has three separate columns that can't be queried together. You can't run a report like "total rentable area across my portfolio" because the fields don't match.

### The DDD Solution: Standardized Field Names

The Domain Data Dictionary defines **258 canonical field names** that every lease maps to, regardless of what the lease itself calls them:

| Lease Term | Maps to DDD Field |
|------------|-------------------|
| `Net Rentable Area` | `premises.area.rentableAreaSqFt` |
| `Net Leasable Area` | `premises.area.rentableAreaSqFt` |
| `Rentable Square Footage` | `premises.area.rentableAreaSqFt` |

**Result:** All three leases populate the same field. You can now query, compare, and aggregate across your entire portfolio.

---

### Measurement Standards Matter: The BOMA Example

A CRE practitioner knows that **area measurements depend on the standard used**. This isn't just semantics — it affects the actual numbers:

| Building | Area | Measurement Standard |
|----------|------|---------------------|
| Building A | 100,000 sf | BOMA 1996 |
| Building B | 100,000 sf | BOMA 2010 |
| Building C | 100,000 sf | BOMA 2017 |

**Can you add these together and say you have 300,000 sf?** No — because:

- **BOMA 1996** measures rentable area one way (includes certain common areas, excludes others)
- **BOMA 2010** changed how multi-tenant floors are measured
- **BOMA 2017** introduced new distinctions for mixed-use buildings

**The same physical space** might measure as:
- 100,000 sf under BOMA 1996
- 99,000 sf under BOMA 2010
- 101,000 sf under BOMA 2017

**All three are correct** — they're just using different measurement rules.

### Why This Matters for Data Consolidation

If you're a measurement firm or portfolio manager:

❌ **Wrong:** Adding 100,000 sf (BOMA 1996) + 100,000 sf (BOMA 2010) = 200,000 sf total

✅ **Right:** Keeping them separate with the standard as a qualifier:
- 100,000 sf (BOMA 1996)
- 100,000 sf (BOMA 2010)

The DDD captures the **measurement standard as metadata** alongside the area value:

```json
{
  "premises": {
    "area": {
      "rentableAreaSqFt": 100000,
      "measurementStandard": "ANSI/BOMA Z65.1-1996"
    }
  }
}
```

This ensures:
- You know **which standard** was used for each lease
- You can **filter or group** by measurement standard when aggregating
- You don't accidentally **mix incompatible measurements**

---

### Re-Measurement Clauses: Area Can Change Without Physical Changes

A naive CRE practitioner might think: *"I just need the total net rentable area across my portfolio to calculate total rent receipts — how hard can that be?"*

**The reality:** Many leases contain **operating cost adjustment clauses** that trigger on re-measurements. This means:

- A building is re-measured (often under a newer BOMA standard or due to renovations)
- The net rentable area changes — **without any physical change to the building footprint**
- Rent obligations are recalculated based on the new area
- Your portfolio's total rentable area fluctuates

**Example:**

| Event | Building A | Building B | Portfolio Total |
|-------|------------|------------|-----------------|
| Initial measurement (BOMA 1996) | 100,000 sf | 150,000 sf | 250,000 sf |
| Building A re-measured (BOMA 2017) | 98,500 sf | 150,000 sf | 248,500 sf |
| **Physical change to Building A?** | **No** | **N/A** | **N/A** |

**Why this matters for data systems:**

Without capturing the **measurement date** and **measurement standard** alongside the area value, you can't explain why:
- Rent receipts changed when the building didn't
- Two abstracts of the same lease show different square footage
- Portfolio totals drift over time

The DDD requires capturing:
- `premises.area.rentableAreaSqFt` — the numeric value
- `premises.area.measurementStandard` — which standard was used
- `premises.area.measurementDate` — when the measurement was taken (if stated)

This creates an **audit trail** that explains area changes and protects against data integrity issues when re-measurement clauses are triggered.

---

### The Bottom Line: Why the DDD Exists

| Without DDD | With DDD |
|-------------|----------|
| Every lease uses its own terminology | All leases map to 258 canonical fields |
| Same concept → different field names | Same concept → same field name |
| Can't query across leases | Portfolio-wide queries work |
| Measurement standards lost | Standards captured as metadata |
| Data consolidation is manual and error-prone | Data consolidation is automatic and reliable |

**Analogy:** The DDD is like a universal translator. Every lease "speaks" its own legal language, but the DDD translates everything into a common dialect that your database, reports, and analysis tools can understand.

**For CRE Practitioners:** This means you can:
- Compare rent per square foot across leases without manual reconciliation
- Run portfolio reports that aggregate correctly
- Filter by measurement standard when precision matters
- Import data into lease management systems without field mapping headaches

---

## How to Use It

```
/skill lease-abstraction <path-to-lease>
```

### Options

| Flag | What It Does |
|------|--------------|
| `--json` | Output in JSON format (for importing into other systems) |
| `--criticaldates` | Extract only dates and deadlines |
| `--ics` | Generate a calendar file for Outlook/Google Calendar |
| `--csv` | Generate a spreadsheet file |
| `--all` | Generate all formats (Markdown + ICS + CSV) |

### Examples

```bash
# Full abstract
/skill lease-abstraction /workspace/leases/123_Main_St.pdf

# Critical dates with calendar export
/skill lease-abstraction /workspace/leases/123_Main_St.pdf --criticaldates --ics

# JSON for data import
/skill lease-abstraction /workspace/leases/123_Main_St.pdf --json
```

---

## Step-by-Step Process — What Happens Behind the Scenes

Here's what the skill does, from start to finish:

### Step 1: Find and Load the Rules

Before reading your lease, the skill loads two reference documents:

1. **The Extraction Rules (REIXS)** — Defines *how* to extract terms consistently
2. **The Field Dictionary (DDD)** — Defines *what* 258 fields to extract across 25 sections

**Why this matters:** Just like a paralegal would review a checklist before starting, the skill loads the rules first to ensure consistent, complete extraction every time.

---

### Step 2: Read Your Lease

The skill reads the lease document you specified:
- **PDF, DOCX, MD, or TXT** — handled directly
- **Large files** — processed in sections
- **URLs** — fetched from the web

It identifies whether the lease is **Office** or **Industrial** based on the permitted use and property type.

---

### Step 3: Extract All 25 Sections

The skill works through the lease section by section, extracting terms across all 25 categories:

| Section | What It Captures |
|---------|------------------|
| 1. Document Information | Abstract date, source file |
| 2. Parties | Landlord, tenant, guarantor |
| 3. Premises | Address, area, use |
| 4. Term | Start, end, renewals |
| 5. Rent | Base rent, escalations |
| 6–21 | Deposits, operating costs, repairs, insurance, etc. |
| 22. Critical Dates | All deadlines compiled in one place |
| 23. Financial Obligations | Payment summary |
| 24. Key Issues & Risks | Red flags and favorable terms |
| 25. Notes & Comments | Abstraction notes |

For **each field**, the skill:
- Searches the entire lease for relevant language
- Assigns a **status**:
  - **FACT** — Verbatim from the lease (includes page + clause reference)
  - **INFERENCE** — Derived or interpreted (includes confidence level)
  - **MISSING** — Not found in the lease (marked "Not specified")
  - **CONFLICT** — Contradictory values found (both are listed for your review)

---

### Step 4: Apply Quality Checks

Before finalizing, the skill validates the extraction:

| Check | What It Catches |
|-------|-----------------|
| No fabrication | Every fact traces to source text |
| Parties correct | Landlord and tenant not swapped |
| Financial values complete | Verbatim text + normalized number both present |
| Currency verified | Not assumed — taken from document |
| Schedule G overrides flagged | Special provisions that contradict main body are marked |
| Missing rate under 30% | If too many fields are missing, flagged for human review |
| Dates normalized | All dates in YYYY-MM-DD format |

If any **critical error** is found (parties swapped, wrong currency, fabricated terms), the skill **stops and reports the error** rather than producing unreliable output.

---

### Step 5: Format and Save

The skill produces your output:

**Default (Markdown):**
- 5–10 page executive summary
- Organized by the 25 sections
- Critical dates table
- Financial obligations summary
- Top risks and favorable terms

**JSON (if `--json`):**
- Same data, structured for importing into other systems

**Critical Dates Only (if `--criticaldates`):**
- Markdown table of all deadlines
- ICS calendar file (if `--ics`)
- CSV spreadsheet (if `--csv`)

Output saves to: `Reports/{BuildingAddress}_Lease_Abstract_{Date}.md`

---

### Step 6: Report Back

You receive a summary like this:

```
✅ Lease abstract complete
📋 Type:     Office
👥 Parties:  ABC Properties Inc. / TechCorp Ltd.
📍 Premises: 123 Main Street, Suite 500
📅 Term:     2024-01-01 to 2034-12-31
📄 Output:   Reports/123_Main_Street_Lease_Abstract_2026-05-05.md
⚠️ 2 Schedule G override(s) detected — review flagged provisions.
```

---

## What You Get

| ✅ Included |
|------------|
| Identification of landlord, tenant, and guarantor |
| All 258 fields across 25 sections |
| Normalized dates (YYYY-MM-DD) |
| Schedule G overrides flagged |
| Top risks, favorable terms, and items for review |
| Critical dates calendar with priority rankings (P1 = critical, P4 = low) |
| Output saved to `Reports/` folder |
| Every fact traceable to a specific page and clause |

---

## What the Skill Does NOT Do

| ❌ Does NOT | Why |
|------------|-----|
| Fabricate terms | If a field is missing, it's marked "Not specified" |
| Silently resolve contradictions | If two clauses conflict, both are flagged for your review |
| Assume currency | Uses the currency stated in the document |
| Replace legal or business review | Output should be reviewed by qualified professionals |
| Guess on ambiguous terms | Low-confidence inferences are flagged for human review |
| Process password-protected PDFs | Technical limitation |

---

## Critical Dates Mode

When you use `--criticaldates`, the skill focuses only on **dates and deadlines**:

### Priority Levels

| Priority | Label | Examples | Reminder Schedule |
|----------|-------|----------|-------------------|
| P1 | CRITICAL | Renewal deadlines, lease expiry, termination notices | 365, 270, 180, 120, 90, 60, 30, 14, 7, 3, 1 days before |
| P2 | HIGH | Rent payments, insurance renewals, compliance filings | 180, 90, 60, 30, 14, 7, 1 days before |
| P3 | MEDIUM | Rent reviews, scheduled inspections | 90, 60, 30, 14, 7 days before |
| P4 | LOW | Administrative reviews | 30, 14 days before |

### Output Formats

| Format | Use Case |
|--------|----------|
| Markdown table | Printing or quick reference |
| ICS file | Imports to Outlook, Google Calendar, Apple Calendar |
| CSV file | Spreadsheet analysis or lease management software import |

---

## When to Use This Skill

| Situation | Recommended Mode |
|-----------|------------------|
| New lease acquisition — need full summary | Default |
| Lease audit — verify key terms | Default |
| Portfolio review — compare multiple leases | Default + `--json` |
| Renewal planning — find upcoming deadlines | `--criticaldates --ics` |
| Legal review — identify risky provisions | Default (focus on Section 24) |
| Data migration — import to lease software | `--json` |

---

## Limitations

| Limitation | Details |
|------------|---------|
| Document types | PDF, DOCX, MD, TXT, or URL (password-protected files will fail) |
| Lease types | Optimized for North American Office and Industrial leases |
| Jurisdiction | Assumes North American legal conventions |
| Language | English-language leases only |

---

## Files Produced

| Mode | Output Files |
|------|--------------|
| Default | `Reports/{Address}_Lease_Abstract_{Date}.md` (or `.json`) |
| `--criticaldates` | `Reports/{Address}_Critical_Dates_{Date}.md` |
| `--criticaldates --ics` | Above + `.ics` calendar file |
| `--criticaldates --csv` | Above + `.csv` spreadsheet |
| `--criticaldates --all` | All three formats |

---

## The Bottom Line

This skill turns a 50–100 page legal document into a **5–10 page executive summary** with every fact traceable to a specific page and clause.

It automates the **mechanical work** of lease abstraction so you can focus on the **judgment work** — evaluating risks, negotiating terms, and making business decisions.

---

## Support

For questions about extraction methodology or to report issues, contact the skill author (Reggie Chan) or refer to the REIXS-LA-NA-001 specification in the `references/` folder.
