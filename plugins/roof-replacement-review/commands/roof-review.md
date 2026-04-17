---
description: Run the full roof replacement tender review pipeline — extracts RFP and bids, evaluates mandatories, scores bids, flags risks, and writes the recommendation memo
argument-hint: "<rfp.pdf> <bid1.pdf> <bid2.pdf> [bid3.pdf ...] [config=<evaluation_config.yaml>]"
---

# /roof-review

Resolve the plugin root from `CLAUDE_PLUGIN_ROOT` or use:

`/home/reggiechan/021-CRE-150/plugins/roof-replacement-review`

## Pipeline

1. **Wave 1 — extract everything in parallel.** Dispatch `N+1` subagents in a **single message**:
   - **One** subagent invokes the `roof-rfp-extract` skill on the RFP argument. It writes `<rfp-dir>/roof-review-output/manifests/rfp.json`.
   - **For each bid PDF argument**, one subagent invokes the `roof-bid-extract` skill. Each writes `<rfp-dir>/roof-review-output/manifests/bid_<slug>.json`.

   These are RFP-independent (see `skills/roof-bid-extract/SKILL.md` "Inputs") so they legitimately run concurrently. The main thread waits for all wave-1 subagents to return before proceeding.

   Per-bid wave-1 subagent prompt template (substitute `<BID_PATH>`, `<RFP_DIR>`, `<PLUGIN_ROOT>`):

   ```
   You are extracting one roofing bid for the roof-replacement-review pipeline.

   Plugin root: <PLUGIN_ROOT>    (also available as $CLAUDE_PLUGIN_ROOT)
   Bid PDF: <BID_PATH>
   Output directory: <RFP_DIR>/roof-review-output/manifests/

   Run the `roof-bid-extract` skill on this single bid. Write the base bid manifest
   to <RFP_DIR>/roof-review-output/manifests/bid_<slug>.json.

   IMPORTANT: rfp.json is being extracted concurrently by a sibling wave-1 subagent
   and is NOT yet available. Do not attempt to read it. Per `roof-bid-extract`
   SKILL.md §Inputs, this skill does not require the RFP manifest — record bid
   facts verbatim and defer RFP comparison to wave 2.

   Do NOT touch rfp.json or any other bid's manifest. Do NOT evaluate mandatory
   gates or sub-scores — that is wave 2's job.

   Return ONLY:
     - Bidder legal name
     - Bid manifest path
     - Base bid (and HST treatment)
     - Declared exclusions count
     - Any extraction_notes items that need owner follow-up
   ```

2. **Wave 2 — review each bid in parallel.** Once wave 1 completes, dispatch `2 × N` subagents in a **single message** (one qual + one tech per bid):
   - Each **qual subagent** invokes `roof-qualification-check` on one bid and writes `bid_<slug>.qual.json`.
   - Each **tech subagent** invokes `roof-technical-review` on the same bid and writes `bid_<slug>.tech.json`.

   Because the two skills write disjoint sidecar files and have disjoint output ownership (gate names, sub-scores, red-flag categories — see `skills/roof-qualification-check/SKILL.md` "Sidecar Output File" and `skills/roof-technical-review/SKILL.md` "Sidecar Output File"), they can run concurrently without conflict.

   Per-bid wave-2 qual subagent prompt template:

   ```
   You are running qualification review for one roofing bid.

   Plugin root: <PLUGIN_ROOT>
   RFP manifest: <RFP_DIR>/roof-review-output/manifests/rfp.json
   Base bid manifest: <RFP_DIR>/roof-review-output/manifests/bid_<slug>.json

   Run the `roof-qualification-check` skill. Write your output ONLY to:
     <RFP_DIR>/roof-review-output/manifests/bid_<slug>.qual.json

   Do NOT modify the base bid manifest or any other file.

   Return ONLY:
     - Bidder legal name
     - Gate pass / fail / needs-clarification counts
     - Sub-scores (experience_references, qualifications_certifications, schedule)
     - Critical qualification issues
   ```

   Per-bid wave-2 tech subagent prompt template:

   ```
   You are running technical review for one roofing bid.

   Plugin root: <PLUGIN_ROOT>
   RFP manifest: <RFP_DIR>/roof-review-output/manifests/rfp.json
   Base bid manifest: <RFP_DIR>/roof-review-output/manifests/bid_<slug>.json

   Run the `roof-technical-review` skill. Write your output ONLY to:
     <RFP_DIR>/roof-review-output/manifests/bid_<slug>.tech.json

   Do NOT modify the base bid manifest or any other file.

   Return ONLY:
     - Bidder legal name
     - Sub-scores (technical_approach, warranty_materials)
     - Critical/high red flag counts
     - Top 3 technical concerns
   ```

   The main thread waits for all `2 × N` subagents to return before proceeding.

