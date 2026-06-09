#!/usr/bin/env python3
"""Reference solution for lab 02: a deliberate tool catalog.

Route a set of support requests through the well-designed catalog and gate. Each intent maps to
exactly one tool, dangerous tools are gated, and the permission gate governs execution. A benign
read goes straight through, a legitimate write runs only when authorized and confirmed, and an
unauthorized high-impact action is escalated rather than executed.

Usage (dry-run, free, deterministic):
    python labs/02-tool-catalog-design/solution/run.py
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT))

from shared.harness.catalog import Catalog, Request, analyze_catalog, drive  # noqa: E402
from shared.harness.model import load_session  # noqa: E402


def main() -> int:
    catalog = Catalog.from_dict(load_session("support_catalog_good"))
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
    for outcome in drive(catalog, requests):
        route = outcome.route
        gate = outcome.gate
        decision = gate.decision if gate else "no_tool"
        reason = gate.reason if gate else "unroutable"
        print("  {0} intent={1:<14} -> {2:<16} [{3}] {4} {5}".format(
            outcome.request.id,
            outcome.request.intent,
            route.selected.name if route.selected else "(none)",
            route.status,
            decision,
            reason,
        ))

    print("")
    print("Every intent had exactly one obvious tool. The read passed, the authorized and "
          "confirmed write executed, the unconfirmed write was blocked, and the unauthorized "
          "destructive action was escalated rather than run.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
