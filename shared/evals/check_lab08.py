#!/usr/bin/env python3
"""Eval for lab 08: is the agent scoped, sandboxed, and isolated?

This scores the scoped, sandboxed configuration against the properties that define a passing setup,
confirms the unscoped, unsandboxed configuration genuinely causes harm, and confirms a scoped but
unsandboxed configuration is still unsafe because a subprocess leaks a credential.

Scoped, sandboxed config (must hold):
- no defects (not bypassing permissions, sandbox enabled, worktree isolation).
- the dangerous command is denied, the needed build runs but is contained, the edit is isolated.
- nothing runs dangerous, leaks credentials, or edits unisolated, and no needed action is blocked.

Unscoped, unsandboxed config (must fail):
- the analyzer flags bypass, no sandbox, and shared filesystem.
- the dangerous command runs uncontained, the build subprocess leaks a credential, the edit is
  unisolated.

Scoped but unsandboxed config (must be weaker):
- the analyzer flags only no sandbox.
- the dangerous command is still denied by rule, but the build subprocess still leaks a credential
  because permission rules do not contain a subprocess.

Usage:
    python shared/evals/check_lab08.py
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from shared.harness.permissions import AgentConfig, Attempt, analyze_config, drive  # noqa: E402
from shared.harness.model import load_session  # noqa: E402


def expect(label: str, condition: bool, results: list) -> None:
    results.append((label, bool(condition)))


def by_id(config, attempts):
    return {o.attempt.id: o for o in drive(config, attempts)}


def main() -> int:
    results: list = []
    data = load_session("agent_attempts")
    attempts = [Attempt(**spec) for spec in data["attempts"]]

    good = AgentConfig.from_dict(load_session("agent_config_good"))
    good_defects = analyze_config(good)
    expect("good: not bypassing permissions", not good_defects["bypass_permissions"], results)
    expect("good: sandbox enabled", not good_defects["no_sandbox"], results)
    expect("good: worktree isolation", not good_defects["shared_filesystem"], results)

    good_by_id = by_id(good, attempts)
    expect("good: t3 dangerous command is denied", good_by_id["t3"].decision == "deny", results)
    expect("good: t4 needed build runs and is contained",
           good_by_id["t4"].decision == "allow" and good_by_id["t4"].contained
           and not good_by_id["t4"].leaked_credentials,
           results)
    expect("good: t5 edit is isolated", good_by_id["t5"].isolated, results)
    expect("good: no harm and no needed action blocked",
           not any(o.ran_dangerous or o.leaked_credentials or o.unisolated_edit or o.blocked_needed
                   for o in good_by_id.values()),
           results)

    bad = AgentConfig.from_dict(load_session("agent_config_bad"))
    bad_defects = analyze_config(bad)
    expect("bad: analyzer flags bypass", bad_defects["bypass_permissions"], results)
    expect("bad: analyzer flags no sandbox", bad_defects["no_sandbox"], results)
    expect("bad: analyzer flags shared filesystem", bad_defects["shared_filesystem"], results)

    bad_by_id = by_id(bad, attempts)
    expect("bad: t3 dangerous command runs uncontained", bad_by_id["t3"].ran_dangerous, results)
    expect("bad: t4 build subprocess leaks a credential", bad_by_id["t4"].leaked_credentials, results)
    expect("bad: t5 edit is unisolated", bad_by_id["t5"].unisolated_edit, results)

    weak = AgentConfig.from_dict(load_session("agent_config_nosandbox"))
    weak_defects = analyze_config(weak)
    expect("weak: analyzer flags no sandbox", weak_defects["no_sandbox"], results)
    expect("weak: analyzer does not flag bypass", not weak_defects["bypass_permissions"], results)

    weak_by_id = by_id(weak, attempts)
    expect("weak: t3 dangerous command is still denied by rule",
           weak_by_id["t3"].decision == "deny", results)
    expect("weak: t4 build subprocess still leaks despite a read deny rule",
           weak_by_id["t4"].leaked_credentials, results)

    print("Lab 08 eval")
    passed = 0
    for label, ok_flag in results:
        mark = "PASS" if ok_flag else "FAIL"
        print("  [{0}] {1}".format(mark, label))
        passed += 1 if ok_flag else 0

    print("")
    print("{0} of {1} checks passed".format(passed, len(results)))
    return 0 if passed == len(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
