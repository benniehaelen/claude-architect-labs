# claude-architect-labs: build brief

You are scaffolding a new public repository. Read this entire brief first, then create the
structure and the fully written cross-cutting documents described below. Stub the labs, but do
not write full lab solution implementations yet. Stop after the scaffold and ask before building
lab internals.

This file should also be committed into the repo as `SPEC.md`, and a condensed version of the
house style and verified-facts discipline should become the repo `CLAUDE.md`.

---

## Mission

`claude-architect-labs` is a hands-on, scenario-driven architecture lab repo for the hard parts of
production Claude work: agent orchestration, tool and MCP boundary design, Claude Code
configuration, structured-output reliability, context management, and governance. It is the
companion to a feature-by-feature API examples repo. Where that repo answers "how do I use this
capability," this one answers "which capability, where does the boundary go, what fails, what must
be enforced, and how do I defend the tradeoff."

It doubles as preparation for the Claude Certified Architect, Foundations (CCA-F) exam.

Positioning, stated plainly in the README: this is an unofficial, community resource. It is not
affiliated with, endorsed by, or sponsored by Anthropic. It contains no exam questions and no
paraphrase of exam questions. It teaches the underlying architectural reasoning only. It is not a
replacement for Anthropic's official training.

## House style (apply to every file you generate)

- Do not use em-dashes anywhere. Use commas, periods, parentheses, or colons.
- Use sentence-case headings.
- Avoid contractions at sentence boundaries.
- Keep any reference to a real healthcare client or named internal platform out of this public
  repo. Use generic phrasing such as "a large healthcare organization" and "a production
  NL-to-SQL platform."
- Prose over bullet soup. Use lists only where the content is genuinely enumerable.

Practice what the repo preaches: create `.claude/rules/house-style.md` with
`paths: ["**/*.md"]` frontmatter encoding the rules above. Note the known limitation below
(path-scoped rules load on Read, not on Write), so also add a pre-commit check or a PostToolUse
hook that greps for em-dashes and fails the commit. That pairing (rule plus enforced check) is
itself a worked example of the repo's central thesis: a prompt or rule guides behavior, a runtime
control governs it.

## Verified facts (verified 2026-06-08; re-verify before each release)

Do not invent features. Every config flag, directive, and primitive in this repo must be real and
dated. Seed `VERIFIED.md` with the following and the URLs.

### Exam shape and domain weights

The exam is scenario-based multiple choice. 60 questions, 120 minutes (two minutes per question),
pass at 720 of 1000. There are five domains with these weights:

| Domain | Weight |
| --- | --- |
| Agentic Architecture and Orchestration | 27% |
| Claude Code Configuration and Workflows | 20% |
| Prompt Engineering and Structured Output | 20% |
| Tool Design and MCP Integration | 18% |
| Context Management and Reliability | 15% |

Governance, safety, and reliability are not separate domains. They run through all five. Treat
them as a cross-cut, never as a standalone lab.

Six anchor scenarios are drawn from real customer deployments: customer support agents,
multi-agent research systems, CI/CD integrations, structured data extraction pipelines, internal
knowledge assistants, and developer-productivity tools. The capstones should mirror these.

### Three real primitives and their sharp edges

These three appear repeatedly as the hinge of hard questions. Each is real, and each has an edge
that a shallow study guide misses.

1. Path-scoped rules. `.claude/rules/*.md` files accept YAML frontmatter with a `paths` field of
   glob patterns. This is real (introduced around Claude Code v2.0.64). Edge: a path-scoped rule
   loads when Claude reads a file matching the pattern, not on every tool use, and there is a
   known issue that it is not injected when Claude writes or creates a matching file. So a rule
   meant to enforce a convention at file-creation time may not fire on its own.
   Source: https://code.claude.com/docs/en/memory

2. Structured outputs and citations are incompatible. Enabling citations together with the
   structured-output format returns a 400 error, because citations interleave citation blocks
   with text and that conflicts with strict JSON schema constraints. Structured outputs use a
   beta header (`structured-outputs-2025-11-13`) and constrained decoding. The correct pattern
   when you need both grounding and machine-readable output is multi-pass: a cited pass first,
   then a transform-to-schema pass, then a verification pass mapping structured claims back to
   cited evidence.
   Source: https://docs.claude.com/en/docs/build-with-claude/structured-outputs

3. Session forking. In the Agent SDK, `resume="<session_id>", fork_session=True` creates a new
   session that copies the parent history and then diverges. The fork gets its own session ID and
   the original is untouched, giving two independent branches. Edge: forking branches the
   conversation history, not the filesystem. If a forked agent edits files, those edits are real
   and visible to any session in the same working directory. To branch and revert file changes
   you need file checkpointing, not forking alone.
   Source: https://code.claude.com/docs/en/agent-sdk/sessions

## Repository structure

```
claude-architect-labs/
  README.md
  SPEC.md                       # this brief
  STUDY_GUIDE.md
  EXAM_DOMAIN_MAP.md            # the five domains, weights, and which labs map where
  SCENARIO_INDEX.md             # the six anchor scenarios and the labs that exercise each
  DISTRACTOR_TAXONOMY.md        # two-branch taxonomy, see below
  ENFORCEMENT_LAYER.md          # prompt-guides vs runtime-governs, per capability
  WHAT_NOT_TO_DO.md             # anti-patterns, see below
  VERIFIED.md                   # dated facts and source URLs

  labs/
    01-agent-loop-observability/
    02-tool-catalog-design/
    03-mcp-boundaries/
    04-claude-code-team-workflow/
    05-structured-output-reliability/
    06-context-management-failure-modes/

  practice/
    scenario_questions.md
    answer_rubrics.md
    timed_set_README.md

  shared/
    harness/
    mock_services/
    fixtures/
    evals/

  .claude/
    settings.json
    rules/
      house-style.md
```

