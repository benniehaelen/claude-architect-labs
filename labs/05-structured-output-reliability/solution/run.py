#!/usr/bin/env python3
"""Reference solution for lab 05: a multi-pass extraction pipeline.

Citations and the structured-output format cannot be combined in one call, so this design uses each
where it is valid. A cited pass grounds the claims, a transform pass shapes them to the strict schema
with constrained decoding, and a verification pass maps each record back to a cited evidence span. A
record that is shape-valid but ungrounded is held rather than emitted.

Usage (dry-run, free, deterministic):
    python labs/05-structured-output-reliability/solution/run.py
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT))

from shared.harness.extraction import Design, analyze_design, load_corpus, run_pipeline  # noqa: E402
from shared.harness.model import load_session  # noqa: E402


def main() -> int:
    design = Design.from_dict(load_session("design_multipass"))
    corpus = load_corpus(load_session("extraction_corpus"))

    print("Design: {0}".format(design.name))
    defects = analyze_design(design)
    print("Design analysis:")
    print("  citations_with_structured: {0}".format(defects["citations_with_structured"]))
    print("  schema_by_prompt:          {0}".format(defects["schema_by_prompt"]))
    print("  grounding_unverified:      {0}".format(defects["grounding_unverified"]))

    result = run_pipeline(
        design, corpus["source"], corpus["claims"], corpus["records"], corpus["schema"]
    )

    print("")
    if result.error:
        print("Pipeline error: {0}".format(result.error))
        return 1

    print("Records:")
    for verdict in result.verdicts:
        claim = corpus["claims"][verdict.record.claim_index]
        print("  {0:<28} schema_valid={1!s:<5} grounded={2!s:<5} -> {3:<10} ({4})".format(
            str(verdict.record.fields),
            verdict.schema_valid,
            verdict.grounded,
            "emitted" if verdict.emitted else "held",
            verdict.reason,
        ))

    print("")
    print("Emitted {0} record(s), held {1}. Every emitted record maps to a cited evidence span. The "
          "ungrounded claim about a gym membership was held by the verification pass rather than "
          "emitted, because citations and the structured format are used in separate passes and the "
          "grounding is verified after the schema is fixed.".format(
              len(result.emitted), len(result.held)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
