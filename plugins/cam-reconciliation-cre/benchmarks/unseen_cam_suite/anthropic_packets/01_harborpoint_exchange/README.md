# Harborpoint Exchange — Anthropic Packet

This directory contains only the materials needed for a manual reconciliation review.

Suggested Claude workflow (slash commands from the
`knowledge-work-plugins/finance` plugin — fully namespaced):
1. `/finance:reconciliation opex 2025`
2. `/finance:variance-analysis opex 2025 vs budget`
3. `/finance:financial-statements annual 2025`
4. Ask: `Based on the lease excerpts, what is the corrected FY2025 recoverable operating expense total after removing non-recoverable items?`

Note: the third command is `financial-statements`, not `income-statement`. Pass `annual 2025` and treat the output as an annual recoverable-OpEx roll-up.

Save the combined answer outside this packet as:
`plugins/cam-reconciliation-cre/benchmarks/unseen_cam_suite/results/anthropic/01_harborpoint_exchange/anthropic_output.txt`
