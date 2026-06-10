#!/usr/bin/env python3
"""Reference solution for lab 03: a scoped MCP server.

Route a set of internal-knowledge-assistant and CI/CD requests through the scoped server and the
trust boundary. The server exposes only the operations the agents need, every sensitive operation is
gated, and each operation caps its output below the host limit. A benign read goes straight through,
a legitimate deploy runs only when authorized and confirmed, an unauthorized environment deletion is
escalated rather than executed, and a large export is bounded so it cannot flood context.

Usage (dry-run, free, deterministic):
    python labs/03-mcp-boundaries/solution/run.py
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT))

from shared.harness.mcp import Request, ServerSpec, analyze_server, drive  # noqa: E402
from shared.harness.model import load_session  # noqa: E402


def main() -> int:
    server = ServerSpec.from_dict(load_session("mcp_server_good"))
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
    for outcome in drive(server, requests, limit):
        route = outcome.route
        boundary_decision = outcome.boundary
        decision = boundary_decision.decision if boundary_decision else "no_op"
        reason = boundary_decision.reason if boundary_decision else "unreachable"
        payload = "{0}t{1}".format(
            outcome.returned_tokens, " truncated" if outcome.truncated else "")
        print("  {0} capability={1:<18} -> {2:<18} [{3}] {4} {5} payload={6}".format(
            outcome.request.id,
            outcome.request.capability,
            route.selected.name if route.selected else "(none)",
            route.status,
            decision,
            reason,
            payload,
        ))

    print("")
    print("Every needed capability was reachable and nothing else was exposed. The read passed, the "
          "authorized and confirmed deploy ran, the unauthorized environment deletion was escalated "
          "rather than run, and the large export was bounded to the server cap so it could not flood "
          "context.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
