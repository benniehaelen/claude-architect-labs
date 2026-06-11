# Start here: lab 08

## What you will build

You will harden the configuration of an unattended CI agent. The deliverable is a configuration that
scopes permission rules to least privilege (deny dangerous, allow only what the job needs), enables the
OS-level Bash sandbox, and runs in an isolated worktree, plus an argument for which threat each layer
covers and why scoping permissions does not contain a subprocess.

## Dry-run path

Run the lab against mocked attempts and recorded fixtures so it costs nothing. The dry-run evaluates the
tool calls a CI agent makes under an unscoped, unsandboxed configuration that causes harm, then under a
scoped, sandboxed one that contains it. A live run is optional and clearly marked.

## Suggested path

1. Read `README.md` for the scenario and the run commands.
2. Run the unscoped configuration and read its analysis. Notice that bypassing permissions lets a
   dangerous command run, the missing sandbox lets a build subprocess exfiltrate a credential, and the
   shared checkout makes the edits irreversible.
3. Run the scoped, sandboxed configuration and compare. The dangerous command is denied, the build runs
   but its subprocess is contained, and the edit is isolated and revertible.
4. Read `../../shared/harness/permissions.py`. Confirm that both runners call the same `drive` engine
   and that only the configuration differs, and study why a credential read inside an allowed subprocess
   is contained only by the sandbox, not by a Read deny rule.
5. Run `python shared/evals/check_lab08.py` to see the properties the configuration must satisfy,
   including the scoped-but-unsandboxed configuration that still leaks the credential.
6. Work `questions.md`, then check `answers.md` and study the branch labels. Finish with the timed set
   in `../../practice/lab08_timed.md` against the clock.
7. Read `DECISION_RECORD.md`, paying attention to the mandatory Governance and escalation section, and
   connect each control to the verified facts in `../../VERIFIED.md`.

Status: built for v0.2.
