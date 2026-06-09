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

Status: the runnable harness and fixtures for this lab are added when the lab is built out. For now
this file records the intended shape of the exercise.
