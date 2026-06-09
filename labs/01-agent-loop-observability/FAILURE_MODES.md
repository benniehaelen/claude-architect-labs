# Failure modes: lab 01 agent loop observability

Each failure mode below names what goes wrong, how it is detected (or why it is not), and what the
reference design does about it. Run the fixtures in `../../shared/fixtures` to see several of these
directly.

## Swallowed tool errors

A tool fails and the loop catches the error and treats it as an empty result, continuing as if
nothing happened. This is the central defect in `bad_version/run.py`. It is invisible by
construction: there is no record that the failure occurred. Detection requires recording the
failure as a structured event, which the instrumented loop does (`tool_error` events). The eval
asserts that exactly three failures are recorded on the failure session rather than swallowed.

## Confident ungrounded answer on failure

After tools fail, the loop still reaches a final answer and returns it confidently. On the failure
session the black-box loop tells the customer the order shipped during an upstream outage. Detection
is impossible from the output alone, since the answer looks normal. The reference design prevents it
by tripping the circuit breaker before the unfounded answer is reached and returning no answer at
all.

## Loop that never converges

A run keeps calling tools without ever finishing, for example a research lead whose searches all
return empty. With no step budget the loop spins. Detection is the step-budget limit. The
instrumented loop stops at the budget, records a `circuit_break` with reason
`step_budget_exhausted`, escalates, and stops with a named reason. The `research_session_budget`
fixture exercises this path.

## Breaker mistuned

A circuit breaker tuned too tight escalates on a single transient blip, creating noise and
unnecessary human load. Tuned too loose, it never fires and the unsafe behaviors above return.
Detection is operational: track the escalation rate and the reasons. The reference exposes
`max_consecutive_failures` and `max_steps` as configuration so the breaker can be tuned to the
service, and it separates a transient single failure (tolerated) from repeated failure (escalated).

## Sensitive data in the trace

The trace records tool arguments and results, which in support and research settings can include
customer or source data. The failure mode is storing the trace where it should not be, or exposing
it to the wrong readers. Detection is a review of where the trace is persisted. The decision record
flags this under data sensitivity and security: the trace is an asset that must be stored and
access-controlled deliberately, not logged to wherever is convenient.

## Observability that cannot act in time

A subtler mode: the loop records the right signal but only after the run finishes, so nothing can
act on it during the run. This is the Branch B trap the exam angle calls out. The reference emits
events through a callback as they happen and ties the breaker to the live failure count, so the
signal governs the run rather than merely describing it afterward.
