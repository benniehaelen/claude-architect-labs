# Answers: lab 07 human escalation patterns

Each answer names the correct option, then labels every distractor by branch (A fabricated feature,
B valid but suboptimal) and states why it fails. The pattern to internalize: feature fluency removes
the Branch A fabrications, and architectural judgment picks the winner among the Branch B survivors
(see `../../DISTRACTOR_TAXONOMY.md`).

## Question 1: correct answer is B

B escalates before the action on the must-escalate triggers, so a human reviews the high-impact request
before it runs. Pre-action timing is the property that stops an irreversible action.

- A is Branch A, fabricated feature. There is no `auto_escalate: true` switch that escalates
  high-impact actions for you. The convenient-sounding flag is the tell, and it would not fix the
  timing on its own.
- C is Branch B, valid but suboptimal. A faster post-action queue still reviews the closure after it
  ran. Right mechanism, wrong point in the flow.
- D is Branch B, valid but suboptimal. A prompt instruction guides but does not guarantee the agent
  stops before acting. Wrong layer for a must-hold stop.

## Question 2: correct answer is A

A expands the triggers to cover every must-escalate case, which closes the coverage gap that let the
out-of-policy exception and the explicit human request through.

- B is Branch A, fabricated feature. There is no `coverage: "all"` setting that defines the
  must-escalate cases for you. Coverage is a design property, not a switch.
- C is Branch B, valid but suboptimal. A prompt instruction guides but does not guarantee that every
  out-of-policy request escalates. Wrong layer for coverage.
- D is Branch B, valid but suboptimal. Random spot checks catch some misses by luck, but a must-escalate
  case cannot rest on sampling.

## Question 3: correct answer is A

A routes escalations to a defined human queue and holds when the route is unavailable, which gives the
escalation somewhere to go and fails safe when it cannot be delivered.

- B is Branch A, fabricated feature. There is no `escalation_target: "auto"` that picks a route for you.
  The route is a design decision.
- C is Branch B, valid but suboptimal. Logging that a request was flagged does not deliver it to a
  human, and proceeding by default handles it anyway. A flag in the logs is not an escalation.
- D is Branch B, valid but suboptimal. Holding every request, including routine reads, over-escalates
  and stalls the agent. The fix is a route plus a hold default on the triggered cases, not a universal
  hold.

## Question 4: correct answer is B

B identifies that pre-action escalation with full coverage, a route, and a hold default is exactly what
the reach-a-human-before-the-action constraint requires.

- A is Branch B, valid but suboptimal. Speed is a real benefit, but escalating after the action does not
  meet the constraint, because the irreversible action has already run.
- C is Branch A, fabricated feature. There is no `escalationLint` build step that sets escalation
  quality. Quality is a design property, not a tool that appears by naming it.
- D is Branch B, valid but suboptimal. Agents do not reliably learn the right escalation boundary within
  a task, and a must-hold escalation cannot rest on it.

## Question 5: correct answer is B

B states the thesis precisely: a prompt guides but does not guarantee coverage, timing, or delivery, so
a must-escalate request can still be handled without a policy control.

- A is Branch B, valid but suboptimal in the sense that it is a coherent but wrong position. Instructing
  the agent to defer is helpful and insufficient.
- C is Branch A, fabricated feature. There is no `require_human_review: true` switch that forces
  deferral. The real control is a policy with coverage, timing, a route, and a safe default.
- D is Branch B, valid but suboptimal. "Usually defers" is not a guarantee, and a must-hold escalation
  cannot depend on usual behavior.
