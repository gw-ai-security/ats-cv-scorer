---
name: testing-quality-gates
description: Pflege Tests, Linting und CI-Qualitaetsregeln; verwenden bei neuen Features oder Aenderungen, die Tests/CI beeinflussen.
---

# Skill: testing-quality-gates

## Zweck
Sichere Qualitaet durch Tests, Linting und CI-Checks.

## Wann anwenden
- Wenn neue Features oder Module hinzukommen.
- Wenn Tests oder CI-Regeln aktualisiert werden muessen.

## Vorgehen (Schritt-fuer-Schritt)
1) Lies `docs/03_quality/QUALITY_GATES.md` und `.github/workflows/ci.yml`.
2) Ergaenze Unit- oder Integrationstests in `tests/`.
3) Pruefe Linting-Regeln mit ruff und passe Code an.
4) Stelle sicher, dass Coverage im CI-Report generiert wird.

## Lernperspektive
- Warum so? Automatisierte Tests und Linting sind Kern fuer Nachvollziehbarkeit.
- Alternativen: manuelle Tests oder kein CI.
- Warum nicht hier? Fehlende Automatisierung reduziert Vertrauen in Ergebnisse.

## Repo-Referenzen
- `tests/`
- `docs/03_quality/QUALITY_GATES.md`
- `.github/workflows/ci.yml`

## Qualitaetscheck
- Tests decken relevante Akzeptanzkriterien ab.
- Linting laeuft ohne Fehler.
- CI-Pipeline bleibt gruen.
## Phasenbezug
| Phase | Aufgabe | Status |
|-------|---------|--------|
| Phase 4 | Tests, Linting und CI-Qualitaetsregeln etablieren | erledigt |