# Synthetic Data Generator Report

## Files Added
- `data/synthetic/skill_taxonomy.json`
- `docs/codex_skills/SKILL_SYNTHETIC_DATA_GENERATOR.md`
- `docs/codex_skills/SKILL_ML_EVALUATION_AND_BIAS_CHECK.md`
- `docs/knowledge_base/de/08_synthetic_data_generation.md`
- `docs/knowledge_base/en/08_synthetic_data_generation.md`
- `docs/knowledge_base/de/09_ml_evaluation_and_bias.md`
- `docs/knowledge_base/en/09_ml_evaluation_and_bias.md`
- `scripts/generate_synth_data.py`
- `scripts/evaluate/evaluate_matching.py`
- `src/data_synth/__init__.py`
- `src/data_synth/generator.py`
- `tests/fixtures/synth/pairs.jsonl`
- `tests/fixtures/synth/pair_0001_cv.txt`
- `tests/fixtures/synth/pair_0001_jd.txt`
- `tests/fixtures/synth/pair_0002_cv.txt`
- `tests/fixtures/synth/pair_0002_jd.txt`
- `tests/fixtures/synth/pair_0003_cv.txt`
- `tests/fixtures/synth/pair_0003_jd.txt`
- `tests/fixtures/synth/pair_0004_cv.txt`
- `tests/fixtures/synth/pair_0004_jd.txt`
- `tests/fixtures/synth/pair_0005_cv.txt`
- `tests/fixtures/synth/pair_0005_jd.txt`
- `tests/fixtures/synth/pair_0006_cv.txt`
- `tests/fixtures/synth/pair_0006_jd.txt`
- `tests/fixtures/synth/pair_0007_cv.txt`
- `tests/fixtures/synth/pair_0007_jd.txt`
- `tests/fixtures/synth/pair_0008_cv.txt`
- `tests/fixtures/synth/pair_0008_jd.txt`
- `tests/fixtures/synth/pair_0009_cv.txt`
- `tests/fixtures/synth/pair_0009_jd.txt`
- `tests/fixtures/synth/pair_0010_cv.txt`
- `tests/fixtures/synth/pair_0010_jd.txt`
- `tests/unit/test_synthetic_dataset.py`

## Files Updated
- `docs/codex_skills/OVERVIEW.md`
- `docs/knowledge_base/de/INDEX.md`
- `docs/knowledge_base/en/INDEX.md`
- `docs/knowledge_base/de/07_data_sources_and_licensing.md`
- `docs/knowledge_base/en/07_data_sources_and_licensing.md`
- `.gitignore`

## Ground Truth Rationale (Kurz)
Ground Truth entsteht deterministisch aus der kontrollierten Skill-Taxonomie, den Regelklassen (strong/partial/mismatch) und den Edge-Case-Flags. Das erwartete Score-Intervall wird aus dem bekannten Skill-Overlap und dem Vorhandensein der Experience-Section abgeleitet.

## ML Evaluation Kurzfazit
Das ML-Matching wird gegen die Baseline auf synthetischen Paaren bewertet. Bias Checks sind indikativ entlang kontrollierter Achsen (job_family, language, difficulty, formatting_noise, synonym_only) und dokumentieren Abweichungen ohne Fairness-Versprechen.
