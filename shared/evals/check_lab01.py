#!/usr/bin/env python3
"""Eval for lab 01: does the instrumented loop have the observability and governance properties?

This scores the reference solution, not a model. It runs the shared instrumented loop on the
fixtures and asserts the properties that define a passing design:

- On the failure session, every tool failure is recorded (not swallowed), the circuit breaker
  trips, the run escalates, and it stops with a named reason rather than returning an answer.
- On the budget session, the loop stops at the step budget and escalates rather than spinning.
- On the ok session, the loop completes with a grounded answer and no escalation.

A black-box loop cannot pass these checks, which is the point of the lab.

Usage:
    python shared/evals/check_lab01.py
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from shared.harness.agentloop import LoopConfig, Outcome, run_agent_loop  # noqa: E402
from shared.harness.model import ScriptedModel, load_session  # noqa: E402
from shared.mock_services.support_tools import build_registry  # noqa: E402


def run(session_name: str, config: LoopConfig) -> Outcome:
    session = load_session(session_name)
    model = ScriptedModel(session["script"])
    tools = build_registry(session)
    return run_agent_loop(model, tools, session["task"], config)


def expect(label: str, condition: bool, results: list) -> None:
    results.append((label, bool(condition)))


def main() -> int:
    results: list = []
    config = LoopConfig(max_steps=8, max_consecutive_failures=3)

    failure = run("support_session_failure", config)
    expect("failure: status is escalated", failure.status == "escalated", results)
    expect("failure: tool errors are recorded, not swallowed", len(failure.trace.errors) == 3, results)
    expect("failure: circuit breaker tripped and escalated", failure.trace.escalated, results)
    expect("failure: no unfounded answer returned", failure.answer is None, results)
    expect(
        "failure: stop reason is named",
        failure.trace.stop_reason == "escalated_repeated_tool_failure",
        results,
    )

    budget = run("research_session_budget", config)
    expect("budget: status is escalated", budget.status == "escalated", results)
    expect("budget: stopped at step budget", budget.reason == "step_budget_exhausted", results)

    ok = run("support_session_ok", config)
    expect("ok: status is completed", ok.status == "completed", results)
    expect("ok: not escalated", not ok.trace.escalated, results)
    expect("ok: grounded answer returned", bool(ok.answer), results)

    print("Lab 01 eval")
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
