"""Structured trace events for the agent loop.

The existence of these events is the whole point of lab 01. A black-box loop emits nothing
structured, so an incident cannot be explained after the fact and a runtime control has no signal
to act on. The instrumented loop records one event per decision point, which is what makes the
loop both auditable and governable.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional


class EventType(str, Enum):
    """The decision points worth recording in an agent loop."""

    STEP_START = "step_start"
    MODEL_DECISION = "model_decision"
    TOOL_CALL = "tool_call"
    TOOL_RESULT = "tool_result"
    TOOL_ERROR = "tool_error"
    CIRCUIT_BREAK = "circuit_break"
    ESCALATE = "escalate"
    STOP = "stop"


@dataclass
class Event:
    seq: int
    step: int
    type: EventType
    data: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return {"seq": self.seq, "step": self.step, "type": self.type.value, "data": self.data}


class Trace:
    """An ordered record of loop events.

    The sequence number is a monotonic counter rather than a wall-clock timestamp so that a
    dry-run trace is deterministic and can be asserted on in evals.
    """

    def __init__(self) -> None:
        self.events: List[Event] = []
        self._seq = 0

    def record(self, step: int, type: EventType, **data: Any) -> Event:
        self._seq += 1
        event = Event(seq=self._seq, step=step, type=type, data=data)
        self.events.append(event)
        return event

    def of_type(self, type: EventType) -> List[Event]:
        return [event for event in self.events if event.type == type]

    @property
    def tool_calls(self) -> List[Event]:
        return self.of_type(EventType.TOOL_CALL)

    @property
    def errors(self) -> List[Event]:
        return self.of_type(EventType.TOOL_ERROR)

    @property
    def escalated(self) -> bool:
        return bool(self.of_type(EventType.ESCALATE))

    @property
    def stop_reason(self) -> Optional[str]:
        stops = self.of_type(EventType.STOP)
        return stops[-1].data.get("reason") if stops else None

    def to_list(self) -> List[Dict[str, Any]]:
        return [event.to_dict() for event in self.events]
