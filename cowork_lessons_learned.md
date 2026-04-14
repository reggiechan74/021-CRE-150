# Claude Cowork — Lessons Learned

---

## Lesson 1 — Subagent dispatch is mandatory for context-heavy pipelines

**Date**: 2026-04-14
**Plugin affected**: `mls-extractor` → `mls-extraction` skill
**Symptom**: Chain of thought went off on a tangent mid-pipeline. Steps 3-4 (formatter execution, verification) failed to execute correctly after PDF vision reads completed.

### What happened

The `mls-extraction` skill was written as a direct instruction set — the primary agent executed all four pipeline steps itself:

1. Read PDF pages via vision (batches of 20 pages)
2. Extract 34-field JSON from page content
3. Run `excel_formatter.py`
4. Verify output

This worked in Claude Code. It broke in Claude Cowork.

### Why it broke

Claude Cowork's primary context window is partially consumed before the skill even starts. Orchestration layers, conversation history, system prompts, and skill routing all take a share of the 200k token budget. By the time the agent finishes reading a 20-page PDF via vision (40K+ tokens of raw visual content) and extracting JSON for 20 properties, there is not enough coherent context remaining to reliably execute Steps 3-4. The chain of thought drifts.

Claude Code gives the agent a full 200k window to itself. Cowork does not.

### The fix

Restructure any pipeline skill that reads large files, processes vision content, or accumulates significant intermediate state. The primary context should only:

1. Parse the user's arguments
2. Resolve file paths and environment variables
3. Dispatch a subagent via the Agent tool
4. Relay the subagent's structured result to the user

The subagent receives a fresh 200k context window and handles all the heavy work.

### Design rules going forward

**Split the work along this boundary:**

| Primary context (thin) | Subagent (full 200k) |
|---|---|
| Argument parsing | PDF / file reading |
| Path resolution | Vision processing |
| Environment variable lookup | Data extraction |
| Subagent dispatch | Script execution |
| Result relay | Verification |

**The subagent prompt must be fully self-contained.** Do not reference environment variables like `${CLAUDE_PLUGIN_ROOT}` — the subagent does not inherit them. Resolve all paths to absolute values in the primary context and embed them in the prompt.

**Use a clear text delimiter for the subagent prompt** — not triple backticks. If the prompt contains code blocks (which it will), nested triple backtick fences will break the prompt boundary:

```
--- BEGIN SUBAGENT PROMPT ---
...prompt content including ```code blocks```...
--- END SUBAGENT PROMPT ---
```

**Define a structured return format.** The subagent should return a compact, parseable block (not a freeform summary) so the primary context can relay results without re-processing large content:

```
EXTRACTION_RESULT
total_properties: N
subject: <address>
excel: Reports/<filename>.xlsx
errors: none
```

**Add a graceful fallback.** If the Agent tool is unavailable in a specific Cowork configuration, the skill should fall back to direct execution rather than failing silently.

### Rule of thumb

If a skill reads files totalling more than ~5 pages, processes vision content, or produces intermediate JSON/data structures before its final step — it needs subagent dispatch in Cowork.

**Secondary trigger — reference files + source doc:**
Page count is necessary but not sufficient. Two or more reference files loaded before the source document is processed creates the same context pressure, even when the source document is short. The pattern to watch for:

1. Read reference file A (~N tokens)
2. Read reference file B (~M tokens)
3. Read source document
4. Extract / transform / format

Steps 1–2 burn context that was already partially consumed by orchestration overhead. By Step 4 the remaining coherent window may be insufficient regardless of the source document's length.

**Trigger checklist** — dispatch a subagent if ANY of these are true:
- Source document > ~5 pages (existing rule)
- Vision content / PDF reads involved (existing rule)
- Two or more reference files are loaded before the source document
- Intermediate JSON or data structures are produced mid-pipeline
