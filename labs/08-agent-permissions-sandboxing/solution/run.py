#!/usr/bin/env python3
"""Reference solution for lab 08: a scoped, sandboxed agent.

Evaluate the tool calls a CI agent attempts under a configuration that scopes permissions least to
most (deny dangerous, allow only what the job needs), enables the OS-level Bash sandbox, and runs in
an isolated worktree. The dangerous command is denied, the needed build runs but its credential-reading
subprocess is contained by the sandbox, and the file edit is isolated and revertible.

Usage (dry-run, free, deterministic):
    python labs/08-agent-permissions-sandboxing/solution/run.py
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT))

from shared.harness.permissions import AgentConfig, Attempt, analyze_config, drive  # noqa: E402
from shared.harness.model import load_session  # noqa: E402


def main() -> int:
    config = AgentConfig.from_dict(load_session("agent_config_good"))
    data = load_session("agent_attempts")
    attempts = [Attempt(**spec) for spec in data["attempts"]]

    print("Config: {0}".format(config.name))
    defects = analyze_config(config)
    print("Config analysis:")
    print("  bypass_permissions: {0}".format(defects["bypass_permissions"]))
    print("  no_sandbox:         {0}".format(defects["no_sandbox"]))
    print("  shared_filesystem:  {0}".format(defects["shared_filesystem"]))

    print("")
    print("Attempts:")
    for o in drive(config, attempts):
        print("  {0} {1:<32} {2:<7} contained={3!s:<5} isolated={4!s:<5}".format(
            o.attempt.id, o.attempt.rule, o.decision, o.contained, o.isolated))

    print("")
    print("The dangerous command was denied, the needed build ran but its credential-reading "
          "subprocess was contained by the sandbox, and the file edit ran in an isolated worktree so "
          "it is revertible. Permission scoping, the sandbox, and worktree isolation each did their "
          "job.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
