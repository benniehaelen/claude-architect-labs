# Start here: lab 04

## What you will build

You will fix a team Claude Code configuration that relies on a path-scoped rule to enforce a
convention at file-creation time. The deliverable is a layered configuration: the rule kept as a
guide, plus a runtime control (a hook or a pre-commit or CI check) that governs the convention on
created files, with an argument for what belongs in each layer.

## Dry-run path

Run the lab against a mocked Claude Code session and recorded fixtures so it costs nothing. The
dry-run demonstrates a new file created without the rule firing, then the same case with the
runtime control in place. This repository's own `.claude/rules/house-style.md` plus its
`check_house_style.py` hook and `.githooks/pre-commit` check are the live reference. A live run is
optional and clearly marked.

Status: the runnable harness and fixtures for this lab are added when the lab is built out. For now
this file records the intended shape of the exercise.
