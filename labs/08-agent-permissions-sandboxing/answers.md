# Answers: lab 08 agent permissions and sandboxing

Each answer names the correct option, then labels every distractor by branch (A fabricated feature,
B valid but suboptimal) and states why it fails. The pattern to internalize: feature fluency removes
the Branch A fabrications, and architectural judgment picks the winner among the Branch B survivors
(see `../../DISTRACTOR_TAXONOMY.md`).

## Question 1: correct answer is B

B enables the OS-level Bash sandbox, which contains the subprocess regardless of what the build runs.
That is the only layer that binds a subprocess, because permission Read deny rules do not reach inside
one (see `../../VERIFIED.md`).

- A is Branch A, fabricated feature. There is no `Bash(no-credentials: true)` setting. The
  convenient-sounding switch is the tell.
- C is Branch B, valid but suboptimal. More Read deny rules still only cover Claude's own file tools,
  not the build subprocess, so the leak persists. Right layer for direct reads, wrong layer for a
  subprocess.
- D is Branch B, valid but suboptimal. A `CLAUDE.md` instruction guides the model but does not bind a
  subprocess, and permission and sandbox behavior is enforced by Claude Code, not the model.

## Question 2: correct answer is A

A runs in `default` mode with a deny rule for dangerous commands and an allow list for the job, which
restores the scoping layer that bypass removed. Deny is evaluated first, so the destructive command is
blocked.

- B is Branch A, fabricated feature. There is no `safeMode: true` setting that blocks destructive
  commands. The real control is a deny rule.
- C is Branch B, valid but suboptimal. A `CLAUDE.md` rule guides but does not enforce, and with bypass
  on there is no permission layer to stop the command.
- D is Branch B, valid but suboptimal. Finishing faster does not contain the damage. A deleted external
  directory is gone regardless of speed.

## Question 3: correct answer is B

B states the verified edge precisely: permission Read and Edit deny rules do not apply to arbitrary
subprocesses, so a build subprocess can still read a credential without the sandbox.

- A is Branch B, valid but suboptimal in the sense that it is a coherent but wrong position. Tight rules
  cover Claude's own tools, not a subprocess that opens files itself.
- C is Branch A, fabricated feature. There is no `permissions.enforceSubprocess: true` setting that
  extends rules into subprocesses. The sandbox is what contains a subprocess.
- D is Branch B, valid but suboptimal. Rarity is not containment, and a credential leak cannot rest on
  the read being uncommon.

## Question 4: correct answer is B

B identifies the layered design: least-privilege rules scope the tool calls, the sandbox contains
subprocesses, and the worktree isolates file edits, which is exactly what unattended containment
requires.

- A is Branch B, valid but suboptimal. Skipping prompts is one way to run unattended, but bypassing
  permissions in the shared checkout removes the scoping the constraint needs. Allow lists and the
  sandbox let an agent run unattended without bypass.
- C is Branch A, fabricated feature. There is no `agentHardening` profile that sets safety. Safety is a
  configuration of real layers, not a named profile.
- D is Branch B, valid but suboptimal. An ephemeral runner discards file changes, but it does not undo a
  credential already exfiltrated to the network.

## Question 5: correct answer is B

B states the verified primitive: forking branches the conversation history, not the filesystem, so file
isolation needs a worktree or file checkpointing.

- A is Branch B, valid but suboptimal in the sense that it is a coherent but wrong expectation. Forking
  was never going to isolate files, so this is not a bug.
- C is Branch A, fabricated feature. There is no `isolate_fs=True` option on forking that snapshots the
  filesystem.
- D is Branch B, valid but suboptimal. Editing again is not a reliable revert, and a destructive edit
  may not be recoverable that way.
