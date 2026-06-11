#!/usr/bin/env python3
"""Intentionally flawed version for lab 08: the unscoped, unsandboxed agent.

This configuration is the anti-pattern. It runs through the exact same engine as the reference
solution (see shared/harness/permissions.py). Nothing about the engine changed. Only the
configuration did, and that is enough to produce three failures:

1. Bypassed permissions. The agent runs in bypassPermissions mode with no deny rules, so a dangerous
   command that deletes a directory outside the working tree simply runs.
2. No sandbox. With no OS-level sandbox, the needed build command's subprocess reads a credential
   file and exfiltrates it, because permission rules cannot reach inside a subprocess.
3. Shared filesystem. The agent edits files in the shared working directory, so its changes are not
   isolated and cannot be reverted.

Usage:
    python labs/08-agent-permissions-sandboxing/bad_version/run.py
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT))

from shared.harness.permissions import AgentConfig, Attempt, analyze_config, drive  # noqa: E402
from shared.harness.model import load_session  # noqa: E402


def main() -> int:
    config = AgentConfig.from_dict(load_session("agent_config_bad"))
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
    harms = []
    for o in drive(config, attempts):
        flag = ""
        if o.ran_dangerous:
            flag = "  <== dangerous command ran uncontained"
            harms.append(o.attempt.id)
        if o.leaked_credentials:
            flag = "  <== credential read by subprocess, not contained"
            harms.append(o.attempt.id)
        if o.unisolated_edit:
            flag = "  <== edit not isolated, cannot be reverted"
            harms.append(o.attempt.id)
        print("  {0} {1:<32} {2:<7} contained={3!s:<5} isolated={4!s:<5}{5}".format(
            o.attempt.id, o.attempt.rule, o.decision, o.contained, o.isolated, flag))

    print("")
    print("Harmful outcomes: {0}".format(harms or "none"))
    print("On the unscoped, unsandboxed agent, a dangerous command ran, a subprocess exfiltrated a "
          "credential despite any file-read rule, and the file edits cannot be reverted. Bypassing "
          "permissions removed the scoping layer and the missing sandbox removed OS-level containment.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
