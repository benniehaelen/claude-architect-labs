#!/usr/bin/env python3
"""Reference solution for lab 01: the instrumented agent loop.

Run a session fixture through the shared instrumented loop and print the structured trace plus the
outcome. The trace makes every decision explainable, and the circuit breaker turns a failing run
into a governed escalation rather than a confident wrong answer.

Usage (dry-run, free, deterministic):
    python labs/01-agent-loop-observability/solution/run.py --session support_session_failure
    python labs/01-agent-loop-observability/solution/run.py --session support_session_ok
    python labs/01-agent-loop-observability/solution/run.py --session research_session_budget
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT))

from shared.harness.agentloop import LoopConfig, run_agent_loop  # noqa: E402
from shared.harness.events import Event  # noqa: E402
from shared.harness.model import ScriptedModel, load_session  # noqa: E402
from shared.mock_services.support_tools import build_registry  # noqa: E402


def print_event(event: Event) -> None:
    detail = {key: value for key, value in event.data.items() if value is not None}
    print("  [{0:>2}] step {1} {2:<14} {3}".format(event.seq, event.step, event.type.value, detail))


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the instrumented agent loop on a session.")
    parser.add_argument("--session", default="support_session_failure")
    parser.add_argument("--max-steps", type=int, default=8)
    parser.add_argument("--max-consecutive-failures", type=int, default=3)
    args = parser.parse_args()

    session = load_session(args.session)
    model = ScriptedModel(session["script"])
    tools = build_registry(session)
    config = LoopConfig(
        max_steps=args.max_steps,
        max_consecutive_failures=args.max_consecutive_failures,
    )

    print("Session: {0}".format(session["name"]))
    print("Task:    {0}".format(session["task"]))
    print("Trace:")
    outcome = run_agent_loop(model, tools, session["task"], config, on_event=print_event)

    print("")
    print("Outcome:")
    print("  status:      {0}".format(outcome.status))
    print("  reason:      {0}".format(outcome.reason))
    print("  answer:      {0}".format(outcome.answer))
    print("  tool_calls:  {0}".format(len(outcome.trace.tool_calls)))
    print("  tool_errors: {0}".format(len(outcome.trace.errors)))
    print("  escalated:   {0}".format(outcome.trace.escalated))
    print("  stop_reason: {0}".format(outcome.trace.stop_reason))

    if outcome.status == "escalated":
        print("")
        print("The run failed safely: it stopped with a named reason and handed off to "
              "{0} instead of asserting an unfounded answer.".format(config.escalation_target))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
