# Lab 07: human escalation patterns

Primary domain: Agentic Architecture and Orchestration (27%). Secondary: Context Management and
Reliability (15%). Anchor scenario: customer support agents.

This is a v0.2 lab. Governance runs through every v0.1 lab as a cross-cut (the mandatory Governance
and escalation section of each decision record). This lab gives the escalation decision itself a
dedicated, deep treatment: how a policy decides when automation stops and a request reaches a human.

## Scenario brief

A customer support agent fields requests and must know when to stop and hand a request to a human.
The hard part is not whether to escalate in the abstract, it is designing the policy: which conditions
must reach a human, whether the handoff happens before or after the agent acts, where the escalation
is routed, and what happens when it cannot be delivered. The policy in `bad_version` escalates only on
high impact, escalates after acting, and proceeds by default, so an out-of-policy exception is handled
silently and a high-impact account closure runs before any human sees it.

## Architecture goal

Design an escalation policy that reaches a human at the right time: triggers that cover every
must-escalate case, escalation before an irreversible action rather than after, a defined route to a
human, and a fail-safe default that holds rather than proceeds when escalation cannot be delivered. The
lab contrasts a weak policy that misses and delays escalations against a sound one.

## How to run (dry-run, free, deterministic)

No installs and no paid API calls are needed. The classification is deterministic and reads a policy
and a request set from `../../shared/fixtures`. From the repository root:

```
python labs/07-human-escalation-patterns/bad_version/run.py
python labs/07-human-escalation-patterns/solution/run.py
python shared/evals/check_lab07.py
```

Both runners use the same escalation engine (`../../shared/harness/escalation.py`). Only the policy
differs. On the weak policy, an out-of-policy exception and an explicit request for a human are handled
automatically, and a high-impact account closure is escalated only after it runs. On the sound policy,
every must-escalate request reaches a human before any action and the routine read is handled. The
eval also runs a no-route policy that identifies the right escalations but drops them because it has
nowhere to send them and proceeds by default.

## Status

Built for v0.2. Includes the weak policy, the sound policy, the shared escalation engine (the trigger
model, the timing and routing logic, and the policy analyzer), the failure-mode catalog, the decision
record, the question set, and a timed practice set (`../../practice/lab07_timed.md`).
