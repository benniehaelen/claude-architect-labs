# Failure modes: lab 04 Claude Code team workflow

Each failure mode names what goes wrong, how it is detected, and what the reference design does
about it. Run `bad_version/run.py` and `solution/run.py` to see several directly, and
`shared/evals/check_lab04.py` for the assertions.

## Write-time gap: a path-scoped rule does not fire on create

A must-hold convention is enforced only by a path-scoped rule, so it holds when Claude edits an
existing file but is unenforced when Claude creates a new one. This is the verified primitive at the
center of the lab: a path-scoped rule loads on read and edit of a matching file, not on its creation
(see `../../VERIFIED.md`). In the rules-and-memory configuration the house-style convention slips on
the create event. Detection is the `uncovered_binding` report listing `house_style_no_em_dash:create`
and the per-event `silent_gap` flag. The reference adds a PostToolUse hook that governs both create
and edit, which closes the gap.

## A must-hold convention placed in a guide layer

A must-hold convention lives in memory or a rule, which are guides, with no control anywhere. Nothing
governs it deterministically, so it holds only when the guide happens to fire and shape behavior. The
rules-and-memory configuration keeps the no-secrets convention in memory alone. Detection is the
`guide_for_must` report. The reference moves each must-hold into a control that fires on its binding
event.

## A must-hold not governed at its binding event

A convention is written down but no control fires on the event where it must hold. The no-secrets
convention in memory cannot block a commit, because memory is not a commit-time control. Detection is
the `uncovered_binding` report listing `no_committed_secrets:commit` and the per-event outcome of
`unenforced` on the commit. The reference governs the commit with a pre-commit check and a CI gate.

## Over-controlled preference

A preference is governed by a blocking control, which pays for a control where a guide would do and
slows the team for no safety benefit. The rules-and-memory configuration governs the heading-case
preference with a hook. Detection is the `control_for_preference` report. The reference guides the
preference with the rule alone, which is the layer a preference belongs in.

## Reliance on a fabricated load-on-write switch

A subtler mode, and the Branch A trap the exam angle calls out: assuming a `CLAUDE.md` directive or a
settings key can force a path-scoped rule to load when a file is created. No such switch exists, and
naming it is the fabricated-feature trap the repository teaches learners to avoid (see
`../../DISTRACTOR_TAXONOMY.md`). The reference does not try to change when the guide fires. It adds a
control that does fire on the event, which is the real pattern.
