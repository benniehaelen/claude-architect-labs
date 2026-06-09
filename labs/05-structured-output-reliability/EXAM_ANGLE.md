# Exam angle: lab 05

## Domain served

Primary: Prompt Engineering and Structured Output (20%). Secondary: Context Management and
Reliability (15%). With Claude Code configuration, prompt engineering anchors the roughly 40% the
pair carries.

## How this maps to CCA-F reasoning

This lab sits on one of the three verified primitives: citations and structured outputs are
incompatible in a single call and return a 400 (see `../../VERIFIED.md`). Questions here test
whether you know that incompatibility and reach for the multi-pass pattern. A Branch A trap names a
fabricated parameter or beta header that claims to enable citations and the structured-output
format together. A Branch B trap offers a real but weaker design: grounding by prompt instruction
alone with no verification pass, or a schema enforced by prompt rather than constrained decoding,
each correct in mechanism but failing the reliability or grounding constraint the scenario binds on.

The transferable judgment: when two real features conflict, the answer is the multi-pass pattern
that uses each where it is valid, not a fabricated flag that pretends the conflict away.
