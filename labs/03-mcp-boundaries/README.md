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

Status: scaffolded for v0.1. The flawed version, reference solution, failure-mode catalog, and
question set are added when this lab is built out.
