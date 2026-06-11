#!/usr/bin/env python3
"""Reference solution for the developer-productivity capstone: the composed environment.

Drive a session of developer actions through an environment that composes the two labs correctly: the
deliberate dev tool catalog with a permission gate (lab 02) and the layered team configuration that
governs conventions on every event (lab 04). Tests run, the source edit and the new doc are held to the
house style at the right event, the unauthorized deploy is escalated rather than run, and the commit is
governed by the no-secrets control.

Usage (dry-run, free, deterministic):
    python capstones/developer-productivity/solution/run.py
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT))

from shared.harness.catalog import Catalog  # noqa: E402
from shared.harness.config import TeamConfig  # noqa: E402
from shared.harness.dev_environment import DevAction, analyze_environment, drive_session  # noqa: E402
from shared.harness.model import load_session  # noqa: E402


def main() -> int:
    design = load_session("dev_design_good")
    catalog = Catalog.from_dict(load_session(design["catalog"]))
    config = TeamConfig.from_dict(load_session(design["config"]))
    session = load_session("dev_session")
    intents_meta = session["dev_intents_meta"]
    actions = [DevAction(**spec) for spec in session["actions"]]

    print("Design: {0}".format(design["name"]))
    defects = analyze_environment(catalog, config, intents_meta)
    print("Composed analysis:")
    print("  catalog.ungated_dangerous: {0}".format(defects["catalog"]["ungated_dangerous"] or "none"))
    print("  catalog.overlaps:          {0}".format(list(defects["catalog"]["overlaps"]) or "none"))
    print("  config.guide_for_must:     {0}".format(defects["config"]["guide_for_must"] or "none"))
    print("  config.uncovered_binding:  {0}".format(defects["config"]["uncovered_binding"] or "none"))

    print("")
    print("Actions:")
    for o in drive_session(actions, catalog, config):
        tool = o.tool or "-"
        gate = o.gate_decision or "-"
        conv = o.convention_outcome or "-"
        print("  {0} tool={1:<12} gate={2:<9} convention={3:<10} harm={4}".format(
            o.action_id, tool, gate, conv, o.harm))

    print("")
    print("The tools were gated where it mattered and the conventions were governed on every event. The "
          "unauthorized deploy was escalated rather than run, the new doc was held to the house style at "
          "creation, and the commit was governed by the no-secrets control. No harm.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
