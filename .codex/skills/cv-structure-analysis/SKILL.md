---
name: cv-structure-analysis
description: Pflege die CV-Strukturanalyse (Abschnitte und Header-Erkennung); verwenden bei Erweiterungen der Abschnittslogik oder Sprachabdeckung.
---

# Skill: cv-structure-analysis

## Zweck
Erkenne CV-Abschnitte stabil und nachvollziehbar fuer weitere Analyseschritte.

## Wann anwenden
- Wenn neue Abschnittstypen oder Header-Muster benoetigt werden.
- Wenn DE/EN-Abdeckung verbessert werden soll.

## Vorgehen (Schritt-fuer-Schritt)
1) Lies FR-003 und bestehende Tests.
2) Aktualisiere `src/core/cv_analyzer.py`.
3) Ergaenze oder passe Tests in `tests/unit/test_cv_sections.py` an.
4) Verifiziere, dass leere oder fehlende Abschnitte sauber behandelt werden.

## Lernperspektive
- Warum so? Regelbasierte Strukturanalyse bleibt erklaerbar und reproduzierbar.
- Alternativen: ML-basierte Segmentierung.
- Warum nicht hier? ML wuerde Transparenz und Determinismus reduzieren.

## Repo-Referenzen
- `src/core/cv_analyzer.py`
- `tests/unit/test_cv_sections.py`
- `docs/01_requirements/FR.en.md`

## Qualitaetscheck
- Abschnittserkennung deckt definierte Header ab.
- Tests enthalten DE/EN Beispiele.
- Fehlende Abschnitte fuehren zu keiner Exception.
## Phasenbezug
| Phase | Aufgabe | Status |
|-------|---------|--------|
| Phase 3 | CV-Strukturerkennung implementieren | erledigt |