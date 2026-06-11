# Decision record: lab 04 Claude Code team workflow

## Scenario

A team adopts Claude Code across developer machines and a CI/CD pipeline and needs its conventions to
hold consistently for every member and every run. Some conventions are must-holds, such as the
house-style rule that Markdown files contain no em-dashes and the security rule that credentials are
never committed. Others are preferences, such as sentence-case headings. The configuration in
`bad_version` writes the conventions into a path-scoped rule and into memory and assumes they hold.
They do not. The house-style rule never fires when Claude creates a new file, the memory-only secrets
convention cannot block a commit, and a preference is over-controlled with a blocking hook.

## Constraints

The binding constraint is that a must-hold convention holds deterministically on the event where it
matters, including file creation, where a path-scoped rule alone does not fire. Convenience and speed
matter, but a convention that silently fails on a new file is worse than no convention, because the
team believes it is covered.

- Latency: a hook or a check adds a small step at write or commit time, not in the agent loop.
- Cost: an over-controlled preference wastes effort by blocking on something that should only be
  guided.
- Reliability: a must-hold convention must be governed on every binding event, not merely written
  down where it might be read.
- Security: the no-secrets convention must be enforced by a control at the commit, not by memory.
- Data sensitivity: a leaked credential is the concrete harm the secrets control prevents.
- Human review: a blocked commit or a failing check routes back to a person to fix, rather than
  landing the violation.
- Operational owner: the team that owns the repository owns the rules, the hooks, and the CI gates,
  and keeps them in version control so every member inherits them.

## Design chosen

A layered configuration (in `team_config_good.json`) where each convention is enforced in the layer
that matches its kind. The distinction is the repository's central thesis: a guide raises the
likelihood of a behavior, a control governs it deterministically (see `../../ENFORCEMENT_LAYER.md`).

The house-style must-hold keeps the path-scoped rule as a guide, because the rule reliably shapes
edits to existing files, and adds a PostToolUse hook that governs both create and edit, with a
pre-commit check as a backstop. The hook is what closes the verified write-time gap: a path-scoped
rule loads when Claude reads or edits a matching file, not when it creates one (see `../../VERIFIED.md`),
so a rule alone would silently miss a new file.

The no-secrets must-hold is governed at the commit by a pre-commit check and a CI gate, because the
commit is its binding event and memory cannot block a commit. The heading-case preference is guided by
the rule alone, because a preference belongs in a guide and governing it with a blocking control would
be wasteful.

The decisive insight, visible in the runners, is that the rules-and-memory configuration and the
layered configuration use the exact same enforcement engine. Only the configuration differs. A
convention holds because of the layer that governs it on the right event, not because it was written
down.

## Alternatives rejected and why

Writing the conventions into `CLAUDE.md` memory and a path-scoped rule and stopping there. Memory and
rules are guides. They reliably shape edits, but the rule does not load on create and memory cannot
block a commit, so the two must-holds silently fail at exactly the events that matter. Correct in
mechanism for edits, wrong layer for a must-hold at creation and commit time.

Inventing a way to force the rule to load on write. The convenient-sounding switch does not exist, and
reaching for it is the fabricated-feature trap the repository teaches learners to avoid. The real fix
is to add a control that does fire on the event, not to wish the guide fired differently.

Governing every convention, including preferences, with a blocking hook or check. This holds the
must-holds, but it pays for a control where a guide would do and slows the team on preferences that do
not warrant a block. It optimizes uniformity over the kind-appropriate layering the constraint asks
for.

## Failure modes

Summarized here and detailed in `FAILURE_MODES.md`: the write-time gap where a path-scoped rule does
not fire on create, a must-hold convention placed in memory that cannot govern its binding event, an
over-controlled preference, reliance on a fabricated load-on-write switch, and a convention that is
written down but governed by no layer on its binding event.

## Controls

- Enforced by prompt: `CLAUDE.md` memory and the path-scoped rule, which guide behavior and reliably
  shape edits to existing files. Helpful, not load-bearing for a must-hold at creation or commit.
- Enforced by runtime: the PostToolUse hook that governs create and edit, the pre-commit check, and
  the CI gate. These are the controls that close the write-time gap and govern the commit.
- Observable: the configuration analysis (guide-only must-holds, uncovered binding events,
  controlled preferences) and the per-event outcome (governed, guided, or unenforced) with the layers
  that fired.
- Auditable: each event records the convention, its kind, the layers that fired, the outcome, and
  whether it was a silent gap.

## Governance and escalation (mandatory)

- Where automation stops: a must-hold convention stops the action at the layer that governs its
  binding event. The hook surfaces a violation on a new or edited file, and the pre-commit check and
  CI gate block a commit that introduces a secret.
- Human-handoff path: a blocked commit or a failing check returns to the author to fix, rather than
  landing the violation. The control fails the action and hands it back to a person.
- Fail-safe behavior (fails safely rather than silently): the layered configuration governs the new
  file and the commit, while the rules-and-memory configuration lets both slip through unenforced. The
  contrast, same event stream and same engine, opposite outcome, is the lesson: a convention is only
  as strong as the layer that governs it, and a guide that silently misses an event is the failure to
  avoid.

## Exam angle

See `EXAM_ANGLE.md`. This lab serves the Claude Code Configuration and Workflows domain (20%) with
Agentic Architecture and Orchestration (27%) as secondary. The transferable judgment is that you must
match the enforcement layer to whether the requirement is a preference or a must, and know the
specific Read-versus-Write limitation that makes a rules-only answer wrong.
