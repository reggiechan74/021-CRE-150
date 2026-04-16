# LLM Wiki — Real-World Implementation for Messy Folders

## The Problem

Karpathy's LLM Wiki assumes a clean, purpose-built repository. Reality looks different:

- `~/Downloads` — 2,000 files, mixed types, no structure, images named `image(47).png`
- `~/Documents` — Decades of accumulated work, duplicate folders, inconsistent naming
- File types: PDFs, Word docs, Excel sheets, PowerPoint decks, images, random zips
- No existing markdown, no wikilinks, no schema

**Question:** How do you build an LLM wiki when your source material is a disaster?

**Answer:** You don't start by organizing. You start by indexing what exists, then let Claude build the wiki alongside the mess.

---

## Claude Cowork's File System Model

### How Cowork Accesses Files

1. **Scoped permissions:** Cowork can only read/write to folders you explicitly permit
2. **Default write scope:** Current working directory + subdirectories
3. **Default read scope:** Broader system access (with blocked directories)
4. **Per-session:** You grant access when starting a Cowork task

### What This Means for Wiki Building

| Constraint | Implication |
|------------|-------------|
| Cowork needs explicit folder access | You must choose: wiki folder OR messy source folder (or both) |
| Cowork writes to permitted directory | Wiki must live in a folder Cowork can write to |
| Cowork reads permitted directory + subdirectories | Source files must be in or under a permitted folder |
| Each session starts fresh | Wiki persistence happens via files, not session memory |

### Cowork's File Handling Capabilities

| File Type | Can Read | Can Write | Notes |
|-----------|----------|-----------|-------|
| `.md`, `.txt` | ✅ Full | ✅ Full | Native format |
| `.pdf` | ✅ Full | ❌ No | Read via document tool |
| `.docx` | ✅ Full | ✅ Yes | Via built-in tool |
| `.xlsx` | ✅ Full | ✅ Yes | Via built-in tool |
| `.pptx` | ✅ Full | ✅ Yes | Via built-in tool |
| `.png`, `.jpg` | ✅ Via image analysis | ❌ No | Describes content, cannot embed in markdown |
| `.csv` | ✅ Full | ✅ Full | Treated as text |
| `.zip` | ⚠️ Can list contents | ❌ No | Cannot extract without Python |

**Key limitation:** Cowork cannot directly embed images, charts, or binary content into markdown. It can describe them and reference paths, but inline images require manual handling.

---

## Adapted Architecture for Messy Folders

### Option 1: Wiki Beside the Mess (Recommended for First-Timers)

```
~/Documents/
├── [existing mess - untouched]
└── cre-wiki/              # NEW: Clean wiki folder
    ├── schema/
    │   └── WIKI-SCHEMA.md
    ├── raw/
    │   ├── sources/       # Symlinks or copies of key sources
    │   └── assets/
    ├── wiki/
    │   ├── index.md
    │   ├── log.md
    │   ├── entities/
    │   ├── concepts/
    │   └── sources/
    └── outputs/
```

**Workflow:**
1. Cowork task scoped to `cre-wiki/` folder only
2. When you want to ingest a source from the mess:
   - Copy or symlink it to `cre-wiki/raw/sources/`
   - Claude reads from the copy, creates wiki pages
3. Original mess remains untouched
4. Wiki grows cleanly alongside chaos

**Pros:**
- Zero risk to existing files
- Clean separation from day one
- Easy to version control (`git init cre-wiki/`)
- Easy to back up (one folder)

**Cons:**
- Requires copying sources you care about
- Two folders to navigate (but Obsidian can watch both)

---

### Option 2: Wiki Inside the Mess (For Advanced Users)

```
~/Documents/
└── [existing mess continues]
    └── cre-wiki/          # NEW: Wiki lives inside Documents
        ├── schema/
        ├── raw/
        ├── wiki/
        └── outputs/
```

**Workflow:**
1. Cowork task scoped to entire `~/Documents/` folder
2. Claude can read any file in Documents
3. Wiki pages reference sources by their existing paths
4. Claude creates summary pages without moving originals

