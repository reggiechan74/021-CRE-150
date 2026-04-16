# LLM Wiki — Cowork-Friendly Implementation

## Overview

Karpathy's LLM Wiki pattern adapted for Claude Cowork. Build a persistent, self-maintaining knowledge base where Claude writes and maintains the wiki while you curate sources and ask questions.

**Core difference from RAG:** Instead of retrieving from raw documents at query time, Claude incrementally builds a structured wiki that compounds knowledge over time.

---

## Architecture

### Three Layers

```
cre-wiki/
├── schema/
│   └── WIKI-SCHEMA.md      # Tells Claude how the wiki works
├── raw/
│   ├── sources/            # Your immutable source documents
│   └── assets/             # Images, PDFs, attachments
├── wiki/
│   ├── index.md            # Content-oriented catalog of all pages
│   ├── log.md              # Chronological activity log
│   ├── entities/           # People, organizations, properties
│   ├── concepts/           # Topics, methodologies, frameworks
│   ├── sources/            # Summary pages for each ingested source
│   └── synthesis/          # Cross-cutting analysis, comparisons
└── outputs/
    ├── queries/            # Query results filed as pages
    └── presentations/      # Marp slides, reports
```

---

## Schema File (`schema/WIKI-SCHEMA.md`)

This is the configuration file that makes Claude a disciplined wiki maintainer. Save this in your wiki repo and reference it at session start.

```markdown
# WIKI SCHEMA

You are a wiki maintainer, not a chatbot. Your job is to build and maintain a persistent knowledge base in markdown format.

## Wiki Structure

- `wiki/index.md` — Catalog of all pages with links, one-line summaries, metadata. Updated on every ingest.
- `wiki/log.md` — Append-only activity log. Format: `## [YYYY-MM-DD] action | Title`
- `wiki/entities/` — Pages for people, organizations, properties, deals
- `wiki/concepts/` — Pages for topics, methodologies, frameworks
- `wiki/sources/` — Summary pages for each ingested source
- `wiki/synthesis/` — Cross-cutting analysis, comparisons, thesis documents

## Operations

### INGEST
When given a new source:
1. Read and discuss key takeaways with user
2. Write summary page in `wiki/sources/`
3. Update/create entity and concept pages touched by this source
4. Update `wiki/index.md` with new pages
5. Append entry to `wiki/log.md`

### QUERY
When asked a question:
1. Search `wiki/index.md` for relevant pages
2. Read relevant pages and synthesize answer with citations
3. If answer is substantial (comparison, analysis, framework), file it as new page in `wiki/outputs/queries/`

### LINT
When asked to health-check:
1. Find contradictions between pages
2. Flag stale claims superseded by newer sources
3. Identify orphan pages with no inbound links
4. Surface important concepts mentioned but lacking pages
5. Suggest missing cross-references

## Conventions

- All pages use `.md` extension
- Links use `[[Page Name]]` wikilink syntax
- Frontmatter includes: `created`, `updated`, `sources`, `tags`
- Cross-references section at bottom of each page: `## References`
- Log entries use parseable format: `## [2026-04-02] ingest | Article Title`
```

---

## Workflows

### Workflow 1: Ingest a Source

**You:** "Ingest this article into the wiki" [paste article or attach PDF]

**Claude:**
1. Reads source, discusses key takeaways with you
2. Creates `wiki/sources/article-name.md` with structured summary
3. Updates entity pages (e.g., `wiki/entities/yardi.md` if article mentions Yardi)
4. Updates concept pages (e.g., `wiki/concepts/cam-reconciliation.md`)
5. Updates `wiki/index.md` with new/modified pages
6. Appends to `wiki/log.md`: `## [2026-04-15] ingest | Article Title`

**Tip:** Ingest one source at a time with supervision for quality control. Or batch-ingest with less oversight for speed.

---

### Workflow 2: Query the Wiki

**You:** "What's the consensus on CAM reconciliation methodologies across the sources I've read?"

**Claude:**
1. Searches `wiki/index.md` for relevant pages
2. Reads `wiki/concepts/cam-reconciliation.md` and related source summaries
3. Synthesizes answer with citations to specific pages
4. If answer is substantial, creates `wiki/outputs/queries/cam-methodologies-comparison.md`

**Why this compounds:** The query result is now filed and discoverable for future questions. You're building up a library of analyses, not losing them to chat history.

---

### Workflow 3: Lint Pass

**You:** "Run a lint pass on the wiki"

**Claude:**
1. Scans for contradictions (e.g., Page A says X, Page B says not-X)
2. Flags stale claims (older sources superseded by newer data)
3. Identifies orphan pages (no inbound links)
4. Surfaces concepts mentioned frequently but lacking dedicated pages
5. Suggests cross-references to add

