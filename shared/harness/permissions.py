"""Agent permission and sandboxing primitives for lab 08.

An autonomous agent, the kind that runs in a CI pipeline, acts through tools. Two complementary
layers decide what it may do, and knowing which layer covers which threat is the heart of the lab
(see VERIFIED.md):

- Permission scoping. Permission rules decide which tool calls Claude Code allows, evaluated deny
  first, then ask, then allow. A deny at any scope wins. Bypassing permissions (the bypassPermissions
  mode or the --dangerously-skip-permissions flag) removes this layer, so an unscoped agent runs
  whatever it decides to run.
- OS-level sandbox. The sandboxed Bash tool confines a command and its child processes at the
  operating-system level, so the boundary holds regardless of what the model chose to run. This is
  the only layer that contains an arbitrary subprocess, because permission Read and Edit deny rules
  apply to Claude's own file tools, not to a build subprocess that opens files itself.
- File-state isolation. Running in a worktree isolates the agent's file edits so they are revertible
  and do not affect the shared tree, which forking alone does not provide (see VERIFIED.md primitive
  on session forking).

The decisive insight, visible in the runners, is that the unscoped agent and the scoped, sandboxed
agent run through the exact same engine. Only the configuration differs. A dangerous action is
contained, or not, because of the permission rules, the sandbox, and the isolation, not because the
agent was told to be careful. In particular, scoping permissions tightly is not the same as
containing a subprocess: only the sandbox does that.
"""

from __future__ import annotations

import fnmatch
from dataclasses import dataclass
from typing import Any, Dict, List

MODES = ("default", "acceptEdits", "plan", "bypassPermissions")
ISOLATIONS = ("shared_cwd", "worktree")

# Kinds of action the agent attempts. dangerous_command and credential_read_subprocess are the two
# that need OS-level containment, because their real effect happens in a subprocess.
ACTION_KINDS = ("benign", "dangerous_command", "credential_read_subprocess", "file_edit")


@dataclass
class Attempt:
    id: str
    rule: str  # the permission rule string this call matches, e.g. "Bash(npm run build)"
    kind: str  # one of ACTION_KINDS
    needed: bool
    description: str


@dataclass
class AgentConfig:
    name: str
    mode: str  # one of MODES
    allow: List[str]
    deny: List[str]
    sandbox_enabled: bool
    isolation: str  # one of ISOLATIONS

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AgentConfig":
        return cls(**data)


@dataclass
class ActionOutcome:
    attempt: Attempt
    decision: str  # "allow", "deny", or "prompt"
    contained: bool
    isolated: bool
    ran_dangerous: bool
    leaked_credentials: bool
    unisolated_edit: bool
    blocked_needed: bool


def _matches(patterns: List[str], rule: str) -> bool:
    return any(fnmatch.fnmatch(rule, pattern) for pattern in patterns)


def decide_permission(config: AgentConfig, attempt: Attempt) -> str:
    """Decide allow, deny, or prompt for one attempt under the permission rules.

    Deny is evaluated first and always wins, even in bypassPermissions mode. With no matching deny,
    bypass mode allows everything; otherwise an allow rule allows the call and anything else prompts,
    which in a non-interactive pipeline is effectively a block.
    """
    if _matches(config.deny, attempt.rule):
        return "deny"
    if config.mode == "bypassPermissions":
        return "allow"
    if _matches(config.allow, attempt.rule):
        return "allow"
    return "prompt"


def evaluate(config: AgentConfig, attempt: Attempt) -> ActionOutcome:
    """Evaluate one attempt: the permission decision, OS-level containment, and file isolation.

    Containment of a subprocess effect comes only from the sandbox. A permission deny rule cannot
    reach inside an allowed subprocess, so a credential read performed by an allowed build command is
    contained only when the sandbox is enabled. File edits are isolated only in a worktree.
    """
    decision = decide_permission(config, attempt)
    ran = decision == "allow"

    if attempt.kind in ("dangerous_command", "credential_read_subprocess"):
        contained = config.sandbox_enabled
    else:
        contained = True

    isolated = config.isolation == "worktree"

    ran_dangerous = ran and attempt.kind == "dangerous_command" and not contained
    leaked_credentials = ran and attempt.kind == "credential_read_subprocess" and not contained
    unisolated_edit = ran and attempt.kind == "file_edit" and not isolated
    blocked_needed = attempt.needed and decision in ("deny", "prompt")

    return ActionOutcome(
        attempt,
        decision,
        contained,
        isolated,
        ran_dangerous,
        leaked_credentials,
        unisolated_edit,
        blocked_needed,
    )


def drive(config: AgentConfig, attempts: List[Attempt]) -> List[ActionOutcome]:
    """Evaluate every attempt under one configuration.

    This is the shared engine. The unscoped agent and the scoped, sandboxed agent call it with
    identical code and differ only in which configuration they pass, which makes the point that
    containment is a property of the configuration, not of the action.
    """
    return [evaluate(config, attempt) for attempt in attempts]


def analyze_config(config: AgentConfig) -> Dict[str, Any]:
    """Score a configuration. A sound configuration returns False for every defect.

    Defects detected:
    - bypass_permissions: the agent bypasses the permission layer, so nothing scopes its tool calls.
    - no_sandbox: the Bash sandbox is disabled, so a subprocess effect is not contained at the OS
      level even when permission rules are tight.
    - shared_filesystem: the agent runs in the shared working directory rather than an isolated
      worktree, so its file edits are not revertible and affect the shared tree.
    """
    return {
        "bypass_permissions": config.mode == "bypassPermissions",
        "no_sandbox": not config.sandbox_enabled,
        "shared_filesystem": config.isolation != "worktree",
    }
