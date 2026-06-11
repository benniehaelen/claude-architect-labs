#!/usr/bin/env python3
"""Reference solution for the multi-agent research capstone: the composed design.

Run a research session whose sources are thin, under a design that composes the two labs correctly: a
bounded, observable orchestration that escalates when it cannot ground an answer (lab 01), and context
budgeting that pins the load-bearing finding and signals overflow with forked subagents isolated in a
worktree (lab 06). The lead cannot reach the convergence threshold, so it escalates to a human with its
evidence intact and an auditable trace, rather than fabricating an answer.

Usage (dry-run, free, deterministic):
    python capstones/multi-agent-research/solution/run.py
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT))

from shared.harness.model import load_session  # noqa: E402
from shared.harness.research_agent import ResearchDesign, analyze_design, run_research  # noqa: E402


def main() -> int:
    design = ResearchDesign.from_dict(load_session("research_design_good"))
    scenario = load_session("research_scenario")

    print("Design: {0}".format(design.name))
    defects = analyze_design(design)
    print("Design analysis:")
    print("  silent_overflow:                {0}".format(defects["silent_overflow"]))
    print("  fork_only_isolation:            {0}".format(defects["fork_only_isolation"]))
    print("  no_escalation_on_no_convergence:{0}".format(defects["no_escalation_on_no_convergence"]))
    print("  not_observable:                 {0}".format(defects["not_observable"]))

    outcome = run_research(design, scenario)
    print("")
    print("Outcome:")
    print("  status:               {0}".format(outcome.status))
    print("  dropped_load_bearing: {0}".format(outcome.dropped_load_bearing or "none"))
    print("  overflow_signaled:    {0}".format(outcome.overflow_signaled))
    print("  leaked_files:         {0}".format(outcome.leaked_files))
    print("  revertible:           {0}".format(outcome.revertible))
    print("  trace events:         {0}".format(len(outcome.trace)))

    print("")
    print("The sources were too thin to ground an answer, so the lead escalated to a human rather than "
          "fabricating one. The load-bearing finding survived overflow because it was pinned and the "
          "overflow was signaled, the forked subagent's file edits were isolated in a worktree, and the "
          "whole run was traced and auditable.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
