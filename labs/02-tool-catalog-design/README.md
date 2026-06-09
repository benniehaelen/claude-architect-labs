# Lab 02: tool catalog design

Primary domain: Tool Design and MCP Integration (18%). Secondary: Agentic Architecture and
Orchestration. Anchor scenarios: customer support agents, developer-productivity tools.

## Scenario brief

An agent is only as good as the tools it is given. A poorly designed catalog (tools that overlap,
tools that are too coarse or too fine, descriptions that mislead the model about when to use them)
produces wrong tool choices, wasted calls, and unsafe actions. This lab is about designing the set
of tools exposed to an agent: their granularity, naming, descriptions, and the boundaries between
them.

## Architecture goal

Design a tool catalog that makes the right tool the obvious choice and the unsafe action hard to
reach by accident. The lab contrasts a sprawling, overlapping catalog against a deliberate one and
shows how tool descriptions guide selection while permissions and gating govern what a tool may
actually do.

## How to run (dry-run, free, deterministic)

No installs and no paid API calls are needed. The routing is deterministic and reads catalogs and a
request set from `../../shared/fixtures`. From the repository root:

```
python labs/02-tool-catalog-design/bad_version/run.py
python labs/02-tool-catalog-design/solution/run.py
python shared/evals/check_lab02.py
```

Both runners use the same routing and gating engine (`../../shared/harness/catalog.py`). Only the
catalog differs. On the bad catalog, the order_status intent is ambiguous, the dangerous tools are
ungated, and an unauthorized account closure runs silently. On the good catalog, every intent has
one obvious tool, the gate lets a read pass, runs an authorized and confirmed write, blocks an
unconfirmed write, and escalates the unauthorized destructive action. The lesson is that a runtime
control is only as good as the catalog wired to it.

## Status

Built for v0.1. Includes the flawed catalog, the reference catalog, the shared catalog harness
(routing, the permission gate, and the catalog analyzer), the failure-mode catalog, the decision
record, the question set, and a timed practice set (`../../practice/lab02_timed.md`).
