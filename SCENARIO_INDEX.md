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

## Scenario to lab mapping (v0.1)

| Scenario | Labs that exercise it |
| --- | --- |
| Customer support agents | 01 agent-loop-observability, 02 tool-catalog-design |
| Multi-agent research systems | 01 agent-loop-observability, 06 context-management-failure-modes |
| CI/CD integrations | 03 mcp-boundaries, 04 claude-code-team-workflow |
| Structured data extraction pipelines | 05 structured-output-reliability |
| Internal knowledge assistants | 03 mcp-boundaries, 06 context-management-failure-modes |
| Developer-productivity tools | 02 tool-catalog-design, 04 claude-code-team-workflow |

## How the capstones will use this index (v1.0)

Each v1.0 capstone takes one anchor scenario end to end, combining the relevant labs into a single
design problem with a full decision record and a timed question set. The capstone for multi-agent
research, for example, draws on the orchestration work in lab 01 and the context-budgeting work in
lab 06, and it exercises session forking and its filesystem edge (see `VERIFIED.md`). The capstones
are out of scope for v0.1 and are listed here so the lab work points toward them.
