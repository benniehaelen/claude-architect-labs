# Start here: lab 06

## What you will build

You will harden a multi-agent system against silent context failure. The deliverable is a design
that budgets context across agents, summarizes or checkpoints at defined boundaries, signals
overflow rather than dropping it, and uses file checkpointing where a branch must revert file
changes, plus an argument for why forking alone is insufficient for file isolation.

## Dry-run path

Run the lab against mocked agents and recorded fixtures so it costs nothing. The dry-run drives a
multi-agent research session into context overflow and a forked session that edits shared files, so
you can observe the silent failures and then the hardened design that surfaces them. A live run is
optional and clearly marked.

## Suggested path

1. Read `README.md` for the scenario and the run commands.
2. Run the silent design and read its analysis. Notice that the overflow drops the early load-bearing
   segment with no signal and the forked branch's file edits leak to the parent and cannot be
   reverted.
3. Run the loud design and compare. The load-bearing context is pinned and the overflow is signaled,
   and the branch's edits are checkpointed, so they are isolated and revertible.
4. Read `../../shared/harness/context.py`. Confirm that both runners call the same `run_session`
   engine and that only the design differs, and see how forking isolates the conversation but not the
   files.
5. Run `python shared/evals/check_lab06.py` to see the properties the design must satisfy, including
   the summarize-lossy design that isolates files but still loses load-bearing detail without
   signaling.
6. Work `questions.md`, then check `answers.md` and study the branch labels. Finish with the timed set
   in `../../practice/lab06_timed.md` against the clock.
7. Read `DECISION_RECORD.md`, paying attention to the mandatory Governance and escalation section, and
   connect it to the session-forking primitive in `../../VERIFIED.md`.

Status: built for v0.1.
