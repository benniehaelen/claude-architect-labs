# Exam angle: lab 01

## Domain served

Primary: Agentic Architecture and Orchestration (27%, the largest single domain). Secondary:
Context Management and Reliability (15%).

## How this maps to CCA-F reasoning

Questions in this area rarely ask whether you can log. They ask whether you instrumented the loop
at the point where a decision is made, so that an incident is explainable and a governance handoff
is possible. The hard distinction is between observability that merely records and observability
that feeds a runtime control (a stop condition, an escalation trigger). A Branch B trap here is an
option that logs the right thing at the wrong point in the loop, after the fact rather than at the
decision point, so that the signal arrives too late to govern anything. A Branch A trap is a
fabricated observability flag that claims to expose loop internals with a single config switch.

The transferable judgment: observability is an architectural choice about where to place
instrumentation in the loop, not a logging afterthought, and the value of a signal depends on
whether anything can act on it in time.
