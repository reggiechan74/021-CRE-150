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

---

## Lesson 2 — Nested subagents require distinct prompt delimiters

**Date**: 2026-04-14
**Plugin affected**: `mls-extractor` → `mls-extraction` skill (verification step)

### What happened

The mls-extraction skill's extraction subagent was extended to dispatch its own verification subagent — a sub-subagent that cross-checks the extracted JSON against the source PDF before the Excel formatter runs.

### The problem

The outer subagent prompt already uses `--- BEGIN SUBAGENT PROMPT ---` / `--- END SUBAGENT PROMPT ---` as its boundary. If the inner verifier prompt uses the same delimiter, the boundary is ambiguous — either the agent or the skill parser sees `--- END SUBAGENT PROMPT ---` inside the verifier block and treats it as the end of the outer prompt.

### The fix

Use distinct delimiters at each nesting level:

| Level | Delimiter |
|---|---|
| Primary → Extraction subagent | `--- BEGIN SUBAGENT PROMPT ---` / `--- END SUBAGENT PROMPT ---` |
| Extraction subagent → Verifier subagent | `=== BEGIN VERIFIER PROMPT ===` / `=== END VERIFIER PROMPT ===` |

Any non-colliding delimiter works. The key is that no delimiter at level N appears verbatim inside any prompt at level N+1.

### Rule of thumb

Each nesting level needs its own delimiter style. Three dashes (`---`) for the outermost, three equals (`===`) for one level in, some other marker for deeper nesting (unlikely to be needed in practice).

---

## Lesson 3 — Verify intermediate artifacts before generating downstream outputs

**Date**: 2026-04-14
**Plugin affected**: `mls-extractor` → `mls-extraction` skill

### What happened

The mls-extraction pipeline originally ordered its steps as:

1. Extract JSON
2. Generate Excel from JSON
3. Verify output (file size, field count)

The final verify step checked the Excel file but couldn't efficiently fix the JSON it was derived from — by that point both files existed and a correction required regenerating both.

### The insight

Excel is generated deterministically from JSON. JSON is the single source of truth. If the JSON is wrong, the Excel is wrong. The cheapest fix is to catch JSON errors before the formatter runs, not after.

### The fix

Reorder the pipeline: verify the intermediate artifact immediately after it is produced, before any downstream outputs are generated:

1. Extract JSON → `/tmp/mls_cleaned.json`
2. **Verify JSON against source PDF** (dispatch verifier subagent)
   - On FAIL: re-extract JSON with correction hints, re-verify once
3. Generate Excel from verified JSON
4. Final file-level checks (size, existence)

### Rule of thumb

For any pipeline where one artifact is derived deterministically from another, verify the source artifact before deriving. A single fix at the source is always cheaper than regenerating all downstream outputs. This applies any time the pipeline shape is: **extract → transform → format**.

---

## Lesson 4 — Embed operational lookup tables in subagent prompts; keep narrative methodology in the primary SKILL.md

**Date**: 2026-04-14
**Plugin affected**: `relative-valuation` skill

### What happened

The `relative-valuation` skill has substantial domain knowledge: 25 variables with weights, encoding rules, ranking direction (higher-is-better vs lower-is-better), persona profiles, competitive tier definitions, sensitivity analysis methodology, communication language, and red flags. This content is ~700 lines in the primary SKILL.md.

When writing the subagent dispatch prompt, the question arose: how much of this domain knowledge belongs in the subagent prompt vs. the primary SKILL.md?

### The insight

The subagent and the primary agent serve different roles. The primary agent reads the SKILL.md and understands the full methodology — strategy, communication, what it all means. The subagent never reads the SKILL.md; it only sees the dispatch prompt. It needs to *execute* correctly, not to *understand* the strategy.

Two categories of content emerged:

**Operational lookup tables** — the subagent needs these to execute without hallucination:
- Variable encoding rules (e.g., "Class A = 5, B = 4, C = 3")
- Ranking direction flags (higher = better vs. lower = better)
- Required field names and JSON schema
- Variable inclusion logic (which fields trigger inclusion of optional variables)
- Persona weight overrides

**Narrative methodology** — the primary agent needs this; the subagent does not:
- Strategy frameworks (what competitive tiers mean, how to interpret positioning)
- Communication language ("Top 3", "Competitive", "Disadvantaged")
- Examples and analogues explaining the algorithm
- Red flags and edge case commentary
- Sensitivity analysis interpretation guidance

