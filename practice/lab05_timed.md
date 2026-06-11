# Timed set: lab 05 structured output reliability

Five questions at two minutes each. Train recognition speed, not derivation. Each answer is hidden
inside a collapsible block, so commit to a choice before you expand "Reveal answer." Each question
carries a Branch A fabricated-feature distractor and at least one Branch B valid-but-suboptimal
distractor. Full reasoning lives in the lab's `answers.md`. Source lab: 05. Domains: Prompt
Engineering and Structured Output, Context Management and Reliability.

## Q1

Records must be grounded in citations and valid against a strict schema. A single call asking for both
returns a 400. Best design?

A. Set `citations_with_schema: true`. B. Cited pass, constrained-decoding transform pass, verification
pass. C. Single call, citations only, parse the schema from text. D. Single call, structured format
only, ground by prompt.

<details>
<summary>Reveal answer</summary>

Answer: B. Rationale: A is a fabricated parameter (Branch A). C drops constrained decoding so the shape
is not guaranteed (Branch B). D drops verifiable grounding (Branch B).

</details>

## Q2

Records must always match a strict JSON schema a parser depends on. Where to enforce the shape?

A. A prompt instruction showing the schema. B. Constrained decoding via the structured-output format.
C. A `schema_lock: true` flag. D. A post-parse retry on parse failure.

<details>
<summary>Reveal answer</summary>

Answer: B. Rationale: C is a fabricated flag (Branch A). A only guides the shape (Branch B). D reacts
after the fact and can loop (Branch B).

</details>

## Q3

A schema-valid record asserts a fact no source span supports. What happens to it?

A. Emit it, it is schema-valid. B. Hold it in a verification pass that maps records to evidence, route
for review. C. Emit it with a low `confidence` field. D. Emit it, the cited pass guarantees grounding.

<details>
<summary>Reveal answer</summary>

Answer: B. Rationale: D asserts a guarantee that does not exist (Branch A in spirit). A emits an
unsupported fact (Branch B). C still emits it and pushes the risk downstream (Branch B).

</details>

## Q4

Design X: one call requesting citations and the structured format. Design Y: cited pass, constrained
transform pass, verification pass. Constraint: grounded, schema-valid output. Which wins?

A. X, cheaper and lower latency. B. Y, separate passes plus verification. C. Neither, the
`structured-outputs` beta header removes the conflict. D. Either, the model usually grounds claims.

<details>
<summary>Reveal answer</summary>

Answer: B. Rationale: C misreads a real header as removing the conflict (Branch A). A returns a 400 so
it produces nothing (Branch B). D rests grounding on usual behavior (Branch B).

</details>

## Q5

A reviewer says grounding is handled because the prompt tells the model to cite. There is no
verification pass. Correct statement?

A. Handled, instructing the model to cite suffices. B. Not handled, a prompt guides but does not
verify, so an ungrounded claim can be emitted. C. Handled once `require_citations: true` is set. D.
Handled well enough, the model usually cites.

<details>
<summary>Reveal answer</summary>

Answer: B. Rationale: C is a fabricated flag (Branch A). A and D treat a guide as a control, the core
error the lab corrects (Branch B).

</details>
