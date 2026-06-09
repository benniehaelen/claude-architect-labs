# Lab 04: Claude Code team workflow

Primary domain: Claude Code Configuration and Workflows (20%). Secondary: Agentic Architecture and
Orchestration. Anchor scenarios: developer-productivity tools, CI/CD integrations.

## Scenario brief

A team adopts Claude Code and needs a shared configuration that enforces conventions consistently
across every member and every pipeline run. The temptation is to write the conventions into memory
and rules and assume they hold. They do not always hold, because path-scoped rules load when a file
is read, not when it is created or written (dated and sourced in `../../VERIFIED.md`). This lab is
about configuring a team for conventions that actually stick.

## Architecture goal

Build a Claude Code configuration where guides (memory and path-scoped rules) and controls (hooks,
permission settings, and CI checks) are layered so that a must-hold convention is governed at
runtime while preferences are guided. The lab contrasts a rules-only setup that silently fails on
new files against a layered setup, and it uses this repository's own house-style enforcement as the
worked example.

Status: scaffolded for v0.1. The flawed version, reference solution, failure-mode catalog, and
question set are added when this lab is built out.
