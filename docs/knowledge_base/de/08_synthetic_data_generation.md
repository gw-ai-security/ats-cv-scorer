# Synthetic Data Generation (DE)

## Zweck
Reproduzierbare, synthetische CV↔JD Paare mit Ground Truth fuer Matching, Explainability und Tests erzeugen.

## Grundsaetze
- Keine echten personenbezogenen Daten (nur synthetisch).
- Deterministisch (Seed + feste Regeln).
- Ground Truth ist explizit und maschinenlesbar.
- Keine grossen Datendumps im Repo; nur kleine Fixtures + Generator.

## Skill-Taxonomie
Die kontrollierte Skill-Taxonomie liegt unter:
- `data/synthetic/skill_taxonomy.json`

Enthaelt:
- Skills (technical/soft/languages/certifications)
- Synonym-Mapping (z. B. `py` -> `python`)
- Job Families mit required/preferred Skills

## Erzeugungsregeln (Ground Truth by construction)
- **Positive (strong_match):** alle required Skills im CV + Experience-Section vorhanden.
- **Partial (partial_match):** 1 required Skill fehlt oder Experience fehlt.
- **Negative (mismatch):** required Skills fehlen deutlich oder falsche Job Family.

### Edge Cases (kontrolliert)
- Keyword stuffing: Skills nur in Skills-Section, nicht in Experience.
- Section missing: z. B. keine Education.
- Noisy formatting: gemischte Bullet-Formate/Spacing.
- Synonym-only matches: nur Synonyme statt exakter Begriffe.

## Ground Truth Schema (pro Pair)
```json
{
  "expected_label": "strong_match|partial_match|mismatch",
  "missing_required_skills": ["..."],
  "matched_skills": ["..."],
  "expected_score_range": [min, max],
  "rationale": "deterministisch aus Regeln",
  "metadata": {
    "language": "en|de",
    "job_family": "backend|data|security",
    "difficulty": "easy|medium|hard",
    "seed": 123,
    "generator_version": "x.y.z"
  }
}
```

## CLI / Usage
```bash
$env:PYTHONPATH='.'; py scripts/generate_synth_data.py --n 10 --seed 13 --lang mixed --job-family mixed --difficulty mixed --outdir tests/fixtures/synth
```

## Tests & Fixtures
- Fixtures: `tests/fixtures/synth/` (kleines Set, z. B. 10 Paare).
- Tests: `tests/unit/test_synthetic_dataset.py`.

## Grenzen
- Synthetische Daten ersetzen keine realen Evaluationsdaten.
- Explainability basiert auf der deterministischen Baseline.
- Edge Cases dienen der Robustheitspruefung, nicht dem Realismus.

## Verweise
- `docs/04_evaluation/EVALUATION_PLAN.md`
- `docs/02_architecture/ADR/ADR-002-ml-matching.md`
- `docs/knowledge_base/de/07_data_sources_and_licensing.md`

## Last Updated
2026-01-21 14:19:44 (Local)
