#!/usr/bin/env python3
"""Intentionally flawed version for lab 07: the weak escalation policy.

This policy is the anti-pattern. It runs through the exact same engine as the reference solution (see
shared/harness/escalation.py). Nothing about the engine changed. Only the policy did, and that is
enough to produce three failures:

1. Coverage gap. The only trigger is high impact, so an out-of-policy exception and an explicit request
   for a human are handled automatically instead of escalated. A must-escalate request is silently
   missed.
2. Late escalation. The policy escalates after acting, so the high-impact account closure runs before
   a human ever sees it.
3. Fail-open default. The default is to proceed, so any escalation that could not be delivered would
   proceed as if it had been handled.

Usage:
    python labs/07-human-escalation-patterns/bad_version/run.py
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT))

from shared.harness.escalation import EscalationPolicy, Request, analyze_policy, drive  # noqa: E402
from shared.harness.model import load_session  # noqa: E402


def main() -> int:
    policy = EscalationPolicy.from_dict(load_session("escalation_policy_bad"))
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
    missed = []
    late = []
    for d in drive(policy, requests):
        timing = d.timing or "-"
        routed = d.routed_to or "-"
        flag = ""
        if d.missed:
            flag = "  <== must escalate, handled automatically"
            missed.append(d.request_id)
        if d.late:
            flag = "  <== high-impact action ran before escalation"
            late.append(d.request_id)
        print("  {0} {1:<10} timing={2:<11} route={3:<18} fired={4}{5}".format(
            d.request_id, d.action, timing, routed, d.fired_triggers or "none", flag))

    print("")
    print("Silently missed escalations: {0}".format(missed or "none"))
    print("Late escalations (action ran first): {0}".format(late or "none"))
    print("The weak policy handled an out-of-policy exception and an explicit human request without "
          "escalating, and it closed an account before a human saw the request. The triggers do not "
          "cover the must-escalate cases and the timing is after the fact.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
