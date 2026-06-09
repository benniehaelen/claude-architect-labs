# Exam domain map

The exam has five domains. Their weights are fixed facts, dated and sourced in `VERIFIED.md`. This
document maps each domain to the labs that exercise it and explains how the build effort is
weighted to match the percentages.

## The five domains and their weights

| Domain | Weight |
| --- | --- |
| Agentic Architecture and Orchestration | 27% |
| Claude Code Configuration and Workflows | 20% |
| Prompt Engineering and Structured Output | 20% |
| Tool Design and MCP Integration | 18% |
| Context Management and Reliability | 15% |

Governance, safety, and reliability do not appear as a sixth row. They are a cross-cut that runs
through all five domains, and they are weighted heavily in practice because nearly every scenario
turns on where automation stops and how the system fails safely. They are enforced here through the
mandatory Governance and escalation section of every `DECISION_RECORD.md`, not through a separate
governance lab.

## Lab to domain mapping (v0.1)

Each lab serves a primary domain and usually touches one or two secondary domains. The cross-cut
applies to all of them.

| Lab | Primary domain | Secondary domains |
| --- | --- | --- |
| 01 agent-loop-observability | Agentic Architecture and Orchestration | Context Management and Reliability |
| 02 tool-catalog-design | Tool Design and MCP Integration | Agentic Architecture and Orchestration |
| 03 mcp-boundaries | Tool Design and MCP Integration | Context Management and Reliability |
| 04 claude-code-team-workflow | Claude Code Configuration and Workflows | Agentic Architecture and Orchestration |
| 05 structured-output-reliability | Prompt Engineering and Structured Output | Context Management and Reliability |
| 06 context-management-failure-modes | Context Management and Reliability | Agentic Architecture and Orchestration |

## How effort is weighted

The build deliberately mirrors the domain percentages rather than spreading effort evenly.

Agentic architecture and orchestration is the largest single domain at 27%, so roughly a quarter
of all labs and questions serve it. In v0.1 that is lab 01 as a primary, with labs 02, 04, and 06
reinforcing orchestration as a secondary concern. As v0.2 and v1.0 add labs (human escalation
patterns, agent permissions and sandboxing, and the multi-agent research capstone), the agentic
share grows toward its target.

The Claude Code and prompt-engineering pair together carry about 40% (20% plus 20%). Labs 04 and 05
are the v0.1 anchors for that pair, and the timed practice sets weight toward them accordingly.

Tool design and MCP integration at 18% is served by labs 02 and 03. Context management and
reliability at 15% is served by lab 06 as a primary and by labs 01, 03, and 05 as a secondary, which
reflects how reliability concerns surface inside other domains rather than in isolation.

## Reading this map for the exam

Two practical implications follow from the weights.

First, do not over-index on prompt engineering. It is one domain of five, and the orchestration,
reliability, context, and Claude Code domains carry the majority of the weight combined. A
candidate who is strong only at prompting will fail the larger share of the exam.

Second, treat governance as present in every question even when the prompt does not name it. A
scenario that looks like a pure tool-design problem will often hinge on where the human handoff
sits or how the system fails safely. The labs train this by making the governance section
mandatory regardless of the lab's primary domain.
