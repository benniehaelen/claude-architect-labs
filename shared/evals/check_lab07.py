#!/usr/bin/env python3
"""Eval for lab 07: does the escalation policy reach a human at the right time?

This scores the sound policy against the properties that define a passing escalation design, confirms
the weak policy genuinely misses and delays escalations, and confirms a no-route policy is weaker
because escalations it correctly identifies are dropped.

Sound policy (must hold):
- no policy defects (pre-action timing, a defined route, a hold default).
- every must-escalate request escalates, and the routine read is handled.
- nothing is missed, escalated late, or dropped, and escalations are pre-action and routed.

Weak policy (must fail):
- the analyzer flags post-action timing and a fail-open default.
- the out-of-policy and explicit-human requests are missed (handled automatically).
- the high-impact account closure is escalated late (after the action).

No-route policy (must be weaker):
- the analyzer flags no route and a fail-open default but not post-action timing.
- the must-escalate requests are dropped because the escalation cannot be delivered.

Usage:
    python shared/evals/check_lab07.py
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from shared.harness.escalation import EscalationPolicy, Request, analyze_policy, drive  # noqa: E402
from shared.harness.model import load_session  # noqa: E402


def expect(label: str, condition: bool, results: list) -> None:
    results.append((label, bool(condition)))


def by_id(policy, requests):
    return {d.request_id: d for d in drive(policy, requests)}


def main() -> int:
    results: list = []
    data = load_session("escalation_requests")
    requests = [Request(**spec) for spec in data["requests"]]

    good = EscalationPolicy.from_dict(load_session("escalation_policy_good"))
    good_defects = analyze_policy(good)
    expect("good: no post-action-timing defect", not good_defects["post_action_timing"], results)
    expect("good: no no-route defect", not good_defects["no_route"], results)
    expect("good: no fail-open-default defect", not good_defects["fail_open_default"], results)

    good_by_id = by_id(good, requests)
    expect("good: q1 out-of-policy escalates pre-action",
           good_by_id["q1"].action == "escalate" and good_by_id["q1"].timing == "pre_action",
           results)
    expect("good: q2 high-impact escalates pre-action and is not late",
           good_by_id["q2"].action == "escalate" and not good_by_id["q2"].late,
           results)
    expect("good: q3 explicit human request escalates", good_by_id["q3"].action == "escalate", results)
    expect("good: q4 routine read is handled", good_by_id["q4"].action == "handle", results)
    expect("good: nothing missed, late, or dropped",
           not any(d.missed or d.late or d.dropped for d in good_by_id.values()),
           results)

    bad = EscalationPolicy.from_dict(load_session("escalation_policy_bad"))
    bad_defects = analyze_policy(bad)
    expect("bad: analyzer flags post-action timing", bad_defects["post_action_timing"], results)
    expect("bad: analyzer flags fail-open default", bad_defects["fail_open_default"], results)

    bad_by_id = by_id(bad, requests)
    expect("bad: q1 out-of-policy is missed", bad_by_id["q1"].missed, results)
    expect("bad: q3 explicit human request is missed", bad_by_id["q3"].missed, results)
    expect("bad: q2 high-impact is escalated late", bad_by_id["q2"].late, results)

    noroute = EscalationPolicy.from_dict(load_session("escalation_policy_noroute"))
    noroute_defects = analyze_policy(noroute)
    expect("noroute: analyzer flags no route", noroute_defects["no_route"], results)
    expect("noroute: analyzer flags fail-open default", noroute_defects["fail_open_default"], results)
    expect("noroute: analyzer does not flag post-action timing",
           not noroute_defects["post_action_timing"], results)

    noroute_by_id = by_id(noroute, requests)
    expect("noroute: q1 is dropped because escalation cannot be delivered",
           noroute_by_id["q1"].dropped, results)
    expect("noroute: q2 is dropped because escalation cannot be delivered",
           noroute_by_id["q2"].dropped, results)

    print("Lab 07 eval")
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
