# Start here: lab 05

## What you will build

You will replace a single-call extraction that asks for citations and a strict schema at once (and
fails with a 400) with a multi-pass pipeline. The deliverable is the three-pass design (cited pass,
transform-to-schema pass, verification pass) plus an argument for where schema shape is governed by
constrained decoding and where grounding is verified.

## Dry-run path

Run the lab against mocked model responses and recorded fixtures so it costs nothing. The dry-run
reproduces the 400 from the single-call design, then runs the multi-pass pipeline against a small
extraction corpus and checks that every structured claim maps to cited evidence. A live run is
optional and clearly marked.

## Suggested path

1. Read `README.md` for the scenario and the run commands.
2. Run the single-call design and read its analysis. Notice that combining citations and the
   structured-output format returns a 400 and emits nothing.
3. Run the multi-pass design and compare. The cited pass grounds the claims, the transform pass shapes
   them with constrained decoding, and the verification pass holds the ungrounded gym-membership claim
   while emitting the two grounded records.
4. Read `../../shared/harness/extraction.py`. Confirm that both runners call the same `run_pipeline`
   engine and that only the design differs, and see how the verification pass maps each record to a
   cited span.
5. Run `python shared/evals/check_lab05.py` to see the properties the pipeline must satisfy, including
   the prompt-only design that emits the ungrounded record for want of a verification pass.
6. Work `questions.md`, then check `answers.md` and study the branch labels. Finish with the timed set
   in `../../practice/lab05_timed.md` against the clock.
7. Read `DECISION_RECORD.md`, paying attention to the mandatory Governance and escalation section, and
   connect it to the primitive in `../../VERIFIED.md`.

Status: built for v0.1.
