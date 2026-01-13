# Qualitaets-Gates

## Tooling
- Lint: ruff
- Tests: pytest
- Coverage: pytest-cov (Report in CI)

## Definition of Done (Requirements)
- Implementierung existiert in `src/`
- Tests decken die Akzeptanzkriterien ab
- Traceability aktualisiert in `docs/01_requirements/TRACEABILITY.*.md`
- CI ist gruen

## Security Basics
- Input-Validierung (Dateityp und Groesse)
- keine persistente Speicherung von CV-Daten
- temporaere Dateien nach Verarbeitung entfernen
