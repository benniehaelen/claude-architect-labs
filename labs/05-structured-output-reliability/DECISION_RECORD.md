# Decision record: lab 05 structured output reliability

## Scenario

A structured data extraction pipeline turns unstructured input, here a benefits policy document, into
machine-readable records that a downstream system parses. The records must be both schema-valid, so
the parser does not break, and grounded, so each value traces to evidence in the source. The design in
`bad_version` asks for citations and the structured-output format in the same call, to get grounding
and a strict shape in one request. The two are incompatible and the call returns a 400 (dated and
sourced in `../../VERIFIED.md`), so the pipeline produces nothing.

## Constraints

The binding constraint is that the pipeline produces records that are both schema-valid and grounded,
under a hard incompatibility between the two features that would most directly provide each. Latency
and cost matter, but the multi-pass design accepts more calls in exchange for output that is correct
in shape and traceable to evidence.

- Latency: the multi-pass design makes three passes instead of one, trading latency for correctness.
- Cost: more passes cost more tokens, which is the price of grounding plus a strict schema.
- Reliability: the schema shape must hold for every record, governed by constrained decoding rather
  than by a prompt instruction.
- Security: not the binding concern here, though emitting an ungrounded claim is a correctness and
  trust harm.
- Data sensitivity: extracted records may carry sensitive values, so an ungrounded or fabricated
  field must not be emitted as fact.
- Human review: a record that fails verification is held for review rather than emitted automatically.
- Operational owner: the team that owns the pipeline owns the schema, the verification step, and the
  claim-to-evidence audit trail.

## Design chosen

A three-pass pipeline (described by `design_multipass.json`) that uses each feature where it is valid.

The cited pass grounds the content. It asks the model for claims with citations, mapping each claim to
a span in the source. This is where citations are valid, because no structured-output format is
requested in the same call.

The transform pass shapes the grounded claims into the strict schema using constrained decoding (the
structured-output format). This is where the structured format is valid, because citations are not
requested in the same call. Constrained decoding is the control that makes the shape hold, rather than
a prompt instruction that only raises the likelihood of valid shape.

The verification pass maps each structured record back through its claim to a cited evidence span and
emits only the records whose claims are backed by evidence. A record that is shape-valid but ungrounded
is held, not emitted. In the corpus, the claim about a gym membership has no supporting span, so the
verification pass holds it.

The decisive insight, visible in the runners, is that the single-call design and the multi-pass design
use the exact same engine. Only the design differs. When two real features conflict, the answer is the
multi-pass pattern that uses each where it is valid, not a fabricated flag that pretends the conflict
away.

## Alternatives rejected and why

The single-call design that requests citations and the structured-output format together. This is the
direct expression of the goal, and it returns a 400. The two features are incompatible in one call, so
the design fails completely. This is the fabricated-convenience trap: there is no flag or beta header
that combines them.

A prompt-only design that asks for the schema and the grounding by instruction, with no constrained
decoding and no verification pass. This is real and it runs, but the schema can drift because the shape
is only guided, and an ungrounded claim is emitted because nothing verifies grounding. In the corpus
this design emits the unsupported gym-membership record. Correct in mechanism, but it fails the
reliability and grounding constraints the scenario binds on.

Dropping grounding and emitting schema-valid records only. This satisfies the parser but abandons the
grounding requirement, so a confident, unsupported value lands as fact. It optimizes shape over the
grounding the scenario requires.

## Failure modes

Summarized here and detailed in `FAILURE_MODES.md`: the 400 from combining citations and the
structured format, a schema enforced by prompt rather than constrained decoding, grounding asserted by
prompt with no verification pass, an ungrounded record emitted as fact, and reliance on a fabricated
flag that claims to combine the two features.

## Controls

- Enforced by prompt: the extraction instructions in the cited pass, which guide what to extract.
  Helpful, not load-bearing for shape or grounding.
- Enforced by runtime: constrained decoding (the structured-output format) governs the schema shape in
  the transform pass, and the verification pass governs grounding by mapping each record to a cited
  span. See `../../ENFORCEMENT_LAYER.md`.
- Observable: the design analysis (citations-with-structured, schema-by-prompt, unverified grounding)
  and the per-record verdict (schema valid, grounded, emitted or held, and the reason).
- Auditable: each emitted record carries a claim-to-evidence mapping, so any value can be traced back
  to the span that supports it.

## Governance and escalation (mandatory)

- Where automation stops: a record that fails verification is not emitted automatically. The pipeline
  emits only records whose claims map to a cited evidence span.
- Human-handoff path: a held record is routed for human review rather than dropped silently or emitted
  as fact, so a person decides what to do with an unsupported claim.
- Fail-safe behavior (fails safely rather than silently): the multi-pass design holds the ungrounded
  record, while the prompt-only design emits it and the single-call design fails outright. The
  contrast, same corpus and same engine, opposite outcome, is the lesson: grounding is governed by a
  verification pass, not by a prompt, and the schema is governed by constrained decoding, not by a
  request that conflicts with citations.

## Exam angle

See `EXAM_ANGLE.md`. This lab serves the Prompt Engineering and Structured Output domain (20%) with
Context Management and Reliability (15%) as secondary. The transferable judgment is that when two real
features conflict, you reach for the multi-pass pattern that uses each where it is valid, you govern
schema shape with constrained decoding rather than a prompt, and you verify grounding rather than
assert it.
