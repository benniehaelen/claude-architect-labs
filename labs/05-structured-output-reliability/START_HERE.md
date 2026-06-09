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

Status: the runnable harness and fixtures for this lab are added when the lab is built out. For now
this file records the intended shape of the exercise.
