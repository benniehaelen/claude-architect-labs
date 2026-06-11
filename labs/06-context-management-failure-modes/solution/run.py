#!/usr/bin/env python3
"""Reference solution for lab 06: context management that fails loudly.

Run a multi-agent research session that overflows the context window and forks a subagent that edits
shared files. The hardened design budgets context with an orchestration limit, pins the load-bearing
segments and summarizes the rest while signaling the overflow, and uses file checkpointing so the
branch's edits are isolated and revertible.

Usage (dry-run, free, deterministic):
    python labs/06-context-management-failure-modes/solution/run.py
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT))

from shared.harness.context import SessionDesign, analyze_design, run_session  # noqa: E402
from shared.harness.model import load_session  # noqa: E402


def main() -> int:
    design = SessionDesign.from_dict(load_session("session_design_good"))
    scenario = load_session("context_scenario")

    print("Design: {0}".format(design.name))
    defects = analyze_design(design)
    print("Design analysis:")
    print("  budget_by_prompt:    {0}".format(defects["budget_by_prompt"]))
    print("  silent_overflow:     {0}".format(defects["silent_overflow"]))
    print("  fork_only_isolation: {0}".format(defects["fork_only_isolation"]))

    result = run_session(design, scenario)
    context = result.context
    isolation = result.isolation

    print("")
    print("Context ({0} of {1} tokens):".format(context.total_tokens, context.limit))
    print("  retained:             {0}".format(context.retained))
    print("  dropped_load_bearing: {0}".format(context.dropped_load_bearing or "none"))
    print("  overflow_signaled:    {0}".format(context.overflow_signaled))

    print("")
    print("Branch isolation (edits: {0}):".format(isolation.branch_edits))
    print("  leaked_to_parent:     {0}".format(isolation.leaked_to_parent))
    print("  revertible:           {0}".format(isolation.revertible))

    print("")
    print("No load-bearing detail was lost and the overflow was signaled, so the failure is loud and "
          "recoverable. The forked branch's file edits were checkpointed, so they are isolated from "
          "the parent and can be reverted, because forking branches the conversation, not the files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
