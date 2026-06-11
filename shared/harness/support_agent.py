"""Customer support agent: the integration harness for the v1.0 capstone.

A capstone takes one anchor scenario end to end and combines the relevant labs into a single design
problem. The customer support agent is the first anchor scenario, and it composes three labs:

- Lab 01, agent loop observability. Every request is handled as a small, observable flow whose
  decisions (escalation check, routing, gate, execution, handoff) are recorded as a trace, so an
  incident is explainable and the run is auditable.
- Lab 02, tool catalog design. A request routes to a tool through the catalog, and a permission gate
  governs whether the selected tool may execute. This module reuses the catalog engine directly.
- Lab 07, human escalation patterns. An escalation policy decides, before the agent acts, whether a
  request must reach a human. This module reuses the escalation engine directly.

The integration is the point. The three controls are layered in a specific order: the escalation
policy decides a human handoff before any tool runs, the catalog makes the right tool obvious, and
the gate governs execution. One refinement appears only when the labs are composed: an authorized and
confirmed high-impact action is not escalated, because the gate governs it, while an unauthorized
high-impact action, an out-of-policy request, or an explicit request for a human is escalated before
the agent acts. The naive design composes the labs' failure modes instead: a post-action escalation,
an ungated catalog, and no observability, so an unauthorized account closure executes before any
human sees it.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from .catalog import Catalog, PermissionGate, Request as CatalogRequest, route as catalog_route
from .catalog import analyze_catalog
from .escalation import EscalationPolicy, Request as EscalationRequest, analyze_policy, classify


@dataclass
class SupportRequest:
    id: str
    intent: str
    impact: str  # "low" or "high"
    in_policy: bool
    authorized: bool
    confirmed: bool
    user_requested_human: bool
    must_escalate: bool
    description: str


@dataclass
class SupportOutcome:
    request_id: str
    status: str  # "handled", "escalated", or "blocked"
    executed_tool: Optional[str]
    executed_effect: Optional[str]
    escalated_before_action: bool
    late_escalation: bool
    missed_escalation: bool
    harm: bool
    trace: List[Dict[str, Any]] = field(default_factory=list)


def _to_catalog_request(request: SupportRequest) -> CatalogRequest:
    return CatalogRequest(
        id=request.id,
        intent=request.intent,
        description=request.description,
        authorized=request.authorized,
        confirmed=request.confirmed,
    )


def _to_escalation_request(request: SupportRequest) -> EscalationRequest:
    return EscalationRequest(
        id=request.id,
        description=request.description,
        impact=request.impact,
        in_policy=request.in_policy,
        confidence="high",
        user_requested_human=request.user_requested_human,
        must_escalate=request.must_escalate,
    )


def handle(
    request: SupportRequest,
    catalog: Catalog,
    policy: EscalationPolicy,
    gate: PermissionGate,
    observable: bool,
) -> SupportOutcome:
    """Handle one support request by composing escalation, routing, and the gate.

    The escalation policy is consulted against the request, and the request is routed to a tool. When
    the policy escalates before acting and the action is not an authorized, confirmed one, the request
    is handed off to a human before any tool runs. Otherwise the gate governs execution. A post-action
    policy executes first and escalates too late, which is how the naive design lets a high-impact
    action run before a human sees it.
    """
    trace: List[Dict[str, Any]] = []

    def rec(**event: Any) -> None:
        if observable:
            trace.append(event)

    decision = classify(policy, _to_escalation_request(request))
    rec(event="escalation_check", action=decision.action, fired=decision.fired_triggers,
        timing=policy.escalate_timing)

    route_result = catalog_route(catalog, _to_catalog_request(request))
    rec(event="route", status=route_result.status,
        tool=route_result.selected.name if route_result.selected else None)

    authorized_action = request.authorized and request.confirmed
    escalated_before_action = False
    late_escalation = False
    executed_tool: Optional[str] = None
    executed_effect: Optional[str] = None
    status: str

    pre_action_handoff = (
        policy.escalate_timing == "pre_action"
        and decision.action == "escalate"
        and not authorized_action
    )

    if pre_action_handoff:
        rec(event="handoff", reason="escalated_pre_action", target=policy.route)
        escalated_before_action = True
        status = "escalated"
    elif route_result.selected is None:
        rec(event="handoff", reason="unroutable", target=policy.route)
        status = "escalated"
    else:
        gate_decision = gate.authorize(route_result.selected, _to_catalog_request(request))
        rec(event="gate", decision=gate_decision.decision, reason=gate_decision.reason)
        if gate_decision.decision == "allow":
            executed_tool = route_result.selected.name
            executed_effect = route_result.selected.effect
            rec(event="execute", tool=executed_tool, effect=executed_effect)
            status = "handled"
        elif gate_decision.decision == "escalate":
            rec(event="handoff", reason=gate_decision.reason, target=policy.route)
            status = "escalated"
        else:
            rec(event="blocked", reason=gate_decision.reason)
            status = "blocked"

        if (
            policy.escalate_timing == "post_action"
            and decision.action == "escalate"
            and executed_tool is not None
            and request.impact == "high"
        ):
            rec(event="late_escalation", reason="escalated_after_action", target=policy.route)
            late_escalation = True

    missed_escalation = (
        request.must_escalate and status == "handled" and not escalated_before_action
    )
    harm = request.must_escalate and executed_tool is not None and not escalated_before_action

    return SupportOutcome(
        request.id,
        status,
        executed_tool,
        executed_effect,
        escalated_before_action,
        late_escalation,
        missed_escalation,
        harm,
        trace,
    )


def drive_session(
    requests: List[SupportRequest],
    catalog: Catalog,
    policy: EscalationPolicy,
    observable: bool,
) -> List[SupportOutcome]:
    """Handle every request in a session through one design.

    A single gate instance governs the session, the same way the bad and good labs share one engine
    and differ only in the catalog, the policy, and whether the flow is observable.
    """
    gate = PermissionGate()
    return [handle(request, catalog, policy, gate, observable) for request in requests]


def analyze_design(
    catalog: Catalog,
    policy: EscalationPolicy,
    observable: bool,
    intents_meta: Dict[str, str],
) -> Dict[str, Any]:
    """Score a capstone design by composing the labs' own analyzers.

    The catalog defects come from lab 02's `analyze_catalog`, the policy defects from lab 07's
    `analyze_policy`, and observability is the lab 01 concern. A sound design has no catalog or policy
    defects and is observable.
    """
    return {
        "catalog": analyze_catalog(catalog, intents_meta),
        "policy": analyze_policy(policy),
        "observable": observable,
    }
