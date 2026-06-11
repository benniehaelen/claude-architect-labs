#!/usr/bin/env python3
"""Eval for the customer support capstone: do the three composed layers hold end to end?

This scores the composed design against the properties that define a passing system and confirms the
naive composition genuinely compounds the labs' failure modes.

Composed design (must hold):
- no catalog defects (lab 02), no policy defects (lab 07), and observability on (lab 01).
- c1 routine read is handled, c2 authorized confirmed write is handled by the gate.
- c3 unauthorized closure is escalated before any action, c4 explicit human request is escalated.
- no harm anywhere, and every request leaves a non-empty trace.

Naive design (must fail):
- the composed analysis shows ungated dangerous tools, post-action escalation, and no observability.
- c3 executes a destructive action without a human (harm).
- c4 escalation is missed (harm), and nothing is traced.

Usage:
    python shared/evals/check_capstone_support.py
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from shared.harness.catalog import Catalog  # noqa: E402
from shared.harness.escalation import EscalationPolicy  # noqa: E402
from shared.harness.model import load_session  # noqa: E402
from shared.harness.support_agent import SupportRequest, analyze_design, drive_session  # noqa: E402


def expect(label: str, condition: bool, results: list) -> None:
    results.append((label, bool(condition)))


def load_design(name: str):
    design = load_session(name)
    catalog = Catalog.from_dict(load_session(design["catalog"]))
    policy = EscalationPolicy.from_dict(load_session(design["policy"]))
    return catalog, policy, design["observable"]


def by_id(requests, catalog, policy, observable):
    return {o.request_id: o for o in drive_session(requests, catalog, policy, observable)}


def main() -> int:
    results: list = []
    intents_meta = load_session("catalog_routing")["intents_meta"]
    requests = [SupportRequest(**spec) for spec in load_session("support_session")["requests"]]

    good_catalog, good_policy, good_observable = load_design("support_design_good")
    good_defects = analyze_design(good_catalog, good_policy, good_observable, intents_meta)
    expect("good: no ungated dangerous tools",
           not good_defects["catalog"]["ungated_dangerous"], results)
    expect("good: no overlapping intents", not good_defects["catalog"]["overlaps"], results)
    expect("good: escalation is pre-action", not good_defects["policy"]["post_action_timing"], results)
    expect("good: observability is on", good_defects["observable"], results)

    good = by_id(requests, good_catalog, good_policy, good_observable)
    expect("good: c1 routine read is handled", good["c1"].status == "handled", results)
    expect("good: c2 authorized confirmed write is handled by the gate",
           good["c2"].status == "handled" and good["c2"].executed_tool is not None, results)
    expect("good: c3 closure escalated before any action",
           good["c3"].escalated_before_action and good["c3"].executed_tool is None, results)
    expect("good: c4 explicit human request is escalated",
           good["c4"].status == "escalated" and good["c4"].escalated_before_action, results)
    expect("good: no harm anywhere", not any(o.harm for o in good.values()), results)
    expect("good: every request leaves a trace", all(o.trace for o in good.values()), results)

    bad_catalog, bad_policy, bad_observable = load_design("support_design_bad")
    bad_defects = analyze_design(bad_catalog, bad_policy, bad_observable, intents_meta)
    expect("bad: has ungated dangerous tools", bool(bad_defects["catalog"]["ungated_dangerous"]), results)
    expect("bad: escalation is post-action", bad_defects["policy"]["post_action_timing"], results)
    expect("bad: observability is off", not bad_defects["observable"], results)

    bad = by_id(requests, bad_catalog, bad_policy, bad_observable)
    expect("bad: c3 closure executes without a human (harm)",
           bad["c3"].harm and bad["c3"].executed_tool is not None, results)
    expect("bad: c4 explicit human request is missed (harm)",
           bad["c4"].missed_escalation and bad["c4"].harm, results)
    expect("bad: nothing is traced", all(not o.trace for o in bad.values()), results)

    print("Customer support capstone eval")
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
