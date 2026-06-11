# Exam angle: lab 08

## Domain served

Primary: Claude Code Configuration and Workflows (20%). Secondary: Tool Design and MCP Integration
(18%). The CI/CD anchor scenario sits here: an agent that runs without a human to approve each action.

## How this maps to CCA-F reasoning

This lab builds on the verified permission and sandboxing facts (see `../../VERIFIED.md`). Questions
here test whether you can configure an unattended agent with the right layers and whether you know which
layer covers which threat. A sound answer scopes permission rules to least privilege, enables the
OS-level sandbox, and isolates file state in a worktree.

A Branch A trap names a fabricated setting that claims to sandbox or auto-scope an agent with a single
switch, as if one flag replaced the layered design. A Branch B trap offers a real but weaker
configuration: tight permission rules with no sandbox, which still leaks because a Read deny rule cannot
reach inside a subprocess, or bypassing permissions in a non-isolated environment for speed. Each is
correct in mechanism but fails the containment the scenario binds on.

The transferable judgment: permission rules scope which tool calls the agent makes, the OS-level
sandbox contains what a subprocess does regardless of the model's choice, and worktree isolation makes
file edits revertible. Scoping permissions is necessary but is not subprocess containment.
