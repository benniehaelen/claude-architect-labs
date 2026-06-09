"""Tool catalog design primitives for lab 02.

A catalog is the set of tools an agent is given. Its design decides whether the right tool is the
obvious choice and whether an unsafe action is hard to reach by accident. This module models the
two layers the lab teaches:

- The catalog and its tool descriptions are the guide layer. They shape which tool the model
  selects. Here that selection is modeled structurally through the `intents` a tool claims to
  serve, which stands in for what a natural-language description tells the model.
- The permission gate is the control layer. It governs whether a selected tool may actually
  execute, independent of what the description suggested. A gate can only govern a tool the catalog
  wired it to, so an ungated dangerous tool runs unchecked. That dependency is the heart of the lab.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

EFFECTS = ("read", "write", "destructive")
EFFECT_RANK = {"read": 0, "write": 1, "destructive": 2}


@dataclass
class ToolSpec:
    name: str
    description: str
    intents: List[str]
    effect: str  # one of EFFECTS
    gated: bool = False


@dataclass
class Catalog:
    name: str
    tools: List[ToolSpec]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Catalog":
        tools = [ToolSpec(**spec) for spec in data["tools"]]
        return cls(name=data["name"], tools=tools)

    def tools_for_intent(self, intent: str) -> List[ToolSpec]:
        return [tool for tool in self.tools if intent in tool.intents]


@dataclass
class Request:
    id: str
    intent: str
    description: str
    authorized: bool = False
    confirmed: bool = False


@dataclass
class GateDecision:
    decision: str  # "allow", "block", or "escalate"
    reason: str
    tool: Optional[str] = None


class PermissionGate:
    """Runtime control over execution.

    Read-effect tools pass freely. Write and destructive tools must be gated by the catalog and must
    carry authorization and confirmation. If a dangerous tool is not gated, there is no control in
    front of it and it simply runs, which is the failure the bad catalog demonstrates.
    """

    def authorize(self, tool: ToolSpec, request: Request) -> GateDecision:
        if tool.effect == "read":
            return GateDecision("allow", "read_only", tool.name)

        if not tool.gated:
            # No gate was wired to this dangerous tool, so nothing governs it.
            return GateDecision("allow", "ungated_dangerous_executed", tool.name)

        if not request.authorized:
            return GateDecision("escalate", "unauthorized_high_impact_action", tool.name)

        if not request.confirmed:
            return GateDecision("block", "confirmation_required", tool.name)

        return GateDecision("allow", "authorized_and_confirmed", tool.name)


@dataclass
class RouteResult:
    request_id: str
    intent: str
    matches: List[str]
    status: str  # "ok", "ambiguous", or "unroutable"
    selected: Optional[ToolSpec] = None


def route(catalog: Catalog, request: Request) -> RouteResult:
    """Select a tool for a request by intent.

    Zero matches is unroutable. More than one match is ambiguous, which is itself a catalog defect:
    a well-designed catalog leaves the model exactly one obvious choice. When matches exist, the
    first declared tool is selected, which mirrors a model resolving ambiguity arbitrarily.
    """
    matches = catalog.tools_for_intent(request.intent)
    names = [tool.name for tool in matches]
    if not matches:
        return RouteResult(request.id, request.intent, names, "unroutable", None)
    status = "ok" if len(matches) == 1 else "ambiguous"
    return RouteResult(request.id, request.intent, names, status, matches[0])


@dataclass
class RequestOutcome:
    request: Request
    route: RouteResult
    gate: Optional[GateDecision]
    executed: bool
    effect: Optional[str]


def drive(catalog: Catalog, requests: List[Request]) -> List[RequestOutcome]:
    """Route and gate every request against one catalog.

    This is the shared engine. The bad version and the reference solution call it with identical
    code and differ only in which catalog they pass, which makes the point that the runtime gate is
    only as good as the catalog wired to it.
    """
    gate = PermissionGate()
    outcomes: List[RequestOutcome] = []
    for request in requests:
        result = route(catalog, request)
        if result.selected is None:
            outcomes.append(RequestOutcome(request, result, None, False, None))
            continue
        decision = gate.authorize(result.selected, request)
        executed = decision.decision == "allow"
        outcomes.append(
            RequestOutcome(request, result, decision, executed, result.selected.effect)
        )
    return outcomes


def analyze_catalog(catalog: Catalog, intents_meta: Dict[str, str]) -> Dict[str, Any]:
    """Score a catalog's design. A clean catalog returns empty lists for every defect.

    Defects detected:
    - overlaps: an intent served by more than one tool, so selection is ambiguous.
    - ungated_dangerous: a write or destructive tool with no permission gate in front of it.
    - coarse: a single tool that bundles a benign read intent together with a write or destructive
      intent, so selecting it for the benign task hands the agent the dangerous capability too.
    - mislabeled: a tool whose declared effect is less dangerous than the intents it actually
      serves, which hides risk from the gate.
    """
    intent_to_tools: Dict[str, List[str]] = {}
    for tool in catalog.tools:
        for intent in tool.intents:
            intent_to_tools.setdefault(intent, []).append(tool.name)
    overlaps = {intent: names for intent, names in intent_to_tools.items() if len(names) > 1}

    ungated_dangerous = [
        tool.name
        for tool in catalog.tools
        if tool.effect in ("write", "destructive") and not tool.gated
    ]

    coarse = []
    mislabeled = []
    for tool in catalog.tools:
        effects = {intents_meta.get(intent, "read") for intent in tool.intents}
        has_read = "read" in effects
        has_danger = bool(effects & {"write", "destructive"})
        if has_read and has_danger:
            coarse.append(tool.name)

        expected_rank = max(
            (EFFECT_RANK[intents_meta.get(intent, "read")] for intent in tool.intents),
            default=0,
        )
        if EFFECT_RANK[tool.effect] < expected_rank:
            mislabeled.append(tool.name)

    return {
        "overlaps": overlaps,
        "ungated_dangerous": ungated_dangerous,
        "coarse": coarse,
        "mislabeled": mislabeled,
    }
