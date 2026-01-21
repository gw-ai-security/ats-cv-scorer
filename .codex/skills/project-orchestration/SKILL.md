---
name: project-orchestration
description: Orchestriere Skills entlang der Projektphasen; verwenden, um die aktive Phase zu bestimmen und die richtigen Skills in Reihenfolge auszufuehren.
---

# Skill: project-orchestration

## Zweck
Koordiniere Skills pro Projektphase und stelle Reihenfolge und Abhaengigkeiten sicher.

## Wann anwenden
- Wenn der aktuelle Projektstand bewertet oder ein naechster Arbeitslauf geplant wird.
- Wenn Skill-Reihenfolge oder Abhaengigkeiten geprueft werden sollen.

## Vorgehen (Schritt-fuer-Schritt)
1) Ermittle die aktive Phase anhand von `docs/00_overview/PROJECT_STATE.md` und dem neuesten Snapshot in `docs/project_state/`.
2) Waehle die Skills fuer diese Phase gemaess Liste unten.
3) Fuehre Skills in der angegebenen Reihenfolge aus.
4) Aktualisiere Status-Dokumente, wenn Aufgaben abgeschlossen wurden.

## Aktive Skills pro Phase
- Phase 0: requirements-traceability, architecture-adr
- Phase 1: requirements-traceability, testing-quality-gates, evaluation-plan
- Phase 2: architecture-adr
- Phase 3: pdf-processing, cv-structure-analysis, skill-extraction, ats-criteria-extraction, jd-parsing, matching-baseline, streamlit-ui
- Phase 4: testing-quality-gates, evaluation-plan
- Phase 5: project-state-snapshot, project-phase-planner

## Abhaengigkeiten
- Traceability setzt stabile Anforderungen voraus.
- Matching setzt ATS- und JD-Extraktion voraus.
- Evaluation setzt definierte NFRs und Metriken voraus.

## Lernperspektive
- Warum so? Orchestrierung verhindert Phasen-Spruenge und inkonsistente Artefakte.
- Alternativen: ad-hoc Ausfuehrung einzelner Skills.
- Warum nicht hier? Ohne Orchestrierung gehen Kontext und Nachweise verloren.

## Repo-Referenzen
- `docs/00_overview/PROJECT_STATE.md`
- `docs/project_state/`
- `docs/codex_skills/OVERVIEW.md`

## Qualitaetscheck
- Aktive Phase ist klar begruendet.
- Skill-Reihenfolge deckt Abhaengigkeiten ab.
- Keine Skills ohne Phasenbezug.

## Phasenbezug
| Phase | Aufgabe | Status |
|-------|---------|--------|
| Phase 5 | Skills orchestrieren und Projektabschluss vorbereiten | offen |