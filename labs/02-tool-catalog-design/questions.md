# Questions: lab 02 tool catalog design

Five scenario questions. Each carries at least one Branch A distractor (a fabricated feature) and
at least two Branch B distractors (valid but suboptimal under the stated constraints). See
`../../DISTRACTOR_TAXONOMY.md`. Answers and branch labels are in `answers.md`. Do not read the
answers until you have committed to a choice.

## Question 1

A support agent has three tools whose descriptions all plausibly cover "look up an order," and it
frequently calls the wrong one. The team wants the right tool to be the obvious choice. What is the
best change?

A. Add a fourth, more general lookup tool so there is always one that fits.
B. Collapse the overlap so each intent maps to exactly one tool with a precise description.
C. Set `toolSelection: "strict"` in the agent config so the model is forced to pick correctly.
D. Add a sentence to each tool description telling the model when not to use it.

## Question 2

One tool, `manage_order`, can look up, cancel, or refund an order. The agent calls it for a routine
status check. Leadership is worried that a routine request now carries the power to cancel. What is
the soundest fix?

A. Keep the tool but add a warning in its description that cancellation is destructive.
B. Split the tool by effect, so the read path and the cancel path are separate tools, and gate the
   cancel tool.
C. Enable `requireConfirm: all` in `settings.json` so every tool call is confirmed.
D. Leave the tool as is but instruct the agent in its system prompt to never cancel unless asked.

## Question 3

A destructive `close_account` tool has no permission gate. An unauthorized request closes an
account with no confirmation and no escalation. Where must the stop be enforced?

A. In the tool's description, by stating that authorization is required.
B. In a runtime permission gate that requires authorization and confirmation and escalates an
   unauthorized request.
C. By setting the tool's `dangerous: true` flag, which makes the platform auto-confirm it.
D. In a post-action audit log that records account closures after they happen.

## Question 4

Two catalogs are proposed. Catalog X has fifteen tools with several overlapping intents. Catalog Y
has eight tools, each mapping to one intent, with write and destructive tools gated. Both are real
and both work. Under a constraint of safe, unambiguous selection, which is better and why?

A. Catalog X, because more tools give the agent more coverage and flexibility.
B. Catalog Y, because one-intent-per-tool removes ambiguity and gating governs the high-impact
   actions, which is what the constraint asks for.
C. Neither, because catalog quality is set by the `catalogLint` build step rather than by design.
D. Either, because the agent will learn which tool to use from experience.

## Question 5

A reviewer says the catalog is safe because every dangerous tool's description warns the model to
be careful. The runtime has no gate. Which statement is correct?

A. The catalog is safe, because a clear description is sufficient to prevent misuse.
B. The catalog is unsafe, because a description guides selection but only a runtime gate governs
   execution, and there is no gate.
C. The catalog is safe once `descriptionEnforcement: true` is enabled to make descriptions binding.
D. The catalog is safe enough, because the model usually follows tool descriptions.
