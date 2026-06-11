"""Human-escalation primitives for lab 07.

Governance runs through every lab as a cross-cut, but the escalation decision itself, when automation
should stop and hand a request to a human, deserves a deep treatment. This module models that decision
as a policy that classifies each request into one of three dispositions: handle it automatically,
escalate it to a human, or hold it under a fail-safe default.

The lab teaches three things about an escalation policy, each enforced at runtime and none of them by
a prompt instruction alone:

- Coverage. The triggers must catch every request that must reach a human (out of policy, high impact,
  low confidence, or an explicit request for a human). A trigger gap means a must-escalate request is
  handled automatically, which is a silent miss.
- Timing. Escalation must happen before an irreversible or high-impact action, not after. A policy
  that acts first and escalates only when something went wrong has already done the harm.
- Delivery and fail-safe. An escalation needs a defined route to a human, and when the route is
  unavailable or the request is uncertain, the default must hold rather than proceed. Escalating to
  nowhere with a fail-open default lets the request proceed as if it had been handled.

The decisive insight, visible in the runners, is that the weak policy and the sound policy run through
the exact same engine. Only the policy differs. A request reaches a human, or does not, because of the
policy's coverage, timing, route, and default, not because the agent was told to be careful.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional

TIMINGS = ("pre_action", "post_action")
DEFAULTS = ("hold", "proceed")


@dataclass
class Request:
    id: str
    description: str
    impact: str  # "low" or "high"
    in_policy: bool
    confidence: str  # "low" or "high"
    user_requested_human: bool
    must_escalate: bool  # ground truth: this request should reach a human


# A trigger fires when its predicate holds for a request.
TRIGGER_PREDICATES: Dict[str, Callable[[Request], bool]] = {
    "out_of_policy": lambda request: not request.in_policy,
    "high_impact": lambda request: request.impact == "high",
    "low_confidence": lambda request: request.confidence == "low",
    "user_request": lambda request: request.user_requested_human,
}


@dataclass
class EscalationPolicy:
    name: str
    triggers: List[str]
    escalate_timing: str  # one of TIMINGS
    route: Optional[str]  # the human target, or None when escalation has nowhere to go
    default: str  # one of DEFAULTS, the fail-safe behavior when escalation cannot be delivered

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "EscalationPolicy":
        return cls(**data)


@dataclass
class Disposition:
    request_id: str
    fired_triggers: List[str]
    action: str  # "handle", "escalate", or "hold"
    timing: Optional[str]
    routed_to: Optional[str]
    missed: bool  # a must-escalate request that no trigger caught, handled automatically
    late: bool  # escalated after a high-impact action instead of before it
    dropped: bool  # a trigger fired but the request proceeded because escalation could not be delivered


def classify(policy: EscalationPolicy, request: Request) -> Disposition:
    """Classify one request under one policy.

    A request that fires a trigger escalates when a route exists, otherwise it falls to the fail-safe
    default. A request that fires no trigger is handled. The flags name the three failures the lab
    teaches: a coverage miss, a late escalation, and a dropped escalation that proceeded anyway.
    """
    fired = [name for name in policy.triggers if TRIGGER_PREDICATES[name](request)]
    needs_escalation = bool(fired)

    if not needs_escalation:
        action, timing, routed = "handle", None, None
    elif policy.route is not None:
        action, timing, routed = "escalate", policy.escalate_timing, policy.route
    elif policy.default == "hold":
        action, timing, routed = "hold", None, None
    else:
        action, timing, routed = "handle", None, None  # fail-open: escalation could not be delivered

    missed = request.must_escalate and action == "handle" and not needs_escalation
    late = action == "escalate" and timing == "post_action" and request.impact == "high"
    dropped = needs_escalation and action == "handle"
    return Disposition(request.id, fired, action, timing, routed, missed, late, dropped)


def drive(policy: EscalationPolicy, requests: List[Request]) -> List[Disposition]:
    """Classify every request under one policy.

    This is the shared engine. The weak policy and the sound policy call it with identical code and
    differ only in which policy they pass, which makes the point that the escalation outcome is a
    property of the policy, not of the request.
    """
    return [classify(policy, request) for request in requests]


def analyze_policy(policy: EscalationPolicy) -> Dict[str, Any]:
    """Score a policy. A sound policy returns False for every defect.

    Defects detected:
    - post_action_timing: the policy escalates after acting rather than before, so a high-impact
      action runs before a human sees it.
    - no_route: the policy has no route to a human, so an escalation has nowhere to go.
    - fail_open_default: the policy's default is to proceed rather than hold, so an undeliverable
      escalation proceeds as if it had been handled.
    """
    return {
        "post_action_timing": policy.escalate_timing == "post_action",
        "no_route": policy.route is None,
        "fail_open_default": policy.default == "proceed",
    }
