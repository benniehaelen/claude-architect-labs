# Capstone: customer support agent

This is the first v1.0 capstone. A capstone takes one anchor scenario end to end and combines the
relevant labs into a single design problem. The customer support agent is anchor scenario 1 (see
`../../SCENARIO_INDEX.md`), and it composes three labs:

- Lab 01, agent loop observability. Each request is handled as an observable flow whose decisions are
  recorded as a trace, so an incident is explainable.
- Lab 02, tool catalog design. A request routes to a tool through the catalog, and a permission gate
  governs whether the selected tool may execute.
- Lab 07, human escalation patterns. An escalation policy decides, before the agent acts, whether a
  request must reach a human.

Primary domains: Agentic Architecture and Orchestration (27%), with Tool Design and MCP Integration
(18%) and Claude Code Configuration and Workflows through the escalation and catalog work.

## The design problem

A support agent fields four requests in one session: a routine order lookup, an authorized and
confirmed order cancellation, an unauthorized out-of-policy account closure, and an explicit request
for a human. The system must handle the routine and authorized requests automatically, escalate the
unauthorized closure and the human request before any action, and leave an auditable trace. The
difficulty is the composition: the three controls must be layered in the right order, and one
refinement appears only when the labs are combined.

That refinement is the relationship between escalation and the gate. An authorized, confirmed
high-impact action (the cancellation) is governed by the permission gate, not escalated to a human,
while an unauthorized high-impact action, an out-of-policy request, or an explicit request for a
human is escalated before the agent acts. Lab 07 in isolation escalates every high-impact request;
the capstone refines that to defer to the gate when the action is authorized and confirmed.

## How to run (dry-run, free, deterministic)

No installs and no paid API calls are needed. The flow is deterministic and reuses the lab catalogs
(`support_catalog_good`, `support_catalog_bad`) and the lab escalation policies
(`escalation_policy_good`, `escalation_policy_bad`) from `../../shared/fixtures`. From the repository
root:

```
python capstones/customer-support-agent/bad_version/run.py
python capstones/customer-support-agent/solution/run.py
python shared/evals/check_capstone_support.py
```

Both runners use the same composed engine (`../../shared/harness/support_agent.py`), which reuses the
catalog engine and the escalation engine directly. Only the design differs. The naive design composes
the labs' failure modes: the sprawling ungated catalog, the weak post-action escalation policy, and no
observability, so the unauthorized account closure executes before any human sees it and the request
for a human is missed. The composed design layers the controls correctly, so the must-escalate
requests reach a human before any action and every request leaves a trace.

## Status

Built for v1.0. Includes the naive composition, the reference composition, the composed engine that
reuses the lab engines, the eval, the decision record, the question set, and a timed practice set
(`../../practice/capstone_support_timed.md`).
