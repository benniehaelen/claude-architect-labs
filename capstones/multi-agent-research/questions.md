# Questions: multi-agent research system capstone

Five integrative scenario questions. Unlike the lab question sets, these require reasoning across more
than one lab at once: the bounded, observable, escalating loop (lab 01) and context management with the
session-forking edge (lab 06). Each carries at least one Branch A distractor (a fabricated feature) and
at least two Branch B distractors (valid but suboptimal). See `../../DISTRACTOR_TAXONOMY.md`. Answers
and branch labels are in `answers.md`. Do not read the answers until you have committed to a choice.

## Question 1

A research lead exhausts its step budget without gathering enough load-bearing findings to ground an
answer. What should it do?

A. Return the best answer it can assemble from what it found, noting low confidence.
B. Trip a circuit breaker and escalate to a human with a named reason and the evidence gathered so far.
C. Set `autoExtendBudget: true` so the lead keeps searching until it converges.
D. Loop again from the start in case the searches return different results.

## Question 2

The lead's context overflows as subagent findings accumulate. One early finding is load-bearing. The
team wants the answer, or the escalation, to keep that finding. Which overflow policy is correct?

A. Evict the oldest findings to fit, since the newest are most relevant.
B. Pin the load-bearing findings, summarize the rest, and signal the overflow.
C. Enable `contextPriority: "auto"` so the model keeps whatever is most important.
D. Summarize everything into one short note so nothing is dropped outright.

## Question 3

A subagent is forked from the lead and edits a shared results file. The team expects the fork to
isolate those edits so a bad subagent run can be discarded. The edits land in the shared tree anyway.
What is correct?

A. Forking should isolate the files, so this is a bug to report.
B. Forking branches the conversation history, not the filesystem, so a forked subagent that edits files
   needs a worktree or file checkpointing.
C. Set `fork_session(isolate_fs=True)` so the fork also snapshots the working directory.
D. Have the subagent avoid editing files the lead also uses.

## Question 4

Two research designs are proposed. Design X returns an answer whenever the loop ends, drops context
silently on overflow, and forks subagents without isolation. Design Y escalates when grounding is thin,
pins load-bearing findings and signals overflow, and isolates forked edits in a worktree. Under a
constraint that the system must fail loudly and keep its evidence, which is better and why?

A. Design X, because always returning an answer is more useful to the user than escalating.
B. Design Y, because escalating on thin grounding, loud overflow, and worktree isolation are what the
   fail-loudly-and-keep-evidence constraint requires.
C. Neither, because research quality is set by the `researchHardening` profile rather than by design.
D. Either, because the lead usually gathers enough evidence in practice.

## Question 5

After an incident, the team cannot reconstruct why a research run returned an unfounded answer, because
the run recorded nothing. The design composes a bounded loop, loud overflow, and worktree isolation but
has no observability. What is the best addition?

A. Record a structured trace of each subagent step, the circuit break, and the escalation, so the run
   is auditable.
B. Enable `autoTrace: true` so the platform reconstructs the orchestration from the final answer.
C. Add a prompt instruction telling the lead to summarize what it did at the end.
D. Keep the subagents' raw search outputs, since they contain everything that happened.
