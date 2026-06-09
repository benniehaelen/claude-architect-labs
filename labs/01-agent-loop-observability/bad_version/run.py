#!/usr/bin/env python3
"""Intentionally flawed version for lab 01: the black-box agent loop.

This loop is the anti-pattern. Study it, run it on the failure session, and notice what you cannot
learn from its output. It has three defects, each one a thing the reference solution fixes:

1. No structured trace. It prints almost nothing, so after a bad run there is no record of what the
   agent decided or which tools failed. The run is neither explainable nor auditable.
2. It swallows tool failures. A ToolError is caught and treated as an empty result, so the loop
   keeps going as if nothing happened. There is no failure signal for any control to act on.
3. No circuit breaker and no escalation. When tools fail, the loop still reaches the scripted final
   answer and returns it confidently, with no evidence behind it. It fails silently rather than
   safely, and there is no human handoff.

Usage:
    python labs/01-agent-loop-observability/bad_version/run.py --session support_session_failure
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT))

from shared.harness.model import ScriptedModel, load_session  # noqa: E402
from shared.harness.tools import ToolError  # noqa: E402
from shared.mock_services.support_tools import build_registry  # noqa: E402


def run_black_box_loop(model, tools, task, max_steps=8):
    """The flawed loop. Returns only a final string, with no trace and no escalation."""
    history = []
    for _ in range(max_steps):
        decision = model.decide(task, history)
        if decision.action == "final":
            # Returns whatever the model asserts, even if every tool call failed.
            return decision.answer
        try:
            result = tools.call(decision.tool, decision.args or {})
            history.append({"tool": decision.tool, "result": result})
        except ToolError:
            # Defect: the failure is swallowed and treated as an empty result.
            history.append({"tool": decision.tool, "result": {}})
    return "I was unable to complete the request."


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the flawed black-box loop on a session.")
    parser.add_argument("--session", default="support_session_failure")
    parser.add_argument("--max-steps", type=int, default=8)
    args = parser.parse_args()

    session = load_session(args.session)
    model = ScriptedModel(session["script"])
    tools = build_registry(session)

    print("Session: {0}".format(session["name"]))
    print("Task:    {0}".format(session["task"]))
    answer = run_black_box_loop(model, tools, session["task"], max_steps=args.max_steps)

    print("")
    print("Final answer returned to the customer:")
    print("  {0}".format(answer))
    print("")
    print("What you cannot tell from this output: how many tool calls were made, which ones "
          "failed, whether the answer is grounded, or why the loop stopped. On the failure "
          "session this loop hands the customer a confident answer it has no evidence for.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
