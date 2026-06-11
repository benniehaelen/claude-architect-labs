# Failure modes: lab 08 agent permissions and sandboxing

Each failure mode names what goes wrong, how it is detected, and what the reference design does
about it. Run `bad_version/run.py` and `solution/run.py` to see several directly, and
`shared/evals/check_lab08.py` for the assertions.

## Bypassed permissions run a dangerous command

The agent bypasses the permission layer (the `bypassPermissions` mode or the
`--dangerously-skip-permissions` flag) with no deny rules, so a dangerous command runs with nothing to
stop it. In the unscoped configuration the command that deletes a sibling directory simply executes.
Detection is the `bypass_permissions` analysis flag and the per-attempt `ran_dangerous` flag. The
reference runs in `default` mode and denies dangerous patterns, and because deny is evaluated first the
command is blocked regardless of any allow rule (see `../../VERIFIED.md`).

## A missing sandbox lets a subprocess exfiltrate a credential

With no OS-level sandbox, a command's child process can read files and reach the network freely. The
build command is legitimately allowed, but its subprocess reads a credential file and exfiltrates it.
Detection is the `no_sandbox` analysis flag and the `leaked_credentials` flag. The reference enables the
Bash sandbox, which confines the subprocess at the operating-system level so the credential read is
contained.

## A tight permission rule that does not contain a subprocess

The subtle and central failure, and the Branch B trap the exam angle calls out: assuming a
`Read(~/.ssh/**)` deny rule stops a credential read. It does not. The documentation states that Read and
Edit deny rules apply to Claude's own file tools, not to an arbitrary subprocess that opens files
itself. The scoped-but-unsandboxed configuration in the eval denies the dangerous command correctly yet
still leaks the credential through the allowed build subprocess. Detection is the `leaked_credentials`
flag on a configuration whose permission rules look tight. The reference contains the subprocess with
the sandbox, the only layer that binds the process rather than the model's tool choice.

## A shared filesystem makes edits irreversible

The agent edits files in the shared checkout rather than an isolated worktree, so its changes are not
revertible and affect the shared tree directly. Detection is the `shared_filesystem` analysis flag and
the `unisolated_edit` flag. The reference runs in a worktree, which isolates the edits and makes them
revertible, because forking branches the conversation, not the filesystem.

## Over-restriction that blocks a needed action

The opposite error: denying or failing to allow a tool call the job needs, so a needed build step is
blocked and the pipeline stalls or fails for the wrong reason. Detection is the `blocked_needed` flag,
which marks a needed attempt that was denied or left to a prompt. The reference allows exactly the tool
calls the job needs and denies the dangerous ones, so needed work proceeds and only the dangerous action
is stopped. See `../../ENFORCEMENT_LAYER.md` for why the control belongs in the permission and sandbox
layers rather than the prompt.