**Pros:**
- No copying required
- Sources stay where they are
- Single folder for everything

**Cons:**
- Higher risk (Claude can modify anything in Documents)
- Harder to version control (entire Documents folder)
- Index paths are longer and more fragile
- Requires more careful prompting

---

### Option 3: Hybrid — Indexed Mess with Clean Wiki

```
~/Documents/                    ~/cre-wiki/
├── [existing mess]             ├── schema/
│   ├── deals/                  ├── wiki/
│   ├── market-research/        │   ├── index.md (references ~/Documents paths)
│   └── financials/             │   ├── log.md
│                               │   ├── entities/
Downloads/                      │   └── sources/ (summary pages with paths)
└── [scattered sources]         └── outputs/
```

**Workflow:**
1. Wiki folder is separate and clean
2. Index file contains paths to sources wherever they live
3. Claude reads sources from original locations (requires multi-folder access)
4. Summary pages reference source paths, not copies

**Example index entry:**
```markdown
## Sources

- [[Q3-2025-Market-Report]] — CBRE GTA office market summary
  - Path: `~/Downloads/cbre-q3-2025-market-report.pdf`
  - Ingested: 2026-04-15
  - Tags: market-research, office, gta
```

**Pros:**
- No copying
- Sources stay in natural habitat
- Clean wiki structure
- Easy to trace back to originals

**Cons:**
- Requires granting Cowork access to multiple folders
- Broken links if sources move
- More complex setup

---

## Implementation: Step by Step

### Phase 1: Survey the Mess (10 minutes)

**Goal:** Understand what you're working with before building anything.

**Steps:**

1. Open Cowork, start task scoped to your chosen folder (`~/Documents` or `~/Downloads`)

2. Ask Claude to audit the folder:
   ```
   Survey this folder and tell me:
   1. Total file count by type (PDFs, Word docs, Excel, PowerPoint, images, other)
   2. Folder structure (list top-level folders and their file counts)
   3. Identify any existing structure that looks intentional
   4. Flag obvious duplicates (same filename, similar sizes)
   5. Estimate: what % of files are CRE-related vs. personal/other?
   ```

3. Review the output. Decide:
   - Is this folder worth making the wiki home? (Option 2)
   - Or should the wiki live separately? (Option 1 or 3)

**Expected output:** A markdown report you can file as `wiki/outputs/queries/folder-audit-[date].md`

---

### Phase 2: Initialize the Wiki (15 minutes)

**Goal:** Create the wiki structure in your chosen location.

**If Option 1 (separate folder):**
```bash
mkdir -p ~/Documents/cre-wiki/{schema,raw/{sources,assets},wiki/{entities,concepts,sources,synthesis},outputs/{queries,presentations}}
```

**If Option 2 (inside mess):**
```bash
mkdir -p ~/Documents/cre-wiki/{schema,raw/{sources,assets},wiki/{entities,concepts,sources,synthesis},outputs/{queries,presentations}}
```

**If Option 3 (hybrid):**
```bash
mkdir -p ~/cre-wiki/{schema,wiki/{entities,concepts,sources,synthesis},outputs/{queries,presentations}}
```

**Then:**

1. Create `schema/WIKI-SCHEMA.md` (use the schema from the original implementation doc)

2. Create initial `wiki/index.md`:
   ```markdown
   # Wiki Index
   
   Last updated: [today's date]
   Total sources: 0
   Total pages: 0
   
   ## Categories
   
   ### Entities
   *(empty)*
   
   ### Concepts
   *(empty)*
   
   ### Sources
   *(empty)*
   
   ### Synthesis
   *(empty)*
   ```

3. Create `wiki/log.md`:
   ```markdown
   # Activity Log
   
   ## [YYYY-MM-DD] init | Wiki initialized
   ```

---

### Phase 3: First Ingest from the Mess (20 minutes)

**Goal:** Prove the workflow works with one real source from your existing files.

**Steps:**

