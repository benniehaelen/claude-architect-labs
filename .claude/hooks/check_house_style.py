#!/usr/bin/env python3
"""PostToolUse hook: enforce the repository house style on Markdown files.

This is the runtime control that governs what the path-scoped house-style rule only guides. The
rule (.claude/rules/house-style.md) loads when Claude reads a Markdown file, but it is not injected
when Claude writes or creates one (see VERIFIED.md). This hook closes that gap by running after
every Write, Edit, or MultiEdit and failing when a forbidden em-dash appears in a Markdown file.

Contract: Claude Code passes the tool call as JSON on stdin. For PostToolUse, exiting with code 2
surfaces stderr back to Claude as actionable feedback. Any other failure exits 0 so the hook never
blocks unrelated work.
"""

import json
import sys

EM_DASH = "—"


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        # If the payload is unreadable, do not block the tool call.
        return 0

    tool_input = payload.get("tool_input", {}) or {}
    file_path = tool_input.get("file_path", "")

    if not file_path.lower().endswith(".md"):
        return 0

    try:
        with open(file_path, "r", encoding="utf-8") as handle:
            lines = handle.readlines()
    except OSError:
        return 0

    offenders = [str(i + 1) for i, line in enumerate(lines) if EM_DASH in line]
    if not offenders:
        return 0

    sys.stderr.write(
        "House-style violation in {path}: em-dash found on line(s) {lines}. "
        "Replace each em-dash with a comma, period, parenthesis, or colon. "
        "See .claude/rules/house-style.md.\n".format(
            path=file_path, lines=", ".join(offenders)
        )
    )
    return 2


if __name__ == "__main__":
    sys.exit(main())
