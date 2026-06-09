# Timed set: lab 01 agent loop observability

Five questions at two minutes each. Train recognition speed, not derivation. Cover the rationale
column until the clock is done. Each question carries a Branch A fabricated-feature distractor and
at least one Branch B valid-but-suboptimal distractor. Full reasoning lives in the lab's
`answers.md`. Source lab: 01. Domains: Agentic Architecture and Orchestration, Context Management
and Reliability.

## Q1

An agent loop fails silently and ops cannot reconstruct the run. Fastest sound fix?

A. Enable the `--trace-loop` CLI flag. B. Structured events per decision point plus a breaker that
escalates. C. Add print statements. D. Lower the temperature.

Answer: B. Rationale: A is a fabricated flag (Branch A). C is real but unstructured and changes no
behavior (Branch B). D is unrelated to observability (Branch B).

## Q2

A must-hold rule says never answer without tool evidence. Where does it belong?

A. System prompt instruction. B. Runtime circuit breaker. C. `CLAUDE.md` `auto_escalate: true`.
D. Larger context window.

Answer: B. Rationale: C is a fabricated directive (Branch A). A enforces a must in the guide layer
(Branch B, wrong layer). D is irrelevant to the requirement (Branch B).

## Q3

A loop never converges and must hand off. Best control?

A. Raise the step budget. B. `settings.json` `"loopGuard": "auto"`. C. Step-budget limit that trips
the breaker and escalates. D. Prompt the model to give up.

Answer: C. Rationale: B is a fabricated key (Branch A). A targets the wrong constraint (Branch B).
D enforces a must-stop in the guide layer (Branch B).

## Q4

A signal must govern the run, not just be logged for later. Which approach?

A. `observability="full"` API parameter. B. Emit events live and read a failure counter in the
breaker. C. Analyze the complete log after the run. D. Email the trace to the on-call engineer.

Answer: B. Rationale: A is a fabricated parameter (Branch A). C records the right thing at the wrong
time in the loop (Branch B). D is even later than C (Branch B).

## Q5

A trace holds customer data and a failed run must reach a human. Soundest design?

A. Default log plus a prompt reminder. B. Governed escalation to a named queue, trace treated as a
controlled sensitive asset. C. `redactPII: true` loop-config switch. D. Discard the trace each run.

Answer: B. Rationale: C is a fabricated switch (Branch A). A enforces protection in the guide layer
and stores carelessly (Branch B). D destroys the auditability the design exists to provide
(Branch B).
