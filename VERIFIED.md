# Verified facts

Every config flag, directive, and primitive used in this repository must be real and dated. This
file is the single source of truth. No lab, question, or document may reference a feature that does
not trace to a dated entry here. A fabricated feature in a public teaching artifact would undercut
the repository's own thesis, so this discipline is not optional.

Verified on 2026-06-08. Re-verify every entry before each tagged release.

## Exam shape and domain weights

The exam is scenario-based multiple choice. It has 60 questions and a 120-minute limit, which is
two minutes per question. The passing score is 720 of 1000. There are five domains with these
weights:

| Domain | Weight |
| --- | --- |
| Agentic Architecture and Orchestration | 27% |
| Claude Code Configuration and Workflows | 20% |
| Prompt Engineering and Structured Output | 20% |
| Tool Design and MCP Integration | 18% |
| Context Management and Reliability | 15% |

Governance, safety, and reliability are not separate domains. They run through all five and are
treated here as a cross-cut, never as a standalone lab.

Six anchor scenarios are drawn from real customer deployments: customer support agents,
multi-agent research systems, CI/CD integrations, structured data extraction pipelines, internal
knowledge assistants, and developer-productivity tools. The capstones mirror these. See
`SCENARIO_INDEX.md`.

## Three real primitives and their sharp edges

These three appear repeatedly as the hinge of hard questions. Each is real, and each has an edge
that a shallow study guide misses.

### 1. Path-scoped rules

`.claude/rules/*.md` files accept YAML frontmatter with a `paths` field of glob patterns. This is
real, introduced around Claude Code v2.0.64.

Edge: a path-scoped rule loads when Claude reads a file matching the pattern, not on every tool
use. There is a known issue that it is not injected when Claude writes or creates a matching file.
A rule meant to enforce a convention at file-creation time may therefore not fire on its own. The
correct response is to pair the rule with a runtime control (a hook or a pre-commit check), which
is exactly what this repository does for its own house style.

Source: https://code.claude.com/docs/en/memory

### 2. Structured outputs and citations are incompatible

Enabling citations together with the structured-output format returns a 400 error. Citations
interleave citation blocks with text, and that conflicts with the strict JSON schema constraints
of structured outputs. Structured outputs use a beta header (`structured-outputs-2025-11-13`) and
constrained decoding.

Edge: when you need both grounding and machine-readable output, you cannot get them in a single
pass. The correct pattern is multi-pass: a cited pass first, then a transform-to-schema pass, then
a verification pass that maps the structured claims back to the cited evidence.

Source: https://docs.claude.com/en/docs/build-with-claude/structured-outputs

### 3. Session forking

In the Agent SDK, `resume="<session_id>", fork_session=True` creates a new session that copies the
parent history and then diverges. The fork gets its own session ID and the original is untouched,
giving two independent branches.

Edge: forking branches the conversation history, not the filesystem. If a forked agent edits
files, those edits are real and visible to any session in the same working directory. To branch
and revert file changes you need file checkpointing, not forking alone.

Source: https://code.claude.com/docs/en/agent-sdk/sessions

## Re-verification checklist

Run this before each tagged release and update the verification date above.

1. Confirm the domain weights and exam shape against the current official exam guide.
2. Confirm path-scoped rules still load on Read and the write-time injection issue. Note the
   minimum Claude Code version that introduced the feature and any version where the bug is fixed.
3. Confirm the citations-plus-structured-output 400 error and the current beta header value.
4. Confirm the `fork_session` semantics and the filesystem-is-not-forked edge.
5. Update every dated reference in the labs and question sets that depends on these facts.
