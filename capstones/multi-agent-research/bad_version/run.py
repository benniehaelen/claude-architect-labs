#!/usr/bin/env python3
"""Intentionally flawed version for the multi-agent research capstone: the naive composition.

This design composes the two labs' failure modes instead of their lessons. It returns an answer even
without enough grounding (lab 01 black-box failure), drops accumulated context silently (lab 06 silent
overflow), relies on forking alone to isolate a subagent's file edits (lab 06 forking edge), and
records no trace. It uses the exact same engine as the reference solution (see
shared/harness/research_agent.py). Only the design differs, and that is enough to compound into a
system failure:

1. The lead returns a confident answer despite thin grounding, instead of escalating.
2. The one load-bearing finding is dropped silently on overflow, so the answer is even less grounded
   than it appears.
3. The forked subagent's file edits land in the shared working directory and cannot be reverted.
4. Nothing is traced, so the run cannot be audited.

Usage:
    python capstones/multi-agent-research/bad_version/run.py
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT))

from shared.harness.model import load_session  # noqa: E402
from shared.harness.research_agent import ResearchDesign, analyze_design, run_research  # noqa: E402


def main() -> int:
    design = ResearchDesign.from_dict(load_session("research_design_bad"))
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
    flag_status = "  <== confident but unfounded answer" if outcome.confident_unfounded else ""
    flag_drop = "  <== load-bearing finding lost silently" if outcome.dropped_load_bearing else ""
    flag_leak = "  <== forked edits leaked to the shared tree" if outcome.leaked_files else ""
    print("  status:               {0}{1}".format(outcome.status, flag_status))
    print("  dropped_load_bearing: {0}{1}".format(outcome.dropped_load_bearing or "none", flag_drop))
    print("  overflow_signaled:    {0}".format(outcome.overflow_signaled))
    print("  leaked_files:         {0}{1}".format(outcome.leaked_files, flag_leak))
    print("  revertible:           {0}".format(outcome.revertible))
    print("  trace events:         {0}".format(len(outcome.trace)))

    print("")
    print("On the naive composition, the lead returned a confident answer with no grounding, the one "
          "load-bearing finding was dropped silently, the forked subagent's edits leaked irreversibly, "
          "and nothing was traced. The two labs' failures compounded into one system failure.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
