# Skill: Synthetic Data Generator

## Zweck
Erzeuge reproduzierbare, synthetische CV↔JD Paare mit Ground Truth fuer Matching, Explainability und Tests.

## Wann anwenden
- Wenn neue Testsaetze fuer Matching/Explainability benoetigt werden.
- Vor ML-Evaluationen, die Labels oder Weak Supervision brauchen.
- Bei Aenderungen an Matching-Logik oder Skill-Taxonomie.

## Vorgehen (Schritt-fuer-Schritt)
1) Pruefe die Taxonomie unter `data/synthetic/skill_taxonomy.json` und passe Job Families/Skills an.
2) Generiere Paare mit `scripts/generate_synth_data.py` (Seed setzen).
3) Lege kleine Fixtures unter `tests/fixtures/synth/` ab (max. ca. 10 Paare).
4) Pruefe Ground Truth: `expected_label`, `missing_required_skills`, `matched_skills`, `expected_score_range`.
5) Ergaenze Tests oder aktualisiere `tests/unit/test_synthetic_dataset.py`.
6) Dokumentiere Regeln/Limitierungen in der Knowledge Base (DE/EN).

## CLI / Usage
```bash
$env:PYTHONPATH='.'; py scripts/generate_synth_data.py --n 10 --seed 13 --lang mixed --job-family mixed --difficulty mixed --outdir tests/fixtures/synth
```

## Qualitaetskriterien
- Gleiche Inputs/Seed liefern gleiche Outputs.
- Ground Truth ist maschinenlesbar (JSON).
- Keine PII, keine realen Firmen/Personen.
- Fixtures sind klein und laufen schnell in Tests.

## Repo-Referenzen
- `scripts/generate_synth_data.py`
- `src/data_synth/generator.py`
- `data/synthetic/skill_taxonomy.json`
- `tests/fixtures/synth/`
- `tests/unit/test_synthetic_dataset.py`
- `docs/knowledge_base/de/08_synthetic_data_generation.md`
- `docs/knowledge_base/en/08_synthetic_data_generation.md`

## Last Updated
2026-01-21 14:19:44 (Local)
