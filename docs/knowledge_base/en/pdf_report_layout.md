# PDF Report Layout Guidelines (EN)

## Purpose
Ensure PDF outputs are structured, readable, and printable without the UI.

## Required Sections
1) Meta Info (timestamp, strategy, dataset, candidate, JD role)
2) Executive Summary (score + verdict)
3) Score Breakdown (components + penalties)
4) Matched Skills + Evidence (top skills with evidence snippets)
5) Missing Required + Suggestions
6) Parsing Notes / Warnings

## Implementation
- Layout renderer: `src/core/pdf_layout.py`
- Template: `src/core/templates/score_report.txt.j2`
- Export schema: `src/core/report_export.py` (JSON + Markdown)
- UI integration: `frontend/streamlit_app.py` (PDF/JSON/MD downloads)
- Uses reportlab with page-safe line wrapping.

## Explainability Requirements
- Always display component scores and penalties.
- Highlight missing required skills explicitly.
- Include evidence snippets for matched skills where possible.
- Keep sections separated for print readability.

## References
- `docs/03_quality/EXPLAINABLE_SCORING_SPEC.md`
- `src/core/pdf_layout.py`
- `src/core/templates/score_report.txt.j2`

## Last Updated
2026-01-21 16:32:30 (Local)
