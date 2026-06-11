#!/usr/bin/env python3
"""Intentionally flawed version for lab 04: the rules-and-memory configuration.

This configuration is the anti-pattern. It runs through the exact same enforcement engine as the
reference solution (see shared/harness/config.py). Nothing about the engine changed. Only the
configuration did, and that is enough to produce three failures:

1. Write-time gap. The house-style must-hold is enforced only by a path-scoped rule. A rule does not
   load when Claude creates a matching file (see VERIFIED.md), so the new file is unenforced. The same
   convention is merely guided on an edit, where the rule does load.
2. A must-hold in memory only. The no-secrets convention lives in CLAUDE.md memory, which cannot
   block a commit. At the binding event the convention is unenforced.
3. Over-controlled preference. A preference is governed by a blocking hook, paying for a control
   where a guide would do.

Usage:
    python labs/04-claude-code-team-workflow/bad_version/run.py
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT))

from shared.harness.config import Event, TeamConfig, analyze_config, drive  # noqa: E402
from shared.harness.model import load_session  # noqa: E402


def main() -> int:
    config = TeamConfig.from_dict(load_session("team_config_bad"))
    stream = load_session("config_events")
    events = [Event(**spec) for spec in stream["events"]]

    print("Configuration: {0}".format(config.name))
    defects = analyze_config(config)
    print("Configuration analysis:")
    print("  guide_for_must:         {0}".format(defects["guide_for_must"] or "none"))
    print("  uncovered_binding:      {0}".format(defects["uncovered_binding"] or "none"))
    print("  control_for_preference: {0}".format(defects["control_for_preference"] or "none"))

    print("")
    print("Events:")
    silent_gaps = []
    for outcome in drive(config, events):
        kind = outcome.convention.kind if outcome.convention else "?"
        flag = ""
        if outcome.silent_gap:
            flag = "  <== silent gap: must-hold not governed"
            silent_gaps.append(outcome.event.id)
        print("  {0} {1:<7} {2:<24} [{3:<10}] {4:<10} fired={5}{6}".format(
            outcome.event.id,
            outcome.event.action,
            outcome.event.target_convention,
            kind,
            outcome.outcome,
            outcome.fired_layers or "none",
            flag,
        ))

    print("")
    print("Events where a must-hold convention was not governed: {0}".format(silent_gaps or "none"))
    print("On the rules-and-memory configuration, the new file slipped past the house-style rule and "
          "the commit slipped past a memory-only secrets convention. The rule never fired on create, "
          "and memory cannot govern a commit.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
