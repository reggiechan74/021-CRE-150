---
title: Exercise 3 — Finance Plugin Test Run Findings
date: 2026-04-15
keywords: [cre-150, exercise-3, test-run, finance-plugin, findings]
lastUpdated: 2026-04-15
category: Training
documentType: Test Report
status: Active
---

# Exercise 3 — Finance Plugin Test Run Findings

**Plugin under test:** `knowledge-work-plugins/finance` v1.2.0 (Anthropic open-source)
**Commands tested:** `/reconciliation`, `/variance-analysis`, `/income-statement`
**Data:** Matheson Gateway Centre FY2025 GL Extract (173 transactions)
**Run date:** 2026-04-15
**Full output:** see `TEST_RUN_OUTPUT.txt`

---

## TL;DR — Exercise Works

The plugin catches **3 of 4 planted discrepancies fully and the 4th correctly-flagged-for-human-review.** It also surfaces **3 false-positive outliers** that are legitimate operating expenses — these are teaching moments, not bugs.

The exercise's pedagogical arc lands: the plugin does the mechanical work in seconds, but every classification decision requires human judgment grounded in lease terms. That's the "before AI / after AI" contrast participants need to see.

---

## Scorecard — Four Planted Discrepancies

### #1 — Property tax MPAC reassessment (+$75,600)

**Status: ✅ CAUGHT — cleanly.**

- `/reconciliation` trend analysis output:
  ```
  Jan–Jun: $35,000/mo
  Jul–Dec: $47,600/mo  ← STEP CHANGE
  ```
- Plugin narrative: *"Pattern consistent with tax reassessment or rate change event. Obtain MPAC Notice or tax rate documentation to confirm driver. Category 2 — legitimate variance if documented, recoverable per lease."*
- Assessment: Plugin identifies the *pattern* but correctly asks the human to *confirm the driver*. Participant has to produce the MPAC notice and confirm the recoverability treatment. Exactly right.

### #2 — Enbridge duplicate invoice ($9,900)

**Status: ✅ CAUGHT — definitively.**

- `/reconciliation` output:
  ```
  >>> DUPLICATE INVOICE DETECTED <<<
      Vendor:     Enbridge Gas Inc.
      Invoice #:  GA-2025-12-4471
      Amount:     $9,900.00
      Postings:
        - 2025-12-22  "Dec 2025 gas — common area + base building"
        - 2025-12-29  "Dec 2025 gas — invoice re-entered in year-end close..."
  ```
- Matched on (vendor, invoice-number, amount) triple. The memo on the duplicate even flags itself.
- Assessment: **This is the canonical "plugin shines" finding.** Deterministic, unambiguous, instant. Before AI a human property accountant might or might not catch this — depending on how closely they compare monthly utility patterns. The plugin catches it with certainty.

### #3 — Janitorial one-time deep clean ($14,500)

**Status: ✅ CAUGHT as outlier — correctly deferred for lease review.**

- `/reconciliation` output:
  ```
  >>> OUTLIER POSTING — investigate <<<
      Date:       2025-10-18
      Vendor:     Clean Pro Services Ltd.
      Amount:     $14,500.00  (typical: $4,200)
      Memo:       Suite 320 move-out deep clean & restoration...
  ```
- The memo essentially confesses to being a tenant-turnover event. `/variance-analysis` explicitly noted: *"Memo indicates tenant-turnover event. Recommend review against lease exclusions before including in recoverable opex."*
- Assessment: Plugin correctly **does not auto-exclude** the item from recoverable opex — it flags for lease review. This is the right behavior. The participant has to read §6.03(c) of the Standard Form Lease and apply the exclusion.

### #4 — Management fee methodology error ($4,000 of the $6,800 variance)

**Status: ⚠️ FLAGGED FOR HUMAN REVIEW — plugin acknowledges its own limitation.**

- `/variance-analysis` output:
  ```
  Budgeted on projected EGI of $2,700,000 × 4% = $108,000
  Actual posted: $114,800
  Implied revenue basis: $2,870,000
  >>> PLUGIN LIMITATION: Cannot determine whether the correct revenue
      basis is Gross Potential Income, Effective Gross Income, or actual
      cash received. Requires reading the Management Agreement §4.1 to
      validate. Flag for human review.
  ```
- Assessment: Plugin **cannot** catch this programmatically — the answer lives in a PDF the plugin doesn't read. But the plugin does something subtler and arguably more valuable: it **back-calculates the implied revenue basis** ($114,800 ÷ 4% = $2,870,000) and surfaces the fact that this differs from the budgeted basis ($2,700,000). That's enough to make a participant go check the Management Agreement.
- This is the **critical pedagogical pivot**: the plugin is honest about what it doesn't know. Participants learn that "plugin didn't flag it" ≠ "no issue exists." Verification of plugin output against source documents is the human's job.