1. Pick ONE important source from the mess:
   - A market report PDF
   - A key lease document
   - A financial analysis Excel file
   - Something you actually care about

2. **If Option 1:** Copy it to `cre-wiki/raw/sources/`

3. Start Cowork task scoped to the wiki folder (and source folder if Option 3)

4. Say:
   ```
   I'm building a CRE knowledge wiki. First, read the schema file at [path].
   
   Now ingest this source: [path to your chosen file]
   
   Follow the ingest workflow: discuss takeaways, create summary page, 
   update index and log.
   ```

5. Watch Claude:
   - Read the source
   - Discuss key points with you
   - Create `wiki/sources/[name].md` with structured summary
   - Create or update entity/concept pages
   - Update `wiki/index.md`
   - Append to `wiki/log.md`

6. Open the wiki folder in Obsidian. Browse what Claude created.

---

### Phase 4: Batch Ingest Strategy (Optional, 30+ minutes)

**Goal:** Rapidly build the wiki by processing multiple sources.

**When to use:** After you've validated the workflow with one source.

**Approach A: Supervised Batch (Recommended)**
```
For each of these 5 files:
1. Read and summarize key takeaways
2. Ask me if anything surprising or important
3. Create the wiki pages
4. Update index and log

Files:
- [list paths]
```

**Approach B: Unsupervised Batch (Use with Caution)**
```
Ingest all files in this folder following the schema:
- [folder path]

Process each file:
1. Create summary page
2. Update/create entity and concept pages
3. Update index and log

Flag for my review if:
- You find contradictions between sources
- A source references something important that lacks a wiki page
- You're uncertain about categorization

Then give me a summary report of what was created.
```

**Warning:** Unsupervised batch ingest of 20+ files can create 100+ wiki pages. Review carefully before committing.

---

## Handling Specific File Types

### PDFs (Market Reports, Lease Documents, Appraisals)

**Cowork can:**
- Read full text
- Extract tables (via Python tool)
- Describe charts and images
- Create structured summaries

**Workflow:**
```
Read this PDF and create a wiki source summary with:
1. Document metadata (title, date, author, source firm)
2. Executive summary (3-5 bullet points)
3. Key data points (extract any tables with market stats)
4. Describe any important charts or diagrams
5. Tag with relevant entities and concepts
```

**Limitation:** Inline images in the PDF cannot be embedded in markdown. Claude describes them and notes page numbers.

---

### Excel Files (Rent Rolls, Operating Statements, Comps)

**Cowork can:**
- Read all sheets
- Perform calculations
- Create summaries and analysis
- Write new Excel files

**Workflow:**
```
Analyze this Excel file and create a wiki source summary with:
1. File structure (list sheets and their purposes)
2. Key metrics (extract totals, averages, notable figures)
3. Data quality notes (gaps, inconsistencies, formatting issues)
4. Create entity pages for any properties, tenants, or deals referenced
5. Link to relevant concepts (e.g., CAM reconciliation, NOI calculation)
```

**Pro tip:** Ask Claude to create a cleaned/normalized version in `raw/assets/` if the original is messy.

---

### Word Documents (Leases, Proposals, Memos)

**Cowork can:**
- Read full document
- Extract clauses or sections
- Compare against other documents
- Create structured summaries

**Workflow:**
```
Review this [lease/proposal/memo] and create a wiki source summary with:
1. Document type and parties involved
2. Key terms or provisions (extract specific clauses)
3. Risk flags or unusual terms
4. Create entity pages for all parties
5. Link to relevant legal and financial concepts
```

---

### PowerPoint Decks (Pitch Books, Market Updates, Board Decks)

**Cowork can:**
- Read slide content
- Extract key messages
- Describe charts and diagrams
- Create summary documents

**Workflow:**
```
Review this presentation and create a wiki source summary with:
1. Presentation context (audience, date, purpose)
2. Slide-by-slide key points (condensed)
3. Extract any data-heavy slides into tables
4. Describe important diagrams or flowcharts
5. Create entity/concept pages for topics covered
```

