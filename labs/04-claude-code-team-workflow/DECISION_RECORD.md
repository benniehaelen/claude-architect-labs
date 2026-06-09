# Decision record: lab 04 Claude Code team workflow

This is the decision-record skeleton for the lab. The section headers are fixed and mandatory. The
content is filled in when the lab is built out. The Governance and escalation section is required
and may not be left empty in the final version.

## Scenario

A team configures Claude Code (developer-productivity and CI/CD) and needs conventions to hold
consistently, including at file-creation time, where a path-scoped rule alone does not fire.

## Constraints

State the binding constraints and which one the design actually optimizes for.

- Latency: to be completed.
- Cost: to be completed.
- Reliability: to be completed.
- Security: to be completed.
- Data sensitivity: to be completed.
- Human review: to be completed.
- Operational owner: to be completed.

## Design chosen

To be completed. State the layered configuration (rule as guide, hook and CI check as control) and
why it wins. Reference the path-scoped-rules primitive in `../../VERIFIED.md`.

## Alternatives rejected and why

To be completed. Include the rules-only or memory-only alternative and the specific judgment reason
it loses (works on Read, silently misses Write).

## Failure modes

To be completed. Summarize and cross-reference `FAILURE_MODES.md`.

## Controls

- Enforced by prompt: to be completed (memory and path-scoped rule).
- Enforced by runtime: to be completed (PostToolUse hook, pre-commit, CI gate).
- Observable: to be completed.
- Auditable: to be completed.

## Governance and escalation (mandatory)

- Where automation stops: to be completed.
- Human-handoff path: to be completed.
- Fail-safe behavior (fails safely rather than silently): to be completed.

## Exam angle

To be completed. Cross-reference `EXAM_ANGLE.md` and name the domain weight served.
