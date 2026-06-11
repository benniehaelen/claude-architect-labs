# Failure modes: lab 06 context management failure modes

Each failure mode names what goes wrong, how it is detected, and what the reference design does
about it. The theme of this lab is silent versus loud failure. Run `bad_version/run.py` and
`solution/run.py` to see several directly, and `shared/evals/check_lab06.py` for the assertions.

## Silent context drop

The context window overflows and the overflow policy evicts the oldest segments to fit, with no
signal. An early load-bearing detail vanishes and nothing announces it, so the run looks healthy while
a hard constraint is gone. In the scenario the silent design drops `seg1`, the load-bearing segment,
on an oldest-first eviction. Detection is the per-run `dropped_load_bearing` list and the
`overflow_signaled` flag of false. The reference pins the load-bearing segments and signals the
overflow, so the detail survives and the loss is loud.

## A lossy summary that loses the load-bearing detail

A subtler form of the same failure: instead of evicting, the policy collapses everything into one
summary, including the load-bearing detail, and emits no signal. The summary looks complete while the
detail that mattered is gone. The summarize-lossy design shows this: it isolates files correctly but
still drops the load-bearing detail without signaling. Detection is the `silent_overflow` analysis
flag and the same `dropped_load_bearing` plus unsignaled overflow. The reference summarizes only the
non-load-bearing segments and pins the rest.

## A context budget enforced by prompt rather than orchestration

The budget is a prompt instruction to be concise rather than an orchestration limit, so it lowers the
chance of overflow but does not enforce a ceiling. A long run overflows anyway. Detection is the
`budget_by_prompt` analysis flag. The reference enforces the budget in the orchestration layer, which
is a control rather than a guide. See `../../ENFORCEMENT_LAYER.md`.

## A forked branch that shares the filesystem

The branch relies on forking alone for isolation. Forking branches the conversation history but not
the filesystem (see `../../VERIFIED.md`), so the forked subagent's file edits land in the shared
working directory and are visible to the parent. Detection is the `fork_only_isolation` analysis flag
and the `leaked_to_parent` flag of true. The reference checkpoints the filesystem before the branch,
which isolates the edits.

## An irreversible file edit from a branch with no checkpoint

A consequence of fork-only isolation: because the branch's edits are real and shared, the branch
cannot revert them. A mistaken or experimental edit is permanent. Detection is the `revertible` flag
of false. The reference uses file checkpointing so the branch's edits can be reverted, which is the
real pattern for a branch that must undo its file changes. Naming a fork flag that snapshots the
filesystem is the Branch A fabricated-feature trap (see `../../DISTRACTOR_TAXONOMY.md`).
