# Scenario index

Six anchor scenarios are drawn from real customer deployments. They are the recurring settings for
the hard questions, and the capstones (planned for v1.0) mirror them directly. This index names the
six and maps each to the labs that exercise it.

## The six anchor scenarios

1. Customer support agents. An agent fields user requests, calls tools to look up account state,
   and must know when to escalate to a human. The hard parts are the escalation boundary, the cost
   of unnecessary tool calls, and safe behavior on ambiguous or out-of-policy requests.

2. Multi-agent research systems. A lead agent decomposes a question, spawns subagents, and
   synthesizes their findings. The hard parts are orchestration, context budgeting across agents,
   session branching, and reconciling conflicting subagent output.

3. CI/CD integrations. Claude runs inside a pipeline, reviewing changes or generating artifacts
   under automation. The hard parts are non-interactive operation, permission scoping, deterministic
   behavior, and failing the build safely rather than silently.

4. Structured data extraction pipelines. The system turns unstructured input into machine-readable
   records, often with a grounding requirement. The hard parts are schema reliability, the
   citations-versus-structured-output incompatibility, and verification of extracted claims.

5. Internal knowledge assistants. An assistant answers questions over a private corpus through
   retrieval and tools. The hard parts are context management, retrieval boundaries, data
   sensitivity, and preventing confident answers that are not grounded.

6. Developer-productivity tools. Claude Code is configured for a team: shared settings, rules,
   subagents, and workflows. The hard parts are configuration layering, the rule-versus-runtime
   enforcement gap, and team-wide governance.

## Scenario to lab mapping

Labs 01 through 06 are v0.1; labs 07 (human escalation patterns) and 08 (agent permissions and
sandboxing) are the first v0.2 additions.

| Scenario | Labs that exercise it |
| --- | --- |
| Customer support agents | 01 agent-loop-observability, 02 tool-catalog-design, 07 human-escalation-patterns |
| Multi-agent research systems | 01 agent-loop-observability, 06 context-management-failure-modes |
| CI/CD integrations | 03 mcp-boundaries, 04 claude-code-team-workflow, 08 agent-permissions-sandboxing |
| Structured data extraction pipelines | 05 structured-output-reliability |
| Internal knowledge assistants | 03 mcp-boundaries, 06 context-management-failure-modes |
| Developer-productivity tools | 02 tool-catalog-design, 04 claude-code-team-workflow |

## The capstones (v1.0)

Each v1.0 capstone takes one anchor scenario end to end, combining the relevant labs into a single
design problem with a full decision record and a timed question set. They live in `capstones/`.

Three capstones are built. The customer support agent (`capstones/customer-support-agent`) composes
lab 01 (observable loop), lab 02 (tool catalog and gate), and lab 07 (escalation policy) into one
support-request handler. The multi-agent research system (`capstones/multi-agent-research`) composes
lab 01 (orchestration) and lab 06 (context management), exercising session forking and its filesystem
edge (see `VERIFIED.md`). The developer-productivity environment (`capstones/developer-productivity`)
composes lab 02 (a catalog of dev tools and the gate) and lab 04 (team configuration enforcement),
gating the deploy tool while governing the team conventions on every event, including file creation.

The remaining capstones, for CI/CD integrations, structured data extraction, and internal knowledge
assistants, are planned. Each capstone reuses the lab engines directly rather than reimplementing them,
and shows how a failure in any one composed layer becomes a system failure.
