# Data Pipeline Standard (EN)

## Purpose
Define the standardized ingestion and processing format for external datasets.

## Pipeline Overview
1) Download (manual or scripted).
2) Parse into standardized JSONL.
3) Store under `data/processed/datasets/`.
4) Use JSONL in evaluation/training pipelines.

## Standard JSONL Schemas
### Resumes
```
{"record_id":"resume_000001","text":"...","language":"en","source":"dataset.csv","metadata":{...}}
```

### Job Descriptions
```
{"record_id":"jd_000001","text":"...","language":"en","source":"dataset.csv","metadata":{...}}
```

### Skill Sets
```
{"record_id":"skill_000001","skill":"python","category":"technical","source":"dataset.csv","metadata":{...}}
```

### CV/JD Pairs
```
{"pair_id":"pair_000001","cv_text":"...","jd_text":"...","expected_label":"partial_match","expected_score_range":[60,80],"metadata":{...}}
```

### Canonical Kaggle Schema (Ingestion)
```
{
  "id": "string",
  "cv_text": "string|null",
  "jd_text": "string|null",
  "label": "strong_match|partial_match|mismatch|null",
  "language": "en|de|unknown",
  "source": "kaggle:<dataset_name>",
  "meta": { "dataset_type": "paired|cv_only|jd_only|skills_only", "job_family": "...", "difficulty": "...", "raw_fields": {...} }
}
```

### Dataset Type Handling
- `paired`: both cv_text and jd_text available; labels optional.
- `cv_only`: only cv_text is present; used for parsing/skill extraction validation.
- `jd_only`: only jd_text is present; used for JD parsing and skill coverage checks.
- `skills_only`: no cv/jd text; use meta fields for taxonomy.

## Scripts
- Download: `scripts/data/download_kaggle_datasets.py`
- Parse resumes: `scripts/data/parse_resumes.py`
- Parse JDs: `scripts/data/parse_job_descriptions.py`
- Parse skills: `scripts/data/parse_skillsets.py`
- Ingest Kaggle datasets: `scripts/data/ingest_kaggle_datasets.py`
- Ingest local ZIPs: `scripts/data/ingest_kaggle_zips.py`
- PII scan (processed): `scripts/data/pii_scan_processed.py`
- External data quality: `scripts/evaluate/external_data_quality.py`
- Evaluate processed pairs: `scripts/evaluate/evaluate_matching.py --processed-dir data/processed`

## Storage Rules
- Raw data must stay out of the repo (`data/external/` ignored).
- Only small, synthetic samples may live in `data/processed/`.
- Register datasets in `data/processed/registry.json`.

## References
- `docs/knowledge_base/en/external_data_sources.md`
- `docs/04_evaluation/EVALUATION_PLAN.md`

## Last Updated
2026-01-21 16:32:30 (Local)
