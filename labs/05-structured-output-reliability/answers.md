# Answers: lab 05 structured output reliability

Each answer names the correct option, then labels every distractor by branch (A fabricated feature,
B valid but suboptimal) and states why it fails. The pattern to internalize: feature fluency removes
the Branch A fabrications, and architectural judgment picks the winner among the Branch B survivors
(see `../../DISTRACTOR_TAXONOMY.md`).

## Question 1: correct answer is B

B uses each feature where it is valid: a cited pass for grounding, a transform pass that applies the
strict schema with constrained decoding, and a verification pass that maps each record to its cited
evidence. That is the multi-pass pattern the incompatibility forces (see `../../VERIFIED.md`).

- A is Branch A, fabricated feature. There is no `citations_with_schema: true` parameter that combines
  citations and the structured-output format. The convenient-sounding switch is the tell.
- C is Branch B, valid but suboptimal. Dropping the structured format and parsing the schema out of
  text gives up constrained decoding, so the shape is no longer guaranteed. It trades a must-hold
  reliability property for convenience.
- D is Branch B, valid but suboptimal. Dropping citations and grounding by prompt gives up verifiable
  grounding, so an ungrounded claim can be emitted. It trades a must-hold grounding property for
  convenience.

## Question 2: correct answer is B

B enforces the schema with constrained decoding via the structured-output format, so the shape holds
by construction. That is the control layer for a must-hold shape.

- A is Branch B, valid but suboptimal. A prompt instruction guides the shape but does not guarantee it,
  so a record can still drift. Wrong layer for a must-hold.
- C is Branch A, fabricated feature. There is no `schema_lock: true` flag that makes any output conform
  automatically. The real mechanism is constrained decoding.
- D is Branch B, valid but suboptimal. A post-parse retry is real and a reasonable backstop, but it
  reacts after the fact and can loop, rather than governing the shape at generation time.

## Question 3: correct answer is B

B holds the unsupported record in a verification pass that maps each record to a cited evidence span
and routes it for review. That is the grounding control, and it fails safely rather than emitting an
unsupported fact.

- A is Branch B, valid but suboptimal. Schema-valid is not the same as grounded. Emitting it satisfies
  the parser and violates the grounding requirement.
- C is Branch B, valid but suboptimal. A low confidence field still emits the unsupported claim as a
  record and pushes the decision downstream, where it may be trusted anyway.
- D is Branch A, fabricated feature in spirit: it asserts a guarantee that does not exist. A cited pass
  does not guarantee that every transformed record is grounded, which is exactly why the verification
  pass exists.

## Question 4: correct answer is B

B identifies that using citations and the structured format in separate passes and verifying grounding
is what the grounded, schema-valid constraint requires.

- A is Branch B, valid but suboptimal. One call is cheaper and lower latency, but it returns a 400, so
  it does not produce output at all. Cost cannot be the deciding factor when the design fails.
- C is Branch A, fabricated feature. The `structured-outputs` beta header enables the structured-output
  format. It does not remove the conflict with citations. Setting it does not make a combined call
  valid.
- D is Branch B, valid but suboptimal. "Usually grounds" is not a guarantee, and a grounding
  requirement cannot rest on usual behavior.

## Question 5: correct answer is B

B states the thesis precisely: a prompt instruction guides but does not verify, so an ungrounded claim
can still be emitted without a verification pass.

- A is Branch B, valid but suboptimal in the sense that it is a coherent but wrong position. Instructing
  the model to cite is helpful and insufficient. It does not verify.
- C is Branch A, fabricated feature. There is no `require_citations: true` flag that makes grounding
  hold. The real control is a verification pass that maps claims to evidence.
- D is Branch B, valid but suboptimal. "Usually cites" is not a guarantee, and a grounding requirement
  cannot depend on usual behavior.
