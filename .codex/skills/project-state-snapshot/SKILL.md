---
name: project-state-snapshot
description: Erzeuge einen Project Snapshot als Markdown und versioniere ihn mit Timestamp; verwenden bei Status-Updates oder Kontextweitergabe an Chatbots.
---

# Skill: project-state-snapshot

## Zweck
Erzeuge einen copy-paste-tauglichen Projektstatus mit Repo-Belegen und versioniere ihn.

## Wann anwenden
- Wenn ein aktueller Status fuer Stakeholder oder Chatbots benoetigt wird.
- Nach groesseren Aenderungen in Anforderungen, Architektur oder Implementierung.

## Vorgehen (Schritt-fuer-Schritt)
1) Scanne zentrale Artefakte: `README.md`, `docs/`, `.github/`, `src/`, `tests/`, `frontend/`.
2) Extrahiere Zweck, Scope, Architektur, Implementierung, Tests, CI/CD, Risiken.
3) Schreibe den Snapshot nach Template.
4) Speichere ihn unter `docs/project_state/YYYY-MM-DD/HHmmss_project_snapshot.md`.
5) Markiere fehlende Infos als "Unbekannt im Repo" und fuehre sie in "To Clarify" auf.

## Lernperspektive
- Warum so? Status-Snapshots machen den Projektstand reproduzierbar.
- Alternativen: informelle Chat-Zusammenfassungen ohne Quellen.
- Warum nicht hier? Ohne Repo-Belege sinkt die Nachvollziehbarkeit.

## Repo-Referenzen
- `docs/project_state/`
- `docs/00_overview/PROJECT_OVERVIEW.md`
- `docs/00_overview/PROJECT_STATE.md`
- `docs/01_requirements/`
- `docs/02_architecture/ADR/`
- `docs/03_quality/QUALITY_GATES.md`
- `docs/04_evaluation/EVALUATION_PLAN.md`

## Qualitaetscheck
- Alle Kernaussagen sind mit Pfaden belegt.
- Snapshot bleibt innerhalb 1-3 Seiten.
- Keine Secrets im Output.
## Phasenbezug
| Phase | Aufgabe | Status |
|-------|---------|--------|
| Phase 5 | Projekt-Status-Snapshot erstellen | offen |