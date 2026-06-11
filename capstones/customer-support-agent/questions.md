# Questions: customer support agent capstone

Five integrative scenario questions. Unlike the lab question sets, these require reasoning across more
than one lab at once: the observable loop (lab 01), the tool catalog and gate (lab 02), and the
escalation policy (lab 07). Each carries at least one Branch A distractor (a fabricated feature) and at
least two Branch B distractors (valid but suboptimal). See `../../DISTRACTOR_TAXONOMY.md`. Answers and
branch labels are in `answers.md`. Do not read the answers until you have committed to a choice.

## Question 1

In the composed support agent, an authorized and confirmed order cancellation arrives. The escalation
policy treats high impact as a trigger, and the cancellation is high impact. What should happen?

A. Escalate it to a human, because every high-impact action must reach a person.
B. Let the permission gate govern it, because an authorized and confirmed action is governed by the
   gate rather than escalated, and escalation is reserved for unauthorized or out-of-policy
   high-impact actions.
C. Set `autoApproveAuthorized: true` so authorized actions skip both the gate and escalation.
D. Block it until a second agent confirms, since one confirmation is not enough for a high-impact
   action.

## Question 2

An unauthorized, out-of-policy request to close an account arrives. The team wants to guarantee it
never executes without a human. Which combination guarantees that?

A. A pre-action escalation policy that covers out-of-policy and high-impact requests, plus a gated
   destructive tool, so both layers stop the closure before it runs.
B. A post-action escalation policy plus an audit log, so the closure is reviewed right after it runs.
C. A `requireHuman: true` flag on the close_account tool that the platform enforces automatically.
D. A strong system-prompt instruction telling the agent to always escalate account closures.

## Question 3

In the naive design, a customer asks to speak to a human about a routine order. The agent neither
escalates nor handles it safely: it routes the request to a destructive-capable tool that runs ungated.
Which two failures compounded?

A. The escalation policy missed the explicit-human case, and the ambiguous, ungated catalog routed a
   read to a destructive-capable tool.
B. The model was not given enough context, and the temperature was set too high.
C. The `humanRequestRouting` setting was disabled, and the catalog lacked a `safeRead` flag.
D. The loop ran too many steps, and the summary dropped the request.

## Question 4

A reviewer says the support agent is safe because its escalation policy is sound. The catalog is the
sprawling, ungated one. Which statement is correct?

A. It is safe, because a sound escalation policy is sufficient on its own.
B. It is not safe, because escalation handles the human handoff but the ungated catalog still lets a
   routine request execute a destructive-capable tool, so the catalog and gate must also be correct.
C. It is safe once `escalationOverridesCatalog: true` is set so escalation supersedes tool routing.
D. It is safe enough, because most requests do not hit the dangerous tools.

## Question 5

The team wants every support decision to be auditable after an incident. The agent composes a sound
catalog, a gated set of tools, and a pre-action escalation policy, but records nothing. What is the
best addition?

A. Record a structured trace of each request's escalation check, routing, gate decision, and execution
   or handoff, so the run is auditable.
B. Enable `autoAudit: true` so the platform reconstructs the decisions from the model's output.
C. Add a system-prompt instruction telling the agent to explain its decisions in its replies.
D. Keep the raw model transcript, since it already contains everything that happened.
