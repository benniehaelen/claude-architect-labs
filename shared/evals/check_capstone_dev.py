#!/usr/bin/env python3
"""Eval for the developer-productivity capstone: do the catalog and config hold together?

This scores the composed environment against the properties that define a passing dev setup and
confirms the naive environment compounds the labs' failure modes.

Composed environment (must hold):
- no catalog defects (lab 02) and no config defects (lab 04).
- d1 tests run, d2 source edit is governed on edit, d3 new doc is governed on create.
- d4 unauthorized deploy is escalated and does not run, d5 commit is governed.
- no harm anywhere.

Naive environment (must fail):
- the composed analysis shows ungated dangerous tools and guide-only must-holds with uncovered events.
- d3 new doc is a convention gap (the write-time gap), d4 deploy runs ungated, d5 commit is a gap.

Usage:
    python shared/evals/check_capstone_dev.py
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from shared.harness.catalog import Catalog  # noqa: E402
from shared.harness.config import TeamConfig  # noqa: E402
from shared.harness.dev_environment import DevAction, analyze_environment, drive_session  # noqa: E402
from shared.harness.model import load_session  # noqa: E402


def expect(label: str, condition: bool, results: list) -> None:
    results.append((label, bool(condition)))


def load_design(name: str):
    design = load_session(name)
    catalog = Catalog.from_dict(load_session(design["catalog"]))
    config = TeamConfig.from_dict(load_session(design["config"]))
    return catalog, config


def by_id(actions, catalog, config):
    return {o.action_id: o for o in drive_session(actions, catalog, config)}


def main() -> int:
    results: list = []
    session = load_session("dev_session")
    intents_meta = session["dev_intents_meta"]
    actions = [DevAction(**spec) for spec in session["actions"]]

    good_catalog, good_config = load_design("dev_design_good")
    good_defects = analyze_environment(good_catalog, good_config, intents_meta)
    expect("good: no ungated dangerous tools",
           not good_defects["catalog"]["ungated_dangerous"], results)
    expect("good: no overlapping intents", not good_defects["catalog"]["overlaps"], results)
    expect("good: no guide-only must-hold", not good_defects["config"]["guide_for_must"], results)
    expect("good: no uncovered binding event", not good_defects["config"]["uncovered_binding"], results)

    good = by_id(actions, good_catalog, good_config)
    expect("good: d1 tests run", good["d1"].executed, results)
    expect("good: d2 source edit governed on edit",
           good["d2"].convention_outcome == "governed" and not good["d2"].convention_gap, results)
    expect("good: d3 new doc governed on create",
           good["d3"].convention_outcome == "governed" and not good["d3"].convention_gap, results)
    expect("good: d4 unauthorized deploy is escalated and does not run",
           good["d4"].gate_decision == "escalate" and not good["d4"].executed, results)
    expect("good: d5 commit governed", good["d5"].convention_outcome == "governed", results)
    expect("good: no harm anywhere", not any(o.harm for o in good.values()), results)

    bad_catalog, bad_config = load_design("dev_design_bad")
    bad_defects = analyze_environment(bad_catalog, bad_config, intents_meta)
    expect("bad: has ungated dangerous tools", bool(bad_defects["catalog"]["ungated_dangerous"]), results)
    expect("bad: has guide-only must-hold", bool(bad_defects["config"]["guide_for_must"]), results)
    expect("bad: has uncovered binding event", bool(bad_defects["config"]["uncovered_binding"]), results)

    bad = by_id(actions, bad_catalog, bad_config)
    expect("bad: d3 new doc is a convention gap on create",
           bad["d3"].convention_gap and bad["d3"].harm, results)
    expect("bad: d4 deploy runs ungated", bad["d4"].ungated_dangerous_ran and bad["d4"].harm, results)
    expect("bad: d5 commit is a convention gap", bad["d5"].convention_gap and bad["d5"].harm, results)

    print("Developer-productivity capstone eval")
    passed = 0
    for label, ok_flag in results:
        mark = "PASS" if ok_flag else "FAIL"
        print("  [{0}] {1}".format(mark, label))
        passed += 1 if ok_flag else 0

    print("")
    print("{0} of {1} checks passed".format(passed, len(results)))
    return 0 if passed == len(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
