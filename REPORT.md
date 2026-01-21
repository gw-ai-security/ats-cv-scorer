# Synthetic Data Generator Report

## Files Added
- `data/synthetic/skill_taxonomy.json`
- `docs/codex_skills/SKILL_SYNTHETIC_DATA_GENERATOR.md`
- `docs/codex_skills/SKILL_ML_EVALUATION_AND_BIAS_CHECK.md`
- `docs/codex_skills/PHASE_2_SIGNOFF.md`
- `docs/knowledge_base/de/08_synthetic_data_generation.md`
- `docs/knowledge_base/en/08_synthetic_data_generation.md`
- `docs/knowledge_base/de/09_ml_evaluation_and_bias.md`
- `docs/knowledge_base/en/09_ml_evaluation_and_bias.md`
- `docs/03_quality/EXPLAINABLE_SCORING_SPEC.md`
- `docs/04_evaluation/EVALUATION_RESULTS.md`
- `docs/knowledge_base/de/external_data_sources.md`
- `docs/knowledge_base/en/external_data_sources.md`
- `docs/knowledge_base/de/data_pipeline_standard.md`
- `docs/knowledge_base/en/data_pipeline_standard.md`
- `docs/knowledge_base/de/pdf_report_layout.md`
- `docs/knowledge_base/en/pdf_report_layout.md`
- `notebooks/analysis_kaggle_datasets.ipynb`
- `scripts/data/download_kaggle_datasets.py`
- `scripts/data/parse_resumes.py`
- `scripts/data/parse_job_descriptions.py`
- `scripts/data/parse_skillsets.py`
- `scripts/data/ingest_kaggle_datasets.py`
- `src/core/pdf_layout.py`
- `src/core/templates/score_report.txt.j2`
- `src/data_pipeline/__init__.py`
- `src/data_pipeline/schema.py`
- `src/data_pipeline/ingest.py`
- `src/data_pipeline/parsers/__init__.py`
- `src/data_pipeline/parsers/resume_parser.py`
- `src/data_pipeline/parsers/jd_parser.py`
- `src/data_pipeline/parsers/skillset_parser.py`
- `src/data_pipeline/adapters/__init__.py`
- `src/data_pipeline/adapters/kaggle_adapters.py`
- `tests/unit/test_pdf_layout.py`
- `tests/unit/test_data_pipeline_parsers.py`
- `data/processed/resumes_sample.jsonl`
- `data/processed/job_descriptions_sample.jsonl`
- `data/processed/skill_sets_sample.jsonl`
- `data/processed/pairs_sample.jsonl`
- `data/external/kaggle/_README.md`
- `data/processed/registry.json`
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
- `docs/codex_skills/PHASE_PLAN.md`
- `docs/knowledge_base/de/INDEX.md`
- `docs/knowledge_base/en/INDEX.md`
- `docs/knowledge_base/de/07_data_sources_and_licensing.md`
- `docs/knowledge_base/en/07_data_sources_and_licensing.md`
- `docs/knowledge_base/de/phase_plan.md`
- `docs/knowledge_base/en/phase_plan.md`
- `docs/02_architecture/ADR/ADR-002-ml-matching.md`
- `docs/03_quality/EXPLAINABLE_SCORING_SPEC.md`
- `docs/04_evaluation/EVALUATION_RESULTS.md`
- `frontend/streamlit_app.py`
- `scripts/evaluate/evaluate_matching.py`
- `src/core/matcher.py`
- `src/utils/config.py`
- `.gitignore`

## Ground Truth Rationale (Kurz)
Ground Truth entsteht deterministisch aus der kontrollierten Skill-Taxonomie, den Regelklassen (strong/partial/mismatch) und den Edge-Case-Flags. Das erwartete Score-Intervall wird aus dem bekannten Skill-Overlap und dem Vorhandensein der Experience-Section abgeleitet.

## ML Evaluation Kurzfazit
Das ML-Matching wird gegen die Baseline auf synthetischen Paaren bewertet. Bias Checks sind indikativ entlang kontrollierter Achsen (job_family, language, difficulty, formatting_noise, synonym_only) und dokumentieren Abweichungen ohne Fairness-Versprechen.

## Phase 2 Status
Phase 2 ist formal abgeschlossen (Signoff vorhanden) mit Evaluation Gate, Explainable Scoring Spec und UI-Demo-Readiness.
