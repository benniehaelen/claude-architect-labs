#!/usr/bin/env python3
"""Eval for lab 02: is the catalog well designed, and does the gate govern execution?

This scores the reference catalog against the properties that define a passing design, and it
confirms the teaching catalog is genuinely flawed so the contrast is real.

Reference catalog (must hold):
- no overlapping intents, no ungated dangerous tools, no coarse tools, no mislabeled tools.
- a benign read routes to a read-effect tool and runs.
- an authorized, confirmed write runs.
- an unconfirmed write is blocked.
- an unauthorized destructive action is escalated and does not run.

Bad catalog (must be flawed):
- has overlaps, ungated dangerous tools, and at least one coarse tool.
- runs the unauthorized destructive action with no gate.

Usage:
    python shared/evals/check_lab02.py
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from shared.harness.catalog import Catalog, Request, analyze_catalog, drive  # noqa: E402
from shared.harness.model import load_session  # noqa: E402


def expect(label: str, condition: bool, results: list) -> None:
    results.append((label, bool(condition)))


def outcomes_by_id(catalog: Catalog, requests):
    return {outcome.request.id: outcome for outcome in drive(catalog, requests)}


def main() -> int:
    results: list = []
    routing = load_session("catalog_routing")
    intents_meta = routing["intents_meta"]
    requests = [Request(**spec) for spec in routing["requests"]]

    good = Catalog.from_dict(load_session("support_catalog_good"))
    good_defects = analyze_catalog(good, intents_meta)
    expect("good: no overlapping intents", not good_defects["overlaps"], results)
    expect("good: no ungated dangerous tools", not good_defects["ungated_dangerous"], results)
    expect("good: no coarse tools", not good_defects["coarse"], results)
    expect("good: no mislabeled tools", not good_defects["mislabeled"], results)

    good_by_id = outcomes_by_id(good, requests)
    expect("good: r1 benign read runs on a read tool",
           good_by_id["r1"].route.status == "ok"
           and good_by_id["r1"].effect == "read"
           and good_by_id["r1"].executed,
           results)
    expect("good: r2 authorized confirmed write runs",
           good_by_id["r2"].executed and good_by_id["r2"].gate.reason == "authorized_and_confirmed",
           results)
    expect("good: r3 unauthorized destructive is escalated and does not run",
           (not good_by_id["r3"].executed) and good_by_id["r3"].gate.decision == "escalate",
           results)
    expect("good: r4 unconfirmed write is blocked",
           (not good_by_id["r4"].executed) and good_by_id["r4"].gate.reason == "confirmation_required",
           results)

    bad = Catalog.from_dict(load_session("support_catalog_bad"))
    bad_defects = analyze_catalog(bad, intents_meta)
    expect("bad: has overlapping intents", bool(bad_defects["overlaps"]), results)
    expect("bad: has ungated dangerous tools", bool(bad_defects["ungated_dangerous"]), results)
    expect("bad: has at least one coarse tool", bool(bad_defects["coarse"]), results)

    bad_by_id = outcomes_by_id(bad, requests)
    expect("bad: r3 unauthorized destructive runs with no gate",
           bad_by_id["r3"].executed
           and bad_by_id["r3"].gate.reason == "ungated_dangerous_executed",
           results)

    print("Lab 02 eval")
    passed = 0
    for label, ok_flag in results:
        mark = "PASS" if ok_flag else "FAIL"
        print("  [{0}] {1}".format(mark, label))
        passed += 1 if ok_flag else 0

    print("")
    print("{0} of {1} checks passed".format(passed, len(results)))
    return 0 if passed == len(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
