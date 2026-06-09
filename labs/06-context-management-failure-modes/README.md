# Lab 06: context management failure modes

Primary domain: Context Management and Reliability (15%). Secondary: Agentic Architecture and
Orchestration. Anchor scenarios: multi-agent research systems, internal knowledge assistants.

## Scenario brief

Long-running and multi-agent systems accumulate context until it overflows, and the dangerous
failures are the quiet ones: information silently dropped, a summarization that loses the load
bearing detail, or a branch that diverges in conversation but shares a filesystem. Session forking
copies conversation history but not the filesystem, so a forked agent's file edits are real and
visible to every session in the same working directory (dated and sourced in `../../VERIFIED.md`).
This lab is about anticipating and detecting context failure modes.

## Architecture goal

Design context management that fails loudly rather than silently: budget context across agents,
checkpoint and summarize at the right boundaries, and use file checkpointing (not forking alone)
when a branch must be able to revert file changes. The lab contrasts a system that silently drops
context against one that detects and signals overflow and isolates file state correctly.

Status: scaffolded for v0.1. The flawed version, reference solution, failure-mode catalog, and
question set are added when this lab is built out.
