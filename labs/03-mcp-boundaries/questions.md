# Questions: lab 03 MCP boundaries

Five scenario questions. Each carries at least one Branch A distractor (a fabricated feature) and at
least two Branch B distractors (valid but suboptimal under the stated constraints). See
`../../DISTRACTOR_TAXONOMY.md`. Answers and branch labels are in `answers.md`. Do not read the
answers until you have committed to a choice.

## Question 1

An MCP server for an internal knowledge assistant exposes, among other things, a raw SQL tool and a
resource that lists stored credentials. The assistant only ever needs document search and a bounded
export. The team wants to narrow the surface to what the assistant needs. What is the best change?

A. Add a line to the assistant's system prompt telling it never to call the raw SQL tool or the
   secrets resource.
B. Scope the server so it exposes only the operations the assistant needs, using `oauth.scopes` to
   pin the granted scope set and approving only that server at the project level.
C. Set `mcpScope: "auto"` on the server so Claude Code prunes unused operations automatically.
D. Leave the surface as is but rename the dangerous operations so the model is less likely to pick
   them.

## Question 2

A CI/CD MCP server exposes a `delete_environment` operation with no gate. An unauthorized request
deletes a production environment with no confirmation and no escalation. Where must the stop be
enforced?

A. In the operation's description, by stating that authorization is required.
B. In a runtime gate at the server that requires authorization and confirmation and escalates an
   unauthorized request.
C. By setting the operation's `destructive: true` flag, which makes Claude Code auto-confirm it.
D. In a post-action audit log that records environment deletions after they happen.

## Question 3

An MCP tool returns a full corpus export of about 120,000 tokens in a single call, filling the
conversation context and pushing out earlier information. The host default output limit is 25,000
tokens. What is the soundest fix?

A. Trust the host `MAX_MCP_OUTPUT_TOKENS` default to cap the result, since 25,000 is below the
   payload.
B. Bound the export at the server so the operation returns a slice under the host limit, for example
   by keeping its declared result size below the cap rather than raising it.
C. Enable `autoTruncate: true` in `settings.json` so any oversized MCP result is trimmed to fit.
D. Tell the assistant in its prompt to ask the server for a smaller export.

## Question 4

A reviewer says the MCP server is safe because its tool descriptions clearly warn the model which
operations are dangerous and how large the results can be. The server exposes every operation, none
are gated, and one read tool raises its own output ceiling to 200,000 characters. Which statement is
correct?

A. The server is safe, because clear descriptions are sufficient to prevent misuse and overflow.
B. The server is unsafe, because a description guides selection but only the exposed surface, the
   gate, and the output caps govern what crosses the boundary, and none of those are in place.
C. The server is safe once `descriptionEnforcement: true` is enabled to make descriptions binding.
D. The server is safe enough, because the model usually respects tool descriptions.

## Question 5

Two MCP server designs are proposed for the same integration. Server X exposes fifteen operations,
including several the agents never use, with no gates and no per-tool output caps. Server Y exposes
only the needed operations, gates the write and destructive ones, and caps each operation's output
below the host limit. Both are real and both connect. Under a constraint of trust and bounded
context, which is better and why?

A. Server X, because more operations give the agents more coverage and flexibility.
B. Server Y, because a narrow surface, gated high-impact operations, and bounded output are exactly
   what the trust and context constraint asks for.
C. Neither, because boundary quality is set by the `mcpLint` build step rather than by design.
D. Either, because Claude Code's host output limit makes the per-tool caps redundant.
