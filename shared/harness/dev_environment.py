"""Developer-productivity environment: the integration harness for the v1.0 dev capstone.

A development team configures Claude Code for everyday work. The capstone composes two labs into one
environment:

- Lab 02, tool catalog design. The team exposes a catalog of developer tools (run tests, read and edit
  source, open a PR, deploy) and a permission gate governs the high-impact ones. This module reuses the
  catalog engine directly.
- Lab 04, Claude Code team workflow. The team enforces conventions (no em-dash house style, no
  committed secrets) in the right layer, where a path-scoped rule guides and a hook, pre-commit check,
  or CI gate governs. This module reuses the config engine directly.

The integration is the point. A developer action both invokes a tool, which the catalog routes and the
gate governs, and may produce an artifact whose convention must be governed on its event by the config
layer. Both must hold. The naive environment composes the labs' failure modes: an ungated deploy tool
runs without authorization (lab 02), and a newly created file violates the house style because the
rule-only config does not fire on creation (lab 04). The composed environment gates the high-impact
tool and governs the convention on every event, so a dangerous action is stopped and a created file is
held to the convention.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from .catalog import Catalog, PermissionGate, Request as CatalogRequest, analyze_catalog, route
from .config import Event as ConfigEvent, TeamConfig, analyze_config, evaluate


@dataclass
class DevAction:
    id: str
    description: str
    intent: Optional[str] = None  # the tool intent, or None for a convention-only action like a commit
    authorized: bool = False
    confirmed: bool = False
    convention: Optional[str] = None  # the convention its artifact is subject to, or None
    event: Optional[str] = None  # "create", "edit", or "commit" for the convention, or None


@dataclass
class DevOutcome:
    action_id: str
    tool: Optional[str]
    gate_decision: Optional[str]
    executed: bool
    tool_effect: Optional[str]
    convention: Optional[str]
    convention_outcome: Optional[str]
    convention_gap: bool
    ungated_dangerous_ran: bool
    harm: bool


def handle(
    action: DevAction,
    catalog: Catalog,
    gate: PermissionGate,
    config: TeamConfig,
) -> DevOutcome:
    """Handle one developer action across both dimensions.

    The tool dimension routes the intent through the catalog and lets the gate govern execution. The
    convention dimension evaluates the artifact's convention under the team config on its event. A
    destructive tool that runs ungated and a must-hold convention that is not governed on its binding
    event are the two failures that compound.
    """
    tool_name: Optional[str] = None
    tool_effect: Optional[str] = None
    gate_decision: Optional[str] = None
    gate_reason: Optional[str] = None
    executed = False

    if action.intent is not None:
        request = CatalogRequest(
            id=action.id,
            intent=action.intent,
            description=action.description,
            authorized=action.authorized,
            confirmed=action.confirmed,
        )
        route_result = route(catalog, request)
        if route_result.selected is not None:
            tool_name = route_result.selected.name
            tool_effect = route_result.selected.effect
            decision = gate.authorize(route_result.selected, request)
            gate_decision = decision.decision
            gate_reason = decision.reason
            executed = decision.decision == "allow"

    convention_outcome: Optional[str] = None
    convention_gap = False
    if action.convention is not None:
        convention = config.convention(action.convention)
        event = ConfigEvent(
            id=action.id,
            action=action.event,
            target_convention=action.convention,
            description=action.description,
        )
        result = evaluate(convention, event)
        convention_outcome = result.outcome
        convention_gap = result.silent_gap

    ungated_dangerous_ran = (
        executed and gate_reason == "ungated_dangerous_executed" and tool_effect == "destructive"
    )
    harm = ungated_dangerous_ran or convention_gap

    return DevOutcome(
        action.id,
        tool_name,
        gate_decision,
        executed,
        tool_effect,
        action.convention,
        convention_outcome,
        convention_gap,
        ungated_dangerous_ran,
        harm,
    )


def drive_session(
    actions: List[DevAction],
    catalog: Catalog,
    config: TeamConfig,
) -> List[DevOutcome]:
    """Handle every developer action through one environment.

    A single gate governs the session, and the catalog and config differ between the naive and composed
    environments, the same way each source lab shares one engine and differs only in its configuration.
    """
    gate = PermissionGate()
    return [handle(action, catalog, gate, config) for action in actions]


def analyze_environment(
    catalog: Catalog,
    config: TeamConfig,
    intents_meta: Dict[str, str],
) -> Dict[str, Any]:
    """Score a dev environment by composing the labs' own analyzers.

    The catalog defects come from lab 02's `analyze_catalog` and the config defects from lab 04's
    `analyze_config`. A sound environment has no ungated dangerous tools and no must-hold convention
    that a guide alone enforces.
    """
    return {
        "catalog": analyze_catalog(catalog, intents_meta),
        "config": analyze_config(config),
    }
