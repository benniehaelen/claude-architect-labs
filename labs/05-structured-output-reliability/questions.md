# Questions: lab 05 structured output reliability

Five scenario questions. Each carries at least one Branch A distractor (a fabricated feature) and at
least two Branch B distractors (valid but suboptimal under the stated constraints). See
`../../DISTRACTOR_TAXONOMY.md`. Answers and branch labels are in `answers.md`. Do not read the
answers until you have committed to a choice.

## Question 1

An extraction pipeline must return records that are both grounded in citations and valid against a
strict schema. A single call requesting citations and the structured-output format returns a 400. What
is the best design?

A. Set the `citations_with_schema: true` parameter so the call accepts both at once.
B. Run a cited pass for grounding, a transform pass that applies the strict schema with constrained
   decoding, and a verification pass that maps each record to its cited evidence.
C. Keep the single call but request citations and drop the structured-output format, parsing the
   schema out of the text afterward.
D. Keep the single call but request the structured-output format and drop citations, adding grounding
   by a prompt instruction.

## Question 2

A team needs the extracted records to always match a strict JSON schema that a downstream parser
depends on. Where should the schema be enforced?

A. In a prompt instruction that shows the schema and asks the model to follow it.
B. In constrained decoding via the structured-output format, so the shape holds by construction.
C. In a `schema_lock: true` flag that makes any model output conform automatically.
D. In a post-parse step that retries the call when the output fails to parse.

## Question 3

In a multi-pass pipeline, the transform pass produces a schema-valid record asserting a fact that no
source span supports. What should happen to that record?

A. Emit it, because it is schema-valid and the parser will accept it.
B. Hold it in a verification pass that maps each record to a cited evidence span, and route it for
   review.
C. Emit it but set its `confidence` field low so the downstream system can decide.
D. Emit it, because the cited pass already ran, so grounding is guaranteed.

## Question 4

Two designs are proposed. Design X makes a single call requesting citations and the structured-output
format. Design Y runs a cited pass, a constrained-decoding transform pass, and a verification pass.
Under a constraint of grounded, schema-valid output, which is better and why?

A. Design X, because one call is cheaper and lower latency.
B. Design Y, because it uses citations and the structured format in separate passes and verifies
   grounding, which is what the constraint requires.
C. Neither, because the conflict is removed by the `structured-outputs` beta header once it is set.
D. Either, because the model usually grounds its claims when asked.

## Question 5

A reviewer says grounding is handled because the extraction prompt tells the model to cite its
sources, and the pipeline has no verification pass. Which statement is correct?

A. Grounding is handled, because instructing the model to cite is sufficient.
B. Grounding is not handled, because a prompt instruction guides but does not verify, so an ungrounded
   claim can still be emitted without a verification pass.
C. Grounding is handled once `require_citations: true` is set to make citations mandatory.
D. Grounding is handled well enough, because the model usually cites when instructed.
