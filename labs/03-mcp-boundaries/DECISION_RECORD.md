# Decision record: lab 03 MCP boundaries

## Scenario

Two agents reach external systems through an MCP server: an internal knowledge assistant that reads
a private corpus, and a CI/CD integration that triggers deployments and manages environments. The
server in `bad_version` is over-exposed. It publishes a raw SQL tool and a secrets-listing resource
the agents never need, leaves the deploy and the environment-deletion operations ungated, labels the
raw SQL tool as a read when arbitrary SQL is destructive, and lets its bulk export raise its own
output ceiling past the host limit. The result is that an unauthorized environment deletion runs
with no checks and a single export floods the conversation context.

## Constraints

The binding constraint is trust and reliability at a single design surface: the server boundary.
Cost and latency matter, but the boundary's first job is to expose only what the agents need, gate
the high-impact actions, and keep what crosses the boundary bounded.

- Latency: a wider surface and larger payloads slow selection and fill context, not raw speed.
- Cost: an unbounded payload consumes context tokens that the rest of the task then cannot use.
- Reliability: a result that floods context can silently drop earlier information, so bounding is a
  reliability control, not only a security one.
- Security: high-impact actions must pass a control before they execute, and the server must not
  expose capabilities the agents do not need.
- Data sensitivity: a secrets-listing resource and an arbitrary-SQL tool should not be reachable at
  all unless they are genuinely required.
- Human review: an unauthorized high-impact action must reach a human rather than run.
- Operational owner: the team that owns the integration owns the server spec, its exposed surface,
  and its output caps.

## Design chosen

A scoped server (in `mcp_server_good.json`) paired with a trust boundary (in `shared/harness/mcp.py`).
Three rules define it, and each maps to a real Claude Code or MCP control recorded in `VERIFIED.md`.

First, expose only the needed capabilities. The server publishes exactly the four operations the two
agents require and nothing else. This is the surface decision. In Claude Code it corresponds to
scoping a server with `oauth.scopes` to a security-team-approved subset and to the project-approval
step that gates a `.mcp.json` server before its tools are usable.

Second, gate every write and destructive operation. The boundary is the control layer. It governs
whether a selected operation may actually execute, independent of what the description suggested. A
read passes, an authorized and confirmed deploy runs, and an unauthorized environment deletion is
escalated rather than executed.

Third, bound what crosses the boundary. Each operation declares an output cap at or under the host
limit, so no single result can flood context. This models the real Claude Code behavior: MCP output
is capped at a default of 25,000 tokens (`MAX_MCP_OUTPUT_TOKENS`) with a warning past 10,000, but a
server can raise its own per-tool ceiling with `anthropic/maxResultSizeChars` up to 500,000
characters. The scoped server keeps its caps under the host limit instead of raising them.

The decisive insight, visible in the runners, is that the over-exposed server and the scoped server
use the exact same boundary engine. Only the server spec differs. A runtime control can only govern
what the server exposes and how the server bounds it, so boundary placement is what makes the
control effective.

## Alternatives rejected and why

Keeping the broad surface but telling the agent in its prompt not to call the raw SQL tool or the
secrets resource. The prompt is a guide. It cannot stop a published tool from being called, and it
does nothing about the unbounded payload. Wrong layer for a must-hold trust requirement, and it
leaves the surface as wide as before.

Relying on the host default output cap alone and letting every operation raise its own ceiling. The
host default protects only tools that do not declare their own limit. An operation that sets a large
`anthropic/maxResultSizeChars` bypasses the default for its text content, so trusting the host cap
while the server raises ceilings is precisely how the bulk export floods context. The fix is to keep
the server caps under the host limit, not to assume the host limit always binds.

Enforcing the boundary in the client rather than at the server. A client-side filter is correct in
mechanism but applied after the surface is already published and the payload is already returned. The
boundary belongs at the server, where the surface is defined and the output is produced, not at the
consumer of it.

## Failure modes

Summarized here and detailed in `FAILURE_MODES.md`: over-exposure of operations the agents never
need, ungated sensitive operations that bypass the control entirely, a mislabeled effect level that
hides risk from the gate, an unbounded payload that floods context, and enforcing the boundary in
the client prompt instead of at the server.

## Controls

- Enforced by prompt: the operation descriptions, which guide selection. Helpful, not load-bearing
  for trust or for bounding.
- Enforced by runtime: the scoped surface (`oauth.scopes`, project approval), the gate on write and
  destructive operations, and the per-operation output caps under the host limit
  (`MAX_MCP_OUTPUT_TOKENS` and the `anthropic/maxResultSizeChars` ceiling). See `VERIFIED.md`.
- Observable: the boundary analysis (over-exposed, ungated, unbounded, mislabeled), and the
  per-request route status, gate decision and reason, returned payload size, and whether it flooded.
- Auditable: each request records the selected operation, its effect, the gate decision, the
  returned token count, and whether it executed.

## Governance and escalation (mandatory)

- Where automation stops: the boundary stops automatically before any write or destructive operation
  runs unless the request is authorized and confirmed, and it caps every returned payload at the
  host limit. Read actions within the bound proceed.
- Human-handoff path: an unauthorized high-impact action returns an `escalate` decision with reason
  `unauthorized_high_impact_action`, which routes the request to a human rather than executing it.
- Fail-safe behavior (fails safely rather than silently): the scoped server escalates the
  unauthorized environment deletion and truncates the oversized export, while the over-exposed server
  runs the deletion with no gate and lets the export flood context. The contrast, same request set
  and same engine, opposite outcome, is the lesson: governance lives in the exposed surface, the
  gate, and the output caps, not in the operation descriptions.

## Exam angle

See `EXAM_ANGLE.md`. This lab serves the Tool Design and MCP Integration domain (18%) with Context
Management and Reliability (15%) as secondary. The transferable judgment is that the MCP boundary is
a trust and reliability decision enforced at the server, that high-impact operations must be gated
rather than described, and that what crosses the boundary must be bounded so it cannot silently flood
or leak context.