Putting the full 700 lines into the subagent prompt wastes context and risks confusing the subagent — it may try to follow strategy guidance that contradicts the mechanical execution steps. Omitting the lookup tables causes hallucination on encoding rules.

### The fix

Embed only the operational lookup tables (~150 lines) in the subagent prompt as compact reference tables. Keep the narrative methodology in the primary SKILL.md where the orchestrating agent can use it.

The boundary to draw:

| Goes in the subagent prompt | Stays in primary SKILL.md |
|---|---|
| Variable names, weights, encoding rules | Tier definitions and what they mean |
| Ranking direction for each variable | Communication language and tone |
| JSON field names and required structure | Sensitivity analysis interpretation |
| Optional variable inclusion thresholds | Red flags and edge case guidance |
| Persona weight overrides | Examples and methodology rationale |

### Rule of thumb

When a skill's domain knowledge exceeds ~150 lines, split it by role: embed only the compact reference tables the subagent needs to execute correctly (variables, encodings, schemas), and keep the strategy, language, and interpretation narrative in the primary SKILL.md. The subagent executes; the primary agent understands.

---

## Lesson 5 — Extract minimal dependencies when porting scripts with shared utility imports

**Date**: 2026-04-14
**Plugin affected**: `tenant-credit` — import from `vp-real-estate/Credit_Analysis`

### What happened

`credit_analysis.py` imports two functions from the source repo's shared utilities module:

```python
from Shared_Utils.financial_utils import calculate_financial_ratios, safe_divide
```

The full `Shared_Utils/financial_utils.py` is 600+ lines with top-level imports of `numpy_financial`, `scipy.optimize`, and others. These packages are not guaranteed to be installed in a Cowork plugin environment. Python fails the import at module load time — before any function is called — so even though `credit_analysis.py` only uses `safe_divide` and `calculate_financial_ratios` (which have zero external dependencies), bundling the full shared module would cause an `ImportError` in any environment missing `scipy`.

### The fix

Create a minimal `financial_utils.py` in the plugin's `scripts/` directory containing only the two functions actually used. This:
- Preserves the import name (`from financial_utils import ...`) so `credit_analysis.py` needs only a one-line change
- Eliminates transitive dependency failures from unused parts of the shared module
- Makes the dependency surface explicit and auditable

### Rule of thumb

When porting scripts that import from a source repo's shared utilities, do not bundle the full shared module. Instead:

1. Identify exactly which functions are imported (grep for `from Shared_Utils import` or similar)
2. Check whether those functions have external dependencies (look at the top of the shared file)
3. If the shared module has heavy imports but the needed functions are pure Python, extract only those functions into a minimal local file
4. If the shared module's imports are all standard library or already available, bundle the full file

The boundary to draw: **if `pip install X` would be required for a function that isn't called, don't import that function.**

---

## Lesson 6 — Replace inline runtime scripts with proper script files during plugin import

**Date**: 2026-04-14
**Plugin affected**: `tenant-credit` — import from `vp-real-estate/Credit_Analysis`

### What happened

The original `tenant-credit.md` slash command wrote `run_credit_analysis.py` to disk at runtime using a heredoc inside the skill step:

```bash
cat > run_credit_analysis.py << 'SCRIPT'
import json, sys
from Credit_Analysis.credit_analysis import ...
...
SCRIPT
python3 run_credit_analysis.py credit_inputs/...
```

This pattern was necessary in the source repo because the command ran in a workspace without a persistent scripts directory. In a plugin, the `scripts/` directory exists and is version-controlled.

### The problem with inline heredoc scripts

- **Quoting fragility**: heredoc content containing `$`, backticks, or single quotes requires careful escaping that is easy to get wrong and hard to debug
- **Not version-controlled as code**: the script lives inside a markdown file, invisible to `git diff` as a Python file
- **Not testable in isolation**: you can't run the script directly without executing the full skill
- **Drift risk**: the skill and the script can diverge if only one is updated

### The fix

During plugin import, move any inline runtime scripts to proper files in `${PLUGIN_ROOT}/skills/${PLUGIN_NAME}/scripts/`. Update the skill to call them directly:

```bash
# Instead of: cat > run_credit_analysis.py << 'SCRIPT' ... SCRIPT
cd "<SCRIPTS_DIR>" && python3 run_credit_analysis.py "<input_json>"
```

### Rule of thumb

If the source skill writes a script to disk at runtime, that script belongs in the `scripts/` directory of the imported plugin. Inline scripts are a workaround for repos without a plugin structure — they should not survive the import.
