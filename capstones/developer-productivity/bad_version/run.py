#!/usr/bin/env python3
"""Intentionally flawed version for the developer-productivity capstone: the naive environment.

This environment composes the two labs' failure modes instead of their lessons. It uses the sprawling,
ungated dev catalog (lab 02 bad) and the rules-and-memory team config that misses file creation and the
commit (lab 04 bad). It uses the exact same engine as the reference solution (see
shared/harness/dev_environment.py). Only the catalog and the config differ, and that is enough to
compound into a system failure:

1. The unauthorized deploy runs, because the catalog leaves the destructive tool ungated.
2. The new doc violates the house style, because the path-scoped rule does not load on file creation.
3. The commit is unenforced, because the no-secrets convention lives only in memory.

Usage:
    python capstones/developer-productivity/bad_version/run.py
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
    design = load_session("dev_design_bad")
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
    harms = []
    for o in drive_session(actions, catalog, config):
        tool = o.tool or "-"
        gate = o.gate_decision or "-"
        conv = o.convention_outcome or "-"
        flag = ""
        if o.ungated_dangerous_ran:
            flag = "  <== deploy ran ungated"
            harms.append(o.action_id)
        elif o.convention_gap:
            flag = "  <== convention not governed on its event"
            harms.append(o.action_id)
        print("  {0} tool={1:<12} gate={2:<25} convention={3:<10} harm={4}{5}".format(
            o.action_id, tool, gate, conv, o.harm, flag))

    print("")
    print("Harmful outcomes: {0}".format(harms or "none"))
    print("On the naive environment, an unauthorized deploy ran with no gate, a newly created doc slipped "
          "past the house-style rule, and the commit slipped past a memory-only secrets convention. The "
          "two labs' failures compounded into one system failure.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
