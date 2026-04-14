# Changelog — mcda-lease-comparison

## [1.0.0] — 2026-04-14

### Added
- Initial plugin release, refactored from vp-real-estate slash command `/relative-valuation`
- 25-variable MCDA competitive positioning calculator (`relative_valuation_calculator.py`)
- Statistical analysis module with regression, correlation, and outlier detection (`statistics_module.py`)
- Distance calculator using Distancematrix.ai API (`calculate_distances.py`)
- Tenant persona weight loader with 4 built-in profiles: default, 3pl, manufacturing, office (`weights_loader.py`, `weights_config.json`)
- JSON input schema validation (`schema_template.json`, `weights_config_schema.json`)
- Reference documentation: RANKING_METHODOLOGY.md, SCHEMA.md, WEIGHTS_CONFIG_GUIDE.md
- Landscape PDF output support via pandoc + wkhtmltopdf (`pdf_style.css`)
- SKILL.md with Step 0 path resolution for plugin-portable execution
