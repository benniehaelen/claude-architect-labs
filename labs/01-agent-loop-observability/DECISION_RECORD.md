# Decision record: lab 01 agent loop observability

## Scenario

An agent runs a multi-step tool-calling loop in production. Two anchor scenarios drive this lab: a
customer support agent that looks up account and order state, and a multi-agent research lead that
dispatches subagent searches. In both, the loop is a black box until something goes wrong. When an
upstream tool fails or a run fails to converge, operators need to know what the agent decided,
which tools it called, what they returned, where it failed, and why it stopped. The flawed loop in
`bad_version/` gives them none of that and, on the failure session, returns a confident answer with
no evidence behind it.

## Constraints

The binding constraint is reliability under partial failure, with data sensitivity and human review
close behind. The design optimizes for explainability and safe failure, not for raw speed.

- Latency: the instrumented loop adds negligible overhead, since recording an event is cheap
  relative to a tool call or a model call.
- Cost: observability is free in the dry-run and near free in production, because events are local
  records, not extra model calls.
- Reliability: the loop must behave predictably when a tool fails repeatedly or a run fails to
  converge.
- Security: the trace records tool names, arguments, and results, so it must be treated as
  potentially sensitive and stored accordingly.
- Data sensitivity: in support and research settings the trace can contain customer or source
  data, which is an argument for controlling where the trace is persisted and who can read it.
- Human review: a failed run must reach a human, so the escalation path is a first-class part of
  the design, not an afterthought.
- Operational owner: the team that runs the agent owns the trace store and the escalation queue.

## Design chosen

An instrumented loop (in `shared/harness/agentloop.py`) that records one structured event per
decision point and ties a circuit breaker to a governed escalation. Three properties define it.

First, it records a Trace: a step-by-step event log of model decisions, tool calls, tool results,
tool errors, breaker trips, escalations, and the stop. The trace makes any run explainable after
the fact and auditable.

Second, it carries a circuit breaker as a runtime control. After a configurable number of
consecutive tool failures, or when a step budget is exhausted, the breaker trips. This is a control
in the loop, not a prompt asking the model to give up politely.

Third, when the breaker trips, the loop escalates to a human queue and stops with a named reason,
returning no answer. The system fails safely (a governed handoff) rather than silently (a confident
wrong answer).

This design wins under the binding reliability constraint because it converts an unobservable,
unsafe failure into an observable, safe one at the exact point in the loop where the failure
occurs.

## Alternatives rejected and why

Adding ad hoc print statements around tool calls. This is real and partially helpful, but it
produces unstructured output that cannot be queried or asserted on, and it does not change the
loop's behavior on failure. It logs in the wrong shape and does nothing about the unsafe answer, so
it loses on the reliability constraint.

Raising the step budget so the loop has more chances to finish. This is the wrong constraint. The
failure session does not need more attempts, it needs to stop and escalate. Raising the budget
makes a spinning loop spin longer and delays the handoff.

Instructing the model in the system prompt to escalate when tools fail. This places a must-hold
behavior in the guide layer. The model may comply, but reliability cannot depend on it. The
breaker belongs in the runtime layer (see `../../ENFORCEMENT_LAYER.md`).

## Failure modes

Summarized here and detailed in `FAILURE_MODES.md`: swallowed tool errors, confident ungrounded
answers on failure, loops that never converge, traces that leak sensitive data if stored carelessly,
and a breaker tuned so tight it escalates on transient blips or so loose it never fires.

## Controls

- Enforced by prompt: nothing load-bearing. Prompt guidance can encourage the model to stop on
  failure, but the design does not rely on it.
- Enforced by runtime: the circuit breaker (consecutive-failure and step-budget limits) and the
  escalation and safe stop. These are deterministic and do not depend on the model choosing well.
- Observable: the full Trace, including every tool error and the breaker trip, surfaced as the run
  executes through the event callback.
- Auditable: the Trace persists the decision sequence and stop reason, so a past incident can be
  reconstructed.

## Governance and escalation (mandatory)

Where automation stops: the loop stops automatically after the configured number of consecutive
tool failures or when the step budget is exhausted. It does not keep trying indefinitely and it
does not answer without evidence.

Human-handoff path: on a breaker trip the loop escalates to a named human queue
(`human_support_queue` in the reference) and returns no answer, so a person picks up the case with
the full trace in hand.

Fail-safe behavior: the run fails safely rather than silently. It stops with a named reason
(`escalated_repeated_tool_failure` or `escalated_step_budget_exhausted`) and returns no answer,
instead of handing the customer a confident statement the agent cannot support. The contrast with
`bad_version/`, which returns "your order has shipped" during an upstream outage, is the whole
lesson.

## Exam angle

See `EXAM_ANGLE.md`. This lab serves the Agentic Architecture and Orchestration domain (27%, the
largest single weight) with Context Management and Reliability (15%) as secondary. The transferable
judgment is that observability is an architectural choice about where to instrument the loop and
whether a control can act on the signal in time, not a logging afterthought.
