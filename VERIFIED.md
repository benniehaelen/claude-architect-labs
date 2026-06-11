# Verified facts

Every config flag, directive, and primitive used in this repository must be real and dated. This
file is the single source of truth. No lab, question, or document may reference a feature that does
not trace to a dated entry here. A fabricated feature in a public teaching artifact would undercut
the repository's own thesis, so this discipline is not optional.

Verified on 2026-06-08. Re-verify every entry before each tagged release.

## Exam shape and domain weights

The exam is scenario-based multiple choice. It has 60 questions and a 120-minute limit, which is
two minutes per question. The passing score is 720 of 1000. There are five domains with these
weights:

| Domain | Weight |
| --- | --- |
| Agentic Architecture and Orchestration | 27% |
| Claude Code Configuration and Workflows | 20% |
| Prompt Engineering and Structured Output | 20% |
| Tool Design and MCP Integration | 18% |
| Context Management and Reliability | 15% |

Governance, safety, and reliability are not separate domains. They run through all five and are
treated here as a cross-cut, never as a standalone lab.

Six anchor scenarios are drawn from real customer deployments: customer support agents,
multi-agent research systems, CI/CD integrations, structured data extraction pipelines, internal
knowledge assistants, and developer-productivity tools. The capstones mirror these. See
`SCENARIO_INDEX.md`.

## Three real primitives and their sharp edges

These three appear repeatedly as the hinge of hard questions. Each is real, and each has an edge
that a shallow study guide misses.

### 1. Path-scoped rules

`.claude/rules/*.md` files accept YAML frontmatter with a `paths` field of glob patterns. This is
real, introduced around Claude Code v2.0.64.

Edge: a path-scoped rule loads when Claude reads a file matching the pattern, not on every tool
use. There is a known issue that it is not injected when Claude writes or creates a matching file.
A rule meant to enforce a convention at file-creation time may therefore not fire on its own. The
correct response is to pair the rule with a runtime control (a hook or a pre-commit check), which
is exactly what this repository does for its own house style.

Source: https://code.claude.com/docs/en/memory

### 2. Structured outputs and citations are incompatible

Enabling citations together with the structured-output format returns a 400 error. Citations
interleave citation blocks with text, and that conflicts with the strict JSON schema constraints
of structured outputs. Structured outputs use a beta header (`structured-outputs-2025-11-13`) and
constrained decoding.

Edge: when you need both grounding and machine-readable output, you cannot get them in a single
pass. The correct pattern is multi-pass: a cited pass first, then a transform-to-schema pass, then
a verification pass that maps the structured claims back to the cited evidence.

Source: https://docs.claude.com/en/docs/build-with-claude/structured-outputs

### 3. Session forking

In the Agent SDK, `resume="<session_id>", fork_session=True` creates a new session that copies the
parent history and then diverges. The fork gets its own session ID and the original is untouched,
giving two independent branches.

Edge: forking branches the conversation history, not the filesystem. If a forked agent edits
files, those edits are real and visible to any session in the same working directory. To branch
and revert file changes you need file checkpointing, not forking alone.

Source: https://code.claude.com/docs/en/agent-sdk/sessions

## MCP boundaries: capability model and runtime controls

Verified on 2026-06-10. Lab 03 (`labs/03-mcp-boundaries`) depends on these facts. The Model Context Protocol is a
client-server protocol. The host (Claude Code) creates one MCP client per server, and a server is a
program that provides context to that client. A server exposes three core primitives: tools
(executable functions the model can invoke to take actions), resources (data sources that provide
contextual information), and prompts (reusable interaction templates). The boundary is therefore a
trust and reliability decision: what the server exposes is what the agent can reach.

Source: https://modelcontextprotocol.io/docs/concepts/architecture

The two boundary controls the lab leans on are real and host-side in Claude Code.

Scope restriction at the authorization layer. Setting `oauth.scopes` (a single space-separated
string) pins the scopes Claude Code requests during the OAuth flow. The documentation calls this
"the supported way to restrict an MCP server to a security-team-approved subset when the upstream
authorization server advertises more scopes than you want to grant." It takes precedence over the
scopes discovered at the well-known endpoints, and a later 403 `insufficient_scope` causes a
re-authentication with the same pin. Separately, Claude Code prompts for approval before using a
project-scoped server from `.mcp.json`; pending servers show as "Pending approval" and rejected ones
as "Rejected," and choices reset with `claude mcp reset-project-choices`.

Output bounding to protect context. MCP tool results are returned into the host conversation
context, so an unbounded payload consumes context. Claude Code warns when any MCP tool output
exceeds 10,000 tokens and enforces a default maximum of 25,000 tokens, adjustable with the
`MAX_MCP_OUTPUT_TOKENS` environment variable.

