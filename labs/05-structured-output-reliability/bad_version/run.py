#!/usr/bin/env python3
"""Intentionally flawed version for lab 05: the single-call extraction.

This design is the anti-pattern. It runs through the exact same engine as the reference solution
(see shared/harness/extraction.py). Nothing about the engine changed. Only the design did, and that
is enough to fail completely:

The design asks for citations and the structured-output format in the same call, to get grounding
and a machine-readable shape in one request. The two are incompatible and the call returns a 400
(see VERIFIED.md), so the pipeline emits nothing. No fabricated flag combines them. The fix is the
multi-pass design that uses each feature where it is valid.

Usage:
    python labs/05-structured-output-reliability/bad_version/run.py
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT))

from shared.harness.extraction import Design, analyze_design, load_corpus, run_pipeline  # noqa: E402
from shared.harness.model import load_session  # noqa: E402


def main() -> int:
    design = Design.from_dict(load_session("design_single_call"))
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
        print("Pipeline error: {0}  <== single call combined citations and the structured format".format(
            result.error))
        print("")
        print("Emitted 0 records. The single call asked for citations and the structured-output "
              "format together, which returns a 400. Grounding and a strict schema cannot be had in "
              "one pass, so this design produces nothing the downstream system can use.")
        return 0

    print("Unexpected success: the single-call design should have returned a 400.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
