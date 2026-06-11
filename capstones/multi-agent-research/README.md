# Capstone: multi-agent research system

This is the second v1.0 capstone, and the one `SCENARIO_INDEX.md` names as the worked example. A
capstone takes one anchor scenario end to end and combines the relevant labs into a single design
problem. The multi-agent research system is anchor scenario 2, and it composes two labs:

- Lab 01, agent loop observability. The lead orchestrates subagents within a step budget, records a
  structured trace, and escalates with a named reason when it cannot ground an answer, rather than
  looping forever or returning a confident but unfounded answer.
- Lab 06, context management. The subagents' findings accumulate into the lead's context, which can
  overflow and must be handled loudly. The subagents are forked, so their file edits need worktree
  isolation, because forking branches the conversation, not the filesystem (see `../../VERIFIED.md`).

Primary domain: Agentic Architecture and Orchestration (27%), with Context Management and Reliability
(15%).

## The design problem

A lead agent researches a niche question whose sources are thin. It spawns subagents to search, most of
which come back empty. The findings that do arrive accumulate past the context limit, one subagent is
forked and edits a shared file, and a second load-bearing source falls outside the step budget, so the
lead cannot reach the convergence threshold. The system must escalate to a human with its evidence
intact and auditable, rather than fabricate an answer, drop the one load-bearing finding, or let the
forked edits leak.

The composition is the difficulty. The orchestration bound and escalation (lab 01), the context
budgeting (lab 06), and the file isolation (lab 06) must all hold at once. A failure in any one
compounds: a silent context drop makes a fabricated answer look even more grounded than it is, and an
unobservable run hides all of it.

## How to run (dry-run, free, deterministic)

No installs and no paid API calls are needed. The flow is deterministic and reuses the lab engines.
From the repository root:

```
python capstones/multi-agent-research/bad_version/run.py
python capstones/multi-agent-research/solution/run.py
python shared/evals/check_capstone_research.py
```

Both runners use the same composed engine (`../../shared/harness/research_agent.py`), which reuses
lab 01's trace and loop config and lab 06's overflow and isolation engines directly. Only the design
differs. The naive design returns a confident answer with no grounding, drops the load-bearing finding
silently, leaks the forked edits, and records nothing. The composed design escalates with the evidence
pinned and the overflow signaled, isolates the forked edits, and leaves a full trace.

## Status

Built for v1.0. Includes the naive composition, the reference composition, the composed engine that
reuses the lab engines, the eval, the decision record, the question set, and a timed practice set
(`../../practice/capstone_research_timed.md`).
