# Timed practice sets

The exam allows two minutes per question, so recognition speed matters as much as depth. The deep
labs build judgment. The timed sets here make it fast. Each deep lab ships a small set of five to
ten scenario questions tied to that lab, each carrying both distractor branches (see
`../DISTRACTOR_TAXONOMY.md`) and a short rationale.

## How to use these sets

Run a set against a clock at two minutes per question. Each answer is hidden inside a collapsible
block, so commit to a choice before you reveal it. When you review, do not stop at the right answer:
read why each real-but-losing option loses, because that judgment is the transferable skill. If a
question takes you longer than two minutes, return to the underlying lab rather than memorizing the
answer.

## Per-lab timed sets

These are added as each lab is built out.

| Set | Source lab | Status |
| --- | --- | --- |
| `lab01_timed.md` | 01 agent-loop-observability | Available |
| `lab02_timed.md` | 02 tool-catalog-design | Available |
| `lab03_timed.md` | 03 mcp-boundaries | Available |
| `lab04_timed.md` | 04 claude-code-team-workflow | Available |
| `lab05_timed.md` | 05 structured-output-reliability | Available |
| `lab06_timed.md` | 06 context-management-failure-modes | Available |
| `lab07_timed.md` | 07 human-escalation-patterns | Available |
| `lab08_timed.md` | 08 agent-permissions-sandboxing | Available |
| `capstone_support_timed.md` | customer support capstone (labs 01, 02, 07) | Available |
| `capstone_research_timed.md` | multi-agent research capstone (labs 01, 06) | Available |
| `capstone_dev_timed.md` | developer-productivity capstone (labs 02, 04) | Available |

Every built lab through v0.2 ships a timed set, and each v1.0 capstone ships an integrative one. The
capstone sets are cross-lab: their questions require composing more than one lab at once.

## Pooled set

`scenario_questions.md` and `answer_rubrics.md` hold an optional pooled set tagged by source lab and
domain, for mixed-topic timed runs. The pool is seeded and fills as more labs ship. See the build
order in `../SPEC.md`.
