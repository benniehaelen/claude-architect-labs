# Questions: lab 07 human escalation patterns

Five scenario questions. Each carries at least one Branch A distractor (a fabricated feature) and at
least two Branch B distractors (valid but suboptimal under the stated constraints). See
`../../DISTRACTOR_TAXONOMY.md`. Answers and branch labels are in `answers.md`. Do not read the
answers until you have committed to a choice.

## Question 1

A support agent escalates to a human only when it has already taken an action and something looks
wrong. A high-impact account closure runs before any human reviews it. What is the best fix?

A. Set `auto_escalate: true` so the platform escalates high-impact actions automatically.
B. Escalate before the action (pre-action) on the must-escalate triggers, so a human reviews the
   high-impact request before it runs.
C. Keep post-action escalation but add a faster review queue so humans catch problems sooner.
D. Add a system-prompt instruction telling the agent to be careful with account closures.

## Question 2

An escalation policy triggers only on high impact. An out-of-policy exception and an explicit customer
request for a human are both handled automatically. What is the soundest fix?

A. Expand the triggers to cover every must-escalate case: out of policy, high impact, low confidence,
   and an explicit human request.
B. Add a `coverage: "all"` setting so the policy escalates every request that could need a human.
C. Tell the agent in its prompt to escalate anything that feels out of policy.
D. Keep the single trigger but escalate a random sample of other requests for spot checks.

## Question 3

A policy correctly identifies which requests must escalate, but it has no route to a human and its
default is to proceed. The flagged requests are handled anyway. What is the correct fix?

A. Route escalations to a defined human queue and set the default to hold when the route is
   unavailable.
B. Set `escalation_target: "auto"` so the platform picks a route automatically.
C. Keep proceeding by default, since the requests were at least flagged in the logs.
D. Hold every request by default, including routine reads, until a human clears it.

## Question 4

Two escalation policies are proposed. Policy X escalates after the action, covers only high impact, and
proceeds by default. Policy Y escalates before the action, covers every must-escalate case, routes to a
human queue, and holds by default. Both are real. Under a constraint that a must-escalate request
reaches a human before any irreversible action, which is better and why?

A. Policy X, because escalating after the action keeps the agent fast and only interrupts on real
   problems.
B. Policy Y, because pre-action escalation with full coverage, a route, and a hold default is what the
   constraint requires.
C. Neither, because escalation quality is set by the `escalationLint` build step rather than by design.
D. Either, because the agent will learn which requests to escalate over time.

## Question 5

A reviewer says escalation is handled because the agent's system prompt tells it to defer sensitive
requests to a human. Sensitive requests still get handled automatically. Which statement is correct?

A. Escalation is handled, because instructing the agent to defer is sufficient.
B. Escalation is not handled, because a prompt guides but does not guarantee coverage, timing, or
   delivery, so a must-escalate request can still be handled without a policy control.
C. Escalation is handled once `require_human_review: true` is set to force deferral.
D. Escalation is handled well enough, because the agent usually defers when instructed.
