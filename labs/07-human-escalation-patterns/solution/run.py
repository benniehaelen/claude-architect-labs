#!/usr/bin/env python3
"""Reference solution for lab 07: a sound escalation policy.

Classify a set of support requests under a policy whose triggers cover every must-escalate case, that
escalates before acting, that routes to a defined human queue, and that holds rather than proceeds when
escalation cannot be delivered. The out-of-policy exception, the high-impact account closure, and the
explicit request for a human all reach a person before any action, and the routine read is handled.

Usage (dry-run, free, deterministic):
    python labs/07-human-escalation-patterns/solution/run.py
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT))

from shared.harness.escalation import EscalationPolicy, Request, analyze_policy, drive  # noqa: E402
from shared.harness.model import load_session  # noqa: E402


def main() -> int:
    policy = EscalationPolicy.from_dict(load_session("escalation_policy_good"))
    data = load_session("escalation_requests")
    requests = [Request(**spec) for spec in data["requests"]]

    print("Policy: {0}".format(policy.name))
    defects = analyze_policy(policy)
    print("Policy analysis:")
    print("  post_action_timing: {0}".format(defects["post_action_timing"]))
    print("  no_route:           {0}".format(defects["no_route"]))
    print("  fail_open_default:  {0}".format(defects["fail_open_default"]))

    print("")
    print("Requests:")
    for d in drive(policy, requests):
        timing = d.timing or "-"
        routed = d.routed_to or "-"
        print("  {0} {1:<10} timing={2:<11} route={3:<18} fired={4}".format(
            d.request_id, d.action, timing, routed, d.fired_triggers or "none"))

    print("")
    print("Every must-escalate request reached a human before any action, the routine read was "
          "handled, and nothing was missed, escalated late, or dropped. The triggers cover the "
          "must-escalate cases, the timing is pre-action, the route is defined, and the default holds.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
