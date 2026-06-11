# Answers: lab 06 context management failure modes

Each answer names the correct option, then labels every distractor by branch (A fabricated feature,
B valid but suboptimal) and states why it fails. The pattern to internalize: feature fluency removes
the Branch A fabrications, and architectural judgment picks the winner among the Branch B survivors
(see `../../DISTRACTOR_TAXONOMY.md`).

## Question 1: correct answer is B

B checkpoints the filesystem before the branch, which isolates the subagent's edits and makes them
revertible. That is the real control for a branch that must undo its file changes, because forking
isolates the conversation, not the files (see `../../VERIFIED.md`).

- A is Branch A, fabricated feature. There is no `isolate_fs=True` option that makes a fork snapshot
  the filesystem. The convenient-sounding switch is the tell.
- C is Branch B, valid but suboptimal. A prompt instruction guides the subagent but does not isolate
  the files, so a mistaken edit still lands in the shared directory. Wrong layer.
- D is Branch B, valid but suboptimal. Dropping the fork removes the branch but also removes the
  parallel exploration the fork was for, and it still does not make file edits revertible.

## Question 2: correct answer is B

B pins the load-bearing context, summarizes the rest at a checkpoint boundary, and signals the
overflow, so the detail that matters survives and the loss is loud and recoverable.

- A is Branch B, valid but suboptimal. A prompt instruction guides but does not enforce, so the
  load-bearing detail can still be dropped on overflow. Wrong layer for a must-hold.
- C is Branch A, fabricated feature. There is no `context_autopreserve: true` switch that guarantees
  important context is never dropped. The real fix is pinning plus a signal.
- D is Branch B, valid but suboptimal. Tuning the eviction threshold still evicts silently, just
  later. It does not pin the load-bearing detail or signal the loss.

## Question 3: correct answer is B

B explains the timing error: summarizing after eviction compacts what remains while the load-bearing
detail is already gone, and the loss is still silent. The summary is applied at the wrong point in the
flow.

- A is Branch B, valid but suboptimal in the sense that it is a coherent but wrong position.
  Summarization cannot recover content that was already evicted.
- C is Branch A, fabricated feature. There is no `summary_recall: true` setting that restores evicted
  messages. Once dropped, they are gone.
- D is Branch B, valid but suboptimal. Speed is not the problem. The problem is that the summary runs
  after the information is lost, so summarizing faster does not help.

## Question 4: correct answer is B

B identifies that forking isolates the conversation but not the files, so file isolation needs file
checkpointing, which is exactly what the revert constraint requires.

- A is Branch B, valid but suboptimal. One mechanism is simpler, but forking does not isolate files,
  so the branch's edits are shared and irreversible. Simplicity does not meet the constraint.
- C is Branch A, fabricated feature. The `fork_session` call does not snapshot the working directory.
  Forking branches conversation history only.
- D is Branch B, valid but suboptimal. Avoiding shared files by convention is fragile and unenforced,
  and it does not give the branch a way to revert edits it does make.

## Question 5: correct answer is B

B states the thesis precisely: a prompt guides but does not enforce a budget, so a long run still
overflows and needs an orchestration limit and a signal.

- A is Branch B, valid but suboptimal. A concise instruction lowers the chance of overflow but does
  not cap context, so a long run still overflows.
- C is Branch A, fabricated feature. There is no `max_context_guard: true` switch that caps context
  automatically. The real control is an orchestration budget plus an overflow signal.
- D is Branch B, valid but suboptimal. "Usually stays concise" is not a guarantee, and a must-hold
  budget cannot depend on usual behavior.
