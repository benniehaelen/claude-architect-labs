# Decision record: multi-agent research system capstone

## Scenario

A lead agent researches a niche question with thin sources. It spawns subagents to search within a
step budget, accumulates their findings into its context, forks a subagent that edits a shared file,
and must decide whether it can answer. In the session, most subagents return empty, only one returns a
load-bearing finding within the budget, the accumulated findings overflow the context limit, and a
second load-bearing source falls outside the budget. The naive design in `bad_version` returns a
confident answer anyway, drops the one load-bearing finding silently, lets the forked edits leak, and
records nothing.

## Constraints

The binding constraint is that the system fails loudly and safely when it cannot ground an answer, with
its evidence and its file state intact and the whole run auditable. A confident but unfounded research
answer is the central harm, and a silent context drop or a leaked file edit makes it worse.

- Latency: the step budget bounds the run, and escalation replaces an unbounded search.
- Cost: spawning subagents costs tokens, so the budget and the convergence threshold keep the lead from
  searching forever.
- Reliability: the load-bearing findings must survive overflow, and the lead must not fabricate an
  answer from thin grounding.
- Security: a forked subagent's file edits must not leak into the shared tree irreversibly.
- Data sensitivity: a fabricated research answer presented as grounded is a trust harm downstream.
- Human review: when the lead cannot ground an answer, a human must receive the question with the
  evidence gathered so far.
- Operational owner: the team that owns the research system owns the step budget, the overflow policy,
  the isolation policy, and the observability.

## Design chosen

The composed design (in `research_design_good.json`) wires the lessons of both labs together, reusing
their engines.

Bounded, observable orchestration with escalation (lab 01). The lead runs within a step budget and
records a trace of every step. When the surviving load-bearing findings do not reach the convergence
threshold, it trips a circuit breaker and escalates to a human with a named reason, rather than
returning a confident but unfounded answer.

Loud context budgeting (lab 06). The overflow policy pins the load-bearing findings, summarizes the
rest, and signals the overflow, so the one load-bearing finding survives and the loss of the rest is
announced rather than silent.

Worktree isolation for forks (lab 06). The forked subagent's file edits are checkpointed, so they are
isolated from the lead and revertible, because forking branches the conversation, not the filesystem.

The decisive insight, visible in the runners, is that the naive design and the composed design use the
exact same engine. Only the four design choices differ. The system fabricates or escalates, loses
evidence or preserves it, leaks files or isolates them, hides the run or records it, because of the
composition, not the workload.

## Alternatives rejected and why

Returning the best answer the lead can assemble even when grounding is thin. This is the lab 01
black-box failure. It produces a confident, unfounded research answer, which is the harm the scenario
most needs to avoid. The lead must escalate when it cannot ground an answer.

Escalating correctly but using a silent overflow policy. The lead would hand the question to a human,
but the one load-bearing finding would already have been dropped silently, so the human inherits less
evidence than the run actually gathered. Loud overflow that pins the load-bearing findings is required
for the escalation to carry its evidence.

Relying on forking alone to isolate the subagents' file edits. Forking branches the conversation
history, not the filesystem, so a forked subagent's edits land in the shared tree and cannot be
reverted. File isolation needs a worktree or file checkpointing.

## Failure modes

Summarized here and detailed across the source labs' `FAILURE_MODES.md`: a confident answer with no
grounding, a silent context drop that loses a load-bearing finding, a forked subagent whose edits leak,
and an unobservable run that cannot be audited. The capstone shows these compounding: the naive design
fabricates an answer that a dropped finding makes look even more grounded, with no trace to catch it.

## Controls

- Enforced by prompt: guidance to the lead to cite and to defer when unsure, which shapes behavior.
  Helpful, not load-bearing.
- Enforced by runtime: the step budget and circuit breaker, the escalation handoff, the overflow policy
  that pins load-bearing findings and signals, and worktree isolation. See `../../ENFORCEMENT_LAYER.md`.
- Observable: the orchestration trace, the dropped-load-bearing list and overflow signal, and the leak
  and revertibility flags.
- Auditable: the trace records each subagent step, the circuit break, and the escalation.

## Governance and escalation (mandatory)

- Where automation stops: the lead stops and escalates when the surviving load-bearing findings do not
  reach the convergence threshold, rather than answering, and the overflow policy stops a silent loss
  by pinning the load-bearing findings.
- Human-handoff path: the lead escalates the question to the research review queue with the evidence it
  gathered, so a person continues the work rather than trusting a fabricated answer.
- Fail-safe behavior (fails safely rather than silently): the composed design escalates with the
  evidence pinned, the overflow signaled, the forked edits isolated, and the run traced, while the naive
  design fabricates an answer, drops the load-bearing finding silently, leaks the edits, and records
  nothing. The contrast, same session and same engine, opposite outcome, is the capstone lesson: a safe
  research system composes a bounded, observable, escalating loop with loud context budgeting and
  worktree isolation, and a failure in any one layer compounds into a system failure.

## Exam angle

This capstone integrates the reasoning from labs 01 and 06. It serves Agentic Architecture and
Orchestration (27%) primarily, with Context Management and Reliability (15%). The transferable judgment
is that a multi-agent system must escalate rather than fabricate when grounding is thin, must budget
context loudly so evidence survives, and must isolate forked file state, because forking branches the
conversation, not the filesystem.
