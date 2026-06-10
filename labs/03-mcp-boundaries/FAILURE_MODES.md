# Failure modes: lab 03 MCP boundaries

Each failure mode names what goes wrong, how it is detected, and what the reference design does
about it. Run `bad_version/run.py` and `solution/run.py` to see several directly, and
`shared/evals/check_lab03.py` for the assertions.

## Over-exposure of operations the agents never need

The server publishes more than the agents require, so the surface is wider than it has to be and a
capability that should never be reachable is one selection away. In the over-exposed server a raw
SQL tool and a secrets-listing resource are published even though neither anchor agent needs them.
Detection is the `over_exposed` report, which flags any exposed operation whose capability is not in
the needed set. The scoped server exposes only the four needed capabilities, which models scoping a
server with `oauth.scopes` and the project-approval step in Claude Code (see `../../VERIFIED.md`).

## Ungated sensitive operations

A write or destructive operation has no gate in front of it, so the boundary has nothing to govern
and the action runs unconditionally. This is the central defect, and it is the same shape as an
ungated tool in lab 02. In the over-exposed server both the deploy and the environment deletion are
ungated, so an unauthorized deletion runs silently. Detection is the `ungated_sensitive` report. The
reference gates every write and destructive operation, which is what gives the boundary something to
act on.

## Mislabeled effect level

An operation declares a lower effect than the capability it actually carries, which hides risk from
the gate. The over-exposed server publishes a raw SQL tool labeled as a read, even though arbitrary
SQL can drop tables and is destructive. A gate that trusts the label would let it pass as a harmless
read. Detection is the `mislabeled` report, which compares the declared effect against the effect
the capability carries in `ops_meta`. The reference labels each operation at its true effect level.

## Unbounded payload that floods context

An operation returns more than the host output limit, so a single call fills the conversation
context and can silently push out earlier information. The over-exposed server raises its bulk export
ceiling to 200,000 tokens, past the host limit of 25,000, so a 120,000-token export returns in full
and floods context. Detection is the `unbounded` report, which flags any exposed operation whose
effective cap exceeds the host limit, and the per-request `flooded` flag. This is the
`anthropic/maxResultSizeChars` edge: the host default protects only tools that do not raise their own
ceiling. The reference keeps every operation's cap under the host limit, so the same export is
truncated to 20,000 tokens instead of flooding.

## Enforcing the boundary in the client instead of at the server

A subtler mode, and the Branch B trap the exam angle calls out: filtering the surface or trimming the
payload in the client prompt and treating that as the boundary. The prompt is a guide and cannot stop
a published operation from being called or a server from returning an oversized result. The reference
enforces the surface, the gate, and the output caps at the server and the host, the control layers,
and uses descriptions only to steer selection. See `../../ENFORCEMENT_LAYER.md`.
