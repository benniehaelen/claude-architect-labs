#!/usr/bin/env python3
"""Eval for lab 05: does the pipeline produce grounded, schema-valid records?

This scores the multi-pass design against the properties that define a passing pipeline, confirms the
single-call design genuinely fails with the 400, and confirms a prompt-only design is weaker because
it emits an ungrounded record.

Multi-pass design (must hold):
- no design defects (no citations-with-structured, no schema-by-prompt, no unverified grounding).
- emits the two grounded records and holds the one ungrounded record.
- every emitted record is grounded.

Single-call design (must fail):
- the analyzer flags citations-with-structured.
- the pipeline returns the 400 and emits nothing.

Prompt-only design (must be weaker):
- the analyzer flags schema-by-prompt and unverified grounding.
- with no verification pass it emits the ungrounded record.

Usage:
    python shared/evals/check_lab05.py
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from shared.harness.extraction import Design, analyze_design, load_corpus, run_pipeline  # noqa: E402
from shared.harness.model import load_session  # noqa: E402


def expect(label: str, condition: bool, results: list) -> None:
    results.append((label, bool(condition)))


def main() -> int:
    results: list = []
    corpus = load_corpus(load_session("extraction_corpus"))

    def run(design):
        return run_pipeline(
            design, corpus["source"], corpus["claims"], corpus["records"], corpus["schema"]
        )

    good = Design.from_dict(load_session("design_multipass"))
    good_defects = analyze_design(good)
    expect("good: no citations-with-structured defect", not good_defects["citations_with_structured"], results)
    expect("good: no schema-by-prompt defect", not good_defects["schema_by_prompt"], results)
    expect("good: no unverified-grounding defect", not good_defects["grounding_unverified"], results)

    good_result = run(good)
    expect("good: pipeline runs without error", good_result.error is None, results)
    expect("good: emits exactly the two grounded records", len(good_result.emitted) == 2, results)
    expect("good: holds the one ungrounded record", len(good_result.held) == 1, results)
    expect("good: every emitted record is grounded",
           all(v.grounded for v in good_result.verdicts if v.emitted),
           results)
    expect("good: the ungrounded record is held with reason ungrounded_held",
           any(v.reason == "ungrounded_held" for v in good_result.verdicts),
           results)

    bad = Design.from_dict(load_session("design_single_call"))
    bad_defects = analyze_design(bad)
    expect("bad: analyzer flags citations-with-structured", bad_defects["citations_with_structured"], results)
    bad_result = run(bad)
    expect("bad: pipeline returns the 400", bad_result.error is not None, results)
    expect("bad: emits nothing", len(bad_result.emitted) == 0, results)

    weak = Design.from_dict(load_session("design_prompt_only"))
    weak_defects = analyze_design(weak)
    expect("weak: analyzer flags schema-by-prompt", weak_defects["schema_by_prompt"], results)
    expect("weak: analyzer flags unverified grounding", weak_defects["grounding_unverified"], results)
    weak_result = run(weak)
    expect("weak: emits the ungrounded record without a verification pass",
           len(weak_result.emitted) == 3
           and any((not v.grounded) and v.emitted for v in weak_result.verdicts),
           results)

    print("Lab 05 eval")
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
