"""Multi-agent research system: the integration harness for the v1.0 research capstone.

A lead agent decomposes a question, spawns subagents that search, and synthesizes their findings. The
capstone composes two labs into one system:

- Lab 01, agent loop observability and orchestration. The lead runs within a step budget, records a
  structured trace of its orchestration, and when it cannot ground an answer it trips a circuit breaker
  and escalates to a human with a named reason, rather than looping forever or returning a confident
  but unfounded answer. This module reuses lab 01's Trace and LoopConfig directly.
- Lab 06, context management. The subagents' findings accumulate into the lead's context, which can
  overflow. The overflow must be handled loudly, pinning the load-bearing findings and signaling, not
  silently dropping them. And subagents are forked, so their file edits need worktree isolation,
  because forking branches the conversation, not the filesystem. This module reuses lab 06's
  apply_overflow and apply_isolation directly.

The integration is the point. The orchestration, the context budgeting, and the file isolation must
all hold at once. The naive design composes the labs' failure modes: an unbounded answer that ignores
thin grounding, a silent context drop that loses the one load-bearing finding, a forked subagent whose
file edits leak, and no trace. The composed design budgets and escalates, pins and signals, isolates,
and records, so a question with thin sources reaches a human with its evidence intact and auditable.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List

from .agentloop import LoopConfig
from .context import Segment, apply_isolation, apply_overflow
from .events import EventType, Trace


@dataclass
class Subagent:
    id: str
    status: str  # "ok" or "empty"
    findings_tokens: int
    load_bearing: bool
    edits_files: bool


@dataclass
class ResearchDesign:
    name: str
    overflow_policy: str  # lab 06 overflow policy
    isolation_policy: str  # lab 06 isolation policy
    escalate_on_no_convergence: bool  # lab 01: escalate rather than return a confident unfounded answer
    observable: bool  # lab 01: record a trace

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ResearchDesign":
        return cls(**data)


@dataclass
class ResearchOutcome:
    status: str  # "answered", "escalated", or "answered_unfounded"
    dropped_load_bearing: List[str]
    overflow_signaled: bool
    leaked_files: bool
    revertible: bool
    confident_unfounded: bool
    trace: List[Dict[str, Any]] = field(default_factory=list)


def run_research(design: ResearchDesign, scenario: Dict[str, Any]) -> ResearchOutcome:
    """Run one research session: orchestrate subagents, budget context, isolate forks, and decide.

    The lead processes subagents within the step budget, recording a trace when observable. Their
    findings are budgeted by the overflow policy and their file edits isolated by the isolation policy.
    The lead converges only when enough load-bearing findings survive; otherwise the design either
    escalates (the governed handoff) or returns a confident but unfounded answer (the black-box
    failure).
    """
    subagents = [Subagent(**spec) for spec in scenario["subagents"]]
    loop = LoopConfig(
        max_steps=scenario["loop"]["max_steps"],
        escalation_target=scenario["loop"]["escalation_target"],
    )
    trace = Trace()

    def rec(step: int, event_type: EventType, **data: Any) -> None:
        if design.observable:
            trace.record(step, event_type, **data)

    processed: List[Subagent] = []
    for index, subagent in enumerate(subagents, start=1):
        if index > loop.max_steps:
            break
        rec(index, EventType.STEP_START, subagent=subagent.id)
        rec(index, EventType.TOOL_CALL, tool="subagent_search", subagent=subagent.id)
        if subagent.status == "ok":
            rec(index, EventType.TOOL_RESULT, subagent=subagent.id,
                tokens=subagent.findings_tokens, load_bearing=subagent.load_bearing)
            processed.append(subagent)
        else:
            rec(index, EventType.TOOL_RESULT, subagent=subagent.id, tokens=0, note="empty")

    segments = [
        Segment(s.id, s.findings_tokens, s.load_bearing) for s in processed
    ]
    context_result = apply_overflow(design.overflow_policy, segments, scenario["context_limit"])

    edits = [s.id for s in processed if s.edits_files]
    isolation_result = apply_isolation(design.isolation_policy, edits)

    total_load_bearing = sum(1 for s in processed if s.load_bearing)
    retained_load_bearing = total_load_bearing - len(context_result.dropped_load_bearing)
    converged = retained_load_bearing >= scenario["convergence_threshold"]

    if converged:
        rec(loop.max_steps, EventType.STOP, reason="answered")
        status = "answered"
    elif design.escalate_on_no_convergence:
        rec(loop.max_steps, EventType.CIRCUIT_BREAK, reason="insufficient_grounding")
        rec(loop.max_steps, EventType.ESCALATE, target=loop.escalation_target,
            reason="insufficient_grounding")
        rec(loop.max_steps, EventType.STOP, reason="escalated_insufficient_grounding")
        status = "escalated"
    else:
        rec(loop.max_steps, EventType.STOP, reason="final_answer")
        status = "answered_unfounded"

    return ResearchOutcome(
        status=status,
        dropped_load_bearing=context_result.dropped_load_bearing,
        overflow_signaled=context_result.overflow_signaled,
        leaked_files=isolation_result.leaked_to_parent,
        revertible=isolation_result.revertible,
        confident_unfounded=status == "answered_unfounded",
        trace=trace.to_list(),
    )


def analyze_design(design: ResearchDesign) -> Dict[str, Any]:
    """Score a research design. A sound design returns False for every defect.

    Defects detected:
    - silent_overflow: context overflow drops findings without signaling, losing a load-bearing one.
    - fork_only_isolation: a forked subagent's file edits rely on forking alone for isolation.
    - no_escalation_on_no_convergence: the lead returns an answer even without enough grounding.
    - not_observable: the run records no trace, so it cannot be audited.
    """
    return {
        "silent_overflow": design.overflow_policy in ("silent_drop", "summarize_lossy"),
        "fork_only_isolation": design.isolation_policy == "fork_only",
        "no_escalation_on_no_convergence": not design.escalate_on_no_convergence,
        "not_observable": not design.observable,
    }
