# vNext Acceptance Checklist

## Commands
1) Ingest local Kaggle ZIPs
```
$env:PYTHONPATH='.'; py scripts/data/ingest_kaggle_zips.py
```

2) Apply license overrides (optional)
```
$env:PYTHONPATH='.'; py scripts/data/update_registry_licenses.py
```

3) Run external data quality report
```
$env:PYTHONPATH='.'; py scripts/evaluate/external_data_quality.py
```

4) Run PII scan on processed datasets
```
$env:PYTHONPATH='.'; py scripts/data/pii_scan_processed.py
```

5) Adapter health report
```
$env:PYTHONPATH='.'; py scripts/data/adapter_health_report.py
```

6) External evaluation (baseline example)
```
$env:PYTHONPATH='.'; py scripts/evaluate/evaluate_matching.py --dataset resume_data_ranking --strategy baseline --limit 200 --summary-out docs/04_evaluation/EVALUATION_RESULTS_EXTERNAL.md
```

7) External evaluation (hybrid ML, optional)
Prerequisite: sentence-transformers model cached locally (no downloads in CI).
```
$env:PYTHONPATH='.'; py scripts/evaluate/evaluate_matching.py --dataset resume_data_ranking --strategy hybrid_ml --limit 50 --summary-out docs/04_evaluation/EVALUATION_RESULTS_EXTERNAL.md
```

8) Train calibrator (optional, labeled data required)
```
$env:PYTHONPATH='.'; py scripts/train/train_from_processed.py --input data/processed/datasets/resume_data_ranking.jsonl
```

9) Run Streamlit demo
```
$env:PYTHONPATH='.'; streamlit run frontend/streamlit_app.py
```

10) Prompt Chain demo (manual)
- Open the "Prompt Chain" tab.
- Use Demo Mode with synthetic fixtures.
- Run Chain and download PDF/JSON/MD.

## Acceptance Checks
- [ ] Raw datasets are not committed (ZIPs/unzipped/processed datasets ignored by git).
- [ ] `data/processed/registry.json` includes `source_url`, `license_label`, `license_url`, `usage_status`, `dataset_type`.
- [ ] `docs/04_evaluation/EXTERNAL_DATA_QUALITY.md` generated.
- [ ] `docs/04_evaluation/PII_SCAN_REPORT.md` generated.
- [ ] `docs/04_evaluation/EVALUATION_RESULTS_EXTERNAL.md` generated.
- [ ] Streamlit demo runs with synthetic fixtures and exports PDF/JSON/MD.
- [ ] Hybrid ML remains gated by evaluation results.
