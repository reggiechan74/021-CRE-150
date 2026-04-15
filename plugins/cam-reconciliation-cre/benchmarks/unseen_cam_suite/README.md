# Unseen CAM Benchmark Suite

Ten unseen benchmark properties for comparing Anthropic's finance plugin workflow against `cam-reconciliation-cre`.

## Layout

- `cases/<case_id>/` contains the manual review packet and plugin input files.
- `anthropic_packets/<case_id>/` contains only the user-facing review materials for a cleaner Claude run.
- `gold/<case_id>.json` contains hidden expected totals and scenario metadata.
- `results/ours/` is populated by the local benchmark harness.
- `results/anthropic/` is where you should place Claude Code finance-plugin outputs for scoring.

## Totals Tracked

- `property_level_recoverable_total`: corrected building-level recoverable OpEx after property-level removals such as duplicates, turnover, and management-fee corrections.
- `pooled_cam_total_after_direct_bills`: the shared CAM pool after removing lease-specific direct-bill items such as restaurant grease-trap costs.
- `direct_bill_total`: lease-specific items billed outside the shared CAM pool.

## Manual Anthropic Procedure

For each packet directory, open Claude Code in `anthropic_packets/<case_id>/` and run:

1. `/reconciliation opex 2025`
2. `/variance-analysis opex 2025 vs budget`
3. `/income-statement annual 2025`
4. A follow-up prompt: `Based on the lease excerpts, what is the corrected FY2025 recoverable operating expense total after removing non-recoverable items?`

Save the combined output as:

`plugins/cam-reconciliation-cre/benchmarks/unseen_cam_suite/results/anthropic/<case_id>/anthropic_output.txt`

Then run:

```bash
python3 plugins/cam-reconciliation-cre/scripts/score_anthropic_benchmark.py
```

## Cases

| Case | Property | Notes |
|------|----------|-------|
| 01_harborpoint_exchange | Harborpoint Exchange | duplicate, turnover, mgmt fee, cap, base year, modified gross, specific exclusion, vacancy |
| 02_kingsway_commons | Kingsway Commons | duplicate, mgmt fee, cap, base year, modified gross |
| 03_cedar_ridge_plaza | Cedar Ridge Plaza | turnover, cap, base year, specific exclusion |
| 04_airport_north_hub | Airport North Business Hub | duplicate, mgmt fee, cap, base year, modified gross, vacancy |
| 05_riverfront_market_centre | Riverfront Market Centre | duplicate, turnover, base year, modified gross, specific exclusion, vacancy |
| 06_westmount_professional_campus | Westmount Professional Campus | mgmt fee, cap, base year |
| 07_meadowvale_station_centre | Meadowvale Station Centre | duplicate, turnover, mgmt fee, cap, modified gross, specific exclusion, vacancy |
| 08_lakeshore_atrium | Lakeshore Atrium | cap, base year, modified gross, specific exclusion |
| 09_northline_commerce_court | Northline Commerce Court | duplicate, mgmt fee, cap, base year, vacancy |
| 10_university_gate_centre | University Gate Centre | duplicate, turnover, mgmt fee, cap, base year, modified gross, specific exclusion, vacancy |
