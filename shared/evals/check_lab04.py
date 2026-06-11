#!/usr/bin/env python3
"""Eval for lab 04: is the team configuration layered so conventions actually hold?

This scores the layered configuration against the properties that define a passing design, and it
confirms the rules-and-memory configuration is genuinely flawed so the contrast is real.

Layered configuration (must hold):
- no must-hold convention is guide-only, no binding event is uncovered, no preference is controlled.
- the new-file event and the edit event for the house-style must-hold are both governed.
- the commit event for the no-secrets must-hold is governed.
- the preference edit is guided, not governed.

Rules-and-memory configuration (must be flawed):
- has a guide-only must-hold, an uncovered binding event, and a controlled preference.
- the new-file event for the house-style must-hold is a silent gap (unenforced).
- the commit event for the no-secrets must-hold is a silent gap (unenforced).

Usage:
    python shared/evals/check_lab04.py
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from shared.harness.config import Event, TeamConfig, analyze_config, drive  # noqa: E402
from shared.harness.model import load_session  # noqa: E402


def expect(label: str, condition: bool, results: list) -> None:
    results.append((label, bool(condition)))


def outcomes_by_id(config: TeamConfig, events):
    return {outcome.event.id: outcome for outcome in drive(config, events)}


def main() -> int:
    results: list = []
    stream = load_session("config_events")
    events = [Event(**spec) for spec in stream["events"]]

    good = TeamConfig.from_dict(load_session("team_config_good"))
    good_defects = analyze_config(good)
    expect("good: no guide-only must-hold", not good_defects["guide_for_must"], results)
    expect("good: no uncovered binding event", not good_defects["uncovered_binding"], results)
    expect("good: no controlled preference", not good_defects["control_for_preference"], results)

    good_by_id = outcomes_by_id(good, events)
    expect("good: e1 new file is governed",
           good_by_id["e1"].outcome == "governed" and not good_by_id["e1"].silent_gap,
           results)
    expect("good: e2 edit is governed", good_by_id["e2"].outcome == "governed", results)
    expect("good: e3 commit is governed",
           good_by_id["e3"].outcome == "governed" and not good_by_id["e3"].silent_gap,
           results)
    expect("good: e4 preference edit is guided, not governed",
           good_by_id["e4"].outcome == "guided",
           results)

    bad = TeamConfig.from_dict(load_session("team_config_bad"))
    bad_defects = analyze_config(bad)
    expect("bad: has a guide-only must-hold", bool(bad_defects["guide_for_must"]), results)
    expect("bad: has an uncovered binding event", bool(bad_defects["uncovered_binding"]), results)
    expect("bad: has a controlled preference", bool(bad_defects["control_for_preference"]), results)

    bad_by_id = outcomes_by_id(bad, events)
    expect("bad: e1 new file is a silent gap (unenforced)",
           bad_by_id["e1"].outcome == "unenforced" and bad_by_id["e1"].silent_gap,
           results)
    expect("bad: e3 commit is a silent gap (unenforced)",
           bad_by_id["e3"].outcome == "unenforced" and bad_by_id["e3"].silent_gap,
           results)

    print("Lab 04 eval")
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
