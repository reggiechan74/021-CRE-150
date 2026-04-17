# Changelog — effective-rent-analyzer

## [1.0.0] — 2026-04-16

### Added

- Initial plugin import from `vp-real-estate` repository
- `eff_rent_calculator.py` — BAF/NER/GER/NPV/breakeven calculator implementing the Ponzi Rental Rate framework
- `landlord_investment_parameters.json` — landlord database with 4 sample entities (2 REITs, 1 institutional, 1 private)
- `landlord_investment_parameters_schema.json` — JSON schema for database validation
- `baf_input_example.json` — example 10-year graduated industrial lease input
- SKILL.md with subagent dispatch pattern (Cowork Lesson 1) for context-heavy PDF pipelines
- Landlord matching: exact name → alias → property-specific → system defaults
- Verification step (Lesson 3): JSON input verified against source lease before calculator runs
- References: `BAF_INPUT_FORMAT.md`, `LANDLORD_INVESTMENT_PARAMETERS.md`

### Sources

- SKILL.md: `reggiechan74/vp-real-estate/.claude/skills/effective-rent-analyzer/SKILL.md`
- Command: `reggiechan74/vp-real-estate/.claude/commands/Financial_Analysis/effective-rent.md`
- Scripts: `reggiechan74/vp-real-estate/Eff_Rent_Calculator/`
