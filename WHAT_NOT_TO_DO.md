# What not to do

These are the anti-patterns this repository is built to correct. They apply both to how a candidate
studies and to how the labs themselves are built. Each one names a tempting shortcut and the
failure it leads to.

## Do not treat the material as a product-knowledge test

Knowing that a feature exists is the floor, not the answer. The scenarios reward systemic use under
constraints. A candidate who can recite every flag will still lose the Branch B comparisons, where
every option is a real feature and the question is which one fits the binding constraint. Study for
judgment, not recall.

## Do not ignore governance and safety

Governance, safety, and reliability are cross-cutting and heavily weighted in practice, even though
they are not a separate domain. A scenario that looks like a pure tool-design or prompting problem
will often hinge on where automation stops and how the system fails safely. Treat the governance
question as present in every scenario, named or not.

## Do not fixate on prompting alone

Prompt engineering is one domain of five. Orchestration, reliability, context management, and
Claude Code configuration carry the majority of the combined weight. A candidate strong only at
prompting is prepared for a minority of the exam.

## Do not build a question bank only

A bank of questions with no underlying lab trains recognition without understanding, and it does
not survive contact with novel scenarios. Every question set in this repository is paired with a
deep lab that builds the judgment the question tests. Questions without a lab are not shipped here.

## Do not build fifty shallow examples

Breadth without depth produces a tour of features and no architectural reasoning. This repository
builds a few deep labs rather than many shallow ones. Each lab carries a flawed version, a
reference solution, a decision record, a failure-mode catalog, and an exam-angle note, because the
reasoning is the product.

## Do not require paid API calls to learn

Cost should never be the barrier to understanding. Every lab ships a dry-run mode, mocked tool
responses, and recorded fixtures, with live runs optional. A learner can complete the reasoning
work of any lab without spending a cent on inference.

## Do not invent features

Every flag, directive, and primitive must trace to a dated entry in `VERIFIED.md`. A public
teaching artifact that drifts into teaching fabricated features would undercut its own thesis, and
it would train candidates to fall for exactly the Branch A distractors the exam uses. When a
convenient switch is needed but does not exist, the honest move is to name the real multi-step
pattern that achieves the goal, as the citations-versus-structured-output entry does.
