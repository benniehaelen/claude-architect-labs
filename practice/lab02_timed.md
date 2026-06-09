# Timed set: lab 02 tool catalog design

Five questions at two minutes each. Train recognition speed, not derivation. Each answer is hidden
inside a collapsible block, so commit to a choice before you expand "Reveal answer." Each question
carries a Branch A fabricated-feature distractor and at least one Branch B valid-but-suboptimal
distractor. Full reasoning lives in the lab's `answers.md`. Source lab: 02. Domains: Tool Design
and MCP Integration, Agentic Architecture and Orchestration.

## Q1

Three tools all plausibly serve "look up an order" and the agent keeps picking wrong. Best fix?

A. Add a more general lookup tool. B. Collapse the overlap to one tool per intent. C.
`toolSelection: "strict"` config. D. Add "when not to use me" lines to each description.

<details>
<summary>Reveal answer</summary>

Answer: B. Rationale: C is a fabricated config key (Branch A). A increases overlap, the wrong
direction (Branch B). D patches in the guide layer while the ambiguity remains (Branch B).

</details>

## Q2

One coarse tool can look up, cancel, or refund an order. A routine status call now carries cancel
power. Soundest fix?

A. Add a destructive warning to the description. B. Split by effect and gate the cancel tool. C.
`requireConfirm: all` settings key. D. Prompt the agent to never cancel unless asked.

<details>
<summary>Reveal answer</summary>

Answer: B. Rationale: C is a fabricated key (Branch A). A and D enforce a must-hold safety property
in the guide layer while the coarse tool keeps the capability (Branch B).

</details>

## Q3

An ungated destructive close_account runs unauthorized with no confirmation. Where to enforce the
stop?

A. In the tool description. B. In a runtime permission gate that requires authorization and
confirmation and escalates. C. A `dangerous: true` flag that auto-confirms. D. A post-action audit
log.

<details>
<summary>Reveal answer</summary>

Answer: B. Rationale: C is a fabricated flag, and auto-confirm would be backwards (Branch A). A is
the wrong layer (Branch B). D records the harm after it happens (Branch B).

</details>

## Q4

Catalog X: fifteen tools with overlaps. Catalog Y: eight tools, one intent each, dangerous tools
gated. Constraint is safe, unambiguous selection. Which wins?

A. X, for coverage. B. Y, because one-intent-per-tool plus gating matches the constraint. C.
Neither, quality is set by a `catalogLint` step. D. Either, the agent learns from experience.

<details>
<summary>Reveal answer</summary>

Answer: B. Rationale: C is a fabricated build step (Branch A). A serves coverage, not the stated
constraint (Branch B). D relies on unreliable in-task learning (Branch B).

</details>

## Q5

A reviewer calls the catalog safe because every dangerous tool's description warns the model. There
is no runtime gate. Correct statement?

A. Safe, a clear description suffices. B. Unsafe, a description guides selection but only a gate
governs execution, and there is none. C. Safe once `descriptionEnforcement: true` is on. D. Safe
enough, the model usually follows descriptions.

<details>
<summary>Reveal answer</summary>

Answer: B. Rationale: C is a fabricated switch (Branch A). A and D treat a guide as a control, which
is the core error the lab corrects (Branch B).

</details>
