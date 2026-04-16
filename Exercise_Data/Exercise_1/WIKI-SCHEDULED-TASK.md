# Wiki Maintenance — Scheduled Task Prompt

## Overview

Use this prompt with Claude Cowork's **Scheduling** feature to automatically maintain your LLM wiki. Set it to run weekly or bi-weekly.

Terminology note: **Scheduling** is the Cowork feature that runs prompts on a recurring cron. **Dispatch** is a separate feature for phone↔desktop remote control. This template uses Scheduling only — Dispatch is not required.

**What this task does:**
- Scans source folders for new files to ingest
- Updates the wiki index with new/modified sources
- Runs health checks (contradictions, orphans, stale content)
- Generates a maintenance report

**What this task does NOT do:**
- Ingest new sources automatically (flags them for your review)
- Delete or modify existing wiki pages without approval
- Move source files from temporary locations

---

## The Prompt

Copy this entire prompt into a Cowork scheduled task. Adjust the paths and frequency to match your setup.

```markdown
# WIKI MAINTENANCE SCHEDULED TASK

You are a wiki maintainer. Run this task every Monday at 8:00 AM.

## Context

I have an LLM wiki at: `~/Documents/cre-wiki/`

My source files live in these folders (scan these for new/changed files):
- `~/Documents/cre-sources/` (stable source folder)
- `~/Downloads/` (temporary — flag important CRE-related files to migrate)
- `~/Documents/market-research/` (secondary source folder)

The wiki structure:
- `wiki/index.md` — Master catalog of all pages
- `wiki/log.md` — Activity log
- `wiki/sources/` — Summary pages for each source
- `wiki/entities/` — Entity pages (people, orgs, properties, deals)
- `wiki/concepts/` — Concept pages (methodologies, frameworks)
- `wiki/synthesis/` — Cross-cutting analysis
- `wiki/health.md` — Health status and last-check dates

## Your Tasks

### Task 1: Scan for New Sources (10 minutes)

Scan the three source folders listed above. Look for:
- PDF files created or modified in the past 7 days
- Excel files with CRE-related names (rent roll, operating statement, CAM, NOI, comp, lease, etc.)
- Word documents with CRE-related names (lease, proposal, memo, agreement, etc.)
- PowerPoint files with CRE-related names (market, pitch, deck, presentation, etc.)

For each file found:
1. Check if it already exists in `wiki/index.md` (search by filename and path)
2. If NOT in index: Add to "Pending Ingest" list
3. If already indexed but modified: Add to "Updated Sources" list

Output format:
```
## New Sources Found (Pending Ingest)

| File | Path | Type | Date Modified | Priority |
|------|------|------|---------------|----------|
| [filename] | [full path] | PDF/Excel/Word/PPT | [date] | HIGH/MED/LOW |

Priority guide:
- HIGH: Market reports, financial statements, lease documents, appraisal reports
- MED: Meeting notes, correspondence, internal memos
- LOW: Drafts, outdated materials, non-CRE files
```

**Do NOT ingest automatically.** Present the list for my review. I will tell you which to ingest.

---

### Task 2: Update Index Health (5 minutes)

Read `wiki/index.md` and verify all source paths still exist.

For each source entry:
1. Check if the file path still exists on disk
2. If file is missing: Flag as "⚠️ FILE NOT FOUND"
3. If file is in a temporary location (Downloads, Desktop): Flag as "📦 MIGRATE TO STABLE LOCATION"

Update the index:
- Add status emoji next to each flagged entry
- Create a "Migration Needed" section at bottom listing all temporary sources

Output format:
```
## Index Health Report

- Total sources indexed: [count]
- Files not found: [count]
- Files in temporary locations: [count]
- Healthy sources: [count]

### Files Not Found (Action Required)
[List with paths]

### Files to Migrate (Action Recommended)
[List with current and suggested target paths]
```

---

### Task 3: Run Lint Pass (10 minutes)

Read all wiki pages in `wiki/entities/`, `wiki/concepts/`, and `wiki/synthesis/`.

Check for:

**1. Contradictions:**
- Find claims that conflict between pages (e.g., Page A says "vacancy is 8.5%" and Page B says "vacancy is 12%")
- Check dates — newer sources should supersede older claims
- Flag with: "⚠️ CONTRADICTION: [brief description]"

**2. Orphan Pages:**
- Find pages with zero inbound links (no other wiki pages link to them)
- For each orphan: Suggest 2-3 pages that SHOULD link to it
- Flag with: "🔗 ORPHAN: Consider linking from [page1], [page2]"

**3. Missing Cross-References:**
- Find pages that mention entities/concepts without linking
- Example: Page mentions "CBRE" but doesn't link to `[[CBRE]]` entity page
- Flag with: "🔗 ADD LINK: [page] should link to [[entity/concept]]"

**4. Stale Content:**
- Find pages that reference outdated data (e.g., "Q2 2025" when Q3 2025 data exists)
- Flag with: "📅 STALE: [description], update with [newer source]"

**5. Concepts Without Pages:**
- Find frequently-mentioned terms that lack dedicated concept pages
- Example: "capitalization rate" mentioned 10 times but no `[[Capitalization Rate]]` page
- Flag with: "📄 CREATE PAGE: [[Term]] mentioned [N] times across [list pages]"

Output format:
```
## Lint Pass Results

