# Questions: lab 01 agent loop observability

Five scenario questions. Each carries at least one Branch A distractor (a fabricated feature) and
at least two Branch B distractors (valid but suboptimal under the stated constraints). See
`../../DISTRACTOR_TAXONOMY.md`. Answers and branch labels are in `answers.md`. Do not read the
answers until you have committed to a choice.

## Question 1

A customer support agent built on a tool-calling loop occasionally stops without producing an
answer, and the on-call team cannot tell from the logs what the agent decided or why it stopped.
The team needs incidents to be explainable and a failed run to reach a human. Under those
constraints, what is the best change?

A. Turn on the `--trace-loop` flag in the Claude Code CLI to expose the loop internals.
B. Add print statements before and after each tool call so the steps show up in the log.
C. Record a structured event at every decision point and tie a circuit breaker to repeated
   failures that escalates to a human queue and stops with a named reason.
D. Increase the loop's step budget so the agent has more chances to finish before it gives up.

## Question 2

During an upstream outage, the order-status tool returns 503 on every call. The agent loop catches
the errors, treats them as empty results, and returns "your order has shipped" to the customer.
The binding requirement is that the agent must never assert an answer it cannot support. Where
should the stop be enforced?

A. In the system prompt, by instructing the model to stop and escalate whenever a tool fails.
B. With a runtime circuit breaker that trips after a set number of consecutive tool failures,
   escalates, and returns no answer.
C. By setting `auto_escalate: true` in the project `CLAUDE.md` so failures hand off automatically.
D. By adding a post-run check that inspects the transcript and flags answers that followed tool
   errors.

## Question 3

A multi-agent research lead dispatches subagent searches that all return empty, and the run never
reaches a final answer. The team wants the system to stop and hand off rather than spin. What is
the best control?

A. Raise the per-run step budget so the lead can try more search angles before concluding.
B. Add a step-budget limit that, when exhausted, trips the breaker, escalates, and stops with a
   named reason.
C. Enable the `settings.json` key `"loopGuard": "auto"` to stop runaway loops automatically.
D. Instruct the lead in its prompt to give up after a few empty searches and escalate.

## Question 4

Two designs both record the agent's tool failures. Design X writes the failures to a log that is
analyzed after the run completes. Design Y emits each event through a callback as it happens and
increments a live failure counter the breaker reads. The requirement is that a control must be able
to act during the run, not only after it. Which design meets the requirement, and why does the
other fall short?

A. Design X, because analyzing the complete log is more thorough than reacting mid-run.
B. Design Y, because the signal reaches a control in time to govern the run, while Design X
   produces the right record at the wrong point in the loop.
C. Neither, because observability should be handled by the `observability="full"` API parameter
   rather than by application code.
D. Either, because both record the same failures and the timing does not matter.

## Question 5

The structured trace for a support agent contains tool arguments and results, including customer
data. Leadership asks how the design handles both the governance handoff and the sensitivity of the
trace. Which answer best reflects a sound design?

A. The trace is written to the default application log, and a prompt rule reminds the model not to
   include sensitive fields.
B. The breaker escalates failed runs to a named human queue, and the trace is treated as a
   sensitive asset with controlled storage and access.
C. The design enables `redactPII: true` in the loop config, which strips sensitive fields from the
   trace automatically.
D. The trace is kept only in memory and discarded at the end of each run, so sensitivity is not a
   concern.
