# Capstone: developer-productivity tools

This is the third v1.0 capstone. A capstone takes one anchor scenario end to end and combines the
relevant labs into a single design problem. The developer-productivity scenario is anchor scenario 6
(see `../../SCENARIO_INDEX.md`): Claude Code configured for a development team. It composes two labs:

- Lab 02, tool catalog design. The team exposes a catalog of developer tools (run tests, read and edit
  source, open a PR, deploy) and a permission gate governs the high-impact ones.
- Lab 04, Claude Code team workflow. The team enforces conventions (no em-dash house style, no
  committed secrets) in the right layer, where a path-scoped rule guides and a hook, pre-commit check,
  or CI gate governs.

Primary domains: Claude Code Configuration and Workflows (20%) and Tool Design and MCP Integration
(18%).

## What the tools are

The developer-facing operations the team's Claude Code setup exposes to the agent: read-only tools
(run the test suite, read source), gated writes (edit source, create a doc, open a PR), and a
high-impact destructive action (deploy to production). Alongside the tools, the team has conventions
that govern the artifacts those tools produce: a Markdown house style and a no-committed-secrets rule.

## The design problem

A developer session mixes both dimensions: running tests, editing a source file, creating a new doc,
deploying, and committing. Each action invokes a tool, which the catalog routes and the gate governs,
and may produce an artifact whose convention must be governed on its event by the config layer. The
system must gate the deploy, hold the new doc to the house style at creation, govern the commit against
the secrets rule, and still let the routine tools run.

The composition is the difficulty. The catalog and gate (lab 02) and the configuration enforcement
(lab 04) must both hold. A failure in either compounds: an ungated deploy runs while a newly created
file silently violates the house style, and the team believes both are covered.

## How to run (dry-run, free, deterministic)

No installs and no paid API calls are needed. The flow is deterministic and reuses the lab 04 team
configs (`team_config_good`, `team_config_bad`) from `../../shared/fixtures`. From the repository root:

```
python capstones/developer-productivity/bad_version/run.py
python capstones/developer-productivity/solution/run.py
python shared/evals/check_capstone_dev.py
```

Both runners use the same composed engine (`../../shared/harness/dev_environment.py`), which reuses the
catalog engine and the config engine directly. Only the catalog and the config differ. The naive
environment runs an ungated deploy and lets a created file and a commit slip past the conventions. The
composed environment gates the deploy, governs every convention on its event, and lets the routine
tools run.

## Status

Built for v1.0. Includes the naive environment, the reference environment, the composed engine that
reuses the lab engines, the eval, the decision record, the question set, and a timed practice set
(`../../practice/capstone_dev_timed.md`).