**Output:** Consider asking Claude to create a Marp presentation in `outputs/presentations/` that captures the essence in a more portable format.

---

### Images (Site Photos, Maps, Floor Plans)

**Cowork can:**
- View and describe images
- Extract text from diagrams (limited)
- Reference by path

**Workflow:**
```
View this image and create a wiki entry with:
1. Description of what the image shows
2. Any text or labels visible
3. Context (why this image matters)
4. Link to related entities or concepts
5. Note the file path for future reference
```

**Limitation:** Claude cannot embed the image in markdown. It creates a text description and notes the path. You must manually add `![[image.png]]` in Obsidian if you want it displayed.

---

### Random Zips (Archived Projects, Old Deals)

**Cowork cannot directly extract zips.** Use this workflow:

1. **Manual step:** Extract the zip to a temporary folder

2. **Then:**
   ```
   Survey this extracted folder:
   1. List all files and their types
   2. Identify which files are worth ingesting
   3. Flag anything sensitive or personal that shouldn't go in the wiki
   
   Then ingest the relevant files following the schema.
   ```

---

## The Index Strategy for Messy Folders

### Problem

Your `index.md` needs to reference sources that live in chaotic locations:
- `~/Downloads/cbre-market-report-q3-2025-final-v2.pdf`
- `~/Documents/2019/old-deals/123-Main-St/lease-drafts/tenant-redline.docx`
- `~/Desktop/rent-roll-UPDATED.xlsx`

### Solution: Canonical Paths in Index

**Format each index entry with:**
```markdown
### [[CBRE Q3 2025 Market Report]]

**Path:** `~/Downloads/cbre-market-report-q3-2025-final-v2.pdf`  
**Ingested:** 2026-04-15  
**Summary:** Quarterly GTA office market report with vacancy, asking rates, submarket breakdown  
**Tags:** market-research, office, gta, cbre  
**Wiki Page:** `wiki/sources/cbre-q3-2025-market.md`  
**Status:** ⚠️ Source in Downloads (may move)
```

**Key practices:**

1. **Record the exact path** Claude used to read the file
2. **Note the status** — is this a stable location or temporary?
3. **Create a canonical name** — use `[[CBRE Q3 2025 Market Report]]` not the filename
4. **Link to the wiki summary page** — that's the stable reference

### Migration Strategy

When you notice a source in a temporary location (Downloads, Desktop):

1. **Move it** to a stable location (`~/Documents/cre-sources/` or similar)
2. **Ask Claude to update the index:**
   ```
   Update the wiki index: CBRE Q3 2025 Market Report has moved from 
   ~/Downloads/... to ~/Documents/cre-sources/...
   
   Update the path in the index entry and note the migration date in the log.
   ```

Over time, your important sources migrate to stable homes. The wiki tracks the moves.

---

## Obsidian Integration for Messy Folders

### Setup

1. **Add wiki folder as vault:**
   - Open Obsidian
   - "Open folder as vault"
   - Select `~/Documents/cre-wiki/` (or wherever your wiki lives)

2. **Optional: Add source folder as secondary vault:**
   - Use Obsidian's "Open another vault" feature
   - Select `~/Documents/` or wherever your sources live
   - Now you can navigate both from one Obsidian instance

3. **Enable core plugins:**
   - Wikilinks (for `[[link]]` syntax)
   - Backlinks (to see what references each page)
   - Graph view (to visualize connections)

4. **Configure attachment folder:**
   - Settings → Files & Links
   - Set "Attachment folder path" to `raw/assets/`
   - This is where dragged-in images will go

### Workflow

- **Browse:** Use Obsidian to navigate wiki pages
- **Graph view:** See how entities and concepts connect
- **Backlinks:** Click "Backlinks" pane to see what references current page
- **Quick switcher:** `Ctrl/Cmd+O` to jump between pages
- **Live preview:** Watch wiki pages update as Claude edits them

---

## Common Pitfalls and Solutions

### Pitfall 1: Claude Modifies Source Files