**Output:** A report with specific fixes Claude can make in the next pass.

---

## Tools & Integrations

### Obsidian (Recommended)

- **Why:** Best graph view, wikilink support, local markdown files
- **Setup:**
  1. Point Obsidian to your `cre-wiki/` folder
  2. Enable "Core Plugins → Wikilinks"
  3. Set attachment folder to `raw/assets/`
  4. Use Graph View to see wiki structure
- **Workflow:** Claude edits files → Obsidian shows changes in real-time → You browse and navigate

### Search (Optional, for 100+ sources)

**qmd** — Local search engine for markdown with hybrid BM25/vector search:
- CLI mode: Claude shells out to `qmd search "query"`
- MCP mode: Claude uses qmd as native tool
- GitHub: `qmd-org/qmd`

**Simple alternative:** Grep over `wiki/index.md` for small wikis

### Marp for Presentations

- **What:** Markdown-based slide deck format
- **Use:** `wiki/outputs/presentations/q2-review.md`
- **Obsidian plugin:** Marp for Obsidian
- **Claude can:** Generate full slide decks from wiki content

### Dataview (Optional)

- **What:** Query language for markdown frontmatter
- **Use:** Generate dynamic tables, lists, dashboards
- **Example:** "Show all sources ingested in past 30 days tagged 'market-research'"

---

## Getting Started — Step by Step

### Step 1: Initialize the Repo (5 minutes)

```bash
cd ~/reggie-life-plan/01_FINANCIAL/1_TENEBRUS_CAPITAL/Services/Training/Curriculum/CRE/CRE-150/04-materials/
mkdir -p cre-wiki/{schema,raw/{sources,assets},wiki/{entities,concepts,sources,synthesis},outputs/{queries,presentations}}
```

Create `cre-wiki/schema/WIKI-SCHEMA.md` with the schema content above.

### Step 2: First Ingest (10 minutes)

- Open Claude Cowork scoped to `cre-wiki/`
- Say: "I'm starting an LLM wiki for CRE knowledge. Read the schema file first."
- Drop in a source article or PDF you care about
- Say: "Ingest this into the wiki following the schema"
- Watch Claude create the first pages

### Step 3: Browse in Obsidian (2 minutes)

- Open Obsidian, add `cre-wiki/` as vault
- Click through the pages Claude created
- Open Graph View to see connections
- Make any manual adjustments you want

### Step 4: Establish Rhythm

- **Daily or weekly:** Ingest 1-3 sources
- **As needed:** Query the wiki instead of asking fresh questions
- **Monthly:** Run a lint pass

---

## Why This Works for CRE

| CRE Use Case | How Wiki Helps |
|-------------|----------------|
| **Deal pipeline tracking** | Entity pages for each deal, updated as new info arrives |
| **Market research** | Synthesis pages comparing submarkets, compounding over time |
| **Tenant relationships** | Entity pages with history, lease terms, communication log |
| **Vendor management** | Entity pages with performance history, contract terms |
| **Learning CRE** | Concept pages for methodologies (CAM, TI, concessions) that build on each other |
| **Due diligence** | Source summaries for reports, inspections, audits — all cross-referenced |

---

## Tips

1. **Start small:** One wiki per major domain (e.g., `cre-wiki/`, `health-wiki/`, `team-wiki/`)
2. **You curate, Claude files:** Your job is sourcing and direction. Claude's job is bookkeeping.
3. **Query before asking fresh:** Train yourself to search the wiki first, then ask Claude to synthesize
4. **File good answers:** When Claude gives you a great analysis, say "File this as a query output"
5. **Version control:** `git init` the wiki folder. You get history, branching, and backup for free.
6. **Images work:** Download images to `raw/assets/`. Claude can reference them by path (though it must view them separately)

---

## Limitations & Workarounds

| Limitation | Workaround |
|-----------|------------|
| Claude can't read markdown with inline images in one pass | Claude reads text first, then views referenced images separately |
| No native wikilink resolution | Use `[[Page Name]]` syntax; Obsidian resolves; Claude follows by path |
| Large wikis need search | Add `qmd` or simple grep script for Claude to use |
| Cowork session context limits | Wiki persists across sessions; index file enables efficient retrieval |

---

## Next Steps

1. Initialize the folder structure
2. Create the schema file
3. Ingest your first source
4. Open in Obsidian and browse
5. Repeat weekly

The maintenance burden that kills most wikis is near-zero because Claude does the filing, cross-referencing, and updating. Your job is to curate sources, ask good questions, and think about what it means.
