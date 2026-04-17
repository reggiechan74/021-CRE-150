# Changelog — effective-rent-analyzer

## [1.0.1] — 2026-04-16

### Fixed

- `eff_rent_calculator.py`: add inline `numpy_financial` fallback (`pv` + `pmt`) so calculator runs in environments where the package is not installed (e.g. Claude Cowork). Without this, import failure caused the subagent to silently fabricate NER results.
- `SKILL.md`: acquisition cost formula now explicitly uses `gla_building_sf` (full building GLA) instead of ambiguous `area_sf`, preventing ~3× understatement of breakeven thresholds on no-match system defaults.
- `SKILL.md`: when commission amounts are not stated in the lease document, GTA market defaults are applied (industrial: 5% Y1 / 2.5% subsequent each side) instead of $0, which was overstating NER by ~$1.22/sf on this deal.

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
