---
name: skill-extraction
description: Pflege die Skill-Extraktion und Kategorisierung; verwenden bei neuen Skill-Listen, Synonymen oder Kategorien.
---

# Skill: skill-extraction

## Zweck
Extrahiere Skills nachvollziehbar und kategorisiert aus CV-Text.

## Wann anwenden
- Wenn Skill-Listen, Synonyme oder Kategorien angepasst werden.
- Wenn Extraktionslogik oder Ausgabeformate geaendert werden.

## Vorgehen (Schritt-fuer-Schritt)
1) Lies FR-004 und bestehende Tests.
2) Aktualisiere `src/core/skill_extractor.py`.
3) Passe Tests in `tests/unit/test_skill_extractor.py` an.
4) Stelle sicher, dass Kategorien konsistent ausgegeben werden.

## Lernperspektive
- Warum so? Regelbasierte Extraktion ist transparent und reproduzierbar.
- Alternativen: ML-Embeddings oder externe Skill-Datenbanken.
- Warum nicht hier? Externe Abhaengigkeiten und Black-Box-Verhalten reduzieren Explainability.

## Repo-Referenzen
- `src/core/skill_extractor.py`
- `tests/unit/test_skill_extractor.py`
- `docs/01_requirements/FR.en.md`

## Qualitaetscheck
- Synonyme werden korrekt normalisiert.
- Kategorien sind stabil und getestet.
- Fehlende Skills fuehren zu leeren, aber gueltigen Ergebnissen.
## Phasenbezug
| Phase | Aufgabe | Status |
|-------|---------|--------|
| Phase 3 | Skill-Extraktion und Kategorisierung implementieren | erledigt |