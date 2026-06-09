# Lab 01: agent loop observability

Primary domain: Agentic Architecture and Orchestration (27%). Secondary: Context Management and
Reliability. Anchor scenarios: customer support agents, multi-agent research systems.

## Scenario brief

An agent runs a multi-step loop: it reasons, calls tools, reads results, and decides whether to
continue or stop. In production this loop is a black box until something goes wrong, at which point
the operator needs to know what the agent decided, which tools it called, what they returned, where
it retried, and why it stopped. This lab is about designing that observability into the loop from
the start rather than bolting it on after an incident.

## Architecture goal

Make the agent loop observable and debuggable without distorting its behavior: capture the decision
points, tool calls, and stop conditions as structured, auditable events, and define which signals
must be enforced at runtime versus merely logged. The lab contrasts a black-box loop against an
instrumented one and shows how observability supports the governance handoff.

## How to run (dry-run, free, deterministic)

No installs and no paid API calls are needed. The dry-run uses scripted models and mocked tools,
backed by fixtures in `../../shared/fixtures`. From the repository root:

```
python labs/01-agent-loop-observability/bad_version/run.py --session support_session_failure
python labs/01-agent-loop-observability/solution/run.py   --session support_session_failure
python shared/evals/check_lab01.py
```

Compare the two runs on the failure session. The black-box loop returns a confident, unfounded
answer and tells you nothing about what happened. The instrumented loop prints the full trace,
trips its circuit breaker at the third consecutive failure, and escalates to a human queue with a
named stop reason. The eval asserts these properties hold.

Other sessions to try: `support_session_ok` (normal completion) and `research_session_budget` (a
run that never converges and stops at the step budget).

## Status

Built for v0.1. Includes the flawed version, the reference solution, the shared harness it runs on,
the failure-mode catalog, the decision record, the question set, and a timed practice set
(`../../practice/lab01_timed.md`).
