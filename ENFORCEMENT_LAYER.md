# Enforcement layer

The central thesis of this repository fits in one sentence: a prompt or rule guides behavior, a
runtime control governs it. Knowing which capability belongs in which layer is the difference
between a design that usually works and a design that is safe to operate. This document states the
distinction, applies it per capability, and points at the repository's own house-style enforcement
as a worked example.

## The distinction

A guide shapes the model's behavior by influencing what it tends to do. System prompts, `CLAUDE.md`
memory, path-scoped rules, and tool descriptions are guides. They are probabilistic. They raise the
likelihood of the intended behavior, and they are invaluable for that, but they do not guarantee
it and they can be skipped, missed, or overridden by context.

A control governs behavior by making the unwanted outcome impossible or by stopping it
deterministically. Hooks, permission settings, pre-commit checks, schema-constrained decoding, CI
gates, and sandbox boundaries are controls. They are deterministic. They do not depend on the
model choosing correctly.

The error the exam probes repeatedly is enforcing a hard requirement with a guide, or paying for a
control where a guide would do. A business rule that must always hold belongs in a control. A
preference or a default that should usually hold belongs in a guide. Putting a must in the guide
layer is the most common Branch B mistake (see `DISTRACTOR_TAXONOMY.md`).

## Per-capability placement

| Capability | Guide layer | Control layer | When the control is mandatory |
| --- | --- | --- | --- |
| House style and conventions | path-scoped rule, `CLAUDE.md` | PostToolUse hook, pre-commit check | When the convention must hold on every created file, not just on files Claude reads |
| Tool use safety | tool description, system prompt | permission settings, hook gating the call | When a tool can take a destructive or outward-facing action |
| Structured output shape | prompt instruction, examples | schema-constrained decoding (structured outputs) | When a downstream system parses the output and cannot tolerate drift |
| Grounding and citations | prompt instruction to cite | verification pass mapping claims to evidence | When an ungrounded confident answer is a real harm |
| Context budgeting | prompt guidance to be concise | orchestration limits, summarization checkpoints, subagent boundaries | When overflow would silently drop information |
| Escalation and human handoff | prompt instruction to defer | runtime stop, routing to a human queue, fail-safe default | Always, for any irreversible or out-of-policy action |
| Agent file changes | prompt instruction to be careful | file checkpointing, sandbox, worktree isolation | When changes must be revertible or isolated between branches |

## Worked example: the repository's own house style

The house style in `.claude/rules/house-style.md` is a path-scoped rule with
`paths: ["**/*.md"]`. That rule is a guide. It loads when Claude reads a matching Markdown file, so
it reliably shapes edits to existing documents.

It has a known gap, dated and sourced in `VERIFIED.md`: a path-scoped rule is not injected when
Claude writes or creates a matching file. A new document can therefore be generated without the
rule ever firing. If the only enforcement were the rule, the convention would hold on edits and
silently fail on new files. That is exactly the guide-where-a-control-is-needed failure.

The repository closes the gap with two controls. A PostToolUse hook
(`.claude/hooks/check_house_style.py`) runs after every Write and Edit and fails when it finds a
forbidden em-dash in a Markdown file, surfacing the problem back to Claude immediately. A git
pre-commit check (`.githooks/pre-commit`) runs the same check on staged files and blocks the
commit. The rule guides, the hook and the pre-commit check govern. Neither layer alone is
sufficient: the rule misses new files, and a control with no guide would catch violations only
after they happen instead of steering away from them in the first place.

This is the pattern the labs train. When you see a requirement that must always hold, ask which
control enforces it, and treat any prompt-only answer to a must-hold requirement as suspect.
