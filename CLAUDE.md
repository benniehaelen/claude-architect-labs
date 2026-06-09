# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this
repository.

This is a public, unofficial teaching repository. Its credibility depends on two disciplines:
exact, current facts and a consistent house style. Both are enforced, not merely requested.

## No invented features

Every config flag, directive, API parameter, beta header, and primitive referenced anywhere in
this repository must be real and must trace to a dated entry in `VERIFIED.md`. Do not introduce a
feature, switch, or behavior that is not recorded there. If a task seems to need a capability that
does not exist, do not invent a plausible flag for it. Either name the real multi-step pattern that
achieves the goal, or stop and say the capability does not exist.

When you add or rely on a new fact, add it to `VERIFIED.md` first, with the verification date and a
source URL, then use it. Fabricated options are the exact trap the repository teaches learners to
avoid (Branch A in `DISTRACTOR_TAXONOMY.md`), so inventing one here would contradict the
repository's own thesis.

## House style

These rules apply to every Markdown file generated or edited in this repository. They are also
encoded as a path-scoped rule in `.claude/rules/house-style.md`.

- Do not use em-dashes anywhere. Use commas, periods, parentheses, or colons.
- Use sentence-case headings.
- Avoid contractions at sentence boundaries.
- Keep any reference to a real healthcare client or named internal platform out of this public
  repository. Use generic phrasing such as "a large healthcare organization" and "a production
  NL-to-SQL platform."
- Prefer prose over bullet soup. Use lists only where the content is genuinely enumerable.

## Why the rule alone is not enough

Path-scoped rules load when Claude reads a matching file, not when Claude writes or creates one
(see `VERIFIED.md`). The house-style rule therefore reliably shapes edits to existing files but can
be missed when a new file is created. For that reason the same rules are enforced at runtime:

- A PostToolUse hook (`.claude/hooks/check_house_style.py`) runs after every Write and Edit and
  fails on a forbidden em-dash in a Markdown file.
- A git pre-commit check (`.githooks/pre-commit`) blocks a commit that introduces one. Enable it
  after cloning with `git config core.hooksPath .githooks`.

This rule-plus-control pairing is itself the worked example of the repository's central thesis: a
prompt or rule guides behavior, a runtime control governs it. See `ENFORCEMENT_LAYER.md`.

## Scope discipline

The labs are built few and deep, one at a time. Do not scaffold lab internals (flawed versions,
reference solutions, full question sets) ahead of an explicit instruction to build a specific lab.
Stub structure is fine; speculative solution code is not.
