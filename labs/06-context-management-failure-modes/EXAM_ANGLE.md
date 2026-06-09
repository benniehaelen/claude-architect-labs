# Exam angle: lab 06

## Domain served

Primary: Context Management and Reliability (15%). Secondary: Agentic Architecture and Orchestration
(27%), since context budgeting is where reliability and orchestration meet.

## How this maps to CCA-F reasoning

This lab sits on one of the three verified primitives: session forking branches conversation
history but not the filesystem (see `../../VERIFIED.md`). Questions here test whether you know that
a forked agent's file edits are real and shared, and whether you reach for file checkpointing
rather than forking alone when a branch must revert file changes. A Branch A trap names a
fabricated flag that claims forking also snapshots or isolates the filesystem. A Branch B trap
offers a real context strategy applied too late or in the wrong place: summarizing after overflow
has already dropped information, or budgeting in the prompt where an orchestration limit is needed.

The transferable judgment: design context handling to fail loudly, and know that forking isolates
the conversation, not the files, so file isolation needs its own control.
