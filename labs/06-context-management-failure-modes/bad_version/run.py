#!/usr/bin/env python3
"""Intentionally flawed version for lab 06: context management that fails silently.

This design is the anti-pattern. It runs through the exact same engine as the reference solution
(see shared/harness/context.py). Nothing about the engine changed. Only the design did, and that is
enough to produce two quiet failures:

1. Silent context drop. The overflow policy evicts the oldest segments to fit, with no signal. An
   early load-bearing detail vanishes and nothing announces it. Budgeting is left to a prompt
   instruction rather than an orchestration limit.
2. Shared filesystem on a fork. The branch relies on forking alone for isolation. Forking branches
   the conversation history but not the filesystem (see VERIFIED.md), so the forked subagent's file
   edits land in the shared working directory and cannot be reverted.

Usage:
    python labs/06-context-management-failure-modes/bad_version/run.py
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT))

from shared.harness.context import SessionDesign, analyze_design, run_session  # noqa: E402
from shared.harness.model import load_session  # noqa: E402


def main() -> int:
    design = SessionDesign.from_dict(load_session("session_design_bad"))
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
    print("  dropped_load_bearing: {0}{1}".format(
        context.dropped_load_bearing or "none",
        "  <== load-bearing detail lost silently" if context.dropped_load_bearing else ""))
    print("  overflow_signaled:    {0}".format(context.overflow_signaled))

    print("")
    print("Branch isolation (edits: {0}):".format(isolation.branch_edits))
    print("  leaked_to_parent:     {0}{1}".format(
        isolation.leaked_to_parent,
        "  <== forked edits visible to the parent" if isolation.leaked_to_parent else ""))
    print("  revertible:           {0}".format(isolation.revertible))

    print("")
    print("A load-bearing detail was dropped with no signal, and the forked branch's edits landed in "
          "the shared working directory with no way to revert. Both failures are silent: the run "
          "looks fine while information and file safety were lost.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
