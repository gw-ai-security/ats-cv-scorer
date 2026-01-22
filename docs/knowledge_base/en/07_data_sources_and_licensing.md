# Data Sources & Licensing (EN)

## Purpose
Document external data sources and perform a licensing/compliance review before use in the project.

## Checklist (per data source)
- Source name:
- URL:
- Data type (CV, JD, Skills, Synthetic):
- License type (e.g., CC, Kaggle License, Public Domain):
- Intended use in the project (training, evaluation, tests):
- Storage (local, transient, not stored):
- Risks (PII, bias, scope drift):
- Decision: approved / restricted / rejected:
- Rationale:

## Decision Logic (Summary)
- **approved**: License fits the purpose, no disallowed PII, scope aligned, storage policy ok.
- **restricted**: License/privacy unclear or usage limited; tests/evaluation only with explicit limits.
- **rejected**: License prohibits use, PII risk not manageable, or scope drift.
- If license is unclear: set `restricted` and document the rationale.

## Kaggle Local ZIP Workflow
- Place ZIPs under `data/external/kaggle/_incoming_zips/` (ignored by git).
- Unzip into `data/external/kaggle/_unzipped/` (ignored by git).
- Run `scripts/data/ingest_kaggle_zips.py` to produce `data/processed/datasets/<dataset_id>.jsonl`.
- Register datasets in `data/processed/registry.json`.
- Current dataset IDs (restricted until license verified):
  - `ats_scoring_dataset`
  - `resume_job_matching`
  - `resume_data_ranking`
  - `job_descriptions_2025`
  - `job_skill_set`

### Registry Fields (Compliance)
- `source_url`: dataset landing page (unknown until verified).
- `license_label`: explicit license name (default `unknown`).
- `license_url`: link to license or terms (optional; default `unknown`).
- `usage_status`: `restricted` until license + PII status is documented.
- `dataset_type`: `paired|cv_only|jd_only|skills_only` for downstream handling.

### Usage Status Meaning
- `restricted`: license/PII not verified; use only for local analysis with strict limits.
- `approved_local_only`: verified license but use only locally; no redistribution.
- `approved`: verified license and approved for project use (still no raw data committed).

### How to Update License Info
1) Edit `data/processed/registry_licenses_overrides.json`.
2) Run `scripts/data/update_registry_licenses.py`.
3) Review `data/processed/REGISTRY_CHANGELOG.md`.

## Current Assessments (initial)
### Kaggle Resume / Job Description Dataset (source pending)
- Source name: Kaggle Resume / Job Description (dataset not selected yet)
- URL: TBD (dataset-specific)
- Data type: CV, JD
- License type: TBD (dataset-specific)
- Intended use in the project: Evaluation/Test (planned)
- Storage: transient (no persistent storage)
- Risks: PII, bias, license clarity
- Decision: restricted
- Rationale: Dataset not selected; license terms and PII status unknown.

### O*NET Skills & Occupations Data
- Source name: O*NET Skills & Occupations Data
- URL: https://www.onetcenter.org/database.html
- Data type: Skills, Occupations
- License type: TBD (license terms must be verified)
- Intended use in the project: Reference/Taxonomy
- Storage: local (derived structures only, no raw data committed)
- Risks: License clarity, scope drift
- Decision: restricted
- Rationale: License terms not yet validated and documented.

### Synthetic / Generated Data (internal)
- Source name: Synthetic / Generated Data (internal)
- URL: N/A
- Data type: Synthetic
- License type: Internal generation (documented generator)
- Intended use in the project: Tests/Evaluation
- Storage: transient or local (no PII)
- Risks: Prompt bias, realism gaps
- Decision: approved
- Rationale: Process and guardrails are documented; no PII and controlled generation (see `docs/knowledge_base/en/08_synthetic_data_generation.md`).

## Example Assessments (Templates)
### Kaggle Resume Dataset (Example)
- Source name: Kaggle Resume Dataset (Example)
- URL: https://www.kaggle.com/datasets/<dataset-name>
- Data type: CV
- License type: Unclear (Example)
- Intended use in the project: Evaluation/Test
- Storage: transient (no persistent storage)
- Risks: PII, bias, license clarity
- Decision: restricted
- Rationale: License and PII status not clearly documented; limit to tests until verified.

### O*NET Skills Data (Example)
- Source name: O*NET Skills Data (Example)
- URL: https://www.onetcenter.org/database.html
- Data type: Skills
- License type: Unclear (Example)
- Intended use in the project: Reference/Taxonomy
- Storage: local (derived structures only, no raw data committed)
- Risks: License clarity, scope drift
- Decision: restricted
- Rationale: License terms and permitted use must be validated for this project.

### Synthetic Data (Example)
- Source name: Synthetic Data (Example)
- URL: N/A (internally generated)
- Data type: Synthetic
- License type: Internal generation (Example)
- Intended use in the project: Tests/Evaluation
- Storage: transient or local (no PII)
- Risks: Prompt bias, realism gaps
- Decision: approved
- Rationale: No PII, clear purpose, controlled usage and storage.

## References
- `docs/04_evaluation/EVALUATION_PLAN.md`
- `docs/02_architecture/ADR/ADR-002-ml-matching.md`
- `docs/knowledge_base/en/external_data_sources.md`
- `docs/project_state/`

## Last Updated
2026-01-22 20:21:30 (Local)
