# Timed set: lab 03 MCP boundaries

Five questions at two minutes each. Train recognition speed, not derivation. Each answer is hidden
inside a collapsible block, so commit to a choice before you expand "Reveal answer." Each question
carries a Branch A fabricated-feature distractor and at least one Branch B valid-but-suboptimal
distractor. Full reasoning lives in the lab's `answers.md`. Source lab: 03. Domains: Tool Design and
MCP Integration, Context Management and Reliability.

## Q1

An MCP server exposes a raw SQL tool and a secrets resource the assistant never needs. Best way to
narrow the surface?

A. Prompt the assistant to never call them. B. Scope the server to the needed operations and pin
`oauth.scopes`. C. Set `mcpScope: "auto"` to auto-prune. D. Rename the dangerous operations.

<details>
<summary>Reveal answer</summary>

Answer: B. Rationale: C is a fabricated setting (Branch A). A leaves the surface wide and lives in
the guide layer (Branch B). D changes the description, not the surface (Branch B).

</details>

## Q2

An ungated `delete_environment` runs unauthorized with no confirmation. Where to enforce the stop?

A. In the operation description. B. In a runtime gate at the server that requires authorization and
confirmation and escalates. C. A `destructive: true` flag that auto-confirms. D. A post-action audit
log.

<details>
<summary>Reveal answer</summary>

Answer: B. Rationale: C is a fabricated flag, and auto-confirm would be backwards (Branch A). A is
the wrong layer (Branch B). D records the harm after it happens (Branch B).

</details>

## Q3

One MCP tool returns a 120,000-token export and floods context. The host default limit is 25,000.
Soundest fix?

A. Trust `MAX_MCP_OUTPUT_TOKENS` to cap it. B. Bound the export at the server, keeping its declared
result size below the host cap. C. Enable `autoTruncate: true` in settings. D. Prompt the assistant
to ask for less.

<details>
<summary>Reveal answer</summary>

Answer: B. Rationale: C is a fabricated key (Branch A). A fails because a tool that raises its own
`anthropic/maxResultSizeChars` bypasses the host default (Branch B). D is an unreliable guide
(Branch B).

</details>

## Q4

A reviewer calls a server safe because its descriptions warn about dangerous and large operations.
Every operation is exposed, none gated, one read tool raised its ceiling to 200,000 chars. Correct
statement?

A. Safe, clear descriptions suffice. B. Unsafe, only the surface, the gate, and the output caps
govern the boundary, and none are in place. C. Safe once `descriptionEnforcement: true` is on. D.
Safe enough, the model usually respects descriptions.

<details>
<summary>Reveal answer</summary>

Answer: B. Rationale: C is a fabricated switch (Branch A). A and D treat a guide as a control, the
core error the lab corrects (Branch B).

</details>

## Q5

Server X: fifteen operations, several unused, no gates, no output caps. Server Y: only needed
operations, sensitive ones gated, output capped below the host limit. Constraint is trust and
bounded context. Which wins?

A. X, for coverage. B. Y, because a narrow surface, gating, and bounded output match the constraint.
C. Neither, quality is set by an `mcpLint` step. D. Either, the host output limit makes per-tool caps
redundant.

<details>
<summary>Reveal answer</summary>

Answer: B. Rationale: C is a fabricated build step (Branch A). A serves coverage, not the stated
constraint (Branch B). D is wrong because a tool that raises its own ceiling floods context despite
the host limit (Branch B).

</details>
