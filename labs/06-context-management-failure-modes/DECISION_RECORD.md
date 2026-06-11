# Decision record: lab 06 context management failure modes

## Scenario

A multi-agent research session, the kind that backs a research system or an internal knowledge
assistant, accumulates context as subagents return findings and forks a subagent to revise shared
files. Two failures threaten it, and both are quiet. The context window overflows and an early
load-bearing detail (a hard user constraint) is dropped with no signal. And the forked subagent edits
shared files, but session forking branches the conversation history, not the filesystem (dated and
sourced in `../../VERIFIED.md`), so those edits land in the shared working directory and cannot be
reverted. The design in `bad_version` lets both happen silently.

## Constraints

The binding constraint is that a context failure is loud and recoverable rather than silent. A system
that drops a load-bearing detail without a signal, or that lets a forked branch mutate shared files
irreversibly, looks healthy while it is losing information and file safety, which is the worst kind of
failure to operate.

- Latency: checkpointing and summarizing at a boundary add a step, paid to avoid silent loss.
- Cost: pinning load-bearing context and summarizing the rest costs tokens, the price of not losing
  the detail that matters.
- Reliability: the load-bearing detail must survive overflow, and an overflow must be signaled.
- Security: a forked branch must not mutate shared files in a way the parent cannot see or revert.
- Data sensitivity: a dropped constraint or a leaked file edit can corrupt a downstream answer or
  artifact.
- Human review: an overflow signal and a held checkpoint give a person something to act on rather
  than a silent gap.
- Operational owner: the team that owns the orchestration owns the context budget, the checkpoint
  boundaries, and the file-isolation control.

## Design chosen

A hardened design (described by `session_design_good.json`) that fails loudly on both facets.

Context is budgeted by an orchestration limit, not a prompt instruction, so the budget is a control
the system enforces rather than a request the model may overrun. When accumulation crosses the
window, the overflow policy pins the load-bearing segments, summarizes the rest, and emits an overflow
signal. The load-bearing detail survives and the loss of the rest is announced, so the failure is loud
and recoverable.

File isolation uses file checkpointing, not forking alone. A forked branch's conversation diverges,
but its file edits would otherwise land in the shared working directory. Checkpointing the filesystem
before the branch isolates those edits and makes them revertible. This is the verified edge: forking
isolates the conversation, not the files, so file isolation needs its own control.

The decisive insight, visible in the runners, is that the silent design and the loud design use the
exact same engine. Only the design differs. A context failure is silent or loud because of the policy,
not because of the workload.

## Alternatives rejected and why

Relying on forking alone to isolate the branch's file changes. Forking branches the conversation
history, not the filesystem, so the branch's edits are real and visible to the parent and cannot be
reverted by the branch. This is the fabricated-convenience trap: there is no fork flag that snapshots
the filesystem. File isolation needs file checkpointing.

Summarizing only after overflow has already dropped information. Summarization is a real and useful
strategy, but applied after an eviction it compacts what is left while the load-bearing detail is
already gone. A lossy summary that collapses everything, including the load-bearing detail, and emits
no signal is the same silent failure in a different form. Correct mechanism, wrong point in the flow.

Budgeting context with a prompt instruction to be concise. A prompt is a guide. It lowers the chance
of overflow but does not enforce a limit, so a long run still overflows and drops context. A must-hold
budget belongs in an orchestration control, not a prompt.

## Failure modes

Summarized here and detailed in `FAILURE_MODES.md`: a silent context drop, a lossy summary that loses
the load-bearing detail, a context budget enforced by prompt rather than orchestration, a forked
branch that shares the filesystem, and an irreversible file edit from a branch with no checkpoint.

## Controls

- Enforced by prompt: a request to be concise or to preserve key facts, which guides behavior.
  Helpful, not load-bearing for a must-hold budget or for file isolation.
- Enforced by runtime: the orchestration budget, the checkpoint-and-signal overflow policy that pins
  load-bearing context, and file checkpointing for branch isolation. See `../../ENFORCEMENT_LAYER.md`.
- Observable: the overflow signal, the retained and dropped segments, and the branch leak and
  revertibility flags.
- Auditable: each run records the total against the limit, which load-bearing segments survived, and
  whether the branch's edits were isolated.

## Governance and escalation (mandatory)

- Where automation stops: the overflow policy stops silent loss by pinning the load-bearing segments
  and signaling, and the isolation control stops an unreviewable file mutation by checkpointing before
  the branch.
- Human-handoff path: the overflow signal surfaces the compaction for review, and a checkpointed
  branch edit can be reverted by a person rather than silently kept.
- Fail-safe behavior (fails safely rather than silently): the loud design preserves the load-bearing
  detail, signals the overflow, and isolates the branch, while the silent design drops the detail with
  no signal and lets the branch mutate shared files irreversibly. The contrast, same scenario and same
  engine, opposite outcome, is the lesson: design context handling to fail loudly, and isolate files
  with their own control because forking isolates the conversation, not the files.

## Exam angle

See `EXAM_ANGLE.md`. This lab serves the Context Management and Reliability domain (15%) with Agentic
Architecture and Orchestration (27%) as secondary. The transferable judgment is that context handling
must be designed to fail loudly, that a must-hold budget belongs in an orchestration control rather
than a prompt, and that forking isolates the conversation, not the files, so file isolation needs file
checkpointing.
