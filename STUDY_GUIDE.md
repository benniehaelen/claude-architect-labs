# Study guide

This guide explains how to use the repository to prepare, in what order, and how to train for speed
as well as depth. It is unofficial and teaches architectural reasoning only. See the README for the
full positioning statement.

## How the pieces fit together

The repository has two kinds of material. The labs in `labs/` build judgment slowly by walking a
scenario from a flawed design to a defensible one. The timed sets in `practice/` make that judgment
fast, because the exam allows two minutes per question and recognition speed matters as much as
depth. Use them together. A lab without its timed set leaves you slow. A timed set without its lab
leaves you shallow.

The cross-cutting documents frame everything. Read `EXAM_DOMAIN_MAP.md` to see where effort should
go, `DISTRACTOR_TAXONOMY.md` to learn how the wrong answers are built, and `ENFORCEMENT_LAYER.md`
for the single distinction that most questions turn on.

## Suggested order

1. Read the cross-cutting documents first, in this order: `EXAM_DOMAIN_MAP.md`,
   `ENFORCEMENT_LAYER.md`, `DISTRACTOR_TAXONOMY.md`, `WHAT_NOT_TO_DO.md`. They give you the lens
   the labs assume.
2. Work the labs in numeric order. Each lab's `START_HERE.md` gives a dry-run path so you build
   before you read the solution.
3. For each lab, do the lab first, then its `questions.md`, then check `answers.md` and study the
   distractor labels, then run the paired timed set in `practice/` against the clock.
4. Re-verify the dated facts in `VERIFIED.md` near your exam date. The three primitives carry
   version gates and open bugs that can change.

## Studying for the two-branch distractors

Train the two competencies separately, then together. For Branch A, build feature fluency until a
fabricated flag looks obviously wrong: the only reliable defense is knowing the real surface, which
is why `VERIFIED.md` is the spine of the repository. For Branch B, practice ranking real options by
the binding constraint. When you check an answer, do not stop at the right option. Read why each
real-but-losing option loses, because that judgment is the transferable skill.

## Studying governance

Governance is not a chapter to study once. It is a question to ask of every scenario: where does
automation stop, what is the human-handoff path, which layer enforces the business rule, and how
does the system fail safely rather than silently. The labs make the Governance and escalation
section of each `DECISION_RECORD.md` mandatory so that the habit becomes automatic.

## Pacing

Practice at the real pace before exam day. Two minutes per question means you will not have time to
derive everything from first principles, so the timed sets train recognition of the pattern and
the binding constraint. If a timed question takes you longer than two minutes, treat that as a
signal to go back to the underlying lab, not as a reason to memorize the answer.
