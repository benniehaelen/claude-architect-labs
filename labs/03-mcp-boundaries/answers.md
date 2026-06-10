# Answers: lab 03 MCP boundaries

Each answer names the correct option, then labels every distractor by branch (A fabricated feature,
B valid but suboptimal) and states why it fails. The pattern to internalize: feature fluency removes
the Branch A fabrications, and architectural judgment picks the winner among the Branch B survivors
(see `../../DISTRACTOR_TAXONOMY.md`).

## Question 1: correct answer is B

B narrows the surface at the server, exposing only what the assistant needs and pinning the granted
scope with `oauth.scopes`. That is the real, supported way to restrict a server to an approved
subset (see `../../VERIFIED.md`), and it removes the dangerous operations from reach entirely.

- A is Branch B, valid but suboptimal. A prompt instruction is real and mildly helpful, but it lives
  in the guide layer and cannot stop a published operation from being called. The surface stays as
  wide as before.
- C is Branch A, fabricated feature. There is no `mcpScope: "auto"` setting that auto-prunes unused
  operations. The convenient-sounding switch is the tell.
- D is Branch B, valid but suboptimal. Renaming changes the description, not the surface. The
  dangerous operations are still exposed and reachable.

## Question 2: correct answer is B

B enforces the stop in a runtime gate at the server, which requires authorization and confirmation
and escalates an unauthorized request. That is the layer where a must-hold action belongs.

- A is Branch B, valid but suboptimal. Stating the requirement in the description is real but does
  not govern execution. Wrong layer for the requirement.
- C is Branch A, fabricated feature. There is no `destructive: true` flag that makes the host
  auto-confirm a deletion. Auto-confirming a destructive action would be the opposite of safe anyway.
- D is Branch B, valid but suboptimal. An audit log is real and useful, but it records the deletion
  after it has already happened. Right mechanism, wrong point in the flow.

## Question 3: correct answer is B

B bounds the export at the server so the operation returns a slice under the host limit. The server
controls what it returns, and keeping its declared result size below the cap is what stops the flood
at the source.

- A is Branch B, valid but suboptimal. The host `MAX_MCP_OUTPUT_TOKENS` default is real, but it
  protects only tools that do not raise their own ceiling. A tool that sets a large
  `anthropic/maxResultSizeChars` bypasses the default for its text content, so trusting the host cap
  is not reliable when the server can raise its own limit (see `../../VERIFIED.md`).
- C is Branch A, fabricated feature. There is no `autoTruncate: true` settings key that trims any
  oversized MCP result. The real controls are the host token limit and the server-side caps.
- D is Branch B, valid but suboptimal. A prompt instruction is a guide and cannot guarantee a
  bounded payload. The bound belongs at the server, not in a request the model may or may not make.

## Question 4: correct answer is B

B states the thesis precisely: a description guides selection, but the exposed surface, the gate, and
the output caps are what govern what crosses the boundary, and none of those are in place.

- A is Branch B, valid but suboptimal in the sense that it is a coherent but wrong position. Clear
  descriptions are helpful and insufficient. They cannot stop execution or overflow.
- C is Branch A, fabricated feature. There is no `descriptionEnforcement: true` switch that makes
  descriptions binding. Descriptions are guidance by nature.
- D is Branch B, valid but suboptimal. "Usually respects" is not a guarantee, and a must-hold trust
  and context property cannot depend on usual behavior.

## Question 5: correct answer is B

B identifies that a narrow surface, gated high-impact operations, and bounded output are exactly what
the trust and bounded-context constraint asks for.

- A is Branch B, valid but suboptimal. More operations and more flexibility is a real tradeoff that
  serves coverage, not the trust and context constraint the question binds on.
- C is Branch A, fabricated feature. There is no `mcpLint` build step that sets boundary quality.
  Quality is a design property, not a tool that appears by naming it.
- D is Branch B, valid but suboptimal. The host output limit is real, but it does not make per-tool
  caps redundant: a tool that raises its own ceiling past the host limit floods context anyway, which
  is exactly what Server X's 200,000-character read tool would do.
