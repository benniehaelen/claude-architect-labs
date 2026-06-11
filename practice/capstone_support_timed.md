# Timed set: customer support agent capstone

Five questions at two minutes each. These are integrative: they require composing the observable loop
(lab 01), the tool catalog and gate (lab 02), and the escalation policy (lab 07). Each answer is hidden
inside a collapsible block, so commit to a choice before you expand "Reveal answer." Each question
carries a Branch A fabricated-feature distractor and at least one Branch B valid-but-suboptimal
distractor. Full reasoning lives in the capstone's `answers.md`. Source: customer support capstone.

## Q1

An authorized, confirmed high-impact cancellation arrives, and the policy treats high impact as a
trigger. What should happen?

A. Escalate it, every high-impact action goes to a human. B. Let the gate govern it, escalation is for
unauthorized or out-of-policy high-impact actions. C. Set `autoApproveAuthorized: true`. D. Block until
a second agent confirms.

<details>
<summary>Reveal answer</summary>

Answer: B. Rationale: C is a fabricated switch (Branch A). A escalates a legitimate authorized action
the gate already governs (Branch B). D adds cost the constraint did not ask for (Branch B).

</details>

## Q2

An unauthorized, out-of-policy account closure must never execute without a human. What guarantees it?

A. Pre-action escalation covering out-of-policy and high-impact, plus a gated destructive tool. B.
Post-action escalation plus an audit log. C. A `requireHuman: true` tool flag. D. A system-prompt
instruction to escalate closures.

<details>
<summary>Reveal answer</summary>

Answer: A. Rationale: C is a fabricated flag (Branch A). B reviews after it runs (Branch B). D guides
but does not guarantee (Branch B).

</details>

## Q3

A customer asks for a human about a routine order. The naive agent neither escalates nor handles it
safely, routing to a destructive-capable ungated tool. Which two failures compounded?

A. The policy missed the explicit-human case, and the ambiguous ungated catalog routed a read to a
destructive-capable tool. B. Not enough context and high temperature. C. `humanRequestRouting` disabled
and no `safeRead` flag. D. Too many loop steps and a lossy summary.

<details>
<summary>Reveal answer</summary>

Answer: A. Rationale: C is a fabricated pair (Branch A). B misdiagnoses as context or sampling (Branch
B). D misattributes to lab 06 concerns (Branch B).

</details>

## Q4

A reviewer says the agent is safe because the escalation policy is sound. The catalog is sprawling and
ungated. Correct statement?

A. Safe, a sound policy suffices. B. Not safe, the ungated catalog still runs a destructive-capable
tool on a routine request, so catalog and gate must be correct too. C. Safe once
`escalationOverridesCatalog: true` is set. D. Safe enough, dangerous tools are rarely hit.

<details>
<summary>Reveal answer</summary>

Answer: B. Rationale: C is a fabricated setting (Branch A). A treats one sound layer as a sound system
(Branch B). D rests safety on rarity (Branch B).

</details>

## Q5

The team wants every decision auditable after an incident. The agent has a sound catalog, gated tools,
and a pre-action policy, but records nothing. Best addition?

A. Record a structured trace of escalation, routing, gate, and execution per request. B. Enable
`autoAudit: true`. C. Prompt the agent to explain its decisions in replies. D. Keep the raw model
transcript.

<details>
<summary>Reveal answer</summary>

Answer: A. Rationale: B is a fabricated switch (Branch A). C produces narrative, not a structured trail
(Branch B). D is noisy and not decision-structured (Branch B).

</details>
