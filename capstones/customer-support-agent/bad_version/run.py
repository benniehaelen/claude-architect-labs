#!/usr/bin/env python3
"""Intentionally flawed version for the customer support capstone: the naive composition.

This design composes the three labs' failure modes instead of their lessons. It uses the sprawling,
ungated catalog (lab 02 bad), the weak escalation policy that escalates after acting and covers only
high impact (lab 07 bad), and it runs with no observability (lab 01 bad). It uses the exact same
engine as the reference solution (see shared/harness/support_agent.py). Only the design differs, and
that is enough to compound into a system failure:

1. The unauthorized account closure executes before any escalation, because the catalog is ungated
   and the policy escalates after the action.
2. The explicit request for a human is missed, because the weak policy does not cover that case, and
   it routes to a destructive-capable tool that runs ungated.
3. Nothing is recorded, so the run cannot be audited after the fact.

Usage:
    python capstones/customer-support-agent/bad_version/run.py
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
    design = load_session("support_design_bad")
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
    harms = []
    for o in drive_session(requests, catalog, policy, observable):
        tool = o.executed_tool or "-"
        flag = ""
        if o.harm:
            flag = "  <== must-escalate action executed without a human"
            harms.append(o.request_id)
        elif o.missed_escalation:
            flag = "  <== escalation missed"
        elif o.late_escalation:
            flag = "  <== escalated after the action"
        print("  {0} {1:<10} tool={2:<18} escalated_before={3!s:<5} harm={4!s:<5} trace={5}{6}".format(
            o.request_id, o.status, tool, o.escalated_before_action, o.harm, len(o.trace), flag))

    print("")
    print("Harmful outcomes: {0}".format(harms or "none"))
    print("On the naive composition, the unauthorized account closure executed before any escalation "
          "and the explicit request for a human was missed and routed to a destructive-capable tool, "
          "with no trace to audit. The three labs' failures compounded into one system failure.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
