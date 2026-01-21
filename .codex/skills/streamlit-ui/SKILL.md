---
name: streamlit-ui
description: Pflege die Streamlit UI fuer Upload, Analyse und Matching; verwenden bei UI-Aenderungen oder neuen Anzeige-Features.
---

# Skill: streamlit-ui

## Zweck
Stelle eine nachvollziehbare UI fuer Upload, Analyse und Ergebnisdarstellung bereit.

## Wann anwenden
- Wenn neue UI-Features oder Anzeigeformate benoetigt werden.
- Wenn Upload- oder Matching-Interaktionen angepasst werden.

## Vorgehen (Schritt-fuer-Schritt)
1) Lies `frontend/streamlit_app.py` und die relevanten FRs.
2) Implementiere UI-Aenderungen in `frontend/streamlit_app.py`.
3) Pruefe, dass Upload-Validierung und Temp-File-Cleanup erhalten bleiben.
4) Halte Anzeigeformate konsistent mit den Core-Outputs.

## Lernperspektive
- Warum so? Streamlit ermoeglicht schnelle, nachvollziehbare Demos (ADR-001).
- Alternativen: FastAPI + React.
- Warum nicht hier? Hoeherer Setup-Aufwand und weniger Fokus auf Lernziel im MVP.

## Repo-Referenzen
- `frontend/streamlit_app.py`
- `docs/02_architecture/ADR/ADR-001-streamlit-mvp.md`
- `docs/01_requirements/FR.en.md`

## Qualitaetscheck
- Upload-Validierung aktiv.
- UI zeigt Fehler kontrolliert und ohne Crash.
- Keine persistente Speicherung von CV/JD Daten.
## Phasenbezug
| Phase | Aufgabe | Status |
|-------|---------|--------|
| Phase 3 | Streamlit UI fuer Upload/Preview fertigstellen | in Arbeit |