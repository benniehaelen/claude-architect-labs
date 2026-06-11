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

## How to run (dry-run, free, deterministic)

No installs and no paid API calls are needed. The enforcement logic is deterministic and reads
configurations and an event stream from `../../shared/fixtures`. From the repository root:

```
python labs/04-claude-code-team-workflow/bad_version/run.py
python labs/04-claude-code-team-workflow/solution/run.py
python shared/evals/check_lab04.py
```

Both runners use the same enforcement engine (`../../shared/harness/config.py`). Only the
configuration differs. On the rules-and-memory configuration, a new file slips past the house-style
rule (the rule does not load on create), a memory-only secrets convention cannot block a commit, and
a preference is over-controlled with a blocking hook. On the layered configuration, a PostToolUse
hook governs both create and edit, a pre-commit check and a CI gate govern the commit, and the
preference is guided by the rule. The lesson is that a convention holds because of the layer that
governs it on the right event, not because it was written down.

## Status

Built for v0.1. Includes the rules-and-memory configuration, the layered configuration, the shared
enforcement engine (the layer model, the event driver, and the configuration analyzer), the
failure-mode catalog, the decision record, the question set, and a timed practice set
(`../../practice/lab04_timed.md`).
