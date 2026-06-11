# Questions: lab 08 agent permissions and sandboxing

Five scenario questions. Each carries at least one Branch A distractor (a fabricated feature) and at
least two Branch B distractors (valid but suboptimal under the stated constraints). See
`../../DISTRACTOR_TAXONOMY.md`. Answers and branch labels are in `answers.md`. Do not read the
answers until you have committed to a choice.

## Question 1

A CI agent runs a build whose subprocess reads an SSH key from the runner and sends it out. The team
has a permission deny rule `Read(~/.ssh/**)`. The leak still happens. What is the best fix?

A. Add `Bash(no-credentials: true)` to the agent config so subprocesses cannot read secrets.
B. Enable the OS-level Bash sandbox, which contains the subprocess at the operating-system level
   regardless of what the build runs.
C. Add a stronger `Read(~/.ssh/**)` deny rule and also deny `Read(~/.aws/**)`.
D. Add a `CLAUDE.md` instruction telling the agent not to read credential files.

## Question 2

An unattended agent in CI runs in `bypassPermissions` mode in the shared checkout to avoid prompts. A
command deletes a directory outside the project. What is the soundest change?

A. Run in `default` mode with a deny rule for dangerous commands and an allow list for what the job
   needs.
B. Keep `bypassPermissions` but add a `safeMode: true` setting that blocks destructive commands.
C. Keep `bypassPermissions` and rely on a `CLAUDE.md` rule to avoid destructive commands.
D. Keep `bypassPermissions` but run the agent only on a fast machine so it finishes before harm spreads.

## Question 3

A reviewer says the agent is safe because its permission rules are tight: a strict allow list and deny
rules for dangerous commands and credential paths. There is no sandbox. Which statement is correct?

A. It is safe, because tight permission rules cover every file and command the agent touches.
B. It is not fully safe, because permission Read and Edit deny rules do not apply to arbitrary
   subprocesses, so a build subprocess can still read a credential without the sandbox.
C. It is safe once `permissions.enforceSubprocess: true` is set to extend the rules into subprocesses.
D. It is safe enough, because subprocess credential reads are rare in practice.

## Question 4

Two configurations are proposed for an unattended CI agent. Config X bypasses permissions and runs in
the shared checkout with no sandbox. Config Y scopes permissions least to most, enables the sandbox, and
runs in a worktree. Under a constraint of containment without a human in the loop, which is better and
why?

A. Config X, because skipping prompts is the only way an agent can run unattended.
B. Config Y, because least-privilege rules scope the tool calls, the sandbox contains subprocesses, and
   the worktree isolates file edits, which is what unattended containment requires.
C. Neither, because agent safety is set by the `agentHardening` profile rather than by configuration.
D. Either, because CI runners are ephemeral, so any damage is discarded at the end of the run.

## Question 5

A team wants a branch of work whose file edits can be thrown away if the agent goes wrong. They enable
session forking and expect it to isolate the files. The edits land in the shared working directory
anyway. What is correct?

A. Forking should have isolated the files, so this is a bug to report.
B. Forking branches the conversation history, not the filesystem, so file isolation needs a worktree or
   file checkpointing.
C. Set `fork_session(isolate_fs=True)` so the fork also snapshots the filesystem.
D. Edits are fine in the shared directory, since the agent can undo them by editing again.
