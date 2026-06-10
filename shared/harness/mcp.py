"""MCP boundary primitives for lab 03.

An MCP server exposes a surface to an agent: a set of operations the agent can reach across the
boundary. Its design decides three things the lab teaches, each enforced at the server or host and
none of them by a client prompt:

- Exposure. What the server publishes is what the agent can reach. A server that exposes operations
  the agent never needs widens the attack and error surface for no benefit. The scoped server
  exposes only the needed capabilities, which models the real `oauth.scopes` restriction and the
  project-approval step in Claude Code (see VERIFIED.md).
- Gating. A write or destructive operation must pass a runtime control before it executes. An
  ungated sensitive operation runs unchecked, which is the same failure lab 02 shows for an ungated
  tool. The gate is the control layer; the operation's description is only a guide.
- Bounded context. An MCP tool result is returned into the host conversation context, so an
  unbounded payload floods context. Claude Code caps MCP output at a default of 25,000 tokens
  (`MAX_MCP_OUTPUT_TOKENS`) and warns past 10,000, but a server can raise its own per-tool ceiling
  with `anthropic/maxResultSizeChars` up to 500,000 characters. So the server's declared limits, not
  just the host default, decide what actually crosses the boundary (see VERIFIED.md).

The decisive insight, visible in the runners, is that the bad server and the scoped server pass
through the exact same boundary engine. Only the server spec differs. A runtime control can only
govern what the server exposes and how the server bounds it, so boundary placement is what makes the
control effective.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

EFFECTS = ("read", "write", "destructive")
EFFECT_RANK = {"read": 0, "write": 1, "destructive": 2}


@dataclass
class Operation:
    name: str
    description: str
    kind: str  # "tool" or "resource"
    capability: str  # the need this operation serves
    effect: str  # one of EFFECTS
    exposed: bool = True
    gated: bool = False
    declared_result_limit: int = 0  # server-set per-tool output cap in tokens; 0 means use host default


@dataclass
class ServerSpec:
    name: str
    operations: List[Operation]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ServerSpec":
        operations = [Operation(**spec) for spec in data["operations"]]
        return cls(name=data["name"], operations=operations)

    def exposed_operations(self) -> List[Operation]:
        return [op for op in self.operations if op.exposed]

    def operations_for_capability(self, capability: str) -> List[Operation]:
        return [op for op in self.exposed_operations() if op.capability == capability]


@dataclass
class Request:
    id: str
    capability: str
    description: str
    authorized: bool = False
    confirmed: bool = False
    result_tokens: int = 0  # size the operation would return for this request


@dataclass
class BoundaryDecision:
    decision: str  # "allow", "block", or "escalate"
    reason: str
    operation: Optional[str] = None


class TrustBoundary:
    """Runtime control at the server boundary.

    Read operations pass freely. Write and destructive operations must be gated by the server and
    must carry authorization and confirmation. If a sensitive operation is not gated, there is no
    control in front of it and it simply runs, which is the failure the over-exposed server
    demonstrates. Payload bounding is a separate concern handled by `bound_payload`, because a result
    can flood context even when the operation that produced it was allowed.
    """

    def __init__(self, output_token_limit: int) -> None:
        self.output_token_limit = output_token_limit

    def authorize(self, op: Operation, request: Request) -> BoundaryDecision:
        if op.effect == "read":
            return BoundaryDecision("allow", "read_only", op.name)

        if not op.gated:
            # No gate was wired to this sensitive operation, so nothing governs it.
            return BoundaryDecision("allow", "ungated_sensitive_executed", op.name)

        if not request.authorized:
            return BoundaryDecision("escalate", "unauthorized_high_impact_action", op.name)

        if not request.confirmed:
            return BoundaryDecision("block", "confirmation_required", op.name)

        return BoundaryDecision("allow", "authorized_and_confirmed", op.name)

    def bound_payload(self, op: Operation, request: Request) -> Dict[str, Any]:
        """Bound the result an operation returns.

        The effective cap is the operation's declared limit when it sets one, otherwise the host
        default. A result is truncated when the request would return more than the effective cap, and
        it floods context when what actually returns still exceeds the host output limit. A server
        that raises its own ceiling past the host limit can therefore flood context even though the
        host has a default cap, which is the sharp edge VERIFIED.md records.
        """
        cap = op.declared_result_limit if op.declared_result_limit > 0 else self.output_token_limit
        returned = min(request.result_tokens, cap)
        truncated = request.result_tokens > cap
        flooded = returned > self.output_token_limit
        return {"returned": returned, "truncated": truncated, "flooded": flooded}


@dataclass
class RouteResult:
    request_id: str
    capability: str
    matches: List[str]
    status: str  # "ok", "ambiguous", or "unreachable"
    selected: Optional[Operation] = None


def route(server: ServerSpec, request: Request) -> RouteResult:
    """Select an exposed operation for a request by capability.

    Zero exposed matches is unreachable: the capability does not cross the boundary, so the agent
    cannot use it. More than one match is ambiguous. When matches exist, the first is selected.
    """
    matches = server.operations_for_capability(request.capability)
    names = [op.name for op in matches]
    if not matches:
        return RouteResult(request.id, request.capability, names, "unreachable", None)
    status = "ok" if len(matches) == 1 else "ambiguous"
    return RouteResult(request.id, request.capability, names, status, matches[0])


@dataclass
class RequestOutcome:
    request: Request
    route: RouteResult
    boundary: Optional[BoundaryDecision]
    returned_tokens: int
    truncated: bool
    flooded: bool
    executed: bool
    effect: Optional[str]


def drive(server: ServerSpec, requests: List[Request], output_token_limit: int) -> List[RequestOutcome]:
    """Route, gate, and bound every request against one server.

    This is the shared engine. The over-exposed server and the scoped server call it with identical
    code and differ only in which server spec they pass, which makes the point that the boundary
    controls are only as good as the server they are placed on.
    """
    boundary = TrustBoundary(output_token_limit)
    outcomes: List[RequestOutcome] = []
    for request in requests:
        result = route(server, request)
        if result.selected is None:
            outcomes.append(
                RequestOutcome(request, result, None, 0, False, False, False, None)
            )
            continue
        op = result.selected
        decision = boundary.authorize(op, request)
        payload = boundary.bound_payload(op, request)
        executed = decision.decision == "allow"
        outcomes.append(
            RequestOutcome(
                request,
                result,
                decision,
                payload["returned"],
                payload["truncated"],
                payload["flooded"],
                executed,
                op.effect,
            )
        )
    return outcomes


def analyze_server(
    server: ServerSpec,
    needed_capabilities: List[str],
    ops_meta: Dict[str, str],
    output_token_limit: int,
) -> Dict[str, Any]:
    """Score a server's boundary. A scoped server returns empty lists for every defect.

    Defects detected:
    - over_exposed: an exposed operation whose capability is not in the needed set, so the surface
      is wider than the agents require.
    - ungated_sensitive: an exposed write or destructive operation with no gate in front of it.
    - unbounded: an exposed operation whose effective output cap exceeds the host output limit, so a
      single call can flood context. This catches an operation that declares a ceiling past the host
      limit, which is the `anthropic/maxResultSizeChars` edge.
    - mislabeled: an exposed operation whose declared effect is less dangerous than the effect its
      capability actually carries, which hides risk from the gate.
    """
    needed = set(needed_capabilities)

    over_exposed = [
        op.name for op in server.operations if op.exposed and op.capability not in needed
    ]

    ungated_sensitive = [
        op.name
        for op in server.operations
        if op.exposed and op.effect in ("write", "destructive") and not op.gated
    ]

    unbounded = []
    mislabeled = []
    for op in server.operations:
        if not op.exposed:
            continue
        cap = op.declared_result_limit if op.declared_result_limit > 0 else output_token_limit
        if cap > output_token_limit:
            unbounded.append(op.name)
        expected = ops_meta.get(op.capability, "read")
        if EFFECT_RANK[op.effect] < EFFECT_RANK[expected]:
            mislabeled.append(op.name)

    return {
        "over_exposed": over_exposed,
        "ungated_sensitive": ungated_sensitive,
        "unbounded": unbounded,
        "mislabeled": mislabeled,
    }
