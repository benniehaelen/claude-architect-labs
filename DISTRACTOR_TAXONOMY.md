# Distractor taxonomy

The exam's difficulty lives in the wrong answers, so this repository trains on the wrong answers
deliberately. Every scenario question in the repository must carry at least one distractor from
each of the two branches described here, and every `answers.md` must label which branch each
distractor belongs to and explain why it fails.

## Branch A: fabricated feature

A confident, plausible option that names a flag, directive, or config switch that does not exist.
The option is attractive precisely because the named switch would be convenient if it were real.

Patterns to use (invent your own for each question, do not copy any real exam item):

- A made-up `CLAUDE.md` directive that claims to toggle a behavior.
- A made-up CLI flag for Claude Code.
- A made-up `settings.json` mapping or permission key.
- A made-up API parameter or beta header.

The lesson is direct: when an option proposes a switch that would solve the problem cleanly if it
existed, distrust it and verify against real feature knowledge. Eliminating Branch A requires
feature fluency. Every real feature this repository relies on is dated and sourced in `VERIFIED.md`,
which is also the standard a question author uses to confirm that a fabricated option is in fact
fabricated.

## Branch B: valid but suboptimal

Two or more options that all actually work, where the question asks for the best option under the
stated constraints. The losing options are wrong on judgment, not on existence. They are usually
one of the following:

- More expensive or more wasteful (extra tool calls, extra model passes, larger context than
  needed).
- Enforced in the wrong layer (a prompt instruction where a runtime control is required, or the
  reverse).
- Correct in mechanism but applied at the wrong point in the loop (after the fact rather than at
  the decision point, or post-hoc cleanup where a guardrail belonged upstream).
- Correct for a different constraint than the one the scenario actually binds on (optimizing
  latency when the binding constraint is data sensitivity, for example).

Eliminating Branch B requires systemic judgment, not feature knowledge. All the survivors are real
features used correctly in isolation. The discriminator is which one fits the constraint the
scenario actually places weight on.

## How the two branches relate

The relationship is the heart of the taxonomy and must be stated in every answer key.

Feature fluency is the gate that removes Branch A. Architectural judgment is the discriminator that
picks the winner among the Branch B survivors. Feature knowledge is necessary but not sufficient. A
candidate who knows every feature can still pick a Branch B loser, because knowing that three
options are all real does not tell you which one is right under the constraint. A candidate who
lacks feature fluency can be lured by a Branch A fabrication before judgment ever comes into play.

The two branches therefore test two different competencies in sequence. The question first checks
whether you can tell the real from the invented, then checks whether you can rank the real options
by fit. Both labs and timed sets are built so that a learner cannot pass by mastering only one of
the two.

## Authoring checklist for every question

1. Include at least one Branch A fabricated-feature distractor, and confirm against `VERIFIED.md`
   that the named switch genuinely does not exist.
2. Include at least two Branch B valid-but-suboptimal options that differ on cost, layer, timing,
   or which constraint they serve.
3. Make the correct option correct only under the stated constraints, so that changing the
   constraint would change the answer.
4. In `answers.md`, label each distractor by branch and state the specific reason it fails: the
   nonexistent switch for Branch A, and the precise judgment error for Branch B.
