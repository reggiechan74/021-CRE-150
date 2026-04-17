#!/usr/bin/env python3
"""Gate reconciliation — uniform treatment across bidders.

Motivating bug (Exercise 6 roof-review output): Summit's bonds gate was marked
'needs_clarification' with the note 'RFP mandatory_requirements does not specify
a bid_bond_percent so bid-bond attachment is not strictly a gate' — yet
Heritage, Pinnacle, Lakeside, and Metro were marked 'fail' on the same gate.
Either the gate is applicable (fail the missing ones) or it isn't (clarify the
missing ones) — you cannot treat identical evidence asymmetrically.

Rule enforced: for every gate name, if ANY bidder has result
'needs_clarification', NO bidder may have result 'fail' for that same gate.
A 'fail' under those conditions indicates either:
  (a) the clarification-marked bidder should have been failed, or
  (b) the failed bidder should have been clarification-marked instead.

Human must resolve — this script does not auto-fix.
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

from gate_applicability import is_gate_applicable


def find_inapplicable_fails(bids: list[dict], rfp: dict) -> list[str]:
    """Report any gate result='fail' on a gate that is not applicable per
    the RFP (Task A). These are illegitimate disqualifications."""
    errors: list[str] = []
    for bid in bids:
        bidder_id = bid.get("bidder_id", "<unknown>")
        gates = bid.get("mandatory_gates") or {}
        for gate_name, gate in gates.items():
            if not isinstance(gate, dict):
                continue
            if gate.get("result") != "fail":
                continue
            if not is_gate_applicable(gate_name, rfp):
                errors.append(
                    f"gate '{gate_name}' is not applicable per the RFP but was "
                    f"marked fail for bidder '{bidder_id}'. The RFP does not "
                    "invoke this gate via mandatory_requirements or "
                    "submission_requirements — demote to needs_clarification "
                    "or drop the gate."
                )
    return errors


def find_asymmetries(bids: list[dict]) -> list[str]:
    """Return a list of human-readable error lines describing gate asymmetries."""
    gate_results: dict[str, dict[str, list[str]]] = defaultdict(lambda: defaultdict(list))
    for bid in bids:
        gates = bid.get("mandatory_gates") or {}
        bidder_id = bid.get("bidder_id", "<unknown>")
        for gate_name, gate in gates.items():
            if not isinstance(gate, dict):
                continue
            result = gate.get("result")
            if result in ("pass", "fail", "needs_clarification"):
                gate_results[gate_name][result].append(bidder_id)

    errors: list[str] = []
    for gate_name, by_result in gate_results.items():
        clarifiers = by_result.get("needs_clarification", [])
        failers = by_result.get("fail", [])
        if clarifiers and failers:
            errors.append(
                f"gate '{gate_name}': asymmetric treatment — "
                f"fail={sorted(failers)} vs needs_clarification={sorted(clarifiers)}. "
                "A gate that is clarifiable for one bidder cannot be a fail for another "
                "on the same underlying issue."
            )
    return errors


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", required=True)
    args = ap.parse_args()

    manifest_path = Path(args.manifest)
    with manifest_path.open("r", encoding="utf-8") as f:
        manifest = json.load(f)

    bids = manifest.get("bids") or []
    rfp = manifest.get("rfp") or {}
    errors = find_inapplicable_fails(bids, rfp) + find_asymmetries(bids)
    if errors:
        print("ERROR: gate reconciliation failed — asymmetric treatment detected:", file=sys.stderr)
        for line in errors:
            print(f"  - {line}", file=sys.stderr)
        print(
            "\nResolve by re-running roof-qualification-check with consistent "
            "applicability rules (see qualification-check SKILL.md Compliance Rule).",
            file=sys.stderr,
        )
        return 1

    print(f"Reconciliation OK across {len(bids)} bid(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