## Per-lab template

Every lab folder has the same shape. Create these files for each v0.1 lab as stubs with the
section headers filled in and a one-line description, not full content.

```
README.md            # Scenario brief and the architecture goal
START_HERE.md        # What the learner must build, with a dry-run path
bad_version/         # An intentionally flawed implementation (placeholder for now)
solution/            # Reference implementation (placeholder for now)
DECISION_RECORD.md   # Why this design wins, with a mandatory governance section
FAILURE_MODES.md     # What can go wrong and how it is detected
EXAM_ANGLE.md        # How this maps to CCA-F reasoning and which domain weight it serves
questions.md         # Scenario questions, each carrying both distractor branches
answers.md           # Explained answers, including why each distractor is wrong
```

The `DECISION_RECORD.md` template must include these sections: Scenario, Constraints (latency,
cost, reliability, security, data sensitivity, human review, operational owner), Design chosen,
Alternatives rejected and why, Failure modes, Controls (what is enforced by prompt, what is
enforced by runtime, what is observable, what is auditable), Governance and escalation (mandatory:
where automation stops, the human-handoff path, the fail-safe behavior), and Exam angle.

## Distractor taxonomy (required in every question set)

The exam's difficulty lives in the wrong answers. Every scenario question in this repo must carry
at least one distractor from each of these two branches, and `answers.md` must label which branch
each distractor belongs to and why it fails.

Branch A, fabricated feature. A confident, plausible option that names a flag, directive, or
config switch that does not exist. Examples of the pattern (invent your own, do not copy any real
exam item): a made-up CLAUDE.md directive that claims to toggle a behavior, a made-up CLI flag, a
made-up settings mapping. The lesson: when an option proposes a switch that would be convenient if
it existed, distrust it. Eliminating this branch requires real feature fluency.

Branch B, valid but suboptimal. Two or more options that all work, where the question asks for the
best under the stated constraints. The losing options are usually more expensive, more wasteful,
enforced in the wrong layer (prompt where runtime is needed), or correct in mechanism but applied
after the fact rather than at the right point in the loop. Eliminating this branch requires
systemic judgment, not feature knowledge.

State the relationship between the branches explicitly in `DISTRACTOR_TAXONOMY.md`: feature
fluency is the gate that removes Branch A, architectural judgment is the discriminator that picks
the winner among the Branch B survivors. Feature knowledge is necessary, not sufficient.

## Governance cross-cut

Do not build a governance lab. Instead, make governance mandatory inside every lab via the
Governance and escalation section of `DECISION_RECORD.md`. Each lab must state where automation
should stop, the escalation or human-handoff path, what business rule is enforced and in which
layer, and how the system fails safely rather than silently.

## Timed reps requirement

The exam is two minutes per question, so recognition speed matters as much as depth. Each deep lab
must ship with a small timed set in `practice/`: five to ten scenario questions tied to that lab,
each with the two-branch distractors and a short rationale. The deep labs build judgment, the
timed sets make it fast.

## What not to do (seed WHAT_NOT_TO_DO.md)

- Do not treat the material as a product-knowledge test. Knowing a feature is the floor, not the
  answer. The questions reward systemic use under constraints.
- Do not ignore governance and safety. They are cross-cutting and heavily weighted in practice.
- Do not fixate on prompting alone. Orchestration, reliability, context, and Claude Code
  configuration carry the majority of the weight.
- Do not build a question bank only. Pair every question set with a deep lab.
- Do not build fifty shallow examples. Build few, deep labs.
- Do not require paid API calls to learn. Provide dry-run mode, mocked tool responses, and
  recorded fixtures, with optional live runs.
- Do not invent features. Every flag and directive must trace to a dated entry in VERIFIED.md.

## Currency and verification discipline

The repo's value depends on exact, current facts, and those facts carry version gates and open
bugs. Add a lightweight guard: keep `VERIFIED.md` dated, and add a CI check or a checklist that
re-verifies the three primitives and the domain weights before each tagged release. A public
artifact that drifts into teaching fabricated features would undercut its own thesis.

## Build order

- v0.1: labs 01 through 06, plus all cross-cutting documents fully written.
- v0.2: add labs for citations versus structured output, human escalation patterns, and agent
  permissions and sandboxing.
- v1.0: add the capstones mapped to the six anchor scenarios, plus a larger timed practice set.

Weight your effort to the domain percentages. Roughly a quarter of all labs and questions should
serve agentic architecture and orchestration, and the Claude Code plus prompt-engineering pair
together should carry about 40%.

## Your first task

Do only this now, then stop and confirm before writing lab internals:

1. Create the directory tree above.
2. Write `README.md` (mission, positioning disclaimer, structure overview).
3. Fully write the cross-cutting documents: `EXAM_DOMAIN_MAP.md`, `SCENARIO_INDEX.md`,
   `DISTRACTOR_TAXONOMY.md`, `ENFORCEMENT_LAYER.md`, `WHAT_NOT_TO_DO.md`, and `VERIFIED.md`
   (seeded with the three primitives and the domain table above, with dates and URLs).
4. For each of the six v0.1 labs, create the folder and the template files as stubs: each
   `README.md`, `START_HERE.md`, `EXAM_ANGLE.md`, and a `DECISION_RECORD.md` with the full
   section skeleton including the mandatory Governance and escalation section. Put `.gitkeep` in
   `bad_version/` and `solution/`.
5. Create `.claude/settings.json` and `.claude/rules/house-style.md` (with `paths: ["**/*.md"]`),
   and a repo `CLAUDE.md` encoding the house style and the no-invented-features rule.
6. Copy this brief to `SPEC.md`.

Then summarize what you created and ask which lab to build out first.