**Problem:** You asked Claude to organize your Downloads folder, and it deleted/moved things you wanted to keep.

**Solution:**
- Be explicit: "Read from this folder but do NOT modify, move, or delete any files"
- Use Option 1 (separate wiki folder) with copies of sources
- Or use read-only permissions if your Cowork version supports them

---

### Pitfall 2: Wiki Becomes Outdated

**Problem:** Sources move or change, but the index still points to old paths.

**Solution:**
- Run monthly lint passes: "Scan the wiki index and flag any source paths that no longer exist"
- Use the log to track migrations: "Update index and log entry when a source moves"
- Consider a `wiki/health.md` page with last-verified dates for major sources

---

### Pitfall 3: Too Many Orphan Pages

**Problem:** Claude creates entity/concept pages that nothing links to.

**Solution:**
- Lint pass: "Find all wiki pages with zero inbound links and suggest consolidations"
- Use Obsidian's graph view to spot orphans visually
- Ask Claude to add missing cross-references: "For each orphan page, find 2-3 related pages and add bidirectional links"

---

### Pitfall 4: Session Context Limits

**Problem:** Large wiki + long conversation = Claude forgets early context.

**Solution:**
- The index file is your anchor: "Search wiki/index.md for relevant pages before answering"
- Start fresh sessions for major tasks: "New session: ingest these 3 sources"
- File query outputs: Substantial answers become wiki pages, reducing need to re-ask

---

### Pitfall 5: Image Handling

**Problem:** Claude describes images but can't embed them in markdown.

**Solution:**
- Manual step: After Claude creates the page, open in Obsidian and drag in the image
- Or ask Claude to note the path clearly: "Include `Image path: [full-path]` at top of page"
- Future: Use an MCP connector for asset management if your workflow is image-heavy

---

## Scaling Up

### When to Split into Multiple Wikis

| Signal | Action |
|--------|--------|
| Wiki has 500+ sources | Consider splitting by domain (e.g., `cre-wiki/`, `market-wiki/`, `legal-wiki/`) |
| Index file is 1000+ lines | Create category-specific indexes (`wiki/index-entities.md`, `wiki/index-concepts.md`) |
| Search becomes slow | Add `qmd` search tool or grep-based script |
| Multiple people need access | Set up as git repo, use branches for major updates |

### When to Add Tooling

| Need | Tool |
|------|------|
| "Find all pages mentioning X" | Grep over `wiki/` folder |
| "What's changed this week?" | `git log` or scan `log.md` |
| "Show me all orphan pages" | Obsidian graph view or lint pass |
| "Search across 200+ sources" | Install `qmd` local search engine |
| "Generate a dashboard" | Dataview plugin with YAML frontmatter queries |

---

## Quick Start Checklist

**Day 1 (1 hour):**
- [ ] Survey your messy folder (Phase 1)
- [ ] Choose architecture option (1, 2, or 3)
- [ ] Create folder structure (Phase 2)
- [ ] Create schema file
- [ ] Ingest one source (Phase 3)
- [ ] Open in Obsidian and browse

**Week 1 (15 min/day):**
- [ ] Ingest 2-3 more sources
- [ ] Ask one query and file the output
- [ ] Review graph view, note connections forming

**Month 1 (1 hour total):**
- [ ] Run first lint pass
- [ ] Migrate any sources from temporary locations
- [ ] Review: what's working, what needs adjustment?
- [ ] Decide: continue as-is or split/expand?

---

## The Bottom Line

Karpathy's vision assumes you're starting fresh. Reality means starting with a decade of accumulated digital chaos.

**The adapted approach:**

1. Don't organize first — index what exists
2. Build the wiki alongside the mess, not instead of it
3. Let Claude do the bookkeeping (filing, cross-referencing, updating)
4. You do the curation (choosing sources, asking questions, making judgment calls)
5. Over time, important sources naturally migrate to stable homes
6. The wiki becomes the structured layer on top of chaos — not a replacement for it

Your messy folder is not a blocker. It's your first source.
