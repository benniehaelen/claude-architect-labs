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

Status: scaffolded for v0.1. The flawed version, reference solution, failure-mode catalog, and
question set are added when this lab is built out.
