# Lab 08: agent permissions and sandboxing

Primary domain: Claude Code Configuration and Workflows (20%). Secondary: Tool Design and MCP
Integration (18%). Anchor scenario: CI/CD integrations.

This is a v0.2 lab. It builds on the verified permission and sandboxing facts in `../../VERIFIED.md`
and on the session-forking filesystem edge that lab 06 introduced.

## Scenario brief

An agent runs unattended in a CI pipeline, so there is no human to approve each action. What it may do
is decided entirely by its configuration. The configuration in `bad_version` bypasses permissions, runs
with no sandbox, and works in the shared checkout, so a dangerous command runs, a build subprocess
reads and exfiltrates a credential, and file edits cannot be reverted. The hard part is knowing which
layer covers which threat: permission scoping decides which tool calls Claude makes, but only the
OS-level sandbox contains what a subprocess does, and only an isolated worktree makes file edits
revertible.

## Architecture goal

Configure an autonomous agent so that least-privilege permission rules scope its tool calls, the
OS-level Bash sandbox contains its subprocesses, and a worktree isolates its file state. The lab
contrasts an unscoped, unsandboxed agent against a scoped, sandboxed one, and shows that scoping
permissions is not the same as containing a subprocess.

## How to run (dry-run, free, deterministic)

No installs and no paid API calls are needed. The evaluation is deterministic and reads a
configuration and an attempt set from `../../shared/fixtures`. From the repository root:

```
python labs/08-agent-permissions-sandboxing/bad_version/run.py
python labs/08-agent-permissions-sandboxing/solution/run.py
python shared/evals/check_lab08.py
```

Both runners use the same engine (`../../shared/harness/permissions.py`). Only the configuration
differs. On the unscoped agent, a dangerous command runs, a build subprocess leaks a credential, and
edits are not isolated. On the scoped, sandboxed agent, the dangerous command is denied, the build runs
but its subprocess is contained, and edits are revertible. The eval also runs a scoped-but-unsandboxed
configuration that still leaks the credential, because a Read deny rule cannot reach inside a
subprocess and only the sandbox can.

## Status

Built for v0.2. Includes the unscoped configuration, the scoped and sandboxed configuration, the shared
engine (the permission decision, OS-level containment, and worktree isolation), the failure-mode
catalog, the decision record, the question set, and a timed practice set
(`../../practice/lab08_timed.md`).
