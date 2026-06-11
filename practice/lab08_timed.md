# Timed set: lab 08 agent permissions and sandboxing

Five questions at two minutes each. Train recognition speed, not derivation. Each answer is hidden
inside a collapsible block, so commit to a choice before you expand "Reveal answer." Each question
carries a Branch A fabricated-feature distractor and at least one Branch B valid-but-suboptimal
distractor. Full reasoning lives in the lab's `answers.md`. Source lab: 08. Domains: Claude Code
Configuration and Workflows, Tool Design and MCP Integration.

## Q1

A build subprocess reads an SSH key and sends it out, despite a `Read(~/.ssh/**)` deny rule. Best fix?

A. Add `Bash(no-credentials: true)`. B. Enable the OS-level Bash sandbox. C. Add more Read deny rules.
D. Add a `CLAUDE.md` rule not to read credentials.

<details>
<summary>Reveal answer</summary>

Answer: B. Rationale: A is a fabricated setting (Branch A). C and D stay in a layer that does not bind a
subprocess; only the sandbox does (Branch B).

</details>

## Q2

An unattended CI agent runs in `bypassPermissions` in the shared checkout. A command deletes a directory
outside the project. Soundest change?

A. Run in `default` mode with a deny rule for dangerous commands and an allow list. B. Keep bypass, add
`safeMode: true`. C. Keep bypass, rely on a `CLAUDE.md` rule. D. Keep bypass, run on a fast machine.

<details>
<summary>Reveal answer</summary>

Answer: A. Rationale: B is a fabricated setting (Branch A). C guides without enforcing under bypass
(Branch B). D does not contain the damage (Branch B).

</details>

## Q3

Tight permission rules (strict allow list, deny for dangerous commands and credential paths), no
sandbox. Correct statement?

A. Safe, tight rules cover everything the agent touches. B. Not fully safe, deny rules do not apply to
arbitrary subprocesses, so a build subprocess can still read a credential. C. Safe once
`permissions.enforceSubprocess: true` is set. D. Safe enough, subprocess reads are rare.

<details>
<summary>Reveal answer</summary>

Answer: B. Rationale: C is a fabricated setting (Branch A). A and D treat permission scoping as
subprocess containment, which it is not (Branch B).

</details>

## Q4

Config X: bypass permissions, shared checkout, no sandbox. Config Y: scoped permissions, sandbox, and a
worktree. Constraint: containment without a human in the loop. Which wins?

A. X, skipping prompts is the only way to run unattended. B. Y, scoping plus sandbox plus worktree is
what unattended containment requires. C. Neither, safety is set by an `agentHardening` profile. D.
Either, CI runners are ephemeral.

<details>
<summary>Reveal answer</summary>

Answer: B. Rationale: C is a fabricated profile (Branch A). A wrongly equates unattended with bypass
(Branch B). D ignores a credential already exfiltrated (Branch B).

</details>

## Q5

A team enables session forking expecting it to isolate a branch's file edits. The edits land in the
shared directory. Correct statement?

A. Forking should isolate files, so report a bug. B. Forking branches conversation history, not the
filesystem, so file isolation needs a worktree or checkpointing. C. Set `fork_session(isolate_fs=True)`.
D. Fine, the agent can undo edits by editing again.

<details>
<summary>Reveal answer</summary>

Answer: B. Rationale: C is a fabricated option (Branch A). A misexpects forking (Branch B). D is not a
reliable revert (Branch B).

</details>
