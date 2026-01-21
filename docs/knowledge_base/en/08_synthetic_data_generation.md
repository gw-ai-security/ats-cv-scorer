# Synthetic Data Generation (EN)

## Purpose
Generate reproducible, synthetic CV↔JD pairs with ground truth for matching, explainability, and tests.

## Principles
- No real personal data (synthetic only).
- Deterministic (seed + fixed rules).
- Ground truth is explicit and machine-readable.
- No large data dumps in the repo; only small fixtures + generator.

## Skill Taxonomy
Controlled skill taxonomy lives at:
- `data/synthetic/skill_taxonomy.json`

Contains:
- Skills (technical/soft/languages/certifications)
- Synonym mapping (e.g., `py` -> `python`)
- Job families with required/preferred skills

## Generation Rules (Ground Truth by construction)
- **Positive (strong_match):** all required skills in CV + Experience section present.
- **Partial (partial_match):** 1 required skill missing or Experience missing.
- **Negative (mismatch):** required skills largely missing or wrong job family.

### Edge Cases (controlled)
- Keyword stuffing: skills only in Skills section, not in Experience.
- Section missing: e.g., no Education.
- Noisy formatting: mixed bullet formats/spacing.
- Synonym-only matches: synonyms instead of exact terms.

## Ground Truth Schema (per pair)
```json
{
  "expected_label": "strong_match|partial_match|mismatch",
  "missing_required_skills": ["..."],
  "matched_skills": ["..."],
  "expected_score_range": [min, max],
  "rationale": "deterministic from rules",
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
- Fixtures: `tests/fixtures/synth/` (small set, e.g. 10 pairs).
- Tests: `tests/unit/test_synthetic_dataset.py`.

## Limits
- Synthetic data does not replace real evaluation data.
- Explainability relies on the deterministic baseline.
- Edge cases are for robustness checks, not realism.

## References
- `docs/04_evaluation/EVALUATION_PLAN.md`
- `docs/02_architecture/ADR/ADR-002-ml-matching.md`
- `docs/knowledge_base/en/07_data_sources_and_licensing.md`

## Last Updated
2026-01-21 14:19:44 (Local)
