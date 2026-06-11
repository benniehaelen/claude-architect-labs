# Timed set: lab 06 context management failure modes

Five questions at two minutes each. Train recognition speed, not derivation. Each answer is hidden
inside a collapsible block, so commit to a choice before you expand "Reveal answer." Each question
carries a Branch A fabricated-feature distractor and at least one Branch B valid-but-suboptimal
distractor. Full reasoning lives in the lab's `answers.md`. Source lab: 06. Domains: Context
Management and Reliability, Agentic Architecture and Orchestration.

## Q1

A forked subagent revises a shared report. The team assumed the fork isolates and lets them revert the
edits. The edits are permanent and visible to the parent. Best fix?

A. Pass `fork_session=True, isolate_fs=True`. B. Checkpoint the filesystem before the branch. C.
Prompt the subagent not to touch needed files. D. Run it in the same session without forking.

<details>
<summary>Reveal answer</summary>

Answer: B. Rationale: A is a fabricated option (Branch A). C only guides and does not isolate files
(Branch B). D removes the parallel branch and still does not make edits revertible (Branch B).

</details>

## Q2

A long session overflows and evicts the oldest messages. A hard user constraint stated early is
silently lost. Soundest fix?

A. Ask the system prompt to keep important details in mind. B. Pin load-bearing context, summarize the
rest at a checkpoint, signal the overflow. C. Enable `context_autopreserve: true`. D. Raise the
eviction threshold.

<details>
<summary>Reveal answer</summary>

Answer: B. Rationale: C is a fabricated switch (Branch A). A only guides (Branch B). D still evicts
silently, just later (Branch B).

</details>

## Q3

A team summarizes, but only after overflow has already evicted messages. Why insufficient?

A. Sufficient, summarization always recovers dropped content. B. Insufficient, summarizing after
eviction compacts what remains while the load-bearing detail is already gone, still silently. C.
Sufficient once `summary_recall: true` restores evicted messages. D. Insufficient only because
summaries are slower.

<details>
<summary>Reveal answer</summary>

Answer: B. Rationale: C is a fabricated setting (Branch A). A claims a recovery that cannot happen
(Branch B). D blames speed, not the timing (Branch B).

</details>

## Q4

Design X: forking for both conversation and file isolation. Design Y: forking for conversation, file
checkpointing for files. Constraint: a branch must revert its file changes. Which wins?

A. X, one mechanism is simpler. B. Y, forking isolates conversation but not files, so files need
checkpointing. C. Neither, `fork_session` snapshots the working directory by default. D. Either, the
branch can avoid shared files.

<details>
<summary>Reveal answer</summary>

Answer: B. Rationale: C misstates `fork_session` (Branch A). A is simpler but does not isolate files
(Branch B). D relies on fragile convention and still cannot revert (Branch B).

</details>

## Q5

A reviewer says overflow is handled because the prompt asks every agent to be concise. Long runs still
drop information. Correct statement?

A. Handled, a concise instruction keeps context in the window. B. Not handled, a prompt guides but
does not enforce a budget, so a long run overflows and needs an orchestration limit and a signal. C.
Handled once `max_context_guard: true` is set. D. Handled well enough, agents usually stay concise.

<details>
<summary>Reveal answer</summary>

Answer: B. Rationale: C is a fabricated switch (Branch A). A and D treat a guide as a control, the core
error the lab corrects (Branch B).

</details>