Edge: the host default is not the whole story, because the server can raise its own ceiling. The
`MAX_MCP_OUTPUT_TOKENS` limit applies only to tools that do not declare their own limit. A server
author can annotate a tool with `_meta["anthropic/maxResultSizeChars"]` in its `tools/list` entry,
which Claude Code honors up to a hard ceiling of 500,000 characters, and that value governs the
tool's text content regardless of `MAX_MCP_OUTPUT_TOKENS`. Without the annotation, an oversized
result is persisted to disk and replaced with a file reference. So bounding what crosses the
boundary is a shared responsibility: the host caps by default, but the exposed surface and the
per-tool size annotations set on the server decide what can actually flood context. Neither a client
prompt nor a tool description governs either control.

Source: https://code.claude.com/docs/en/mcp

## Agent permissions and sandboxing

Verified on 2026-06-11. Lab 08 (`labs/08-agent-permissions-sandboxing`) depends on these facts.
Claude Code controls what an agent may do with two complementary layers, and knowing which layer
covers which threat is the heart of the lab.

Permission rules. The `permissions` object in a settings file has `allow`, `ask`, and `deny` arrays.
Rules are evaluated in order: deny, then ask, then allow, and the first match wins, so a deny at any
settings scope cannot be overridden by an allow at another. A rule is `Tool` or `Tool(specifier)`,
for example `Bash(npm run test:*)`, `Read(./.env)`, `Edit(/src/**)`, `WebFetch(domain:example.com)`,
`mcp__server__tool`, or `Agent(Explore)`. Permission rules are enforced by Claude Code, not by the
model: a `CLAUDE.md` instruction shapes what Claude tries but does not change what is allowed.

Permission modes, set with `defaultMode`: `default`, `acceptEdits`, `plan`, `auto` (a research
preview), `dontAsk`, and `bypassPermissions`. The `bypassPermissions` mode skips prompts except those
forced by an explicit `ask` rule, with `rm -rf /` and `rm -rf ~` still prompting as a circuit breaker.
The `--dangerously-skip-permissions` CLI flag likewise skips the whether-each-tool-runs checks and is
blocked when running as root. An administrator can set `permissions.disableBypassPermissionsMode` to
`"disable"` to prevent bypass mode.

Sandbox. The sandboxed Bash tool provides OS-level filesystem and network isolation (Seatbelt on
macOS, bubblewrap on Linux and WSL2). Enabled with `sandbox.enabled`, it confines writes to the
working directory and the session temp directory by default and routes network through an allowlist
(`allowedDomains`, `deniedDomains`), with `sandbox.filesystem.allowWrite`, `denyWrite`, `denyRead`,
and `allowRead` to adjust the boundary. The isolation is enforced by the operating system on the
running process, so it holds "regardless of what the model chose to run and even if an allowed
command does more than its name suggests."

Edge: the two layers cover different threats, and the gap between them is the lab's hinge. Read and
Edit permission deny rules apply to Claude's own file tools and to file commands Claude Code
recognizes in Bash, but the documentation states plainly that they "do not apply to arbitrary
subprocesses that read or write files indirectly, like a Python or Node script that opens files
itself." So a tight `Read(~/.ssh/**)` deny rule does not stop a credential read performed inside an
allowed build subprocess. Only the OS-level sandbox contains that, because it binds the process, not
the model's tool choice. Permission scoping and the sandbox are therefore complementary, and scoping
alone is not subprocess containment.

Sources: https://code.claude.com/docs/en/permissions and https://code.claude.com/docs/en/sandboxing

## Re-verification checklist

Run this before each tagged release and update the verification date above.

1. Confirm the domain weights and exam shape against the current official exam guide.
2. Confirm path-scoped rules still load on Read and the write-time injection issue. Note the
   minimum Claude Code version that introduced the feature and any version where the bug is fixed.
3. Confirm the citations-plus-structured-output 400 error and the current beta header value.
4. Confirm the `fork_session` semantics and the filesystem-is-not-forked edge.
5. Confirm the MCP primitives (tools, resources, prompts), the `MAX_MCP_OUTPUT_TOKENS` default of
   25,000 and the 10,000-token warning, the `anthropic/maxResultSizeChars` 500,000-character
   ceiling, and the `oauth.scopes` restriction behavior.
6. Confirm the permission rule precedence (deny, ask, allow), the permission modes including
   `bypassPermissions` and `--dangerously-skip-permissions`, the `sandbox.enabled` OS-level Bash
   isolation, and the edge that Read and Edit deny rules do not cover arbitrary subprocesses.
7. Update every dated reference in the labs and question sets that depends on these facts.
