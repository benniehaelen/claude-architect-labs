#!/usr/bin/env python3
"""Eval for lab 06: does context management fail loudly and isolate files correctly?

This scores the loud design against the properties that define a passing system, confirms the silent
design genuinely loses context and file safety, and confirms a summarize-lossy design is weaker
because it drops load-bearing detail without signaling even though it isolates files.

Loud design (must hold):
- no design defects (orchestration budget, signaled overflow, file checkpointing).
- no load-bearing segment is dropped and the overflow is signaled.
- the branch's edits are isolated from the parent and revertible.

Silent design (must fail):
- the analyzer flags prompt budgeting, silent overflow, and fork-only isolation.
- a load-bearing segment is dropped with no signal.
- the branch's edits leak to the parent and are not revertible.

Summarize-lossy design (must be weaker):
- the analyzer flags silent overflow but not fork-only isolation.
- a load-bearing segment loses its detail with no signal, while files stay isolated.

Usage:
    python shared/evals/check_lab06.py
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from shared.harness.context import SessionDesign, analyze_design, run_session  # noqa: E402
from shared.harness.model import load_session  # noqa: E402


def expect(label: str, condition: bool, results: list) -> None:
    results.append((label, bool(condition)))


def main() -> int:
    results: list = []
    scenario = load_session("context_scenario")

    good = SessionDesign.from_dict(load_session("session_design_good"))
    good_defects = analyze_design(good)
    expect("good: no prompt-budget defect", not good_defects["budget_by_prompt"], results)
    expect("good: no silent-overflow defect", not good_defects["silent_overflow"], results)
    expect("good: no fork-only-isolation defect", not good_defects["fork_only_isolation"], results)

    good_result = run_session(good, scenario)
    expect("good: no load-bearing segment dropped",
           not good_result.context.dropped_load_bearing, results)
    expect("good: overflow is signaled", good_result.context.overflow_signaled, results)
    expect("good: branch edits do not leak to the parent",
           not good_result.isolation.leaked_to_parent, results)
    expect("good: branch edits are revertible", good_result.isolation.revertible, results)

    bad = SessionDesign.from_dict(load_session("session_design_bad"))
    bad_defects = analyze_design(bad)
    expect("bad: analyzer flags prompt budgeting", bad_defects["budget_by_prompt"], results)
    expect("bad: analyzer flags silent overflow", bad_defects["silent_overflow"], results)
    expect("bad: analyzer flags fork-only isolation", bad_defects["fork_only_isolation"], results)

    bad_result = run_session(bad, scenario)
    expect("bad: a load-bearing segment is dropped",
           bool(bad_result.context.dropped_load_bearing), results)
    expect("bad: the drop is not signaled", not bad_result.context.overflow_signaled, results)
    expect("bad: branch edits leak to the parent", bad_result.isolation.leaked_to_parent, results)
    expect("bad: branch edits are not revertible", not bad_result.isolation.revertible, results)

    weak = SessionDesign.from_dict(load_session("session_design_summarize"))
    weak_defects = analyze_design(weak)
    expect("weak: analyzer flags silent overflow", weak_defects["silent_overflow"], results)
    expect("weak: analyzer does not flag fork-only isolation",
           not weak_defects["fork_only_isolation"], results)

    weak_result = run_session(weak, scenario)
    expect("weak: loses load-bearing detail without signaling",
           bool(weak_result.context.dropped_load_bearing)
           and not weak_result.context.overflow_signaled,
           results)
    expect("weak: files stay isolated", not weak_result.isolation.leaked_to_parent, results)

    print("Lab 06 eval")
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
