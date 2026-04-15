# roof-replacement-review

Evaluates roofing contractor tender submissions against an owner's RFP for Ontario roof replacement projects. Supports commercial (OBC Part 3) low-slope membrane systems and residential (OBC Part 9) steep-slope systems. Produces three owner-side deliverables from a single pipeline: a scored evaluation matrix, a red-flag report, and a recommendation memo.

## Scope

- **Landlord/owner-side** review of contractor bids — not contractor bid prep, not tenant-side
- **Ontario jurisdiction** — OBC, WSIB, Skilled Trades Ontario, O. Reg. 297/13 working-at-heights, CRCA standards
- **Commercial and residential** roofs — materials dictionaries and code references branch on building classification
- **Structured evaluation** — mandatory pass/fail gates + weighted MCDA rated criteria

## Commands

- `/roof-review <rfp.pdf> <bid1.pdf> <bid2.pdf> ...` — full pipeline, produces all three deliverables
- `/roof-extract-rfp <rfp.pdf>` — parse the owner's RFP into the normalized schema
- `/roof-extract-bid <rfp.pdf> <bid.pdf>` — parse a single bid against the RFP schema
- `/roof-redflags <manifest.json>` — red-flag report only (pass/fail gates + qualitative risks)
- `/roof-memo <manifest.json>` — recommendation memo only

## Skills

| Skill | Purpose |
|---|---|
| `roof-rfp-extract` | Parse owner's RFP PDF: scope, specs, mandatories, evaluation weights |
| `roof-bid-extract` | Parse a contractor bid PDF against the RFP schema |
| `roof-technical-review` | Technical compliance — materials, warranty adequacy, OBC compliance, manufacturer certification |
| `roof-qualification-check` | Mandatory gates — WSIB, CGL, bonding, WAH training, references, financial capacity |
| `roof-score-matrix` | Weighted MCDA ranking across bidders, configurable weights |
| `roof-recommendation-memo` | Synthesize scored matrix and red flags into an executive memo |

## Inputs

- **RFP PDF** — the owner's tender document
- **Bid PDFs** — one per contractor submission

Optional:

- `evaluation_config.yaml` — override the default weighting (Price 45 / Technical 15 / Experience 15 / Warranty 10 / Schedule 5 / Qualifications 10)

## Outputs

Running `/roof-review` writes to `<rfp-dir>/roof-review-output/`:

- `manifests/tender_manifest.json` — normalized RFP + bids + scores + red flags
- `scoring_matrix.md` — weighted MCDA table across bidders
- `redflag_report.md` — mandatory gate results and qualitative risks with severity
- `recommendation_memo.md` — executive memo for owner/board
- `audit_log.md` — extraction citations and decision provenance

## Domain Knowledge

Fixed reference material the skills cite from (not LLM memory):

- `fixtures/domain_knowledge/01_ontario_roofing_codes.md` — OBC Part 3/9, WAH, environmental
- `fixtures/domain_knowledge/02_roofing_materials_warranties.md` — membrane/shingle specs, manufacturer certification programs
- `fixtures/domain_knowledge/03_tender_evaluation_methodology.md` — CCDC-23, MCDA weighting patterns, bid pathologies
- `fixtures/domain_knowledge/04_contractor_qualification.md` — WSIB, CGL, Skilled Trades Ontario, financial capacity

## Scoring Method

Two-stage evaluation:

**Stage 1 — Mandatory gates (pass/fail).** Any `fail` = bid non-compliant and excluded from ranking. Default gates: WSIB clearance, CGL ≥ $5M with owner as additional insured, bid bond, performance/L&M bond commitment, WAH training, addenda acknowledgment, non-collusion declaration.

**Stage 2 — Weighted rated criteria.** Price scored via `(lowest_compliant_bid / this_bid) × price_weight`. Other criteria scored 0–100 against rubrics. Weighted total determines rank.

Weights shift based on project type:
- Occupied commercial — schedule + technical approach weight higher
- Heritage/complex — technical weight higher
- Straightforward re-roof — price weight higher
- BPS/public — price-heaviest (BPS Procurement Directive)

## Red-Flag Categories

Severity: `critical` (excludes bid) / `high` (negotiate or reject) / `medium` (clarify) / `low` (note)

Categories monitored: pricing (unbalanced, low-bid trap), scope (vague exclusions, allowance manipulation), warranty (prorated language, uncertified installer), materials (mis-matched components, inadequate thickness), qualifications (expired WSIB, insufficient COI), schedule (unrealistic), insurance (named insured mismatch), safety (no fall-protection plan), subcontracting (unnamed subs), references (unresponsive, affiliated).

## Setup

```bash
python3 plugins/roof-replacement-review/scripts/bootstrap.py
```

## License

See `LICENSE`.
