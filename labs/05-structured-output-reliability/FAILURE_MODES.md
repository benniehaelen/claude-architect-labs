# Failure modes: lab 05 structured output reliability

Each failure mode names what goes wrong, how it is detected, and what the reference design does
about it. Run `bad_version/run.py` and `solution/run.py` to see several directly, and
`shared/evals/check_lab05.py` for the assertions.

## The 400 from combining citations and the structured format

The design asks for citations and the structured-output format in the same call, to get grounding and
a strict shape at once. The two are incompatible and the request returns a 400 (see `../../VERIFIED.md`),
so the pipeline produces nothing. This is the central defect. Detection is the `citations_with_structured`
analysis flag and the pipeline error in the runner. The reference splits the two into separate passes,
a cited pass and a transform pass, so neither call combines them.

## Schema enforced by prompt rather than constrained decoding

The design asks for the schema by instruction instead of using the structured-output format, so the
shape is only guided and a record can drift out of schema. Detection is the `schema_by_prompt` flag.
The reference governs the shape with constrained decoding in the transform pass, which makes the
record shape-valid by construction.

## Grounding asserted by prompt with no verification pass

The design tells the model to ground its claims but never checks, so an ungrounded claim is emitted as
fact. Detection is the `grounding_unverified` flag, and in the corpus the prompt-only design emits the
unsupported gym-membership record. The reference adds a verification pass that maps each record back to
a cited evidence span and holds any record whose claim is unsupported.

## An ungrounded record emitted as fact

A consequence of skipping verification: a shape-valid record that no evidence supports lands in the
output and the downstream system treats it as true. Detection is the per-record verdict, where the
prompt-only design shows an emitted record with `grounded` false. The reference holds that record with
the reason `ungrounded_held` and routes it for review rather than emitting it.

## Reliance on a fabricated flag that combines the two features

A subtler mode, and the Branch A trap the exam angle calls out: assuming a parameter or beta header can
enable citations and the structured-output format together. No such flag exists, and naming it is the
fabricated-feature trap the repository teaches learners to avoid (see `../../DISTRACTOR_TAXONOMY.md`).
The reference does not try to combine the two. It uses the multi-pass pattern that applies each feature
where it is valid.
