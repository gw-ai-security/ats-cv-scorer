# Evaluation Plan

## Metrics
- PDF success rate (extraction succeeds without errors)
- response time (end-to-end processing time)
- usability (SUS survey after demo)
- privacy checks (no files retained after session)
- ML matching (optional): nDCG / MRR, F1 / ROC-AUC (if calibrator used)
- explainability review (top matched chunks and skill overlap sanity)

## Measurement
- log success vs. failure per upload during test runs
- measure response time per request; compute P95
- collect SUS scores from pilot users
- verify temp files removed and no persisted CV data
- evaluate ranking metrics on labeled CV/JD pairs (synthetic or public)
- review explanation artifacts for consistency and relevance

## Kaggle Dataset Evaluation (External)
- Use processed JSONL pairs stored under `data/processed/` (not committed raw data).
- Run ingestion with `scripts/data/ingest_kaggle_zips.py` to populate `data/processed/datasets/`.
- Run evaluation with `scripts/evaluate/evaluate_matching.py --dataset <dataset_id>`.
- Run data quality summary with `scripts/evaluate/external_data_quality.py`.
- Run PII scan on processed JSONL with `scripts/data/pii_scan_processed.py`.
- Track per-source data quality (missing fields, language mix, label balance).
- Document licensing and data source constraints before use.

## Acceptance Thresholds
- PDF success rate >= 95% on sample set
- response time P95 < 30 seconds
- SUS score >= 70
- privacy checks: 100% pass
- ML metrics tracked and documented in `docs/04_evaluation/EVALUATION_RESULTS.md`
