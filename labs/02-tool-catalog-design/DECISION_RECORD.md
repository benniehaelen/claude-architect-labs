# Decision record: lab 02 tool catalog design

## Scenario

An agent (a customer support agent, and by extension a developer-productivity agent) is given a set
of tools. The two anchor scenarios share a shape: the agent must pick the right tool for a request,
and some tools can take high-impact actions such as cancelling an order, issuing a refund, or
closing an account. The catalog in `bad_version` is sprawling: intents overlap across tools,
dangerous tools are ungated, and a coarse `manage_order` tool bundles a benign lookup with cancel
and refund. The result is that the agent has no obvious choice for a simple read, and an
unauthorized account closure runs with no checks at all.

## Constraints

The binding constraint is safety under a single design surface: the catalog itself. Cost and
latency matter, but the catalog's first job is to make the right tool obvious and the dangerous
action hard to reach by accident.

- Latency: tool count and overlap affect selection quality, not raw speed.
- Cost: ambiguous or coarse tools cause wrong or wasted calls, which is the cost lever here.
- Reliability: selection must be deterministic in the sense that one intent has one obvious tool.
- Security: high-impact actions must pass a control before they execute.
- Data sensitivity: a read tool should not also carry the capability to mutate or destroy.
- Human review: an unauthorized high-impact action must reach a human rather than run.
- Operational owner: the team that owns the agent owns the catalog and the permission gate.

## Design chosen

A deliberate catalog (in `support_catalog_good.json`) paired with a permission gate (in
`shared/harness/catalog.py`). Four rules define it.

First, one intent maps to exactly one tool. There is no ambiguity, so the right tool is the obvious
choice. This is the guide layer: a precise tool, with a precise description, is what steers
selection.

Second, each tool has a single effect level (read, write, or destructive). No tool bundles a benign
read with a destructive capability, so selecting a tool for a read never hands the agent the power
to destroy.

Third, every write and destructive tool is gated. The gate is the control layer. It governs whether
a selected tool may actually execute, independent of what the description suggested.

Fourth, the gate requires authorization and confirmation for high-impact actions and escalates an
unauthorized one. A benign read passes, an authorized and confirmed write runs, an unconfirmed write
is blocked, and an unauthorized destructive action is escalated rather than executed.

The decisive insight, visible in the runners, is that the bad version and the solution use the
exact same routing and gating engine. Only the catalog differs. The runtime gate can only govern a
tool the catalog wired it to, so catalog design is what makes the control effective.

## Alternatives rejected and why

Keeping the coarse `manage_order` tool but writing a strong warning into its description. The
description is a guide. It cannot stop the tool from executing a cancel, and it does nothing about
the ambiguity. Wrong layer for a must-hold safety requirement.

Adding more tools to cover every case without removing overlap. More tools without deduplication
makes selection harder, not easier, and multiplies the surface where a dangerous capability hides.
This optimizes coverage over the binding safety and clarity constraint.

Relying on the model to choose conservatively among overlapping tools. Selection among ambiguous
options is not reliable, and reliability of a high-impact action cannot rest on it. The fix is to
remove the ambiguity at the catalog level, not to hope the model resolves it well.

## Failure modes

Summarized here and detailed in `FAILURE_MODES.md`: ambiguous selection from overlapping intents,
over-privilege from coarse tools, ungated dangerous tools that bypass the control entirely,
mislabeled effect levels that hide risk from the gate, and a benign read that routes to a
destructive-capable tool.

## Controls

- Enforced by prompt: the tool descriptions, which guide selection. Helpful, not load-bearing for
  safety.
- Enforced by runtime: the permission gate, which requires authorization and confirmation for
  write and destructive tools and escalates unauthorized actions. The single-effect and gating
  rules are properties of the catalog that the gate depends on.
- Observable: the routing status (ok, ambiguous, unroutable) and the gate decision and reason for
  every request.
- Auditable: each request records the selected tool, its effect, the gate decision, and whether it
  executed.

## Governance and escalation (mandatory)

Where automation stops: the gate stops automatically before any write or destructive tool runs
unless the request is authorized and confirmed. Read actions proceed.

Human-handoff path: an unauthorized high-impact action returns an `escalate` decision with reason
`unauthorized_high_impact_action`, which routes the request to a human rather than executing it.

Fail-safe behavior: the system fails safely rather than silently. The reference catalog escalates
the unauthorized close_account, while the bad catalog runs it with no gate at all. The contrast,
same request and same engine, opposite outcome, is the lesson: governance lives in the catalog and
the gate, not in the tool descriptions.

## Exam angle

See `EXAM_ANGLE.md`. This lab serves the Tool Design and MCP Integration domain (18%) with Agentic
Architecture and Orchestration (27%) as secondary. The transferable judgment is that a tool
description guides selection while a permission control governs execution, that granularity should
be chosen by the cost and ambiguity it creates, and that a runtime control is only as good as the
catalog wired to it.
