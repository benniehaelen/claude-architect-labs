#!/usr/bin/env python3
"""Reference solution for lab 04: a layered Claude Code configuration.

Run a stream of create, edit, and commit events through the layered configuration. The house-style
must-hold keeps the path-scoped rule as a guide and adds a PostToolUse hook that governs both create
and edit, with a pre-commit check as a backstop. The no-secrets must-hold is governed at the commit
by a pre-commit check and a CI gate. The preference is guided by a rule, not governed by a blocking
control. Every must-hold convention is governed on its binding events and the preference is guided in
the right layer.

Usage (dry-run, free, deterministic):
    python labs/04-claude-code-team-workflow/solution/run.py
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT))

from shared.harness.config import Event, TeamConfig, analyze_config, drive  # noqa: E402
from shared.harness.model import load_session  # noqa: E402


def main() -> int:
    config = TeamConfig.from_dict(load_session("team_config_good"))
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
    for outcome in drive(config, events):
        kind = outcome.convention.kind if outcome.convention else "?"
        print("  {0} {1:<7} {2:<24} [{3:<10}] {4:<10} fired={5}".format(
            outcome.event.id,
            outcome.event.action,
            outcome.event.target_convention,
            kind,
            outcome.outcome,
            outcome.fired_layers or "none",
        ))

    print("")
    print("Every must-hold convention was governed on its binding events: the new file and the edit "
          "both hit the hook, and the commit hit the pre-commit check and the CI gate. The preference "
          "was guided by the rule rather than blocked, which is the right layer for a preference.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
