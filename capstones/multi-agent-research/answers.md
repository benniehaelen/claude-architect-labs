# Answers: multi-agent research system capstone

Each answer names the correct option, then labels every distractor by branch (A fabricated feature,
B valid but suboptimal) and states why it fails. These questions reward composing the labs: feature
fluency removes the Branch A fabrications, and the integration judgment across labs 01 and 06 picks the
winner among the Branch B survivors (see `../../DISTRACTOR_TAXONOMY.md`).

## Question 1: correct answer is B

B trips the circuit breaker and escalates to a human with a named reason and the evidence gathered, the
lab 01 governed handoff. When grounding is thin, escalating is the safe failure rather than fabricating
an answer.

- A is Branch B, valid but suboptimal. A low-confidence answer is still a confident-sounding research
  result built on thin grounding, which is the harm the scenario most needs to avoid.
- C is Branch A, fabricated feature. There is no `autoExtendBudget: true` switch, and removing the
  budget would let the lead search forever.
- D is Branch B, valid but suboptimal. Looping again wastes budget on the same thin sources and does not
  change the grounding.

## Question 2: correct answer is B

B pins the load-bearing findings, summarizes the rest, and signals the overflow, the lab 06 loud-overflow
policy, so the load-bearing finding survives and the loss of the rest is announced.

- A is Branch B, valid but suboptimal. Evicting the oldest drops the early load-bearing finding silently,
  which is exactly the failure to avoid.
- C is Branch A, fabricated feature. There is no `contextPriority: "auto"` setting that preserves
  importance. Pinning is a policy you build, not a switch.
- D is Branch B, valid but suboptimal. A single lossy summary collapses the load-bearing detail along
  with the rest and signals nothing.

## Question 3: correct answer is B

B states the verified primitive: forking branches the conversation history, not the filesystem, so a
forked subagent that edits files needs a worktree or file checkpointing.

- A is Branch B, valid but suboptimal in the sense that it is a coherent but wrong expectation. Forking
  was never going to isolate files, so this is not a bug.
- C is Branch A, fabricated feature. There is no `isolate_fs=True` option on forking that snapshots the
  working directory.
- D is Branch B, valid but suboptimal. Avoiding shared files by convention is fragile and does not make
  a subagent's edits revertible.

## Question 4: correct answer is B

B identifies the composed design: escalating on thin grounding, loud overflow, and worktree isolation
are exactly what the fail-loudly-and-keep-evidence constraint requires.

- A is Branch B, valid but suboptimal. Always returning an answer feels useful, but an unfounded research
  answer is worse than an honest escalation.
- C is Branch A, fabricated feature. There is no `researchHardening` profile that sets quality. Quality is
  a composition of real controls.
- D is Branch B, valid but suboptimal. "Usually gathers enough" is a frequency argument, and a
  fail-loudly requirement cannot rest on the thin-source case being rare.

## Question 5: correct answer is A

A records a structured trace of each subagent step, the circuit break, and the escalation, the lab 01
observability control that makes the run auditable.

- B is Branch A, fabricated feature. There is no `autoTrace: true` switch that reconstructs the
  orchestration from the answer. Observability is built into the loop.
- C is Branch B, valid but suboptimal. A prompt instruction to summarize produces a narrative, not a
  reliable structured trail of the decisions.
- D is Branch B, valid but suboptimal. Raw search outputs are not a record of the lead's orchestration
  decisions, so they do not explain why it answered or escalated.
