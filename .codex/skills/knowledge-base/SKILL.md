---
name: knowledge-base
description: Pflege die zweisprachige Knowledge Base (DE/EN) fuer ATS CV Scorer; verwenden nach Updates an Requirements, Architektur, Quality, Evaluation, Skills, Phasenplan oder Snapshots.
---

# Skill: knowledge-base

## Zweck
Halte die Knowledge Base aktuell und konsistent (DE/EN gespiegelt).

## Wann anwenden
- Nach jedem neuen Project Snapshot.
- Nach Aenderungen in `docs/01_requirements/`, `docs/02_architecture/`, `docs/03_quality/`, `docs/04_evaluation/`.
- Nach Updates an Skills oder Phasenplan.

## Vorgehen (Schritt-fuer-Schritt)
1) Lies den neuesten Snapshot unter `docs/project_state/`.
2) Aktualisiere die Seiten unter `docs/knowledge_base/de/` und `docs/knowledge_base/en/` spiegelgleich.
3) Verlinke Repo-Artefakte, dupliziere keine Inhalte.
4) Aktualisiere `Last Updated` je Seite.
5) Pruefe Navigation in beiden `INDEX.md`.

## Lernperspektive
- Warum so? Eine KB reduziert Kontextverlust zwischen Sessions.
- Alternativen: verstreute Doku ohne zentrale Verlinkung.
- Warum nicht hier? Ohne zentrale KB ist der Projektstand schwer auditierbar.

## Repo-Referenzen
- `docs/knowledge_base/`
- `docs/project_state/`
- `docs/codex_skills/PHASE_PLAN.md`
- `docs/codex_skills/OVERVIEW.md`

## Qualitaetscheck
- DE/EN Struktur ist identisch.
- Jede Seite hat Zweck, Kerninhalt, Verweise, Last Updated.
- Keine unbelegten Annahmen.