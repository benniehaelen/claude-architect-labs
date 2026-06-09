# Start here: lab 01

## What you will build

You will take a black-box agent loop and make it observable. The deliverable is an instrumented
loop that emits structured events at each decision point (tool selection, tool result, retry, and
stop), plus a short written argument for which signals must be governed at runtime versus only
logged.

## Dry-run path

Run the lab against mocked tools and recorded fixtures so it costs nothing. The dry-run replays a
realistic support-agent session and a small multi-agent research session, both of which include a
failure you must be able to explain from your instrumentation alone. A live run against real models
is optional and clearly marked.

## Suggested path

1. Read `README.md` for the scenario and the run commands.
2. Run the black-box loop on `support_session_failure` and notice what you cannot learn from its
   output, then read `bad_version/run.py` and find the three defects called out in its docstring.
3. Run the reference loop on the same session and read the trace. Trace the circuit breaker trip
   and the escalation in `../../shared/harness/agentloop.py`.
4. Run `python shared/evals/check_lab01.py` to see the properties the design must satisfy.
5. Work `questions.md`, then check `answers.md` and study the branch labels. Finish with the timed
   set in `../../practice/lab01_timed.md` against the clock.
6. Read `DECISION_RECORD.md`, paying attention to the mandatory Governance and escalation section.

Status: built for v0.1.
