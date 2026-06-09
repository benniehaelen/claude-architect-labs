# Answers: lab 02 tool catalog design

Each answer names the correct option, then labels every distractor by branch (A fabricated feature,
B valid but suboptimal) and states why it fails. The pattern to internalize: feature fluency removes
the Branch A fabrications, and architectural judgment picks the winner among the Branch B survivors
(see `../../DISTRACTOR_TAXONOMY.md`).

## Question 1: correct answer is B

B removes the ambiguity at the catalog level, so each intent has one obvious tool. That is the
direct fix for wrong selection among overlapping tools.

- A is Branch B, valid but suboptimal. Adding a tool is real but makes selection harder, not
  easier. It increases overlap when the goal is to remove it. Wrong direction under the constraint.
- C is Branch A, fabricated feature. There is no `toolSelection: "strict"` config that forces
  correct selection. The convenient-sounding switch is the tell.
- D is Branch B, valid but suboptimal. Negative guidance in descriptions is real and mildly
  helpful, but it patches the symptom in the guide layer while the overlap remains. It does not
  make the right tool obvious.

## Question 2: correct answer is B

B splits the tool by effect and gates the dangerous path, which removes the over-privilege and puts
the high-impact action behind a control.

- A is Branch B, valid but suboptimal. A description warning is real but lives in the guide layer
  and cannot stop the cancel from executing. The routine call still carries destructive power.
- C is Branch A, fabricated feature. There is no `requireConfirm: all` settings key. It is also the
  wrong instrument, since confirming every read is wasteful.
- D is Branch B, valid but suboptimal. A prompt instruction enforces a must-hold safety property in
  the guide layer, so it is not reliable, and the coarse tool still bundles the capability.

## Question 3: correct answer is B

B enforces the stop in the runtime gate, which requires authorization and confirmation and escalates
an unauthorized request. That is the layer where a must-hold action belongs.

- A is Branch B, valid but suboptimal. Stating the requirement in the description is real but does
  not govern execution. Wrong layer for the requirement.
- C is Branch A, fabricated feature. There is no `dangerous: true` flag that makes the platform
  auto-confirm. Auto-confirming a destructive action would be the opposite of safe anyway.
- D is Branch B, valid but suboptimal. An audit log is real and useful, but it records the closure
  after it has already happened. Right mechanism, wrong point in the flow.

## Question 4: correct answer is B

B identifies that one-intent-per-tool removes ambiguity and gating governs the high-impact actions,
which is exactly what the safe, unambiguous-selection constraint asks for.

- A is Branch B, valid but suboptimal. More tools and more flexibility is a real tradeoff that
  serves coverage, not the safety and clarity constraint the question binds on.
- C is Branch A, fabricated feature. There is no `catalogLint` build step that sets catalog quality.
  Quality is a design property, not a tool that appears by naming it.
- D is Branch B, valid but suboptimal. Agents do not reliably learn correct selection from
  experience within a task, and reliability cannot rest on it.

## Question 5: correct answer is B

B states the thesis precisely: a description guides selection but only a runtime gate governs
execution, and with no gate the catalog is unsafe.

- A is Branch B, valid but suboptimal in the sense that it is a coherent but wrong position. A clear
  description is helpful and insufficient. It cannot prevent execution.
- C is Branch A, fabricated feature. There is no `descriptionEnforcement: true` switch that makes
  descriptions binding. Descriptions are guidance by nature.
- D is Branch B, valid but suboptimal. "Usually follows" is not a guarantee, and a must-hold safety
  property cannot depend on usual behavior.
