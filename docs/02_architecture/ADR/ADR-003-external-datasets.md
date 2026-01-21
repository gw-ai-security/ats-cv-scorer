# ADR-003: External Datasets (Local Ingestion + Compliance)

## Status
Accepted (vNext)

## Context
The project needs to evaluate and optionally train on external datasets (e.g., Kaggle) without committing raw data to the repository. Licensing and PII risks must be documented, and ingestion must be reproducible offline.

## Decision
- External datasets are ingested locally from ZIP files stored under `data/external/kaggle/_incoming_zips/` (git-ignored).
- Raw ZIPs and unzipped files are excluded from git (`data/external/kaggle/_incoming_zips/`, `data/external/kaggle/_unzipped/`).
- Canonical JSONL outputs are written to `data/processed/datasets/` (git-ignored).
- Only registry metadata (`data/processed/registry.json`) and ingest reports (`data/processed/INGEST_REPORT.md`) are committed.
- License status defaults to `restricted` until verified; no claims are made without sources.

## Consequences
- All ingest/evaluation steps are reproducible via CLI.
- Any dataset added must register `source_url`, `license_label`, `usage_status`, and `dataset_type`.
- Downstream evaluation uses processed JSONL only.

## References
- `scripts/data/ingest_kaggle_zips.py`
- `data/processed/registry.json`
- `docs/knowledge_base/en/07_data_sources_and_licensing.md`
