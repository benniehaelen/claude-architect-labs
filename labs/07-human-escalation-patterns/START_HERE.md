# Start here: lab 07

## What you will build

You will fix a weak escalation policy. The deliverable is a policy that covers every must-escalate
case with triggers, escalates before an irreversible action rather than after, routes to a defined
human queue, and holds rather than proceeds when escalation cannot be delivered, plus an argument for
why each of those four properties is a runtime control rather than a prompt instruction.

## Dry-run path

Run the lab against mocked requests and recorded fixtures so it costs nothing. The dry-run classifies a
set of support requests under a weak policy that misses and delays escalations, then under a sound
policy that reaches a human at the right time. A live run is optional and clearly marked.

## Suggested path

1. Read `README.md` for the scenario and the run commands.
2. Run the weak policy and read its analysis. Notice that the out-of-policy exception and the explicit
   human request are handled automatically, and the high-impact account closure is escalated only after
   it runs.
3. Run the sound policy and compare. Every must-escalate request reaches a human before any action, and
   the routine read is still handled automatically.
4. Read `../../shared/harness/escalation.py`. Confirm that both runners call the same `drive` engine and
   that only the policy differs, and study how coverage, timing, route, and default each change the
   disposition.
5. Run `python shared/evals/check_lab07.py` to see the properties the policy must satisfy, including the
   no-route policy that identifies the right escalations but drops them.
6. Work `questions.md`, then check `answers.md` and study the branch labels. Finish with the timed set
   in `../../practice/lab07_timed.md` against the clock.
7. Read `DECISION_RECORD.md`, paying attention to the mandatory Governance and escalation section, which
   for this lab is the subject rather than a cross-cut.

Status: built for v0.2.