---

## False Positives — Teaching Moments, Not Bugs

The plugin flagged 3 additional outliers that are legitimate, non-recoverable-question operating expenses:

| Outlier | Amount | Plugin says | Reality |
|---------|--------|-------------|---------|
| Dec snow plowing | $11,400 | "Review invoice" | Legitimate — 7 snow events that month |
| LED retrofit (Mar) | $8,900 | "If one-time event, may require reclassification" | Possibly capital — worth discussing |
| Asphalt crack sealing (Sep) | $6,800 | "Review invoice" | Legitimate pre-winter maintenance |

**This is the correct plugin behavior.** If the plugin silently auto-classified these, it would be making lease-reading decisions it has no basis for. By flagging and deferring, it puts the judgment work where it belongs — on the human.

**Teaching opportunity:** The LED retrofit is genuinely ambiguous. Is a $8,900 parking garage LED upgrade a repair (recoverable) or a capital improvement (amortized per §6.04)? That's a real property-management judgment call. Participants should expect to debate it.

---

## Exercise-Design Implications

### What works
- **Duplicate detection** is deterministic and repeatable — reliable anchor finding.
- **Step-change trend analysis** reliably catches the tax reassessment.
- **Outlier detection** surfaces the janitorial anomaly and three honest false positives — richer for discussion than a clean four-catch would be.
- **Plugin self-awareness** on the management fee methodology issue is pedagogically excellent: it demonstrates that the "before AI / after AI" frame is not "AI does everything" — it's "AI does everything mechanical, human does everything judgment."

### Terminology note
The Anthropic Finance plugin is built for **corporate accounting workflows** (GL-to-subledger, bank reconciliation, month-end close), **not CRE CAM reconciliation.** The word "reconciliation" means different things in the two contexts:
- Corporate finance: compare GL to subledger → find posting errors
- CRE property management: compare actual opex to budget → true-up tenant billings

The plugin's reconciliation skill adapts reasonably to the CRE context (the underlying methodology — categorize items as Timing / Adjustments / Investigation — applies) but participants should be briefed on this terminology overlap during facilitation. It's worth 30 seconds at the start of the exercise: *"In your day-to-day, 'CAM reconciliation' means the tenant recovery true-up. The Finance plugin's `/reconciliation` was built for corporate month-end close. The methodology applies — but keep the distinction in mind."*

### Aging-bucket noise
The plugin's aging analysis flagged all items as "90+ days" because we're reconciling FY2025 in April 2026. That's a real artifact of applying a corporate reconciliation methodology (designed for monthly close cycles) to annual CAM reconciliation (designed for year-end true-up). It's worth mentioning once, then setting aside.

### Plugin command reality check
The exercise doc lists `/reconciliation`, `/variance-analysis`, and `/income-statement` as commands. The Finance plugin v1.2.0 exposes all three as slash commands. Confirmed working. The commands are methodology wrappers — they tell Claude to apply the documented skill methodology to whatever data the user provides. Output quality depends on how well the data is structured. **The Exercise 3 dataset is well-structured enough that the plugin produces clean, useful output across all three commands.**

---

## Recommended Facilitator Script Adjustments

Based on this test run, suggest these small tweaks to the exercise facilitation:

1. **Opening terminology note** (~30 sec): Flag the corporate-vs-CRE reconciliation terminology overlap.
2. **After `/reconciliation` runs**: Pause on the 3 false-positive outliers. Ask participants: *"The plugin surfaced these. Should you dig in, or can you wave them through? What would make you confident?"* — this is the judgment muscle the exercise is trying to build.
3. **Management fee moment**: After `/variance-analysis`, before participants look at the Management Agreement PDF, ask: *"The plugin is telling you it doesn't know. What do you need to know?"* — force participants to articulate that they need to read §4.1 of a specific document before moving forward.
4. **Close the loop**: Show the income statement output. Ask: *"If you just hit send on this to the tenant, what would you be wrong about?"* The answer is $28,400 of non-recoverable items embedded in the draft. That's the payoff.

---

## Confidence for Workshop Delivery

**High.** The plugin + dataset combination produces the intended pedagogical arc reliably. The four planted discrepancies are all surfaced (3 definitively, 1 flagged-with-limitation). The false positives are additive, not confusing. The exercise is ready for delivery.

**One pre-workshop todo**: Confirm the plugin marketplace and install flow work on participants' machines. Pre-install the Finance plugin if the workshop room's network can't pull from GitHub during the session.
