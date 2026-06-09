# Decision record: lab 05 structured output reliability

This is the decision-record skeleton for the lab. The section headers are fixed and mandatory. The
content is filled in when the lab is built out. The Governance and escalation section is required
and may not be left empty in the final version.

## Scenario

A structured data extraction pipeline must produce schema-valid, grounded records, but citations
and the structured-output format cannot be combined in a single call.

## Constraints

State the binding constraints and which one the design actually optimizes for.

- Latency: to be completed (the multi-pass design trades calls for correctness).
- Cost: to be completed.
- Reliability: to be completed.
- Security: to be completed.
- Data sensitivity: to be completed.
- Human review: to be completed.
- Operational owner: to be completed.

## Design chosen

To be completed. State the three-pass pipeline (cited, transform-to-schema, verification) and why
it wins. Reference the citations-versus-structured-output primitive in `../../VERIFIED.md`.

## Alternatives rejected and why

To be completed. Include the single-call design (fails with a 400) and a prompt-only grounding or
prompt-only schema design, with the specific judgment reason each loses.

## Failure modes

To be completed. Summarize and cross-reference `FAILURE_MODES.md`.

## Controls

- Enforced by prompt: to be completed.
- Enforced by runtime: to be completed (constrained decoding for schema, verification pass for
  grounding).
- Observable: to be completed.
- Auditable: to be completed (claim-to-evidence mapping).

## Governance and escalation (mandatory)

- Where automation stops: to be completed (for example, a record that fails verification is not
  emitted automatically).
- Human-handoff path: to be completed.
- Fail-safe behavior (fails safely rather than silently): to be completed.

## Exam angle

To be completed. Cross-reference `EXAM_ANGLE.md` and name the domain weight served.
