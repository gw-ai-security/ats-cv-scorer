# ADR-004: Reporting and Export Formats (PDF/JSON/MD)

## Status
Accepted (vNext)

## Context
The project requires explainable reports that are readable without the UI and exportable in machine-friendly formats. Reports must be consistent with the Explainable Scoring Spec and usable for audit/portfolio review.

## Decision
- A single report payload schema is generated and exported to:
  - PDF (human-friendly)
  - JSON (machine-friendly)
  - Markdown (review-friendly)
- The report includes: meta, executive summary, score breakdown, matched skills + evidence, missing requirements, and parsing warnings.
- The Streamlit UI exposes download buttons for all three formats.

## Consequences
- Reporting logic is centralized in `src/core/report_export.py`.
- PDF layout templates align with JSON/MD content.
- Any scoring change must update the report payload to keep exports consistent.

## References
- `src/core/report_export.py`
- `src/core/pdf_layout.py`
- `src/core/templates/score_report.txt.j2`
- `docs/03_quality/EXPLAINABLE_SCORING_SPEC.md`
