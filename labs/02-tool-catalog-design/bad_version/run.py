#!/usr/bin/env python3
"""Intentionally flawed version for lab 02: the sprawling tool catalog.

This catalog is the anti-pattern. It runs through the exact same routing and gating engine as the
reference solution (see shared/harness/catalog.py). Nothing about the engine changed. Only the
catalog did, and that is enough to produce three failures:

1. Ambiguous selection. The order_status intent matches three tools, so there is no obvious choice
   and the agent resolves it arbitrarily. A coarse, destructive-capable tool can win a benign read.
2. Ungated dangerous tools. The dangerous tools carry no gate, so the permission control has
   nothing to govern. It can only protect a tool the catalog wired it to.
3. Silent high-impact action. An unauthorized close_account request runs immediately, with no
   authorization, no confirmation, and no escalation. The same request is escalated by the
   reference solution.

Usage:
    python labs/02-tool-catalog-design/bad_version/run.py
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT))

from shared.harness.catalog import Catalog, Request, analyze_catalog, drive  # noqa: E402
from shared.harness.model import load_session  # noqa: E402


def main() -> int:
    catalog = Catalog.from_dict(load_session("support_catalog_bad"))
    routing = load_session("catalog_routing")
    requests = [Request(**spec) for spec in routing["requests"]]

    print("Catalog: {0}".format(catalog.name))
    defects = analyze_catalog(catalog, routing["intents_meta"])
    print("Catalog analysis:")
    print("  overlaps:          {0}".format(defects["overlaps"] or "none"))
    print("  ungated_dangerous: {0}".format(defects["ungated_dangerous"] or "none"))
    print("  coarse:            {0}".format(defects["coarse"] or "none"))
    print("  mislabeled:        {0}".format(defects["mislabeled"] or "none"))

    print("")
    print("Routing:")
    dangerous_silent = []
    for outcome in drive(catalog, requests):
        route = outcome.route
        gate = outcome.gate
        decision = gate.decision if gate else "no_tool"
        reason = gate.reason if gate else "unroutable"
        flag = ""
        if reason == "ungated_dangerous_executed":
            flag = "  <== executed with no gate"
            dangerous_silent.append(outcome.request.id)
        print("  {0} intent={1:<14} -> {2:<16} [{3}] {4} {5}{6}".format(
            outcome.request.id,
            outcome.request.intent,
            route.selected.name if route.selected else "(none)",
            route.status,
            decision,
            reason,
            flag,
        ))

    print("")
    print("Requests that ran a dangerous tool with no gate: {0}".format(dangerous_silent or "none"))
    print("On the bad catalog, the unauthorized close_account ran silently. The gate never saw it, "
          "because the catalog never put a gate in front of the tool.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
