#!/usr/bin/env python3
"""Reference solution for the customer support capstone: the composed design.

Drive a customer support session through a design that composes the three labs correctly: an
observable flow (lab 01), the deliberate catalog and permission gate (lab 02), and the sound
escalation policy (lab 07). The routine read is handled, the authorized and confirmed cancel is
governed by the gate rather than escalated, the unauthorized account closure is escalated before any
action, and the explicit request for a human is escalated. Every request leaves an auditable trace.

Usage (dry-run, free, deterministic):
    python capstones/customer-support-agent/solution/run.py
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT))

from shared.harness.catalog import Catalog  # noqa: E402
from shared.harness.escalation import EscalationPolicy  # noqa: E402
from shared.harness.model import load_session  # noqa: E402
from shared.harness.support_agent import SupportRequest, analyze_design, drive_session  # noqa: E402


def main() -> int:
    design = load_session("support_design_good")
    catalog = Catalog.from_dict(load_session(design["catalog"]))
    policy = EscalationPolicy.from_dict(load_session(design["policy"]))
    observable = design["observable"]
    intents_meta = load_session("catalog_routing")["intents_meta"]
    requests = [SupportRequest(**spec) for spec in load_session("support_session")["requests"]]

    print("Design: {0}".format(design["name"]))
    defects = analyze_design(catalog, policy, observable, intents_meta)
    print("Composed analysis:")
    print("  catalog.ungated_dangerous: {0}".format(defects["catalog"]["ungated_dangerous"] or "none"))
    print("  catalog.overlaps:          {0}".format(list(defects["catalog"]["overlaps"]) or "none"))
    print("  policy.post_action_timing: {0}".format(defects["policy"]["post_action_timing"]))
    print("  policy.no_route:           {0}".format(defects["policy"]["no_route"]))
    print("  observable:                {0}".format(defects["observable"]))

    print("")
    print("Requests:")
    for o in drive_session(requests, catalog, policy, observable):
        tool = o.executed_tool or "-"
        print("  {0} {1:<10} tool={2:<18} escalated_before={3!s:<5} harm={4!s:<5} trace={5}".format(
            o.request_id, o.status, tool, o.escalated_before_action, o.harm, len(o.trace)))

    print("")
    print("The routine read was handled, the authorized and confirmed cancel was governed by the gate, "
          "the unauthorized account closure was escalated before any action, and the explicit request "
          "for a human was escalated. No harm, and every request left an auditable trace.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
