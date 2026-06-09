# Exam angle: lab 04

## Domain served

Primary: Claude Code Configuration and Workflows (20%). Secondary: Agentic Architecture and
Orchestration (27%). Together with prompt engineering, the Claude Code domain anchors the roughly
40% that the configuration-plus-prompting pair carries.

## How this maps to CCA-F reasoning

This lab sits on one of the three verified primitives: path-scoped rules load on Read, not on Write
(see `../../VERIFIED.md`). Questions here test whether you know that a rule guiding file creation
can silently fail, and whether you reach for a runtime control to govern a must-hold convention. A
Branch B trap offers a rules-only or memory-only answer that works for edits but misses new files,
correct in mechanism but applied in the wrong layer for the binding requirement. A Branch A trap
names a fabricated `CLAUDE.md` directive or settings key that claims to force a rule to load on
write.

The transferable judgment: match the enforcement layer to whether the requirement is a preference
or a must, and know the specific Read-versus-Write limitation that makes a rules-only answer wrong.