3. **Merge manifests.** Run the merge script with both sidecar globs:

```bash
python3 "$CLAUDE_PLUGIN_ROOT/scripts/normalize.py" \
  --rfp "<rfp-output-dir>/manifests/rfp.json" \
  --bids "<rfp-output-dir>/manifests/bid_*.json" \
  --qual-sidecars "<rfp-output-dir>/manifests/bid_*.qual.json" \
  --tech-sidecars "<rfp-output-dir>/manifests/bid_*.tech.json" \
  --out "<rfp-output-dir>/manifests/tender_manifest.json"
```

The `--bids` glob picks up only `bid_<slug>.json` (base manifests); the sidecar globs match the `.qual.json` and `.tech.json` siblings. `normalize.py` will refuse to merge if the two sidecars collide on a gate/score/rationale key — that indicates a skill wrote outside its ownership boundary and must be fixed before scoring.

4. **Score.** Run the scoring engine. If the user passed `config=<path>` in the arguments, append `--config <path>` to override the RFP's weights and price scoring method:

```bash
python3 "$CLAUDE_PLUGIN_ROOT/scripts/score.py" \
  --manifest "<rfp-output-dir>/manifests/tender_manifest.json" \
  [--config <evaluation_config.yaml>]
```

`score.py` runs `reconcile_gates` (gate applicability + cross-bid symmetry) as its first action and refuses to score if a bidder has been failed on a gate the RFP never invoked, or if identical evidence has been treated asymmetrically across bidders. Fix the flagged bid sidecars by re-running the relevant wave-2 subagent on the offending bid(s), then re-run step 3 and step 4.

Example config at `templates/evaluation_config.yaml`. Common uses: occupied-building weighting (raise schedule + technical), BPS procurement (raise price, use `lowest_compliant` method), heritage/complex roof (raise technical).

5. **Render deliverables (deterministic fast path, then optional LLM polish).**

   Run all three renderer scripts **in parallel** — pure Python, no LLM, typically <1s total. Issue all three `Bash` tool calls in a single message so they execute concurrently (they only read the manifest and write disjoint output files, so there is no ordering or race risk):

```bash
python3 "$CLAUDE_PLUGIN_ROOT/scripts/render_matrix.py" \
  --manifest "<rfp-output-dir>/manifests/tender_manifest.json" \
  --out "<rfp-output-dir>/scoring_matrix.md"
```

```bash
python3 "$CLAUDE_PLUGIN_ROOT/scripts/redflags.py" \
  --manifest "<rfp-output-dir>/manifests/tender_manifest.json" \
  --out "<rfp-output-dir>/redflag_report.md"
```

```bash
python3 "$CLAUDE_PLUGIN_ROOT/scripts/render_memo.py" \
  --manifest "<rfp-output-dir>/manifests/tender_manifest.json" \
  --out "<rfp-output-dir>/recommendation_memo.md"
```

   Then invoke the skills **as refinement passes** over the generated files — not from-scratch regeneration. Issue both refinement subagent calls in a **single message** so they run concurrently:
   - `roof-score-matrix` — read `scoring_matrix.md`, refine wording only if the mechanical output reads awkwardly; leave numbers and structure alone.
   - `roof-recommendation-memo` — read `recommendation_memo.md`, polish §1 Recommendation prose and trim/reorder award conditions in §5 for owner tone; keep §3, §4, §6, §7, §8 as-is unless data is wrong.

   Skip the refinement passes entirely if the user asked for a fast/cheap run, or if the Python output already reads cleanly.

## Output

All artifacts land in `<rfp-dir>/roof-review-output/`:

- `manifests/tender_manifest.json` — complete normalized manifest
- `scoring_matrix.md` — weighted MCDA table
- `redflag_report.md` — mandatory gates + qualitative risks
- `recommendation_memo.md` — executive memo for the owner
- `audit_log.md` — extraction citations and decision provenance

## Summary

After all steps complete, report to the user:

- Number of bids received vs compliant
- Recommended bidder and weighted score
- Price delta between recommended and low compliant bid
- Count of critical/high red flags
- Top three award conditions the owner must resolve before signing
