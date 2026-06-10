# Start here: lab 03

## What you will build

You will scope an over-exposed MCP server. The deliverable is a revised boundary: the set of
operations the server exposes, the trust and data boundary it enforces, and the limits it places on
returned context, plus an argument for which limits are governed at runtime versus described in
guidance.

## Dry-run path

Run the lab against a mocked MCP server and recorded fixtures so it costs nothing. The dry-run
presents an internal knowledge assistant and a CI/CD integration, each reaching a server that
exposes or returns more than it should. A live run is optional and clearly marked.

## Suggested path

1. Read `README.md` for the scenario and the run commands.
2. Run the over-exposed server and read its analysis. Notice the operations the agents never need,
   the ungated sensitive operations, the mislabeled raw SQL tool, and that one export floods context.
3. Run the scoped server and compare. Only the needed operations are exposed, the gate escalates the
   unauthorized environment deletion, and the export is bounded under the host output limit.
4. Read `../../shared/harness/mcp.py`. Confirm that both runners call the same `drive` engine and
   that only the server spec differs.
5. Run `python shared/evals/check_lab03.py` to see the properties the boundary must satisfy.
6. Work `questions.md`, then check `answers.md` and study the branch labels. Finish with the timed
   set in `../../practice/lab03_timed.md` against the clock.
7. Read `DECISION_RECORD.md`, paying attention to the mandatory Governance and escalation section,
   and confirm each control against the real features recorded in `../../VERIFIED.md`.

Status: built for v0.1.
