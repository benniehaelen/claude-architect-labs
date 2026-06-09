# Lab 02: tool catalog design

Primary domain: Tool Design and MCP Integration (18%). Secondary: Agentic Architecture and
Orchestration. Anchor scenarios: customer support agents, developer-productivity tools.

## Scenario brief

An agent is only as good as the tools it is given. A poorly designed catalog (tools that overlap,
tools that are too coarse or too fine, descriptions that mislead the model about when to use them)
produces wrong tool choices, wasted calls, and unsafe actions. This lab is about designing the set
of tools exposed to an agent: their granularity, naming, descriptions, and the boundaries between
them.

## Architecture goal

Design a tool catalog that makes the right tool the obvious choice and the unsafe action hard to
reach by accident. The lab contrasts a sprawling, overlapping catalog against a deliberate one and
shows how tool descriptions guide selection while permissions and gating govern what a tool may
actually do.

Status: scaffolded for v0.1. The flawed version, reference solution, failure-mode catalog, and
question set are added when this lab is built out.
