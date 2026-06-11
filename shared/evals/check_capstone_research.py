#!/usr/bin/env python3
"""Eval for the multi-agent research capstone: do orchestration and context hold together?

This scores the composed design against the properties that define a passing system and confirms the
naive composition compounds the labs' failure modes.

Composed design (must hold):
- no design defects (loud overflow, worktree isolation, escalates on no convergence, observable).
- with thin sources the lead escalates rather than answering.
- the load-bearing finding survives, the overflow is signaled, the forked edits are isolated and
  revertible, and the run leaves a trace.

Naive design (must fail):
- the analyzer flags silent overflow, fork-only isolation, no escalation, and no observability.
- the lead returns a confident, unfounded answer.
- the load-bearing finding is dropped silently, the forked edits leak, and nothing is traced.

Usage:
    python shared/evals/check_capstone_research.py
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from shared.harness.model import load_session  # noqa: E402
from shared.harness.research_agent import ResearchDesign, analyze_design, run_research  # noqa: E402


def expect(label: str, condition: bool, results: list) -> None:
    results.append((label, bool(condition)))


def main() -> int:
    results: list = []
    scenario = load_session("research_scenario")

    good = ResearchDesign.from_dict(load_session("research_design_good"))
    good_defects = analyze_design(good)
    expect("good: no silent overflow", not good_defects["silent_overflow"], results)
    expect("good: no fork-only isolation", not good_defects["fork_only_isolation"], results)
    expect("good: escalates on no convergence",
           not good_defects["no_escalation_on_no_convergence"], results)
    expect("good: observable", not good_defects["not_observable"], results)

    good_outcome = run_research(good, scenario)
    expect("good: escalates rather than answering", good_outcome.status == "escalated", results)
    expect("good: no load-bearing finding dropped",
           not good_outcome.dropped_load_bearing, results)
    expect("good: overflow is signaled", good_outcome.overflow_signaled, results)
    expect("good: forked edits do not leak", not good_outcome.leaked_files, results)
    expect("good: forked edits are revertible", good_outcome.revertible, results)
    expect("good: run leaves a trace", bool(good_outcome.trace), results)

    bad = ResearchDesign.from_dict(load_session("research_design_bad"))
    bad_defects = analyze_design(bad)
    expect("bad: flags silent overflow", bad_defects["silent_overflow"], results)
    expect("bad: flags fork-only isolation", bad_defects["fork_only_isolation"], results)
    expect("bad: flags no escalation", bad_defects["no_escalation_on_no_convergence"], results)
    expect("bad: flags no observability", bad_defects["not_observable"], results)

    bad_outcome = run_research(bad, scenario)
    expect("bad: returns a confident unfounded answer",
           bad_outcome.status == "answered_unfounded" and bad_outcome.confident_unfounded, results)
    expect("bad: load-bearing finding dropped silently",
           bool(bad_outcome.dropped_load_bearing) and not bad_outcome.overflow_signaled, results)
    expect("bad: forked edits leak", bad_outcome.leaked_files, results)
    expect("bad: nothing is traced", not bad_outcome.trace, results)

    print("Multi-agent research capstone eval")
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
