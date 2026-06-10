#!/usr/bin/env python3
"""Eval for lab 03: is the MCP boundary scoped, gated, and bounded?

This scores the scoped server against the properties that define a passing boundary, and it confirms
the teaching server is genuinely flawed so the contrast is real.

Scoped server (must hold):
- no over-exposed operations, no ungated sensitive operations, no unbounded operations, no
  mislabeled operations.
- a benign read is reachable, runs, and does not flood context.
- an authorized, confirmed deploy runs.
- an unauthorized environment deletion is escalated and does not run.
- a large export is bounded (truncated, not flooding context).

Over-exposed server (must be flawed):
- has over-exposed, ungated sensitive, unbounded, and mislabeled operations.
- runs the unauthorized environment deletion with no gate.
- floods context on the large export.

Usage:
    python shared/evals/check_lab03.py
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from shared.harness.mcp import Request, ServerSpec, analyze_server, drive  # noqa: E402
from shared.harness.model import load_session  # noqa: E402


def expect(label: str, condition: bool, results: list) -> None:
    results.append((label, bool(condition)))


def outcomes_by_id(server: ServerSpec, requests, limit):
    return {outcome.request.id: outcome for outcome in drive(server, requests, limit)}


def main() -> int:
    results: list = []
    boundary = load_session("mcp_boundary")
    limit = boundary["output_token_limit"]
    needed = boundary["needed_capabilities"]
    ops_meta = boundary["ops_meta"]
    requests = [Request(**spec) for spec in boundary["requests"]]

    good = ServerSpec.from_dict(load_session("mcp_server_good"))
    good_defects = analyze_server(good, needed, ops_meta, limit)
    expect("good: no over-exposed operations", not good_defects["over_exposed"], results)
    expect("good: no ungated sensitive operations", not good_defects["ungated_sensitive"], results)
    expect("good: no unbounded operations", not good_defects["unbounded"], results)
    expect("good: no mislabeled operations", not good_defects["mislabeled"], results)

    good_by_id = outcomes_by_id(good, requests, limit)
    expect("good: r1 benign read is reachable, runs, and does not flood context",
           good_by_id["r1"].route.status == "ok"
           and good_by_id["r1"].effect == "read"
           and good_by_id["r1"].executed
           and not good_by_id["r1"].flooded,
           results)
    expect("good: r2 authorized confirmed deploy runs",
           good_by_id["r2"].executed
           and good_by_id["r2"].boundary.reason == "authorized_and_confirmed",
           results)
    expect("good: r3 unauthorized destructive is escalated and does not run",
           (not good_by_id["r3"].executed) and good_by_id["r3"].boundary.decision == "escalate",
           results)
    expect("good: r4 large export is bounded and does not flood context",
           good_by_id["r4"].truncated and not good_by_id["r4"].flooded,
           results)

    bad = ServerSpec.from_dict(load_session("mcp_server_bad"))
    bad_defects = analyze_server(bad, needed, ops_meta, limit)
    expect("bad: has over-exposed operations", bool(bad_defects["over_exposed"]), results)
    expect("bad: has ungated sensitive operations", bool(bad_defects["ungated_sensitive"]), results)
    expect("bad: has unbounded operations", bool(bad_defects["unbounded"]), results)
    expect("bad: has at least one mislabeled operation", bool(bad_defects["mislabeled"]), results)

    bad_by_id = outcomes_by_id(bad, requests, limit)
    expect("bad: r3 unauthorized destructive runs with no gate",
           bad_by_id["r3"].executed
           and bad_by_id["r3"].boundary.reason == "ungated_sensitive_executed",
           results)
    expect("bad: r4 large export floods context",
           bad_by_id["r4"].flooded,
           results)

    print("Lab 03 eval")
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
