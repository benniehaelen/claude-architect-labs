"""Claude Code team-configuration primitives for lab 04.

A team configures Claude Code so that conventions hold across every member and every pipeline run.
The lab teaches one judgment: match the enforcement layer to whether the requirement is a preference
or a must, and know the specific Read-versus-Write limitation that makes a rules-only answer wrong.

This module models the configuration layers and the events they actually fire on. The load-bearing
fact, dated and sourced in VERIFIED.md, is that a path-scoped rule loads when Claude reads or edits a
matching file, not when it creates one. So a rule meant to enforce a convention at file-creation time
can silently fail. A guide raises the likelihood of a behavior; a control governs it deterministically
on the events it fires on (see ENFORCEMENT_LAYER.md).

The decisive insight, visible in the runners, is that the rules-only configuration and the layered
configuration run through the exact same enforcement engine. Only the configuration differs. The
engine decides whether each convention is governed, merely guided, or unenforced on each event, and a
must-hold convention that is not governed on its binding event is the silent gap the lab corrects.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

# Each layer is either a guide (raises likelihood) or a control (governs deterministically).
LAYER_KIND = {
    "memory": "guide",      # CLAUDE.md memory, present in context
    "rule": "guide",        # path-scoped rule, .claude/rules/*.md with a paths glob
    "hook": "control",      # PostToolUse hook, runs after Write and Edit
    "precommit": "control", # git pre-commit check
    "ci": "control",        # CI gate in the pipeline
}

# The events each layer actually fires on. The rule firing on "edit" but not "create" is the verified
# edge: a path-scoped rule loads on read and edit of a matching file, not on its creation.
LAYER_FIRES_ON = {
    "memory": {"create", "edit"},
    "rule": {"edit"},
    "hook": {"create", "edit"},
    "precommit": {"commit"},
    "ci": {"commit"},
}

EVENTS = ("create", "edit", "commit")


@dataclass
class Convention:
    name: str
    kind: str  # "preference" or "must"
    description: str
    enforced_by: List[str]  # layer names from LAYER_KIND
    binding_events: List[str]  # events a must-hold convention must be governed on; empty for a preference


@dataclass
class TeamConfig:
    name: str
    conventions: List[Convention]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TeamConfig":
        conventions = [Convention(**spec) for spec in data["conventions"]]
        return cls(name=data["name"], conventions=conventions)

    def convention(self, name: str) -> Optional[Convention]:
        for convention in self.conventions:
            if convention.name == name:
                return convention
        return None


@dataclass
class Event:
    id: str
    action: str  # one of EVENTS
    target_convention: str
    description: str


@dataclass
class EventOutcome:
    event: Event
    convention: Optional[Convention]
    fired_layers: List[str]
    outcome: str  # "governed", "guided", "unenforced", or "no_convention"
    silent_gap: bool  # a must-hold convention not governed on a binding event


def _layers_firing(convention: Convention, action: str) -> List[str]:
    return [
        layer
        for layer in convention.enforced_by
        if layer in LAYER_FIRES_ON and action in LAYER_FIRES_ON[layer]
    ]


def evaluate(convention: Optional[Convention], event: Event) -> EventOutcome:
    """Decide how a single event is enforced under one configuration.

    A control that fires governs the event. Failing that, a guide that fires merely guides it. Failing
    both, the event is unenforced. A must-hold convention that is not governed on one of its binding
    events is a silent gap: the configuration looks like it covers the convention but does not enforce
    it where it matters.
    """
    if convention is None:
        return EventOutcome(event, None, [], "no_convention", False)

    fired = _layers_firing(convention, event.action)
    governed = any(LAYER_KIND[layer] == "control" for layer in fired)
    guided = any(LAYER_KIND[layer] == "guide" for layer in fired)

    if governed:
        outcome = "governed"
    elif guided:
        outcome = "guided"
    else:
        outcome = "unenforced"

    silent_gap = (
        convention.kind == "must"
        and event.action in convention.binding_events
        and not governed
    )
    return EventOutcome(event, convention, fired, outcome, silent_gap)


def drive(config: TeamConfig, events: List[Event]) -> List[EventOutcome]:
    """Run every event through one configuration.

    This is the shared engine. The rules-only configuration and the layered configuration call it with
    identical code and differ only in which configuration they pass, which makes the point that a
    convention holds because of the layer that governs it, not because it was written down.
    """
    return [evaluate(config.convention(event.target_convention), event) for event in events]


def analyze_config(config: TeamConfig) -> Dict[str, Any]:
    """Score a configuration. A sound configuration returns empty lists for every defect.

    Defects detected:
    - guide_for_must: a must-hold convention enforced only by guides, with no control anywhere, so
      nothing governs it deterministically.
    - uncovered_binding: a "convention:event" pair where a must-hold convention's binding event has no
      control firing on it. The house-style convention on a "create" event is the verified write-time
      gap.
    - control_for_preference: a preference governed by a blocking control, which pays for a control
      where a guide would do and is the inverse error.
    """
    guide_for_must = []
    uncovered_binding = []
    control_for_preference = []

    for convention in config.conventions:
        controls = [layer for layer in convention.enforced_by if LAYER_KIND.get(layer) == "control"]

        if convention.kind == "must":
            if not controls:
                guide_for_must.append(convention.name)
            for event in convention.binding_events:
                firing_controls = [
                    layer for layer in controls if event in LAYER_FIRES_ON.get(layer, set())
                ]
                if not firing_controls:
                    uncovered_binding.append("{0}:{1}".format(convention.name, event))

        if convention.kind == "preference" and controls:
            control_for_preference.append(convention.name)

    return {
        "guide_for_must": guide_for_must,
        "uncovered_binding": uncovered_binding,
        "control_for_preference": control_for_preference,
    }
