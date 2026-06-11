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

## How to run (dry-run, free, deterministic)

No installs and no paid API calls are needed. The session logic is deterministic and reads a design
and a scenario from `../../shared/fixtures`. From the repository root:

```
python labs/06-context-management-failure-modes/bad_version/run.py
python labs/06-context-management-failure-modes/solution/run.py
python shared/evals/check_lab06.py
```

Both runners use the same session engine (`../../shared/harness/context.py`). Only the design
differs. The silent design budgets context by prompt, evicts the oldest segments on overflow with no
signal (dropping an early load-bearing detail), and relies on forking alone, so the forked branch's
file edits leak to the parent and cannot be reverted. The loud design budgets by an orchestration
limit, pins the load-bearing context and signals the overflow, and checkpoints the filesystem so the
branch is isolated and revertible. The eval also runs a summarize-lossy design that isolates files
but still loses load-bearing detail without signaling.

## Status

Built for v0.1. Includes the silent design, the loud design, the shared session engine (the overflow
policies, the branch-isolation policies, and the design analyzer), the failure-mode catalog, the
decision record, the question set, and a timed practice set
(`../../practice/lab06_timed.md`).
