# Project Snapshot - ATS CV Scorer - 2026-01-22 16:32:03 (Local)

## 1) Kurzueberblick
- Zweck / Problem: Transparente, nachvollziehbare CV-Bewertung statt intransparenter ATS-Systeme. Quelle: `docs/00_overview/PROJECT_OVERVIEW.md`
- Zielgruppe / Nutzer: Recruiter und Kandidaten, Portfolio-Review fuer Engineering Case Study. Quelle: `docs/00_overview/PROJECT_OVERVIEW.md`, `README.md`
- Aktueller Stand in 5 Bulletpoints:
  - Kaggle ZIP Ingestion laeuft lokal (Registry + Adapter + Reports); raw data bleibt git-ignored. Quelle: `scripts/data/ingest_kaggle_zips.py`, `data/processed/registry.json`, `data/processed/INGEST_REPORT.md`
  - External Data Quality + PII Scan Reports erzeugt. Quelle: `docs/04_evaluation/EXTERNAL_DATA_QUALITY.md`, `docs/04_evaluation/PII_SCAN_REPORT.md`
  - External Evaluation Summary dokumentiert (baseline, limitierter Run). Quelle: `docs/04_evaluation/EVALUATION_RESULTS_EXTERNAL.md`
  - Report Exports (PDF/JSON/MD) implementiert und UI-Downloads ergaenzt inkl. Demo Mode. Quelle: `src/core/report_export.py`, `src/core/pdf_layout.py`, `frontend/streamlit_app.py`
  - vNext Governance (ADRs, Release Notes, DoD, Acceptance Checklist) angelegt. Quelle: `docs/02_architecture/ADR/ADR-003-external-datasets.md`, `docs/02_architecture/ADR/ADR-004-reporting-and-exports.md`, `docs/00_overview/RELEASE_NOTES_vNEXT.md`

## 2) Scope & Nicht-Scope
- In Scope:
  - Lokale Ingestion externer Datensaetze (Kaggle ZIPs, offline). Quelle: `data/external/kaggle/_README.md`, `scripts/data/ingest_kaggle_zips.py`
  - Externe Evaluation mit Quality- und PII-Reports. Quelle: `docs/04_evaluation/`
  - Report Exports (PDF/JSON/MD) und Demo-Flow. Quelle: `src/core/report_export.py`, `frontend/streamlit_app.py`
- Out of Scope:
  - Keine Rohdaten im Repo (ZIPs/unzipped/processed datasets ignoriert). Quelle: `.gitignore`
  - Keine PII im Repo (nur Counts/Reports). Quelle: `docs/04_evaluation/PII_SCAN_REPORT.md`

## 3) Architektur & Komponenten (repo-basiert)
- High-level Architektur:
  - Streamlit UI -> Upload/Validation -> Analyse/Extraktion -> Matching -> Exports. Quelle: `frontend/streamlit_app.py`, `src/core/`
  - Externe Daten: ZIPs -> Unzip -> Adapter -> Canonical JSONL -> Eval/Train. Quelle: `scripts/data/ingest_kaggle_zips.py`, `src/data_ingest/`
- Komponenten/Module (Pfad -> Verantwortung):
  - `src/data_ingest/adapters/`: Kaggle Adapter (cv_only/jd_only/skills_only/paired).
  - `scripts/data/pii_scan_processed.py`: PII Counts Report.
  - `scripts/evaluate/external_data_quality.py`: Data Quality Summary.
  - `scripts/evaluate/evaluate_matching.py`: External evaluation summary via `--dataset`.
  - `src/core/report_export.py`: Report payload + JSON/MD exports.

## 4) Aktuelle Implementierung (was existiert wirklich)
- Tests/Qualitaet:
  - Adapter/Registry Tests + Report Export Test vorhanden. Quelle: `tests/unit/test_registry_and_adapters.py`, `tests/unit/test_report_export.py`
- Dokumentation:
  - vNext Release Notes + Acceptance Checklist vorhanden. Quelle: `docs/00_overview/RELEASE_NOTES_vNEXT.md`, `docs/00_overview/VNEXT_ACCEPTANCE_CHECKLIST.md`

## 5) Backlog: Offene Punkte & naechste Schritte
1. Lizenz-/URL-Details pro Kaggle Dataset verifizieren und Registry aktualisieren. Quelle: `data/processed/registry.json`
2. Hybrid ML Evaluation auf externen Datasets (wenn Embeddings verfügbar). Quelle: `scripts/evaluate/evaluate_matching.py`
3. Adapter-Validierung gegen weitere reale Kaggle Formate. Quelle: `src/data_ingest/adapters/`

## 6) Risiken / Blocker
- Kaggle-Formate variieren stark; Adapter brauchen laufende Pflege. Quelle: `src/data_ingest/adapters/`
- Hybrid ML Evaluation benoetigt Embedding-Modelle (Download/Runtime). Quelle: `src/core/ml/embedding_model.py`

## 7) Repo-Referenzen (wichtigste Dateien)
- Registry: `data/processed/registry.json`
- Ingestion Script: `scripts/data/ingest_kaggle_zips.py`
- PII Scan: `scripts/data/pii_scan_processed.py`
- External Data Quality: `scripts/evaluate/external_data_quality.py`
- External Evaluation Results: `docs/04_evaluation/EVALUATION_RESULTS_EXTERNAL.md`
- Report Export: `src/core/report_export.py`
- UI Demo: `frontend/streamlit_app.py`
