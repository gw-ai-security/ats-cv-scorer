---
name: requirements-traceability
description: Pflege Functional/Non-Functional Requirements und Traceability fuer ATS CV Scorer; verwenden bei Aenderungen an Anforderungen, Prioritaeten, Status, Akzeptanzkriterien oder Mapping zu Code/Tests.
---

# Skill: requirements-traceability

## Zweck
Sichere, dass Anforderungen, Status und Traceability konsistent, pruefbar und repo-basiert bleiben.

## Wann anwenden
- Wenn neue Anforderungen entstehen oder bestehende angepasst werden.
- Wenn Implementierungen oder Tests hinzugekommen sind und das Mapping aktualisiert werden muss.

## Vorgehen (Schritt-fuer-Schritt)
1) Lies die vorhandenen Anforderungen und den Status.
2) Aktualisiere FR/NFR mit klaren Akzeptanzkriterien und Status.
3) Aktualisiere die Traceability-Matrix mit Pfaden zu `src/` und `tests/`.
4) Pruefe, ob `docs/00_overview/PROJECT_STATE.md` den Status widerspiegelt; bei Abweichungen markieren.

## Lernperspektive
- Warum so? Requirements und Traceability machen Entscheidungen und Umsetzung auditierbar.
- Alternativen: reine Issue-Tracker oder lose Notizen.
- Warum nicht hier? Reine Tickets sind ohne Repo-Beleg schwer nachvollziehbar und brechen die Nachweis-Kette.

## Repo-Referenzen
- `docs/01_requirements/FR.en.md`
- `docs/01_requirements/FR.de.md`
- `docs/01_requirements/NFR.en.md`
- `docs/01_requirements/NFR.de.md`
- `docs/01_requirements/TRACEABILITY.en.md`
- `docs/01_requirements/TRACEABILITY.de.md`
- `docs/00_overview/PROJECT_STATE.md`

## Qualitaetscheck
- Jede Anforderung hat Akzeptanzkriterien und Status.
- Traceability verweist auf existierende Pfade in `src/` und `tests/`.
- Keine Annahmen ohne Repo-Beleg.
## Phasenbezug
| Phase | Aufgabe | Status |
|-------|---------|--------|
| Phase 1 | FR/NFR und Traceability pflegen | erledigt |