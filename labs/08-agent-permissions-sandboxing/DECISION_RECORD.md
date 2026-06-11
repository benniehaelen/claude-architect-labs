# Decision record: lab 08 agent permissions and sandboxing

## Scenario

An agent runs unattended in a CI pipeline. There is no human to approve each action, so its
configuration decides what it may do. The attempt set is realistic for a build job: run the tests,
read source, run the build, edit a config file, and a dangerous command that would delete a sibling
directory outside the checkout. The configuration in `bad_version` bypasses permissions, runs with no
sandbox, and works in the shared checkout. The dangerous command runs, the build subprocess reads and
exfiltrates a credential, and the file edits cannot be reverted.

## Constraints

The binding constraint is containment without a human in the loop: every action the agent takes must be
scoped, contained, and reversible by configuration alone. Speed matters in CI, but an agent that can
delete files outside its tree, exfiltrate a credential, or make irreversible edits is not safe to run
unattended.

- Latency: the sandbox and permission checks add little, and they replace the human approvals CI cannot
  provide.
- Cost: a contained agent avoids the far larger cost of a leaked credential or a destroyed workspace.
- Reliability: the configuration must behave deterministically across runs, not depend on a prompt.
- Security: a dangerous command must be denied, and a subprocess must be contained at the OS level.
- Data sensitivity: credentials on the runner (SSH keys, cloud tokens) must not be reachable by a build
  subprocess.
- Human review: there is none at run time, so the controls must hold without it, and a blocked needed
  action should fail the build rather than stall.
- Operational owner: the team that owns the pipeline owns the permission rules, the sandbox settings,
  and the worktree isolation.

## Design chosen

A scoped, sandboxed configuration (in `agent_config_good.json`) with three layers, each a runtime
control mapped to a verified Claude Code feature (see `../../VERIFIED.md`).

Permission scoping. The configuration runs in `default` mode, not `bypassPermissions`, denies dangerous
patterns such as `Bash(rm *)` and `Bash(curl *)`, and allows only the tool calls the job needs. Deny is
evaluated first, so a dangerous command is blocked regardless of any allow rule. This scopes which tool
calls Claude makes.

OS-level sandbox. The Bash sandbox is enabled, so a command and its child processes are confined at the
operating-system level. This is the layer that contains the build subprocess that reads a credential
file. A `Read(~/.ssh/**)` deny rule does not stop that read, because the documentation states that Read
and Edit deny rules do not apply to arbitrary subprocesses. Only the sandbox binds the process.

Worktree isolation. The agent runs in an isolated worktree, so its file edits are revertible and do not
affect the shared tree. Forking branches the conversation, not the filesystem, so file isolation needs
its own control.

The decisive insight, visible in the runners, is that the unscoped agent and the scoped, sandboxed
agent use the exact same engine. Only the configuration differs. An action is contained, or not,
because of the configuration, not because the agent was told to be careful.

## Alternatives rejected and why

Bypassing permissions for speed in a non-isolated environment. The `bypassPermissions` mode and the
`--dangerously-skip-permissions` flag remove the scoping layer, so a dangerous command runs. They are
only appropriate in an environment that is already isolated, such as a container or VM. In the shared
checkout they remove the very control the scenario needs.

Scoping permission rules tightly but not enabling the sandbox. This is the scoped-but-unsandboxed
configuration in the eval. It denies the dangerous command correctly, because that is Claude's own
tool call, but it still leaks the credential, because the read happens inside an allowed build
subprocess that a Read deny rule cannot reach. Correct for direct tool calls, insufficient for
subprocess containment. Permission scoping is necessary and is not the same as a sandbox.

Relying on file checkpointing alone without scoping or a sandbox. Isolation makes edits revertible but
does nothing about a dangerous command or a credential read. It is one layer of three, not a substitute
for the others.

## Failure modes

Summarized here and detailed in `FAILURE_MODES.md`: bypassed permissions that run a dangerous command,
a missing sandbox that lets a subprocess exfiltrate a credential, a shared filesystem that makes edits
irreversible, over-restriction that blocks a needed action, and the belief that a tight permission rule
contains a subprocess.

## Controls

- Enforced by prompt: a `CLAUDE.md` instruction to avoid dangerous commands, which guides behavior.
  Helpful, not load-bearing, since permission rules are enforced by Claude Code and not the model.
- Enforced by runtime: the permission rules (deny first), the OS-level Bash sandbox, and worktree
  isolation. These are the controls that scope, contain, and isolate. See `../../ENFORCEMENT_LAYER.md`.
- Observable: the per-attempt decision (allow, deny, or prompt), whether the action was contained, and
  whether the edit was isolated, plus the ran-dangerous, leaked-credentials, and unisolated-edit flags.
- Auditable: each attempt records its decision, containment, and isolation, so a run can be reviewed
  after the fact.

## Governance and escalation (mandatory)

- Where automation stops: a deny rule stops a dangerous tool call before it runs, the sandbox stops a
  subprocess from reaching outside its boundary, and a needed action that is not allowed prompts, which
  in CI fails the build rather than proceeding.
- Human-handoff path: a blocked needed action surfaces as a failed build for a human to review and
  widen the policy deliberately, rather than the agent escalating its own privileges.
- Fail-safe behavior (fails safely rather than silently): the scoped, sandboxed agent denies the
  dangerous command, contains the subprocess, and isolates the edit, while the unscoped agent runs all
  three harms and the scoped-but-unsandboxed agent still leaks the credential. The contrast, same
  attempts and same engine, opposite outcome, is the lesson: permission scoping, the sandbox, and
  isolation are complementary, and scoping alone is not subprocess containment.

## Exam angle

See `EXAM_ANGLE.md`. This lab serves the Claude Code Configuration and Workflows domain (20%) with Tool
Design and MCP Integration (18%) as secondary. The transferable judgment is that permission rules scope
which tool calls the agent makes, the OS-level sandbox contains what a subprocess does, and worktree
isolation makes file edits revertible, so a safe unattended agent layers all three.
