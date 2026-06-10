#!/usr/bin/env python3
"""Intentionally flawed version for lab 03: the over-exposed MCP server.

This server is the anti-pattern. It runs through the exact same boundary engine as the reference
solution (see shared/harness/mcp.py). Nothing about the engine changed. Only the server spec did,
and that is enough to produce four failures:

1. Over-exposure. The server publishes a raw SQL tool and a secrets-listing resource the agents
   never need, widening the surface for no benefit.
2. Ungated sensitive operations. The deploy and the environment deletion carry no gate, so the
   boundary has nothing to govern. It can only protect an operation the server placed it on.
3. Mislabeled effect. The raw SQL tool is published as a read while arbitrary SQL is destructive,
   so it would slip past a gate that trusts the label.
4. Unbounded payload. The bulk export raises its own ceiling past the host output limit, so a
   single call floods context. The same export is bounded by the reference solution.

Usage:
    python labs/03-mcp-boundaries/bad_version/run.py
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT))

from shared.harness.mcp import Request, ServerSpec, analyze_server, drive  # noqa: E402
from shared.harness.model import load_session  # noqa: E402


def main() -> int:
    server = ServerSpec.from_dict(load_session("mcp_server_bad"))
    boundary = load_session("mcp_boundary")
    limit = boundary["output_token_limit"]
    requests = [Request(**spec) for spec in boundary["requests"]]

    print("Server: {0}".format(server.name))
    print("Host output limit: {0} tokens (warns past {1})".format(
        limit, boundary["warning_threshold"]))
    defects = analyze_server(server, boundary["needed_capabilities"], boundary["ops_meta"], limit)
    print("Boundary analysis:")
    print("  over_exposed:      {0}".format(defects["over_exposed"] or "none"))
    print("  ungated_sensitive: {0}".format(defects["ungated_sensitive"] or "none"))
    print("  unbounded:         {0}".format(defects["unbounded"] or "none"))
    print("  mislabeled:        {0}".format(defects["mislabeled"] or "none"))

    print("")
    print("Requests:")
    sensitive_silent = []
    flooded_context = []
    for outcome in drive(server, requests, limit):
        route = outcome.route
        boundary_decision = outcome.boundary
        decision = boundary_decision.decision if boundary_decision else "no_op"
        reason = boundary_decision.reason if boundary_decision else "unreachable"
        flag = ""
        if reason == "ungated_sensitive_executed":
            flag = "  <== executed with no gate"
            sensitive_silent.append(outcome.request.id)
        if outcome.flooded:
            flag = "  <== flooded context"
            flooded_context.append(outcome.request.id)
        payload = "{0}t{1}".format(
            outcome.returned_tokens, " truncated" if outcome.truncated else "")
        print("  {0} capability={1:<18} -> {2:<18} [{3}] {4} {5} payload={6}{7}".format(
            outcome.request.id,
            outcome.request.capability,
            route.selected.name if route.selected else "(none)",
            route.status,
            decision,
            reason,
            payload,
            flag,
        ))

    print("")
    print("Requests that ran a sensitive operation with no gate: {0}".format(
        sensitive_silent or "none"))
    print("Requests that flooded context: {0}".format(flooded_context or "none"))
    print("On the over-exposed server, the unauthorized environment deletion ran silently and the "
          "bulk export flooded context. The boundary never saw the deletion as a gated action, and "
          "the server raised its own output ceiling past the host limit.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
