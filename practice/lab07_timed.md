# Timed set: lab 07 human escalation patterns

Five questions at two minutes each. Train recognition speed, not derivation. Each answer is hidden
inside a collapsible block, so commit to a choice before you expand "Reveal answer." Each question
carries a Branch A fabricated-feature distractor and at least one Branch B valid-but-suboptimal
distractor. Full reasoning lives in the lab's `answers.md`. Source lab: 07. Domains: Agentic
Architecture and Orchestration, Context Management and Reliability.

## Q1

An agent escalates only after acting, so a high-impact account closure runs before any human reviews
it. Best fix?

A. Set `auto_escalate: true`. B. Escalate before the action on the must-escalate triggers. C. Keep
post-action escalation but add a faster queue. D. Prompt the agent to be careful with closures.

<details>
<summary>Reveal answer</summary>

Answer: B. Rationale: A is a fabricated switch (Branch A). C still reviews after the action runs (Branch
B). D guides but does not stop the action (Branch B).

</details>

## Q2

A policy triggers only on high impact, so an out-of-policy exception and an explicit human request are
handled automatically. Soundest fix?

A. Expand triggers to cover out of policy, high impact, low confidence, and explicit human request. B.
Set `coverage: "all"`. C. Prompt the agent to escalate anything out of policy. D. Spot-check a random
sample.

<details>
<summary>Reveal answer</summary>

Answer: A. Rationale: B is a fabricated setting (Branch A). C guides but does not guarantee coverage
(Branch B). D rests a must-escalate case on sampling (Branch B).

</details>

## Q3

A policy flags the right escalations but has no route and proceeds by default, so they are handled
anyway. Correct fix?

A. Route to a defined human queue and hold when the route is unavailable. B. Set `escalation_target:
"auto"`. C. Keep proceeding, the requests were logged. D. Hold every request, including routine reads.

<details>
<summary>Reveal answer</summary>

Answer: A. Rationale: B is a fabricated value (Branch A). C logs but never delivers and proceeds anyway
(Branch B). D over-escalates and stalls the agent (Branch B).

</details>

## Q4

Policy X: escalate after the action, cover only high impact, proceed by default. Policy Y: escalate
before the action, full coverage, routed, hold by default. Constraint: reach a human before any
irreversible action. Which wins?

A. X, faster and only interrupts on real problems. B. Y, pre-action plus coverage plus route plus hold
default. C. Neither, quality is set by an `escalationLint` step. D. Either, the agent learns over time.

<details>
<summary>Reveal answer</summary>

Answer: B. Rationale: C is a fabricated build step (Branch A). A acts before the human sees it (Branch
B). D rests the boundary on unreliable in-task learning (Branch B).

</details>

## Q5

A reviewer says escalation is handled because the prompt tells the agent to defer sensitive requests.
Sensitive requests still get handled. Correct statement?

A. Handled, instructing the agent to defer suffices. B. Not handled, a prompt guides but does not
guarantee coverage, timing, or delivery without a policy control. C. Handled once `require_human_review:
true` is set. D. Handled well enough, the agent usually defers.

<details>
<summary>Reveal answer</summary>

Answer: B. Rationale: C is a fabricated switch (Branch A). A and D treat a guide as a control, the core
error the lab corrects (Branch B).

</details>
