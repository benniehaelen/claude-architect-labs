"""Model clients for the loop.

The dry-run model is a scripted replay so the lab runs free and deterministically. A real model
call is the optional live counterpart and is not required for the reasoning work of the lab. This
mirrors the repository contract: no paid API calls to learn (see WHAT_NOT_TO_DO.md).
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

FIXTURES_DIR = Path(__file__).resolve().parents[1] / "fixtures"


@dataclass
class Decision:
    """A single model decision: call a tool, or finish with an answer."""

    action: str  # "call_tool" or "final"
    tool: Optional[str] = None
    args: Optional[Dict[str, Any]] = None
    answer: Optional[str] = None


class ScriptedModel:
    """Deterministic dry-run model that replays decisions from a session fixture.

    The script is a list of decisions. The model returns them in order regardless of history, which
    is exactly what makes a dry-run reproducible. Running past the end of the script yields a final
    decision so a loop can never hang on an exhausted script.
    """

    def __init__(self, script: List[Dict[str, Any]]) -> None:
        self._script = list(script)
        self._index = 0

    def decide(self, task: str, history: List[Dict[str, Any]]) -> Decision:
        if self._index >= len(self._script):
            return Decision(action="final", answer="(no further scripted decisions)")
        step = self._script[self._index]
        self._index += 1
        return Decision(
            action=step["action"],
            tool=step.get("tool"),
            args=step.get("args"),
            answer=step.get("answer"),
        )


def load_session(name: str) -> Dict[str, Any]:
    """Load a session fixture by name from shared/fixtures."""
    path = FIXTURES_DIR / "{0}.json".format(name)
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)
