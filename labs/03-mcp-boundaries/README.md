# Lab 03: MCP boundaries

Primary domain: Tool Design and MCP Integration (18%). Secondary: Context Management and
Reliability. Anchor scenarios: internal knowledge assistants, CI/CD integrations.

## Scenario brief

The Model Context Protocol lets an agent reach external systems through a server, but where the
boundary sits and what the server exposes determines the trust, security, and reliability of the
whole system. A server that exposes too much, returns unbounded payloads, or blurs the trust
boundary turns a useful integration into a liability. This lab is about placing the MCP boundary
deliberately.

## Architecture goal

Decide what an MCP server should expose and what it should withhold, where the trust and data
boundary sits, and how to keep returned context bounded and safe. The lab contrasts an
over-exposed server against a scoped one and shows how the boundary is governed at runtime, not
merely described.

## How to run (dry-run, free, deterministic)

No installs and no paid API calls are needed. The boundary logic is deterministic and reads server
specs and a request set from `../../shared/fixtures`. From the repository root:

```
python labs/03-mcp-boundaries/bad_version/run.py
python labs/03-mcp-boundaries/solution/run.py
python shared/evals/check_lab03.py
```

Both runners use the same boundary engine (`../../shared/harness/mcp.py`). Only the server spec
differs. On the over-exposed server, a raw SQL tool and a secrets resource are published, the
sensitive operations are ungated, an unauthorized environment deletion runs silently, and a bulk
export floods the conversation context. On the scoped server, only the needed operations are
exposed, the gate escalates the unauthorized deletion, and the export is bounded under the host
output limit. The lesson is that a runtime control can only govern the surface and the caps the
server places on it.

## Status

Built for v0.1. Includes the over-exposed server, the scoped server, the shared boundary engine
(routing, the trust boundary, payload bounding, and the boundary analyzer), the failure-mode
catalog, the decision record, the question set, and a timed practice set
(`../../practice/lab03_timed.md`).
