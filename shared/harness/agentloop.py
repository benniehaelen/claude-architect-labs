"""The instrumented agent loop.

This is the reference loop for lab 01. Three properties distinguish it from the black-box loop in
the lab's bad_version:

1. It records a structured event at every decision point (a Trace), so an incident is explainable
   and the run is auditable.
2. It ties a circuit breaker to repeated tool failures and to a step budget, a runtime control
   rather than a prompt instruction.
3. When the breaker trips it escalates to a human queue and stops with a named reason, so the
   system fails safely (a governed handoff) rather than silently returning a confident wrong
   answer.

The contrast between this loop and the bad_version is the lab.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional

from .events import Event, EventType, Trace
from .tools import ToolError, ToolRegistry


@dataclass
class LoopConfig:
    max_steps: int = 8
    max_consecutive_failures: int = 3
    escalation_target: str = "human_support_queue"


@dataclass
class Outcome:
    status: str  # "completed" or "escalated"
    reason: str
    answer: Optional[str]
    trace: Trace


def run_agent_loop(
    model: Any,
    tools: ToolRegistry,
    task: str,
    config: Optional[LoopConfig] = None,
    on_event: Optional[Callable[[Event], None]] = None,
) -> Outcome:
    config = config or LoopConfig()
    trace = Trace()

    def emit(step: int, type: EventType, **data: Any) -> None:
        event = trace.record(step, type, **data)
        if on_event is not None:
            on_event(event)

    history: List[Dict[str, Any]] = []
    consecutive_failures = 0

    for step in range(1, config.max_steps + 1):
        emit(step, EventType.STEP_START)

        decision = model.decide(task, history)
        emit(
            step,
            EventType.MODEL_DECISION,
            action=decision.action,
            tool=decision.tool,
            args=decision.args,
        )

        if decision.action == "final":
            emit(step, EventType.STOP, reason="model_final")
            return Outcome("completed", "model_final", decision.answer, trace)

        emit(step, EventType.TOOL_CALL, tool=decision.tool, args=decision.args)
        try:
            result = tools.call(decision.tool, decision.args or {})
        except ToolError as exc:
            emit(step, EventType.TOOL_ERROR, tool=decision.tool, message=str(exc))
            consecutive_failures += 1
            history.append({"tool": decision.tool, "error": str(exc)})

            if consecutive_failures >= config.max_consecutive_failures:
                emit(
                    step,
                    EventType.CIRCUIT_BREAK,
                    reason="repeated_tool_failure",
                    consecutive_failures=consecutive_failures,
                )
                emit(
                    step,
                    EventType.ESCALATE,
                    target=config.escalation_target,
                    reason="repeated_tool_failure",
                )
                emit(step, EventType.STOP, reason="escalated_repeated_tool_failure")
                return Outcome("escalated", "repeated_tool_failure", None, trace)
            continue

        emit(step, EventType.TOOL_RESULT, tool=decision.tool, result=result)
        consecutive_failures = 0
        history.append({"tool": decision.tool, "result": result})

    emit(
        config.max_steps,
        EventType.CIRCUIT_BREAK,
        reason="step_budget_exhausted",
        max_steps=config.max_steps,
    )
    emit(
        config.max_steps,
        EventType.ESCALATE,
        target=config.escalation_target,
        reason="step_budget_exhausted",
    )
    emit(config.max_steps, EventType.STOP, reason="escalated_step_budget_exhausted")
    return Outcome("escalated", "step_budget_exhausted", None, trace)
