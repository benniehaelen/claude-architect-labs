# Lab 05: structured output reliability

Primary domain: Prompt Engineering and Structured Output (20%). Secondary: Context Management and
Reliability. Anchor scenario: structured data extraction pipelines.

## Scenario brief

A pipeline turns unstructured input into machine-readable records that a downstream system parses,
and the records must be grounded in the source. The naive design asks for citations and a strict
output schema in the same call, which returns a 400 error because citations and the structured
output format are incompatible (dated and sourced in `../../VERIFIED.md`). This lab is about
building extraction that is both reliable in shape and grounded in evidence.

## Architecture goal

Design a multi-pass pipeline that produces grounded, schema-valid output despite the
citations-versus-structured-output incompatibility: a cited pass for grounding, a transform pass to
the strict schema, and a verification pass that maps each structured claim back to its cited
evidence. The lab contrasts the single-call design that fails against the multi-pass design that
holds.

## How to run (dry-run, free, deterministic)

No installs and no paid API calls are needed. The pipeline logic is deterministic and reads a design
and an extraction corpus from `../../shared/fixtures`. From the repository root:

```
python labs/05-structured-output-reliability/bad_version/run.py
python labs/05-structured-output-reliability/solution/run.py
python shared/evals/check_lab05.py
```

Both runners use the same pipeline engine (`../../shared/harness/extraction.py`). Only the design
differs. The single-call design asks for citations and the structured-output format in one request
and returns a 400, so it emits nothing. The multi-pass design grounds with a cited pass, shapes with
a constrained-decoding transform pass, and verifies each record against the source, emitting the two
grounded records and holding the one ungrounded claim. The eval also runs a prompt-only design to
show it emits the ungrounded record because it has no verification pass.

## Status

Built for v0.1. Includes the single-call design, the multi-pass design, the shared pipeline engine
(the 400 model, the pass logic, schema validation, and grounding verification), the failure-mode
catalog, the decision record, the question set, and a timed practice set
(`../../practice/lab05_timed.md`).
