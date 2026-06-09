# Failure modes: lab 02 tool catalog design

Each failure mode names what goes wrong, how it is detected, and what the reference design does
about it. Run `bad_version/run.py` and `solution/run.py` to see several directly, and
`shared/evals/check_lab02.py` for the assertions.

## Ambiguous selection from overlapping intents

Two or more tools claim the same intent, so the agent has no obvious choice and resolves it
arbitrarily. In the bad catalog the order_status intent matches three tools. Detection is the
`analyze_catalog` overlaps report and the per-request routing status of `ambiguous`. The reference
catalog maps each intent to exactly one tool, so the status is always `ok`.

## Over-privilege from coarse tools

A single tool bundles a benign read with a write or destructive capability, so selecting it for the
benign task hands the agent the dangerous capability too. The bad catalog's `manage_order` serves
order_status, cancel_order, and refund_order at once. Detection is the `coarse` report, which flags
any tool whose intents mix a read with a write or destructive effect. The reference splits each
effect level into its own tool.

## Ungated dangerous tools

A write or destructive tool has no permission gate in front of it, so the control has nothing to
govern and the action runs unconditionally. This is the central defect. In the bad catalog both
dangerous tools are ungated, so every routed request executes without a check. Detection is the
`ungated_dangerous` report. The reference gates every write and destructive tool, which is what
gives the permission control something to act on.

## Mislabeled effect level

A tool declares a lower effect than the intents it actually serves, which hides risk from the gate.
A tool that can close an account but is labeled read would slip past a gate that trusts the label.
Detection is the `mislabeled` report, which compares a tool's declared effect against the maximum
expected effect of its intents. The reference labels each tool at the true effect level of its most
dangerous intent.

## Benign read routing to a destructive-capable tool

A consequence of overlap plus coarseness: a simple status request lands on a tool that can also
destroy. In the bad version the benign order_status request routes to `manage_order` and runs an
ungated destructive-capable tool. Detection is the combination of routing status and the selected
tool's effect. The reference guarantees a read intent routes to a read-effect tool.

## Enforcing safety in the description instead of the gate

A subtler mode, and the Branch B trap the exam angle calls out: writing a strong warning into a
coarse tool's description and treating that as the safeguard. The description is a guide and cannot
stop execution. The reference enforces the high-impact stop in the gate, the control layer, and
uses descriptions only to steer selection. See `../../ENFORCEMENT_LAYER.md`.
