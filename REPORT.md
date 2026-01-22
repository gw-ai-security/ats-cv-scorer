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

## vNext Update (External Data + Reporting)
### New Files
- `docs/02_architecture/ADR/ADR-003-external-datasets.md`
- `docs/02_architecture/ADR/ADR-004-reporting-and-exports.md`
- `docs/00_overview/RELEASE_NOTES_vNEXT.md`
- `docs/00_overview/VNEXT_ACCEPTANCE_CHECKLIST.md`
- `docs/03_quality/DEFINITION_OF_DONE_vNEXT.md`
- `docs/04_evaluation/EXTERNAL_DATA_QUALITY.md`
- `docs/04_evaluation/EVALUATION_RESULTS_EXTERNAL.md`
- `docs/04_evaluation/PII_SCAN_REPORT.md`
- `docs/04_evaluation/TRAINING_SUMMARY.md`
- `scripts/data/pii_scan_processed.py`
- `scripts/evaluate/external_data_quality.py`
- `src/core/report_export.py`
- `tests/unit/test_report_export.py`
- `docs/project_state/2026-01-21/154201_project_snapshot.md`

### Updated Files (vNext scope)
- `scripts/data/ingest_kaggle_zips.py`
- `src/data_ingest/adapters/ats_scoring_dataset.py`
- `src/data_ingest/adapters/resume_job_matching.py`
- `src/data_ingest/adapters/resume_data_ranking.py`
- `src/data_ingest/adapters/job_descriptions_2025.py`
- `src/data_ingest/adapters/job_skill_set.py`
- `src/data_ingest/adapters/base.py`
- `data/processed/registry.json`
- `scripts/evaluate/evaluate_matching.py`
- `scripts/train/train_from_processed.py`
- `src/core/matcher.py`
- `src/core/pdf_layout.py`
- `src/core/templates/score_report.txt.j2`
- `frontend/streamlit_app.py`
- `docs/03_quality/EXPLAINABLE_SCORING_SPEC.md`
- `docs/04_evaluation/EVALUATION_PLAN.md`
- `docs/knowledge_base/en/07_data_sources_and_licensing.md`
- `docs/knowledge_base/de/07_data_sources_and_licensing.md`
- `docs/knowledge_base/en/data_pipeline_standard.md`
- `docs/knowledge_base/de/data_pipeline_standard.md`
- `docs/knowledge_base/en/pdf_report_layout.md`
- `docs/knowledge_base/de/pdf_report_layout.md`
- `docs/codex_skills/PHASE_PLAN.md`

### vNext Status Summary
- Local Kaggle ZIP ingestion runs and produces canonical JSONL (ignored by git).
- External data quality + PII scan reports are generated.
- External evaluation summary captured (baseline-only, limited run, labeled thresholds documented).
- Report exports available in PDF/JSON/MD and wired into Streamlit demo mode.

## vNext.1 Update (License Workflow + Adapter Validation)
### New Files
- `data/processed/registry_licenses_overrides.json`
- `data/processed/REGISTRY_CHANGELOG.md`
- `scripts/data/update_registry_licenses.py`
- `src/core/ml/embedding_runtime.py`
- `scripts/data/adapter_health_report.py`
- `docs/04_evaluation/ADAPTER_HEALTH_REPORT.md`
- `docs/00_overview/USABILITY_CHECKLIST_vNEXT.md`
- `tests/unit/test_ingest_adapters_schema.py`
- `tests/fixtures/ingest/ats_scoring_dataset/train_data.json`
- `tests/fixtures/ingest/resume_job_matching/train.csv`
- `tests/fixtures/ingest/resume_data_ranking/resume_data_for_ranking.csv`
- `tests/fixtures/ingest/job_descriptions_2025/job_dataset.csv`
- `tests/fixtures/ingest/job_skill_set/resume_extraction.csv`

### Updated Files (vNext.1 scope)
- `data/processed/registry.json`
- `data/processed/INGEST_REPORT.md`
- `scripts/evaluate/evaluate_matching.py`
- `docs/04_evaluation/EVALUATION_RESULTS_EXTERNAL.md`
- `docs/00_overview/VNEXT_ACCEPTANCE_CHECKLIST.md`
- `docs/00_overview/RELEASE_NOTES_vNEXT.md`
- `docs/knowledge_base/en/07_data_sources_and_licensing.md`
- `docs/knowledge_base/de/07_data_sources_and_licensing.md`

## Prompt Chain Feature
### New Files
- `src/prompt_chain/models.py`
- `src/prompt_chain/engine.py`
- `src/prompt_chain/heuristics.py`
- `src/prompt_chain/providers/base.py`
- `src/prompt_chain/providers/noop.py`
- `src/prompt_chain/providers/openai_provider.py`
- `src/prompt_chain/__init__.py`
- `docs/codex_skills/SKILL_PROMPT_CHAIN_WORKFLOW.md`
- `docs/knowledge_base/en/10_prompt_chain_workflow.md`
- `docs/knowledge_base/de/10_prompt_chain_workflow.md`
- `tests/unit/test_prompt_chain_fallback.py`
- `tests/unit/test_prompt_chain_schema.py`

### Updated Files
- `frontend/streamlit_app.py`
- `src/core/report_export.py`
- `src/core/pdf_layout.py`
- `src/core/templates/score_report.txt.j2`
- `docs/00_overview/RELEASE_NOTES_vNEXT.md`
- `docs/00_overview/VNEXT_ACCEPTANCE_CHECKLIST.md`
- `docs/knowledge_base/en/INDEX.md`
- `docs/knowledge_base/de/INDEX.md`
