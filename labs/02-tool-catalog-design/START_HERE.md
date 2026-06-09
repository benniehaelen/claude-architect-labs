# Start here: lab 02

## What you will build

You will redesign a flawed tool catalog. The deliverable is a revised set of tool definitions
(names, descriptions, and granularity) plus a short argument for where the catalog relies on
descriptions to guide selection and where it relies on permissions to govern action.

## Dry-run path

Run the lab against mocked tools and recorded fixtures so it costs nothing. The dry-run presents a
support agent and a developer-productivity agent, each with a catalog that causes a wrong or unsafe
tool choice you must diagnose and fix. A live run is optional and clearly marked.

## Suggested path

1. Read `README.md` for the scenario and the run commands.
2. Run the bad catalog and read its analysis. Notice the overlapping intents, the ungated dangerous
   tools, and that every routed request executes a dangerous tool with no gate.
3. Run the reference catalog and compare. Each intent has one obvious tool, and the gate escalates
   the unauthorized destructive action instead of running it.
4. Read `../../shared/harness/catalog.py`. Confirm that both runners call the same `drive` engine
   and that only the catalog differs.
5. Run `python shared/evals/check_lab02.py` to see the properties the design must satisfy.
6. Work `questions.md`, then check `answers.md` and study the branch labels. Finish with the timed
   set in `../../practice/lab02_timed.md` against the clock.
7. Read `DECISION_RECORD.md`, paying attention to the mandatory Governance and escalation section.

Status: built for v0.1.
