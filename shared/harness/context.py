"""Context-management primitives for lab 06.

Long-running and multi-agent systems accumulate context until it overflows, and the dangerous
failures are the quiet ones: information silently dropped, a summarization that loses the load-bearing
detail, or a branch that diverges in conversation but shares a filesystem. This module models the two
facets the lab hardens and contrasts a design that fails silently against one that fails loudly.

- Context overflow. As segments accumulate past the window limit, the overflow policy decides what
  happens. A silent drop evicts the oldest segments with no signal, so a load-bearing detail can
  vanish unnoticed. A lossy summary collapses everything, including the load-bearing detail, again
  with no signal. A checkpoint-and-signal policy pins the load-bearing segments, summarizes the rest,
  and emits an overflow signal, so the failure is loud and recoverable.
- Branch file isolation. Session forking branches the conversation history but not the filesystem (see
  VERIFIED.md). A forked agent's file edits are real and visible to every session in the same working
  directory. Forking alone therefore does not isolate files. A branch that must revert file changes
  needs file checkpointing.

The decisive insight, visible in the runners, is that the silent design and the loud design run
through the exact same engine. Only the design differs. Context handling must be designed to fail
loudly, and file isolation needs its own control because forking isolates the conversation, not the
files.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List

OVERFLOW_POLICIES = ("silent_drop", "summarize_lossy", "checkpoint_signal")
ISOLATION_POLICIES = ("fork_only", "file_checkpoint")
BUDGET_ENFORCEMENT = ("orchestration", "prompt", "none")


@dataclass
class Segment:
    id: str
    tokens: int
    load_bearing: bool


@dataclass
class SessionDesign:
    name: str
    budget_enforcement: str  # "orchestration", "prompt", or "none"
    overflow_policy: str  # one of OVERFLOW_POLICIES
    isolation_policy: str  # one of ISOLATION_POLICIES

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SessionDesign":
        return cls(**data)


@dataclass
class ContextResult:
    total_tokens: int
    limit: int
    retained: List[str]
    dropped_load_bearing: List[str]
    overflow_signaled: bool


@dataclass
class IsolationResult:
    leaked_to_parent: bool
    revertible: bool
    branch_edits: List[str]


@dataclass
class SessionResult:
    context: ContextResult
    isolation: IsolationResult


def apply_overflow(policy: str, segments: List[Segment], limit: int) -> ContextResult:
    """Apply an overflow policy to accumulated segments.

    Under the limit, every segment is retained. Over the limit, the policy decides what is lost and
    whether the loss is signaled. The two metrics that matter are whether a load-bearing segment lost
    its detail and whether the overflow was signaled.
    """
    total = sum(segment.tokens for segment in segments)
    if total <= limit:
        return ContextResult(total, limit, [s.id for s in segments], [], False)

    if policy == "silent_drop":
        # Evict the oldest segments until the running total fits. No signal is emitted.
        running = total
        index = 0
        dropped: List[Segment] = []
        while running > limit and index < len(segments):
            dropped.append(segments[index])
            running -= segments[index].tokens
            index += 1
        retained = segments[index:]
        dropped_load_bearing = [s.id for s in dropped if s.load_bearing]
        return ContextResult(total, limit, [s.id for s in retained], dropped_load_bearing, False)

    if policy == "summarize_lossy":
        # Collapse everything into one summary, losing the load-bearing detail. No signal.
        dropped_load_bearing = [s.id for s in segments if s.load_bearing]
        return ContextResult(total, limit, ["summary"], dropped_load_bearing, False)

    if policy == "checkpoint_signal":
        # Pin the load-bearing segments, summarize the rest, and signal the overflow.
        load_bearing = [s for s in segments if s.load_bearing]
        retained = [s.id for s in load_bearing] + ["summary_of_rest"]
        return ContextResult(total, limit, retained, [], True)

    raise ValueError("unknown overflow policy: {0}".format(policy))


def apply_isolation(policy: str, branch_edits: List[str]) -> IsolationResult:
    """Apply a branch-isolation policy to the files a forked branch edits.

    Forking branches the conversation history but not the filesystem, so fork-only edits land in the
    shared working directory and cannot be reverted by the branch. File checkpointing isolates the
    branch's edits and makes them revertible.
    """
    if policy == "fork_only":
        return IsolationResult(leaked_to_parent=True, revertible=False, branch_edits=branch_edits)
    if policy == "file_checkpoint":
        return IsolationResult(leaked_to_parent=False, revertible=True, branch_edits=branch_edits)
    raise ValueError("unknown isolation policy: {0}".format(policy))


def run_session(design: SessionDesign, scenario: Dict[str, Any]) -> SessionResult:
    """Run one design over a scenario of accumulating segments and a forked branch that edits files.

    This is the shared engine. The silent design and the loud design call it with identical code and
    differ only in which design they pass, which makes the point that a context failure is silent or
    loud because of the policy, not because of the workload.
    """
    segments = [Segment(**spec) for spec in scenario["segments"]]
    context = apply_overflow(design.overflow_policy, segments, scenario["context_limit"])
    isolation = apply_isolation(design.isolation_policy, list(scenario["branch_edits"]))
    return SessionResult(context=context, isolation=isolation)


def analyze_design(design: SessionDesign) -> Dict[str, Any]:
    """Score a design. A sound design returns False for every defect.

    Defects detected:
    - budget_by_prompt: context budgeting is left to a prompt instruction or skipped, where an
      orchestration limit is needed.
    - silent_overflow: the overflow policy drops or collapses context without signaling, so a loss
      passes unnoticed.
    - fork_only_isolation: a branch relies on forking alone for file isolation, which forking does not
      provide.
    """
    return {
        "budget_by_prompt": design.budget_enforcement != "orchestration",
        "silent_overflow": design.overflow_policy in ("silent_drop", "summarize_lossy"),
        "fork_only_isolation": design.isolation_policy == "fork_only",
    }
