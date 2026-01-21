---
name: master-orchestration
description: Orchestriere Rollen, Skills und Aufgaben entlang der Projektphasen; verwenden fuer Phasenbestimmung und Skill-Reihenfolge.
---

# Skill: master-orchestration

## Zweck
Steuere den Projektablauf ueber Phasen, Rollen und Skill-Reihenfolgen.

## Wann anwenden
- Vor jedem Arbeitslauf.
- Bei Phasenwechsel oder Status-Updates.

## Vorgehen (Schritt-fuer-Schritt)
1) Ermittle aktive Phase aus `docs/codex_skills/PHASE_PLAN.md` und `docs/00_overview/PROJECT_STATE.md`.
2) Waehle Skills gemaess Phase.
3) Fuehre Skills in Abhaengigkeitsreihenfolge aus.
4) Aktualisiere Status und Snapshots.

## Aktive Skills pro Phase
- Phase 0: requirements-traceability, architecture-adr, project-phase-planner
- Phase 1: requirements-traceability, testing-quality-gates, evaluation-plan, knowledge-base
- Phase 2: architecture-adr
- Phase 3: pdf-processing, cv-structure-analysis, skill-extraction, ats-criteria-extraction, jd-parsing, matching-baseline, streamlit-ui
- Phase 4: testing-quality-gates, evaluation-plan
- Phase 5: project-state-snapshot, project-phase-planner, knowledge-base

## Lernperspektive
- Warum so? Orchestrierung macht Fortschritt messbar und verhindert Phasen-Spruenge.
- Alternativen: ad-hoc Arbeit ohne Phasenbezug.
- Warum nicht hier? Ohne Orchestrierung entstehen Inkonsistenzen.

## Repo-Referenzen
- `docs/codex_skills/PHASE_PLAN.md`
- `docs/codex_skills/OVERVIEW.md`
- `.codex/skills/`

## Qualitaetscheck
- Phase ist begruendet.
- Skill-Reihenfolge deckt Abhaengigkeiten ab.
- Statusupdates sind dokumentiert.