### Contradictions Found
| Page | Issue | Resolution Needed |
|------|-------|-------------------|
| [page] | [description] | [what to check/update] |

### Orphan Pages
| Page | Suggested Links From |
|------|---------------------|
| [page] | [page1], [page2] |

### Missing Cross-References
| Page | Should Link To |
|------|----------------|
| [page] | [[entity/concept]] |

### Stale Content
| Page | Issue | Newer Source Available |
|------|-------|------------------------|
| [page] | [description] | [source name] |

### Concepts Needing Pages
| Term | Mention Count | Where Mentioned |
|------|---------------|-----------------|
| [term] | [N] | [page1], [page2] |
```

---

### Task 4: Update Health Page (2 minutes)

Update `wiki/health.md` with:

```markdown
# Wiki Health Status

## Last Maintenance
- Date: [today's date]
- Maintainer: Claude (scheduled task)

## Current Status
- Total sources: [count]
- Total entity pages: [count]
- Total concept pages: [count]
- Total synthesis pages: [count]
- Orphan pages: [count]
- Contradictions to resolve: [count]
- Files needing migration: [count]

## Action Items
[List from Tasks 1-3]

## Maintenance History
| Date | Action | Notes |
|------|--------|-------|
| [date] | Weekly maintenance | [brief summary] |
```

Append today's entry to the maintenance history table.

---

### Task 5: Generate Maintenance Report (3 minutes)

Create a new file: `outputs/queries/maintenance-report-[YYYY-MM-DD].md`

Format:
```markdown
# Wiki Maintenance Report — [Date]

## Executive Summary
[2-3 sentences: overall wiki health, critical issues, recommended actions]

## This Week's Activity
- New sources found: [count]
- Sources ingested: [count]
- Pages created: [count]
- Pages updated: [count]
- Contradictions resolved: [count]

## Critical Issues (Review Required)
[List high-priority items from Tasks 1-3]

## Recommended Actions
1. [action] — Priority: HIGH/MED/LOW
2. [action] — Priority: HIGH/MED/LOW
3. [action] — Priority: HIGH/MED/LOW

## Appendix: Full Findings
[Copy output from Tasks 1-3]
```

---

## Output Instructions

After completing all 5 tasks:

1. **Present me with a summary:**
   ```
   ## Wiki Maintenance Complete — [Date]
   
   ### Quick Summary
   - [1-line health status]
   - [number] action items requiring your review
   
   ### What I Did
   - Scanned [N] source folders
   - Found [N] new sources pending ingest
   - Flagged [N] index health issues
   - Found [N] contradictions, [N] orphans, [N] missing links
   
   ### What I Need From You
   1. Review new sources list — tell me which to ingest
   2. Decide on file migrations (Downloads → stable folder)
   3. Approve contradiction resolutions
   4. [any other specific decisions needed]
   
   ### Files Created/Updated
   - `wiki/health.md` — Updated with status
   - `outputs/queries/maintenance-report-[date].md` — Full report
   - `wiki/index.md` — Updated with flags
   - [any other changes]
   ```

2. **Wait for my instructions** before:
   - Ingesting any new sources
   - Resolving contradictions
   - Migrating files
   - Creating new concept pages

3. **If you find nothing new or broken:**
   - Still create the maintenance report
   - Note "No issues found — wiki is healthy"
   - Update the health page with current counts

---

## Scheduling Notes

**Frequency:** Run every Monday at 8:00 AM

**If the task fails** (e.g., folder structure changed, file permissions issue):
- Leave a note in `wiki/log.md`: `## [YYYY-MM-DD] ⚠️ scheduled-maintenance-failed | [error description]`
- Send me a notification: "Scheduled wiki maintenance failed. Error: [description]. Please check folder permissions and re-run."

**If the wiki grows large (200+ sources):**
- Task may take 20-30 minutes instead of 15
- Consider splitting into two tasks:
  - Task A: Scan + Index Health (weekly)
  - Task B: Lint Pass (monthly)

---

## First Run Setup

Before scheduling this task recurring:

1. **Test run once:** "Run the wiki maintenance task now as a one-time test"
2. **Review output:** Confirm the format and findings make sense
3. **Adjust paths:** Update source folder paths if needed
4. **Then schedule:** "Set this as a recurring task for every Monday at 8 AM"

---

## Customization Hooks

**If you want automatic ingest (advanced):**

Add this to Task 1:
```
AUTO-INGEST MODE: If a new source is in `~/Documents/cre-sources/` (stable folder) 
and is tagged LOW priority, ingest it automatically without waiting for review.
Create the summary page, update index and log, and note in the report what was auto-ingested.

Still flag HIGH and MED priority sources for manual review.
```

**If you want monthly deep cleans:**

Add this as Task 6 (run on first Monday of each month only):
```
## Task 6: Monthly Deep Clean (First Monday Only)

1. Read every wiki page and verify:
   - All wikilinks resolve to existing pages
   - All frontmatter is complete (created, updated, tags, sources)
   - All "References" sections are populated

2. Consolidate duplicate or near-duplicate pages:
   - Find pages with overlapping content
   - Suggest mergers: "Merge [[Page A]] and [[Page B]] → [[Unified Page Name]]"

3. Graph view analysis:
   - Identify top 5 hub pages (most inbound links)
   - Identify bottom 5 pages (fewest inbound links)
   - Suggest ways to improve connectivity

4. Archive old content:
   - Find pages not updated in 90+ days
   - Flag for review: "📅 ARCHIVE CANDIDATE: [page] — last updated [date]"
```

---

## Troubleshooting

**Problem:** Task reports "no sources found" but you know files exist

**Fix:** Check folder paths in the Context section. Cowork may not have permission to scan those folders. Either:
- Move sources into folders Cowork can access
- Grant Cowork broader read permissions at session start

---

**Problem:** Task takes too long (30+ minutes)

**Fix:** Reduce scope:
- Scan fewer folders (remove Downloads if it's huge)
- Run lint pass monthly instead of weekly
- Add file count limits: "Scan max 50 new files per run"

---

**Problem:** Too many false positives on "new sources"

**Fix:** Tighten the scan criteria:
- Add date filter: "Only files modified in past 7 days"
- Add name patterns: "Only files containing: market, lease, rent, CAM, NOI, comp, appraisal"
- Exclude patterns: "Ignore files containing: draft, temp, copy, old"

---

## Bottom Line

This scheduled task turns wiki maintenance from a manual chore into an automated health check. You review the findings and make judgment calls. Claude does the scanning, checking, and bookkeeping.

Set it up once. Adjust the prompts based on your first few runs. Then let it run in the background while you focus on using the wiki.
```

---

## How to Set Up the Scheduled Task

### Step 1: Test Run First (15 minutes)

1. Open Claude Cowork
2. Start task scoped to your wiki folder: `~/Documents/cre-wiki/`
3. Also grant read access to your source folders
4. Paste the prompt above
5. Say: "Run this wiki maintenance task now as a one-time test"
6. Review the output — adjust paths and criteria as needed

### Step 2: Schedule as Recurring Task (2 minutes)

1. In Cowork, open **Scheduling** and create a new scheduled task
2. **Task prompt:** Paste the full prompt above
3. **Frequency:** Weekly
4. **Day/Time:** Monday at 8:00 AM (or your preference)
5. Confirm folder permissions include:
   - Wiki folder (`~/Documents/cre-wiki/`)
   - Source folders (Documents, Downloads, etc.)

### Step 3: First Few Weeks — Monitor and Adjust

**Week 1:**
- Review the maintenance report when it arrives
- Note: Did it find the right files? Too many false positives?
- Adjust the prompt's scan criteria if needed

**Week 2-3:**
- Confirm the task is running reliably
- Check `wiki/health.md` is being updated
- Verify no permission errors

**Week 4+:**
- Task should be "set and forget"
- Review reports monthly instead of weekly
- Consider reducing frequency if wiki is stable

---

## Expected Output Example

After each run, you'll receive something like:

```
## Wiki Maintenance Complete — 2026-04-21

### Quick Summary
Wiki is healthy with 23 sources. 3 action items requiring your review.

### What I Did
- Scanned 3 source folders
- Found 2 new sources pending ingest
- Flagged 1 index health issue (file in Downloads)
- Found 0 contradictions, 2 orphans, 5 missing links

### What I Need From You
1. Review 2 new sources — tell me which to ingest:
   - CBRE Q1 2026 Market Report (HIGH priority)
   - Tenant correspondence re: Unit 204 renewal (MED priority)
2. Migrate CBRE report from Downloads → cre-sources/
3. Approve linking orphan pages to relevant entities

### Files Created/Updated
- `wiki/health.md` — Updated with status
- `outputs/queries/maintenance-report-2026-04-21.md` — Full report
- `wiki/index.md` — Added flags for 2 pending sources
```

You review, reply with decisions, and Claude executes — all from your phone if you want.

---

## Why This Works

| Manual Wiki Maintenance | Scheduled Task Maintenance |
|------------------------|---------------------------|
| You remember to check for new files | Claude scans automatically |
| You manually verify paths still exist | Claude checks every link weekly |
| You spot-check for contradictions | Claude systematically compares all pages |
| You update health status when you remember | Health page updated every run |
| Maintenance burden grows with wiki size | Task scales — same prompt at 20 or 200 sources |

The wiki stays healthy because the maintenance is automated. Your job is curation and judgment — not bookkeeping.
