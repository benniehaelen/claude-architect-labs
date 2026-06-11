# Exam angle: lab 07

## Domain served

Primary: Agentic Architecture and Orchestration (27%). Secondary: Context Management and Reliability
(15%). Escalation is where orchestration and reliability meet: the policy decides where automation
stops and how the system fails safely.

## How this maps to CCA-F reasoning

Governance and escalation are a cross-cut that the exam weights heavily in practice, and they are the
mandatory section of every decision record in this repository. This lab makes the escalation decision
the subject. Questions here test whether you can design an escalation policy with four properties:
coverage of every must-escalate case, escalation before an irreversible action rather than after, a
defined route to a human, and a fail-safe default that holds rather than proceeds.

A Branch A trap names a fabricated setting that claims to auto-escalate or auto-confirm the right
requests, as if a flag could replace the policy. A Branch B trap offers a real but weaker design:
escalating after the action instead of before, covering only some of the must-escalate cases, or
identifying the right escalations but routing them nowhere with a default that proceeds. Each is correct
in mechanism but fails the timing, coverage, or delivery the scenario binds on.

The transferable judgment: an escalation policy must reach a human before the irreversible action, cover
every must-escalate case at runtime rather than by prompt, and fail safe when the handoff cannot be
delivered.
