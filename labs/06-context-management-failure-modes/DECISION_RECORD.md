# Decision record: lab 06 context management failure modes

This is the decision-record skeleton for the lab. The section headers are fixed and mandatory. The
content is filled in when the lab is built out. The Governance and escalation section is required
and may not be left empty in the final version.

## Scenario

A multi-agent system (research and internal knowledge) accumulates context toward overflow and uses
session forking, where forking branches conversation history but not the filesystem.

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

To be completed. State the context-budgeting, checkpointing, and file-isolation design and why it
wins. Reference the session-forking primitive in `../../VERIFIED.md`.

## Alternatives rejected and why

To be completed. Include a forking-only file-isolation approach and a summarize-after-overflow
approach, with the specific judgment reason each loses.

## Failure modes

To be completed. Summarize and cross-reference `FAILURE_MODES.md`. Emphasize silent versus loud
failure.

## Controls

- Enforced by prompt: to be completed.
- Enforced by runtime: to be completed (orchestration limits, summarization checkpoints, file
  checkpointing).
- Observable: to be completed (overflow signals).
- Auditable: to be completed.

## Governance and escalation (mandatory)

- Where automation stops: to be completed.
- Human-handoff path: to be completed.
- Fail-safe behavior (fails safely rather than silently): to be completed.

## Exam angle

To be completed. Cross-reference `EXAM_ANGLE.md` and name the domain weight served.
