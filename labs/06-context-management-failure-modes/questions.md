# Questions: lab 06 context management failure modes

Five scenario questions. Each carries at least one Branch A distractor (a fabricated feature) and at
least two Branch B distractors (valid but suboptimal under the stated constraints). See
`../../DISTRACTOR_TAXONOMY.md`. Answers and branch labels are in `answers.md`. Do not read the
answers until you have committed to a choice.

## Question 1

A multi-agent research lead forks a subagent to revise a shared report file. The team assumes the fork
isolates the subagent's file changes so they can be reverted. The changes turn out to be permanent and
visible to the parent. What is the best fix?

A. Pass `fork_session=True, isolate_fs=True` so the fork also snapshots the filesystem.
B. Checkpoint the filesystem before the branch so the subagent's edits are isolated and revertible.
C. Tell the subagent in its prompt not to touch files the parent still needs.
D. Run the subagent in the same session without forking, so there is only one history.

## Question 2

A long-running session overflows the context window. The current design evicts the oldest messages to
fit and continues. A hard user constraint stated early is silently lost. What is the soundest fix?

A. Add a line to the system prompt asking the model to keep important details in mind.
B. Pin the load-bearing context, summarize the rest at a checkpoint boundary, and signal the overflow.
C. Enable `context_autopreserve: true` so the model never drops important context.
D. Increase the eviction threshold so fewer messages are dropped.

## Question 3

A team adds summarization to a multi-agent system, but only after the context overflows and messages
have already been evicted. Why is this insufficient?

A. It is sufficient, because summarization always recovers the dropped content.
B. It is insufficient, because summarizing after eviction compacts what remains while the load-bearing
   detail is already gone, and the loss is still silent.
C. It is sufficient once `summary_recall: true` is set to restore evicted messages.
D. It is insufficient only because summaries are slower, so the fix is to summarize faster.

## Question 4

Two designs are proposed for a forking multi-agent workflow that edits files. Design X relies on
forking for both conversation and file isolation. Design Y forks for conversation and checkpoints the
filesystem for file isolation. Under a constraint that a branch must be able to revert its file
changes, which is better and why?

A. Design X, because forking is one mechanism for both and is simpler.
B. Design Y, because forking isolates the conversation but not the files, so file isolation needs file
   checkpointing.
C. Neither, because the `fork_session` call snapshots the working directory by default.
D. Either, because the branch can just avoid editing files the parent uses.

## Question 5

A reviewer says context overflow is handled because the system prompt asks every agent to be concise.
Long runs still drop information. Which statement is correct?

A. Overflow is handled, because a concise instruction keeps context within the window.
B. Overflow is not handled, because a prompt guides but does not enforce a budget, so a long run still
   overflows and needs an orchestration limit and a signal.
C. Overflow is handled once `max_context_guard: true` is set to cap context automatically.
D. Overflow is handled well enough, because agents usually stay concise when asked.
