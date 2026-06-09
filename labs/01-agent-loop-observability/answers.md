# Answers: lab 01 agent loop observability

Each answer names the correct option, then labels every distractor by branch (A fabricated feature,
B valid but suboptimal) and states why it fails. The pattern to internalize: feature fluency
removes the Branch A fabrications, and architectural judgment picks the winner among the Branch B
survivors (see `../../DISTRACTOR_TAXONOMY.md`).

## Question 1: correct answer is C

C records structured events at each decision point and ties a runtime breaker to a governed
escalation, which makes incidents explainable and routes failures to a human. That is exactly the
binding requirement.

- A is Branch A, fabricated feature. There is no `--trace-loop` Claude Code CLI flag that exposes
  agent loop internals. It is attractive because a single switch would be convenient, which is the
  tell. Eliminating it requires knowing the real CLI surface.
- B is Branch B, valid but suboptimal. Print statements work and are real, but they produce
  unstructured output that cannot be queried or asserted on, and they do not change failure
  behavior. Right instinct, wrong shape, and it does nothing for the escalation requirement.
- D is Branch B, valid but suboptimal. Increasing the step budget is a real lever aimed at the
  wrong constraint. The problem is not too few attempts, it is the absence of observability and a
  handoff.

## Question 2: correct answer is B

B places the must-hold stop in the runtime layer, where reliability does not depend on the model
choosing to comply. The breaker trips, escalates, and returns no answer.

- A is Branch B, valid but suboptimal. A prompt instruction is real and helpful, but it enforces a
  must-hold safety requirement in the guide layer. The model may not comply, and reliability cannot
  rest on that. Wrong layer for the requirement (see `../../ENFORCEMENT_LAYER.md`).
- C is Branch A, fabricated feature. There is no `auto_escalate` directive in `CLAUDE.md` that
  hands off on failure. `CLAUDE.md` is guidance, not a control plane with escalation switches.
- D is Branch B, valid but suboptimal. A post-run check is real but applied at the wrong point in
  the loop. It flags the bad answer after it has already been sent to the customer, which does not
  meet the requirement to never assert the unsupported answer in the first place.

## Question 3: correct answer is B

B adds a step-budget limit that trips the breaker and escalates, which stops the non-converging run
and hands it off as required.

- A is Branch B, valid but suboptimal. Raising the step budget is real and targets the wrong
  constraint. A loop that never converges will not converge with more steps, it will just spin
  longer and delay the handoff.
- C is Branch A, fabricated feature. There is no `"loopGuard": "auto"` key in `settings.json`. The
  plausible name is the lure.
- D is Branch B, valid but suboptimal. A prompt instruction to give up is real but enforces a
  must-stop behavior in the guide layer, so the stop is not guaranteed.

## Question 4: correct answer is B

B identifies that Design Y delivers the signal to a control in time to govern the run, while Design
X records the right thing at the wrong point in the loop (after the fact).

- A is Branch B, valid but suboptimal. Design X is a real, reasonable logging approach, but
  thoroughness after the run does not satisfy a requirement to act during the run. Wrong timing in
  the loop.
- C is Branch A, fabricated feature. There is no `observability="full"` API parameter that handles
  this. The convenient-sounding switch is the tell.
- D is Branch B, valid but suboptimal. It treats timing as irrelevant when timing is the entire
  point of the stated requirement, so it serves the wrong constraint.

## Question 5: correct answer is B

B pairs the governed escalation with treating the trace as a sensitive asset, which addresses both
the handoff and the data-sensitivity concern the question raises.

- A is Branch B, valid but suboptimal. Writing to the default log plus a prompt reminder is real
  but enforces data protection in the guide layer and stores a sensitive asset carelessly. Wrong
  layer and wrong storage decision.
- C is Branch A, fabricated feature. There is no `redactPII` loop-config switch that strips
  sensitive fields automatically. Redaction is real work, not a toggle.
- D is Branch B, valid but suboptimal. Discarding the trace destroys the auditability the lab is
  built to provide, trading one requirement away to avoid another instead of handling both.
