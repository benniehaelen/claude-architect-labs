"""A minimal tool registry for the loop.

Tools are deliberately thin here. Lab 02 is where catalog design gets serious. For lab 01 a tool
is just a named handler that either returns a result or raises ToolError, which is enough to drive
the success and failure paths the observability lab needs.
"""

from __future__ import annotations

from typing import Any, Callable, Dict


class ToolError(Exception):
    """Raised when a tool call fails. The loop treats this as a recordable failure signal."""


class ToolRegistry:
    def __init__(self) -> None:
        self._handlers: Dict[str, Callable[[Dict[str, Any]], Any]] = {}

    def register(self, name: str, handler: Callable[[Dict[str, Any]], Any]) -> None:
        self._handlers[name] = handler

    def call(self, name: str, args: Dict[str, Any]) -> Any:
        if name not in self._handlers:
            raise ToolError("unknown tool: {0}".format(name))
        return self._handlers[name](args or {})
