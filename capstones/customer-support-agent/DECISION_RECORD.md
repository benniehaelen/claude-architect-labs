# Decision record: customer support agent capstone

## Scenario

A customer support agent handles a session of four requests: a routine order lookup, an authorized
and confirmed order cancellation, an unauthorized out-of-policy account closure, and an explicit
request for a human. The capstone composes three labs into one system, so the design must satisfy all
three at once: the loop must be observable (lab 01), the catalog must route to the right tool and gate
the dangerous ones (lab 02), and the escalation policy must hand the right requests to a human before
the agent acts (lab 07). The naive design in `bad_version` composes the three labs' failure modes
instead, and the unauthorized account closure executes before any human sees it.

## Constraints

The binding constraint is that the composition is correct end to end: a failure in any one layer
compounds into a system failure. Each request must reach the right disposition (handled, escalated, or
blocked) through the right layer, and the run must be auditable.

- Latency: the layered checks add little, and they replace the unsafe shortcuts the naive design takes.
- Cost: an ambiguous catalog causes wasted or wrong tool calls, and an over-eager escalation wastes
  human time, so the design must be precise in both directions.
- Reliability: the routine and authorized requests must be handled deterministically, and the
  must-escalate requests must reach a human every time.
- Security: an unauthorized high-impact action must be stopped before it runs, by escalation and by
  the gate.
- Data sensitivity: an account closure and a cancellation are high-impact actions whose execution must
  be governed.
- Human review: the escalation route is the human path, and it must be reached before the action.
- Operational owner: the team that owns the agent owns the catalog, the gate, the escalation policy,
  and the observability.

## Design chosen

The composed design (in `support_design_good.json`) wires the three controls in order, reusing the lab
engines directly.

First, the escalation policy decides a human handoff before any tool runs. The sound policy covers
out-of-policy, high-impact, low-confidence, and explicit-human cases, escalates pre-action, and routes
to a human queue (lab 07). The unauthorized account closure and the explicit request for a human are
escalated before the agent touches a tool.

Second, the catalog makes the right tool obvious and the gate governs execution. The deliberate
catalog maps each intent to one tool and gates every write and destructive tool (lab 02). The routine
read passes the gate, and the authorized and confirmed cancellation is governed by the gate.

Third, the flow is observable. Each request records a trace of its escalation check, routing, gate
decision, and execution or handoff (lab 01), so the run is auditable.

The composition adds one refinement that neither lab states alone: an authorized, confirmed high-impact
action is governed by the gate, not escalated. Lab 07 escalates every high-impact request, but in the
composed system the cancellation is a legitimate authorized action, so it proceeds to the gate rather
than to a human. An unauthorized high-impact action, an out-of-policy request, or an explicit request
for a human still escalates before the action. This is the integration judgment the capstone teaches.

The decisive insight, visible in the runners, is that the naive design and the composed design use the
exact same engine. Only the catalog, the policy, and the observability flag differ. The system is safe
or unsafe because of how the three layers are composed, not because of the workload.

## Alternatives rejected and why

Escalating every high-impact request, including the authorized cancellation. This is lab 07 applied
without the gate. It is safe but wasteful: it sends a legitimate, authorized action to a human, which
adds latency and trains reviewers to rubber-stamp. The composed design defers an authorized, confirmed
action to the gate.

Using a strong escalation policy but the sprawling, ungated catalog. The policy would escalate the
unauthorized closure, but the ambiguous catalog still routes a routine read to a destructive-capable,
ungated tool, so a benign request can run a dangerous action. The catalog must be deliberate for the
gate to have anything to govern.

Composing the controls but skipping observability. The system might behave correctly and still be
unauditable, so an incident cannot be explained and a silent regression cannot be caught. The trace is
the control that makes the other two reviewable.

## Failure modes

Summarized here and detailed across the source labs' `FAILURE_MODES.md`: a post-action escalation that
runs the action first, an ungated catalog that executes a dangerous tool, an ambiguous catalog that
routes a read to a destructive-capable tool, a coverage gap that misses the explicit human request,
and a flow with no trace that cannot be audited. The capstone shows these compounding: the naive design
closes an account without authorization and misses the request for a human, with no record.

## Controls

- Enforced by prompt: tool descriptions and any system-prompt guidance, which steer behavior. Helpful,
  not load-bearing.
- Enforced by runtime: the escalation policy (coverage, pre-action timing, route), the permission gate,
  and the observability trace. These are the controls that compose into a safe system. See
  `../../ENFORCEMENT_LAYER.md`.
- Observable: the per-request status, the tool executed, whether escalation happened before the action,
  and the recorded trace.
- Auditable: each request's trace records the escalation check, routing, gate decision, and execution
  or handoff.

## Governance and escalation (mandatory)

- Where automation stops: the escalation policy stops automatically before any out-of-policy,
  unauthorized high-impact, or explicit-human request and routes it to a human, and the gate stops a
  write or destructive tool unless it is authorized and confirmed. The routine read and the authorized
  cancellation proceed.
- Human-handoff path: a triggered request escalates to the human review queue before the action runs,
  so a person decides on the closure and on the explicit request for a human.
- Fail-safe behavior (fails safely rather than silently): the composed design escalates the
  unauthorized closure and the human request before acting and records every decision, while the naive
  design closes the account without authorization, misses the human request, and records nothing. The
  contrast, same session and same engine, opposite outcome, is the capstone lesson: a safe agent is a
  correct composition of an observable loop, a gated catalog, and a pre-action escalation policy, and a
  failure in any one layer compounds into a system failure.

## Exam angle

This capstone integrates the reasoning from labs 01, 02, and 07. It serves Agentic Architecture and
Orchestration (27%) primarily, with Tool Design and MCP Integration (18%) through the catalog and gate.
The transferable judgment is that the controls compose in a specific order, that an authorized,
confirmed action is governed by the gate rather than escalated, and that observability is what makes
the composed system auditable.
