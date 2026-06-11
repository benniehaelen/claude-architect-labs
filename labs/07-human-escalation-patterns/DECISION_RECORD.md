# Decision record: lab 07 human escalation patterns

## Scenario

A customer support agent fields requests and must hand the right ones to a human. The request set mixes
an out-of-policy exception the agent is not authorized to grant, a high-impact account closure, an
explicit request for a human, and a routine order-status read. The policy in `bad_version` escalates
only on high impact, escalates after the agent has already acted, and proceeds by default. The result
is that the out-of-policy exception and the explicit human request are handled automatically and the
account closure runs before any human sees it.

## Constraints

The binding constraint is that a must-escalate request reaches a human before an irreversible action,
and that the system fails safe when the handoff cannot be delivered. Throughput matters, but an
escalation that arrives after the action, or never arrives, is the failure to avoid.

- Latency: escalating a routine read would add needless delay, so the policy must not over-escalate.
- Cost: a human handoff costs human time, so escalation is reserved for the cases that need it.
- Reliability: every must-escalate case must reach a human, governed by the policy rather than by the
  model choosing well.
- Security: a high-impact or out-of-policy action must be stopped before it runs, not reviewed after.
- Data sensitivity: an out-of-policy exception can expose data or money, so it must reach a human.
- Human review: the escalation route is the human review path itself, and it must be defined and
  reachable.
- Operational owner: the team that owns the agent owns the triggers, the routing target, and the
  fail-safe default.

## Design chosen

A sound policy (in `escalation_policy_good.json`) with four properties, each a runtime control.

Coverage. The triggers catch every must-escalate case: out of policy, high impact, low confidence, and
an explicit request for a human. A trigger gap is a silent miss, so coverage is the first property.

Timing. Escalation happens before the action (pre-action), so a high-impact or out-of-policy request
reaches a human before anything irreversible runs. A policy that acts first and escalates only on
trouble has already done the harm.

Delivery. The policy routes to a defined human queue, so an escalation has somewhere to go. An
escalation with no route is not an escalation.

Fail-safe default. When escalation cannot be delivered, the default holds rather than proceeds, so an
undeliverable handoff stops the request instead of letting it through.

The decisive insight, visible in the runners, is that the weak policy and the sound policy use the
exact same engine. Only the policy differs. A request reaches a human, or does not, because of the
policy's coverage, timing, route, and default, not because the agent was told to be careful.

## Alternatives rejected and why

Escalating after the action and reviewing what the agent did. Post-action review is real and useful for
learning, but it does not stop a high-impact action, because the action has already run. Wrong point in
the flow for a must-hold stop.

Covering only the high-impact case and trusting the agent to handle the rest. This misses the
out-of-policy exception and the explicit human request, both of which must reach a human. Partial
coverage is a silent miss on the cases it omits.

Identifying the right escalations but routing them nowhere, with a default that proceeds. This is the
no-route policy in the eval. It correctly flags the escalations and then drops them, because there is
no route and the default is to proceed. Correct identification, no delivery, so the request proceeds as
if it had been handled.

Instructing the agent in its prompt to escalate sensitive requests. A prompt is a guide. It raises the
chance of escalation but does not guarantee coverage, timing, or delivery, so a must-escalate request
can still be handled. A must-hold escalation belongs in a policy control.

## Failure modes

Summarized here and detailed in `FAILURE_MODES.md`: a coverage gap that handles a must-escalate request,
a late escalation that runs the action first, an escalation routed nowhere, a fail-open default that
proceeds when the handoff cannot be delivered, and over-escalation of routine requests.

## Controls

- Enforced by prompt: a system-prompt instruction to defer on sensitive requests, which guides behavior.
  Helpful, not load-bearing for coverage, timing, or delivery.
- Enforced by runtime: the trigger set (coverage), the pre-action timing, the routing target, and the
  hold default. These are the controls that make the escalation hold. See `../../ENFORCEMENT_LAYER.md`.
- Observable: the per-request disposition (handle, escalate, or hold), the triggers that fired, the
  timing, and the route, plus the missed, late, and dropped flags.
- Auditable: each request records its disposition and whether it was missed, escalated late, or dropped.

## Governance and escalation (mandatory)

For this lab the escalation decision is the subject, not a cross-cut, so this section states the design
directly.

- Where automation stops: the policy stops automatically before any out-of-policy, high-impact,
  low-confidence, or human-requested action and routes it to a human, while routine in-policy reads
  proceed.
- Human-handoff path: a triggered request escalates to the defined human review queue before the action
  runs, so a person decides.
- Fail-safe behavior (fails safely rather than silently): when escalation cannot be delivered the
  default holds the request rather than proceeding. The sound policy reaches a human before acting,
  while the weak policy misses two escalations and runs a high-impact action first, and the no-route
  policy drops the escalations it correctly identified. The contrast, same request set and same engine,
  opposite outcome, is the lesson: escalation is a policy of coverage, timing, delivery, and a safe
  default, not a prompt instruction to be careful.

## Exam angle

See `EXAM_ANGLE.md`. This lab serves the Agentic Architecture and Orchestration domain (27%) with
Context Management and Reliability (15%) as secondary. The transferable judgment is that an escalation
policy must reach a human before the irreversible action, cover every must-escalate case at runtime
rather than by prompt, and fail safe when the handoff cannot be delivered.
