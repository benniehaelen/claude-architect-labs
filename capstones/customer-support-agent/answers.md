# Answers: customer support agent capstone

Each answer names the correct option, then labels every distractor by branch (A fabricated feature,
B valid but suboptimal) and states why it fails. These questions reward composing the labs: feature
fluency removes the Branch A fabrications, and the integration judgment across labs 01, 02, and 07
picks the winner among the Branch B survivors (see `../../DISTRACTOR_TAXONOMY.md`).

## Question 1: correct answer is B

B states the integration refinement: an authorized and confirmed action is governed by the permission
gate rather than escalated, and escalation is reserved for unauthorized or out-of-policy high-impact
actions. This is the judgment that appears only when lab 02 and lab 07 are composed.

- A is Branch B, valid but suboptimal. Escalating every high-impact action is safe but wasteful, and it
  sends a legitimate authorized action to a human, which the gate already governs.
- C is Branch A, fabricated feature. There is no `autoApproveAuthorized: true` switch, and skipping
  both the gate and escalation would remove the very control the action needs.
- D is Branch B, valid but suboptimal. Requiring a second confirmation is a real control for some
  actions, but the scenario's gate already authorizes and confirms, so this adds cost without the
  constraint asking for it.

## Question 2: correct answer is A

A combines a pre-action escalation policy that covers the out-of-policy and high-impact case with a
gated destructive tool, so both layers stop the closure before it runs. Defense in depth across lab 07
and lab 02 is what guarantees it.

- B is Branch B, valid but suboptimal. A post-action policy plus an audit log reviews the closure after
  it has already executed. Right mechanism, wrong point in the flow.
- C is Branch A, fabricated feature. There is no `requireHuman: true` tool flag the platform enforces.
  The real controls are the escalation policy and the gate.
- D is Branch B, valid but suboptimal. A system-prompt instruction guides but does not guarantee, so a
  must-hold stop cannot depend on it.

## Question 3: correct answer is A

A names the two compounding failures precisely: the escalation policy missed the explicit-human case
(lab 07 coverage gap), and the ambiguous, ungated catalog routed a read to a destructive-capable tool
(lab 02 ambiguity plus missing gate). The capstone shows these stacking.

- B is Branch B, valid but suboptimal in the sense that it is a plausible but wrong diagnosis. The
  failure is structural, not a context or sampling problem.
- C is Branch A, fabricated feature. There is no `humanRequestRouting` setting and no `safeRead` flag.
  The convenient-sounding switches are the tell.
- D is Branch B, valid but suboptimal. Step count and summarization are lab 06 concerns and not what
  happened here. Misattributed failure.

## Question 4: correct answer is B

B states the composition thesis: escalation handles the human handoff, but the ungated catalog still
lets a routine request execute a destructive-capable tool, so the catalog and gate must also be
correct. A sound policy does not rescue a sprawling, ungated catalog.

- A is Branch B, valid but suboptimal in the sense that it is a coherent but wrong position. One sound
  layer is not a sound system.
- C is Branch A, fabricated feature. There is no `escalationOverridesCatalog: true` setting that makes
  escalation supersede routing. The layers are complementary, not substitutes.
- D is Branch B, valid but suboptimal. "Most requests do not hit the dangerous tools" is a frequency
  argument, and a safety property cannot rest on the dangerous path being rare.

## Question 5: correct answer is A

A records a structured trace of each request's escalation check, routing, gate decision, and execution
or handoff, which is the lab 01 observability control that makes the composed system auditable.

- B is Branch A, fabricated feature. There is no `autoAudit: true` switch that reconstructs decisions.
  Observability is something you build into the loop, not a flag.
- C is Branch B, valid but suboptimal. Asking the agent to explain itself in replies is guidance, and a
  narrative reply is not a structured, reliable audit trail.
- D is Branch B, valid but suboptimal. A raw transcript is noisy and not structured around the
  decisions, so it does not give a clean audit of escalation, routing, and gating.
