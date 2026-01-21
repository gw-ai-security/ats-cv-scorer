# Data Pipeline Standard (DE)

## Zweck
Standardisiere Ingestion und Verarbeitung externer Datensaetze.

## Pipeline-Ueberblick
1) Download (manuell oder Script).
2) Parsing in standardisiertes JSONL.
3) Speicherung unter `data/processed/datasets/`.
4) Nutzung in Evaluation/Training.

## Standard-JSONL-Schemas
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

### CV/JD Paare
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

### Dataset-Type Logik
- `paired`: cv_text und jd_text vorhanden; Labels optional.
- `cv_only`: nur cv_text; fuer Parsing/Skill-Checks.
- `jd_only`: nur jd_text; fuer JD-Parsing und Skill-Abdeckung.
- `skills_only`: keine Texte; Taxonomie ueber meta Felder.

## Skripte
- Download: `scripts/data/download_kaggle_datasets.py`
- Resumes parsen: `scripts/data/parse_resumes.py`
- JDs parsen: `scripts/data/parse_job_descriptions.py`
- Skills parsen: `scripts/data/parse_skillsets.py`
- Kaggle ingestieren: `scripts/data/ingest_kaggle_datasets.py`
- Lokale ZIPs ingestieren: `scripts/data/ingest_kaggle_zips.py`
- PII Scan (processed): `scripts/data/pii_scan_processed.py`
- External Data Quality: `scripts/evaluate/external_data_quality.py`
- Evaluation der processed Paare: `scripts/evaluate/evaluate_matching.py --processed-dir data/processed`

## Storage-Regeln
- Rohdaten bleiben ausserhalb des Repos (`data/external/` ignoriert).
- Nur kleine, synthetische Samples in `data/processed/`.
- Datasets in `data/processed/registry.json` registrieren.

## Verweise
- `docs/knowledge_base/de/external_data_sources.md`
- `docs/04_evaluation/EVALUATION_PLAN.md`

## Last Updated
2026-01-21 16:32:30 (Local)
