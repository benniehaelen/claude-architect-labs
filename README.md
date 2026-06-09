# claude-architect-labs

A hands-on, scenario-driven architecture lab repository for the hard parts of production Claude
work: agent orchestration, tool and MCP boundary design, Claude Code configuration,
structured-output reliability, context management, and governance.

## Positioning

This is an unofficial, community resource. It is not affiliated with, endorsed by, or sponsored by
Anthropic. It contains no exam questions and no paraphrase of exam questions. It teaches the
underlying architectural reasoning only. It is not a replacement for Anthropic's official
training.

The repository doubles as preparation for the Claude Certified Architect, Foundations (CCA-F)
exam, but its real subject is architecture. Where a feature-by-feature API examples repository
answers "how do I use this capability," this repository answers a harder set of questions: which
capability, where the boundary goes, what fails, what must be enforced, and how to defend the
tradeoff.

## What makes this different

Most study material treats the subject as a product-knowledge test. Knowing that a feature exists
is the floor here, not the answer. The scenarios reward systemic use under real constraints:
latency, cost, reliability, security, data sensitivity, human review, and operational ownership.
The difficulty lives in the wrong answers, so every question set carries a two-branch distractor
taxonomy (see `DISTRACTOR_TAXONOMY.md`).

Governance, safety, and reliability are not a standalone topic here. They run through every lab as
a cross-cut, enforced through the mandatory Governance and escalation section of each lab's
`DECISION_RECORD.md`.

## Repository structure

The root holds the cross-cutting documents that frame the whole repository:

- `STUDY_GUIDE.md`: how to use the labs, in what order, and how to study for speed as well as
  depth.
- `EXAM_DOMAIN_MAP.md`: the five domains, their weights, and which labs map where.
- `SCENARIO_INDEX.md`: the six anchor scenarios and the labs that exercise each.
- `DISTRACTOR_TAXONOMY.md`: the two-branch wrong-answer taxonomy used across all question sets.
- `ENFORCEMENT_LAYER.md`: prompt-guides versus runtime-governs, per capability.
- `WHAT_NOT_TO_DO.md`: the anti-patterns this repository is built to correct.
- `VERIFIED.md`: dated facts, version gates, open bugs, and source URLs.
- `SPEC.md`: the build brief for the repository.

The work itself lives in two trees:

- `labs/`: a small number of deep, scenario-driven labs. Each lab has a flawed version, a
  reference solution, a decision record, a failure-mode catalog, an exam-angle note, and a paired
  question set.
- `practice/`: timed scenario sets tied to the labs, built for the two-minutes-per-question pace
  of the exam.

Shared infrastructure lives in `shared/`: a harness, mocked services, recorded fixtures, and
evals. No lab requires paid API calls to learn. Every built lab ships a dry-run mode with mocked
tool responses and recorded fixtures, with optional live runs where appropriate.

## House style and self-enforcement

This repository practices what it teaches. The writing rules live in `.claude/rules/house-style.md`
as a path-scoped rule, and the same rules are enforced at runtime by a hook and a git pre-commit
check. That pairing, a rule that guides plus a control that governs, is itself a worked example of
the central thesis. See `ENFORCEMENT_LAYER.md` and `CLAUDE.md`.

To enable the local git hook after cloning:

```
git config core.hooksPath .githooks
```

## Status

Version 0.1 in progress.

Built:
- Lab 01: agent-loop-observability
- Lab 02: tool-catalog-design

Scaffolded:
- Lab 03: mcp-boundaries
- Lab 04: claude-code-team-workflow
- Lab 05: structured-output-reliability
- Lab 06: context-management-failure-modes

The built labs include flawed versions, reference solutions, dry-run execution paths, decision
records, failure-mode catalogs, exam-angle notes, question sets, evals, and timed practice. They
pass their evals (`python shared/evals/check_lab01.py` and `check_lab02.py`). The scaffolded labs
have their README, START_HERE, EXAM_ANGLE, and a full-skeleton DECISION_RECORD in place, ready to
build out.
