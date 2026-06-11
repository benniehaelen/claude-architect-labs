# Start here: lab 04

## What you will build

You will fix a team Claude Code configuration that relies on a path-scoped rule to enforce a
convention at file-creation time. The deliverable is a layered configuration: the rule kept as a
guide, plus a runtime control (a hook or a pre-commit or CI check) that governs the convention on
created files, with an argument for what belongs in each layer.

## Dry-run path

Run the lab against a mocked Claude Code session and recorded fixtures so it costs nothing. The
dry-run demonstrates a new file created without the rule firing, then the same case with the
runtime control in place. This repository's own `.claude/rules/house-style.md` plus its
`check_house_style.py` hook and `.githooks/pre-commit` check are the live reference. A live run is
optional and clearly marked.

## Suggested path

1. Read `README.md` for the scenario and the run commands.
2. Run the rules-and-memory configuration and read its analysis. Notice that the new-file event is
   unenforced because the rule does not load on create, the commit is unenforced because memory
   cannot block it, and a preference is over-controlled by a hook.
3. Run the layered configuration and compare. The hook governs create and edit, the pre-commit check
   and CI gate govern the commit, and the preference is guided by the rule.
4. Read `../../shared/harness/config.py`. Confirm that both runners call the same `drive` engine and
   that only the configuration differs, and study the `LAYER_FIRES_ON` table where the rule fires on
   edit but not create.
5. Run `python shared/evals/check_lab04.py` to see the properties the configuration must satisfy.
6. Work `questions.md`, then check `answers.md` and study the branch labels. Finish with the timed
   set in `../../practice/lab04_timed.md` against the clock.
7. Read `DECISION_RECORD.md`, paying attention to the mandatory Governance and escalation section,
   and connect it to this repository's own house-style enforcement and the primitive in
   `../../VERIFIED.md`.

Status: built for v0.1.
