# Exam angle: lab 02

## Domain served

Primary: Tool Design and MCP Integration (18%). Secondary: Agentic Architecture and Orchestration
(27%).

## How this maps to CCA-F reasoning

Questions here test whether you understand that a tool description is a guide and a permission is a
control. A Branch B trap offers a catalog that prevents misuse by writing a strong warning into the
tool description, where the safe answer enforces the limit with a permission or a gating hook. Another
Branch B trap splits or merges tools at the wrong granularity, producing more calls or more ambiguity
than the constraint allows. A Branch A trap names a fabricated catalog-level switch that claims to
auto-resolve overlapping tools.

The transferable judgment: design the catalog so the right tool is the obvious one, place the safety
limit in the layer that governs rather than the layer that suggests, and pick granularity by the cost
and ambiguity it creates in the loop.
