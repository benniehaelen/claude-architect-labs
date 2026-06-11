# Timed set: multi-agent research system capstone

Five questions at two minutes each. These are integrative: they require composing the bounded,
observable, escalating loop (lab 01) and context management with the session-forking edge (lab 06).
Each answer is hidden inside a collapsible block, so commit to a choice before you expand "Reveal
answer." Each question carries a Branch A fabricated-feature distractor and at least one Branch B
valid-but-suboptimal distractor. Full reasoning lives in the capstone's `answers.md`. Source:
multi-agent research capstone.

## Q1

The lead exhausts its step budget without enough load-bearing findings to ground an answer. What should
it do?

A. Return its best answer with a low-confidence note. B. Trip the circuit breaker and escalate with a
named reason and the evidence. C. Set `autoExtendBudget: true`. D. Loop again from the start.

<details>
<summary>Reveal answer</summary>

Answer: B. Rationale: C is a fabricated switch (Branch A). A still ships an unfounded answer (Branch B).
D burns budget on the same thin sources (Branch B).

</details>

## Q2

Context overflows; an early finding is load-bearing and must survive. Which overflow policy?

A. Evict the oldest to fit. B. Pin load-bearing, summarize the rest, signal the overflow. C. Enable
`contextPriority: "auto"`. D. Summarize everything into one note.

<details>
<summary>Reveal answer</summary>

Answer: B. Rationale: C is a fabricated setting (Branch A). A drops the load-bearing finding silently
(Branch B). D collapses the load-bearing detail too (Branch B).

</details>

## Q3

A forked subagent edits a shared file, expected to be isolated. The edits land in the shared tree.
Correct?

A. Forking should isolate files, report a bug. B. Forking branches conversation, not the filesystem, so
use a worktree or checkpointing. C. Set `fork_session(isolate_fs=True)`. D. Have the subagent avoid
shared files.

<details>
<summary>Reveal answer</summary>

Answer: B. Rationale: C is a fabricated option (Branch A). A misexpects forking (Branch B). D is fragile
and not revertible (Branch B).

</details>

## Q4

Design X: always answers, silent overflow, forks without isolation. Design Y: escalates on thin
grounding, loud overflow, worktree isolation. Constraint: fail loudly and keep evidence. Which wins?

A. X, always answering is more useful. B. Y, escalation plus loud overflow plus isolation match the
constraint. C. Neither, quality is set by a `researchHardening` profile. D. Either, the lead usually has
enough evidence.

<details>
<summary>Reveal answer</summary>

Answer: B. Rationale: C is a fabricated profile (Branch A). A prefers an unfounded answer (Branch B). D
rests on the thin case being rare (Branch B).

</details>

## Q5

After an incident, the team cannot reconstruct why a run answered unfounded: it recorded nothing. Best
addition?

A. Record a structured trace of each subagent step, the circuit break, and the escalation. B. Enable
`autoTrace: true`. C. Prompt the lead to summarize at the end. D. Keep the raw search outputs.

<details>
<summary>Reveal answer</summary>

Answer: A. Rationale: B is a fabricated switch (Branch A). C produces narrative, not a structured trail
(Branch B). D is not a record of orchestration decisions (Branch B).

</details>
