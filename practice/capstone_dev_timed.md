# Timed set: developer-productivity tools capstone

Five questions at two minutes each. These are integrative: they require composing the tool catalog and
gate (lab 02) and the team configuration enforcement (lab 04). Each answer is hidden inside a
collapsible block, so commit to a choice before you expand "Reveal answer." Each question carries a
Branch A fabricated-feature distractor and at least one Branch B valid-but-suboptimal distractor. Full
reasoning lives in the capstone's `answers.md`. Source: developer-productivity capstone.

## Q1

An ungated deploy tool runs unauthorized, and a path-scoped house-style rule misses a newly created
doc. Which two changes fix both?

A. Gate the deploy tool and add a PostToolUse hook governing house style on create. B. Set
`devSafeMode: true`. C. A stern `CLAUDE.md` instruction. D. Make deploy read-only and move the rule into
the prompt.

<details>
<summary>Reveal answer</summary>

Answer: A. Rationale: B is a fabricated switch (Branch A). C guides but governs neither (Branch B). D
breaks a needed tool and still misses create (Branch B).

</details>

## Q2

A path-scoped house-style rule holds on an edit but not on a new file. Why, and what fixes it?

A. It fails on neither, no change needed. B. It loads on edit, not create, so a hook is needed to govern
create. C. `ruleScope` is too narrow, widen to `**/*`. D. Move the convention entirely to a CI check
after the fact.

<details>
<summary>Reveal answer</summary>

Answer: B. Rationale: C is a fabricated setting (Branch A). A denies the real gap (Branch B). D governs
late, after the file was created (Branch B).

</details>

## Q3

A coarse ungated `dev_tool` bundles edit, open PR, and deploy. A routine edit selects it. Soundest fix?

A. Split by effect, gate the write and the destructive deploy separately. B. Add a `confirmDeploy: true`
parameter. C. Warn about deploy in the description. D. Instruct the agent to use it only for edits.

<details>
<summary>Reveal answer</summary>

Answer: A. Rationale: B is a fabricated parameter (Branch A). C and D leave the bundled deploy capability
in place (Branch B).

</details>

## Q4

Setup X: sound config, ungated catalog. Setup Y: gated catalog, rules-and-memory config that misses
create. Constraint: tools and conventions must both hold. Acceptable?

A. X, conventions matter more. B. Neither, each fails one dimension and both must hold. C. Y, gating
matters more. D. Either, the agent compensates.

<details>
<summary>Reveal answer</summary>

Answer: B. Rationale: D asserts a capability that does not exist (Branch A in spirit). A and C each accept
a setup that fails one required dimension (Branch B).

</details>

## Q5

A reviewer calls the environment safe because the catalog is deliberate and dangerous tools are gated.
Conventions live only in a rule and `CLAUDE.md`. Correct statement?

A. Safe, a gated catalog is the only control that matters. B. Not fully safe, conventions are guided not
governed, so a created file or a secret can slip without a hook or check. C. Safe once
`conventionEnforcement: true` is set. D. Safe enough, developers usually follow conventions.

<details>
<summary>Reveal answer</summary>

Answer: B. Rationale: C is a fabricated switch (Branch A). A treats one layer as the whole system, and D
rests on usual behavior (Branch B).

</details>
