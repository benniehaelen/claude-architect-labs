# Decision record: developer-productivity tools capstone

## Scenario

A development team configures Claude Code for everyday work. It exposes a catalog of developer tools
and enforces team conventions on the artifacts those tools produce. A session mixes both dimensions:
running tests, editing a source file, creating a new doc, deploying to production, and committing. The
naive environment in `bad_version` composes the two labs' failure modes: the sprawling, ungated catalog
lets an unauthorized deploy run, and the rules-and-memory config misses the new file at creation and the
commit, so a created doc violates the house style and a secret could be committed.

## Constraints

The binding constraint is that both dimensions hold at once: the high-impact tool is gated, and the
must-hold conventions are governed on every event, including file creation, where a path-scoped rule
alone does not fire. The routine tools must still run without friction.

- Latency: gating the deploy and governing conventions with a hook adds little, and it replaces the
  human review a fast team does not pause for.
- Cost: an ambiguous catalog causes wrong tool calls, and an over-gated catalog slows routine work, so
  granularity must be precise.
- Reliability: the conventions must hold on every binding event, not only when a rule happens to load.
- Security: the deploy must be gated, and a secret must be blocked at the commit.
- Data sensitivity: a created doc that violates the house style or a committed secret is the concrete
  harm.
- Human review: an unauthorized deploy must reach a human, and a blocked commit or failing check returns
  to the author.
- Operational owner: the team owns the catalog, the gate, the rules, the hooks, and the CI gates, and
  keeps them in version control so every member inherits them.

## Design chosen

The composed environment (in `dev_design_good.json`) wires both labs together, reusing their engines.

Deliberate catalog with a gate (lab 02). Each dev intent maps to one tool, each tool has a single effect
level, and every write or destructive tool is gated. The routine read tools run, the gated writes run
when confirmed, and the destructive deploy is escalated when unauthorized.

Layered configuration (lab 04). The conventions keep the path-scoped rule as a guide and add a hook that
governs both create and edit, with a pre-commit check and a CI gate governing the commit. The new doc is
held to the house style at creation, which closes the verified write-time gap, and the commit is governed
against the secrets rule.

The decisive insight, visible in the runners, is that the naive environment and the composed environment
use the exact same engine. Only the catalog and the config differ. A dev action is contained, or not,
because of the catalog, the gate, and the configuration layer, not because the agent was told to be
careful.

## Alternatives rejected and why

A strong configuration but the sprawling, ungated catalog. The conventions would be governed, but the
ungated deploy still runs without authorization, so the environment is unsafe on the tool dimension. The
catalog must be deliberate and the high-impact tools gated.

A deliberate catalog but the rules-and-memory configuration. The deploy would be gated, but a newly
created doc still violates the house style because the rule does not load on creation, and a secret could
be committed because the rule is a guide, not a control. The configuration must be layered.

Enforcing every convention and gating every tool with the heaviest control. This holds the must-holds but
slows routine work and over-gates benign reads, optimizing uniformity over the precise granularity the
constraint asks for.

## Failure modes

Summarized here and detailed across the source labs' `FAILURE_MODES.md`: an ungated destructive tool, an
ambiguous catalog, a must-hold convention enforced by a guide that does not fire on creation, and a
secrets convention that memory cannot govern at the commit. The capstone shows these compounding: the
naive environment deploys without authorization and lets a created file and a commit slip past the
conventions.

## Controls

- Enforced by prompt: tool descriptions and `CLAUDE.md` guidance, which steer behavior. Helpful, not
  load-bearing.
- Enforced by runtime: the permission gate on write and destructive tools, and the hook, pre-commit
  check, and CI gate that govern the conventions. See `../../ENFORCEMENT_LAYER.md`.
- Observable: the per-action tool, gate decision, and convention outcome, plus the harm flag.
- Auditable: each action records its tool, gate decision, and whether its convention was governed.

## Governance and escalation (mandatory)

- Where automation stops: the gate stops a write or destructive tool unless it is authorized and
  confirmed, and the configuration controls stop a convention violation on create, edit, or commit.
- Human-handoff path: an unauthorized deploy is escalated to a human, and a blocked commit or failing
  check returns to the author to fix.
- Fail-safe behavior (fails safely rather than silently): the composed environment escalates the
  unauthorized deploy and governs every convention on its event, while the naive environment runs the
  deploy ungated and lets a created file and a commit slip through. The contrast, same session and same
  engine, opposite outcome, is the capstone lesson: a safe developer environment composes a gated
  catalog with a layered configuration, and a failure in either dimension compounds into a system
  failure.

## Exam angle

This capstone integrates the reasoning from labs 02 and 04. It serves Claude Code Configuration and
Workflows (20%) and Tool Design and MCP Integration (18%). The transferable judgment is that a
team-configured agent is safe only when the tool catalog gates the high-impact actions and the
configuration governs the conventions on every event, including file creation.
