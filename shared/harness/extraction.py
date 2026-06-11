"""Structured-output extraction primitives for lab 05.

A pipeline turns unstructured input into machine-readable records that a downstream system parses,
and the records must be grounded in the source. The naive design asks for citations and the
structured-output format in the same call, which returns a 400 because the two are incompatible
(dated and sourced in VERIFIED.md). Citations interleave citation blocks with text, and that
conflicts with the strict JSON schema constraints of the structured-output format.

This module models the two reliability concerns the lab separates and the multi-pass pattern that
satisfies both:

- Schema shape is governed by constrained decoding (the structured-output format). When a pass uses
  it, the record is shape-valid by construction. When shape is left to a prompt instruction, a record
  can drift.
- Grounding is governed by a verification pass that maps each structured claim back to a cited
  evidence span. A claim with no evidence in the source is held, not emitted.

The decisive insight, visible in the runners, is that the single-call design and the multi-pass
design run through the exact same engine. Only the design differs. When two real features conflict,
the answer is the multi-pass pattern that uses each where it is valid, not a fabricated flag that
pretends the conflict away.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


class CitationsStructuredConflictError(Exception):
    """Raised when a design combines citations and the structured-output format in one call.

    This models the real 400. The structured-output beta header and constrained decoding cannot be
    combined with citations in a single request (see VERIFIED.md).
    """


@dataclass
class Schema:
    required: List[str]

    def validate(self, fields: Dict[str, Any]) -> bool:
        return all(
            key in fields and isinstance(fields[key], str) and fields[key].strip()
            for key in self.required
        )


@dataclass
class Source:
    doc_id: str
    spans: Dict[str, str]

    def has(self, span_id: Optional[str]) -> bool:
        return span_id is not None and span_id in self.spans


@dataclass
class Claim:
    text: str
    evidence: Optional[str]  # a span id in the source, or None when the claim is ungrounded


@dataclass
class Record:
    fields: Dict[str, str]
    claim_index: int


@dataclass
class Verdict:
    record: Record
    schema_valid: bool
    grounded: bool
    emitted: bool
    reason: str


@dataclass
class PipelineResult:
    error: Optional[str]
    verdicts: List[Verdict] = field(default_factory=list)
    emitted: List[Record] = field(default_factory=list)
    held: List[Record] = field(default_factory=list)


@dataclass
class Design:
    name: str
    single_call: bool  # combines citations and the structured-output format in one request
    requests_citations: bool
    requests_structured_format: bool
    schema_enforcement: str  # "constrained", "prompt", or "none"
    grounding: str  # "verified", "prompt", or "none"

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Design":
        return cls(**data)


def analyze_design(design: Design) -> Dict[str, Any]:
    """Score a design. A sound design returns False for every defect.

    Defects detected:
    - citations_with_structured: the design combines citations and the structured-output format in a
      single call, which returns a 400.
    - schema_by_prompt: the schema shape is left to a prompt instruction rather than constrained
      decoding, so a record can drift out of shape.
    - grounding_unverified: grounding is left to a prompt or skipped, with no verification pass, so an
      ungrounded claim can be emitted.
    """
    return {
        "citations_with_structured": (
            design.single_call
            and design.requests_citations
            and design.requests_structured_format
        ),
        "schema_by_prompt": design.schema_enforcement == "prompt",
        "grounding_unverified": design.grounding != "verified",
    }


def run_pipeline(
    design: Design,
    source: Source,
    claims: List[Claim],
    records: List[Record],
    schema: Schema,
) -> PipelineResult:
    """Run one design over a cited pass and a transform pass, then verify.

    The single-call design raises the 400 and emits nothing. Otherwise the transform-pass records are
    checked: schema shape is trusted when constrained decoding produced it and validated otherwise,
    and grounding is verified against the source only when the design includes a verification pass. A
    record that is shape-valid but ungrounded is held when grounding is verified and slips through when
    it is not.
    """
    if design.single_call and design.requests_citations and design.requests_structured_format:
        return PipelineResult(error="400 citations_and_structured_output_incompatible")

    verdicts: List[Verdict] = []
    for record in records:
        claim = claims[record.claim_index]
        if design.schema_enforcement == "constrained":
            schema_valid = True  # constrained decoding guarantees the shape
        else:
            schema_valid = schema.validate(record.fields)

        grounded = source.has(claim.evidence)

        if design.grounding == "verified":
            emitted = schema_valid and grounded
            if emitted:
                reason = "emitted"
            elif not schema_valid:
                reason = "schema_invalid"
            else:
                reason = "ungrounded_held"
        else:
            # No verification pass: grounding is not checked, so an ungrounded record is emitted.
            emitted = schema_valid
            reason = "emitted_unverified" if emitted else "schema_invalid"

        verdicts.append(Verdict(record, schema_valid, grounded, emitted, reason))

    emitted_records = [verdict.record for verdict in verdicts if verdict.emitted]
    held_records = [verdict.record for verdict in verdicts if not verdict.emitted]
    return PipelineResult(None, verdicts, emitted_records, held_records)


def load_corpus(data: Dict[str, Any]) -> Dict[str, Any]:
    """Build the source, scripted pass outputs, and schema from a corpus fixture."""
    source = Source(doc_id=data["doc_id"], spans=data["spans"])
    claims = [Claim(**spec) for spec in data["claims"]]
    records = [Record(**spec) for spec in data["records"]]
    schema = Schema(required=data["schema"]["required"])
    return {"source": source, "claims": claims, "records": records, "schema": schema}
