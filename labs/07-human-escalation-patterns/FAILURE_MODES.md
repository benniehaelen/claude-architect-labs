# Failure modes: lab 07 human escalation patterns

Each failure mode names what goes wrong, how it is detected, and what the reference design does
about it. Run `bad_version/run.py` and `solution/run.py` to see several directly, and
`shared/evals/check_lab07.py` for the assertions.

## Coverage gap: a must-escalate request handled automatically

The triggers do not cover a case that must reach a human, so the agent handles it on its own. In the
weak policy the only trigger is high impact, so the out-of-policy exception and the explicit request
for a human are handled automatically. Detection is the per-request `missed` flag, which marks a
must-escalate request that fired no trigger and was handled. The reference covers out of policy, high
impact, low confidence, and an explicit human request, so every must-escalate case fires a trigger.

## Late escalation: the action runs before the handoff

The policy escalates after acting rather than before, so a high-impact or irreversible action has
already run by the time a human sees the request. In the weak policy the account closure is escalated
post-action. Detection is the `late` flag, which marks an escalation that is post-action on a
high-impact request, and the `post_action_timing` analysis flag. The reference escalates pre-action, so
the action is stopped before it runs.

## Escalation routed nowhere

The policy identifies a request that must escalate but has no route to a human, so the escalation has
nowhere to go. This is the no-route policy in the eval. Detection is the `no_route` analysis flag. The
reference routes to a defined human review queue, so an escalation can be delivered.

## Fail-open default: proceeding when the handoff cannot be delivered

When escalation cannot be delivered, the default decides what happens. A fail-open default proceeds, so
the request is handled as if it had been escalated and resolved. The no-route policy combines no route
with a proceed default, so its correctly identified escalations are dropped and proceed. Detection is
the `dropped` flag and the `fail_open_default` analysis flag. The reference holds rather than proceeds,
so an undeliverable escalation stops the request.

## Over-escalation of routine requests

The opposite error: escalating requests that the agent should handle, which wastes human time and
trains reviewers to ignore the queue. A policy that escalates everything is as poorly designed as one
that escalates nothing. Detection is a routine request (the order-status read) that should be handled
but is escalated. The reference handles the routine read automatically and reserves escalation for the
must-escalate cases. See `../../ENFORCEMENT_LAYER.md` for why the control belongs at the policy layer.
