# PDF Report Layout Guidelines (DE)

## Zweck
PDF-Outputs strukturiert, lesbar und druckbar machen (ohne UI).

## Pflichtsektionen
1) Meta Info (Timestamp, Strategy, Dataset, Kandidat, JD-Rolle)
2) Executive Summary (Score + Verdict)
3) Score Breakdown (Komponenten + Penalties)
4) Matched Skills + Evidence (Top Skills mit Evidence Snippets)
5) Missing Required + Suggestions
6) Parsing Notes / Warnings

## Implementierung
- Layout-Renderer: `src/core/pdf_layout.py`
- Template: `src/core/templates/score_report.txt.j2`
- Export-Schema: `src/core/report_export.py` (JSON + Markdown)
- UI-Integration: `frontend/streamlit_app.py` (PDF/JSON/MD Downloads)
- Reportlab mit Seitenumbruechen.

## Explainability Anforderungen
- Komponenten-Scores und Penalties immer anzeigen.
- Missing Required Skills explizit hervorheben.
- Evidence Snippets fuer Matched Skills bereitstellen.
- Sections klar trennen fuer Druckbarkeit.

## Verweise
- `docs/03_quality/EXPLAINABLE_SCORING_SPEC.md`
- `src/core/pdf_layout.py`
- `src/core/templates/score_report.txt.j2`

## Last Updated
2026-01-21 16:32:30 (Local)
