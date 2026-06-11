# Timed set: lab 04 Claude Code team workflow

Five questions at two minutes each. Train recognition speed, not derivation. Each answer is hidden
inside a collapsible block, so commit to a choice before you expand "Reveal answer." Each question
carries a Branch A fabricated-feature distractor and at least one Branch B valid-but-suboptimal
distractor. Full reasoning lives in the lab's `answers.md`. Source lab: 04. Domains: Claude Code
Configuration and Workflows, Agentic Architecture and Orchestration.

## Q1

A path-scoped Markdown rule holds on edits but is violated on files Claude creates. The convention
must always hold. Best fix?

A. Add `loadOnWrite: true` to the rule frontmatter. B. Keep the rule as a guide and add a PostToolUse
hook on Write and Edit. C. Move it into `CLAUDE.md`. D. Tell the rule to apply to new files too.

<details>
<summary>Reveal answer</summary>

Answer: B. Rationale: A is a fabricated frontmatter field (Branch A). C is still a guide and can slip
(Branch B). D does not change when the rule loads (Branch B).

</details>

## Q2

"Never commit credentials" lives in `CLAUDE.md`. A secret gets committed anyway. Where must
enforcement live?

A. In `CLAUDE.md`, in all capitals. B. In a pre-commit check or CI gate that blocks the commit. C. A
`secretScan: true` settings key. D. A path-scoped rule on likely-secret files.

<details>
<summary>Reveal answer</summary>

Answer: B. Rationale: C is a fabricated key (Branch A). A is still a guide (Branch B). D loads on
edit, not at the commit, and misses unmatched files (Branch B).

</details>

## Q3

A reviewer wants every convention, including heading case, governed by a blocking pre-commit check.
Assessment?

A. Sound, uniform is simplest. B. Overbuilt, a preference belongs in a guide and a blocking control
is for must-holds. C. Sound once `enforcementLevel: "all"` is set. D. Overbuilt, so drop the
preferences entirely.

<details>
<summary>Reveal answer</summary>

Answer: B. Rationale: C is a fabricated key (Branch A). A pays for a control where a guide would do
(Branch B). D throws away useful guidance instead of guiding it (Branch B).

</details>

## Q4

Config X: all conventions in memory and rules. Config Y: rules as guides plus hooks for write-time
must-holds and a CI gate for the commit-time security rule. Constraint: must-holds cannot silently
fail. Which wins?

A. X, simpler and in one place. B. Y, each must-hold governed by a control on its binding event while
rules still guide. C. Neither, quality is set by a `claude config lint` step. D. Either, Claude
generally follows memory and rules.

<details>
<summary>Reveal answer</summary>

Answer: B. Rationale: C is a fabricated step (Branch A). A silently misses create and commit (Branch
B). D rests a must-hold on usual behavior (Branch B).

</details>

## Q5

A lead says the house-style rule is safe because it is committed and every member has it. New files
keep violating it. Correct statement?

A. Safe, a committed rule applies to every file. B. Not safe, a rule loads on read and edit, not
create, so new files need a control like a hook. C. Safe once `rules.applyOnCreate: true` is enabled.
D. Safe enough, most files are edited not created.

<details>
<summary>Reveal answer</summary>

Answer: B. Rationale: C is a fabricated setting (Branch A). A and D treat a guide that misses the
create event as if it governed it, the core error the lab corrects (Branch B).

</details>
