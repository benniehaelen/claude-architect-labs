"""Mock support and research tools driven by a session fixture.

A session fixture carries a `tool_behaviors` map. Each entry sets a tool to return data (`mode:
ok`) or to fail (`mode: error`). Building the registry from that map means the same fixture defines
both the scripted model decisions and how each tool responds, so a failure scenario is fully
described in one file.
"""

from __future__ import annotations

from typing import Any, Dict

from shared.harness.tools import ToolError, ToolRegistry


def build_registry(session: Dict[str, Any]) -> ToolRegistry:
    behaviors = session.get("tool_behaviors", {})
    registry = ToolRegistry()

    def make_handler(name: str):
        spec = behaviors.get(name, {"mode": "ok", "data": {}})

        def handler(args: Dict[str, Any]) -> Any:
            if spec.get("mode") == "error":
                raise ToolError(spec.get("message", "{0} failed".format(name)))
            return spec.get("data", {})

        return handler

    for name in behaviors:
        registry.register(name, make_handler(name))

    return registry
