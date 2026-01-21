# Project Snapshot - ATS CV Scorer - 2026-01-21 15:42:01 (Local)

## 1) Kurzueberblick
- Zweck / Problem: Transparente, nachvollziehbare CV-Bewertung statt intransparenter ATS-Systeme. Quelle: `docs/00_overview/PROJECT_OVERVIEW.md`
- Zielgruppe / Nutzer: Recruiter und Kandidaten, Portfolio-Review fuer Engineering Case Study. Quelle: `docs/00_overview/PROJECT_OVERVIEW.md`, `README.md`
- Aktueller Stand in 5 Bulletpoints:
  - Kaggle Local ZIP Ingestion Pipeline umgesetzt (Registry + Adapter + Ingest Script). Quelle: `scripts/data/ingest_kaggle_zips.py`, `src/data_ingest/`, `data/processed/registry.json`
  - Externe Datenstaging-Ordner + Gitignore-Regeln dokumentiert. Quelle: `data/external/kaggle/_README.md`, `.gitignore`
  - Evaluation Script kann processed Datasets via `--dataset` nutzen. Quelle: `scripts/evaluate/evaluate_matching.py`
  - Knowledge Base um External Data Sources, Data Pipeline Standard und PDF Layout Guidelines erweitert. Quelle: `docs/knowledge_base/en/`, `docs/knowledge_base/de/`
  - Phase-2 Ergebnisse (Evaluation, Explainable Scoring, Gate, UI) bleiben dokumentiert. Quelle: `docs/04_evaluation/EVALUATION_RESULTS.md`, `docs/03_quality/EXPLAINABLE_SCORING_SPEC.md`

## 2) Scope & Nicht-Scope
- In Scope:
  - PDF Upload und Validierung, deterministische Textextraktion, strukturierte Analyse, Streamlit UI. Quelle: `README.md`, `docs/00_overview/PROJECT_OVERVIEW.md`
  - Synthetic Data fuer Tests und Evaluation (Ground Truth). Quelle: `src/data_synth/`, `tests/fixtures/synth/`
  - Lokale Ingestion externer Datensaetze (Kaggle ZIPs, kein Download im Code). Quelle: `scripts/data/ingest_kaggle_zips.py`, `data/external/kaggle/_README.md`
- Out of Scope:
  - Keine persistente Speicherung realer CVs, kein produktionsreifer ATS-Ersatz, kein Black-Box-Scoring. Quelle: `README.md`, `docs/00_overview/PROJECT_OVERVIEW.md`
  - Keine Rohdaten im Repo (ZIPs/unzipped ignoriert). Quelle: `.gitignore`
  - Keine realen personenbezogenen Daten im Repo. Quelle: `docs/knowledge_base/de/08_synthetic_data_generation.md`, `docs/knowledge_base/en/08_synthetic_data_generation.md`

## 3) Architektur & Komponenten (repo-basiert)
- High-level Architektur:
  - Streamlit UI -> Upload/Validation -> PDF-Verarbeitung -> Analyse/Extraktion -> Matching. Quelle: `frontend/streamlit_app.py`, `src/utils/validation.py`, `src/core/`
  - Externe Daten: ZIPs -> Unzip -> Adapter -> Canonical JSONL -> Training/Eval. Quelle: `scripts/data/ingest_kaggle_zips.py`, `src/data_ingest/`
- Komponenten/Module (Pfad -> Verantwortung):
  - `frontend/streamlit_app.py`: UI, Upload, Anzeige der Extraktions- und Matching-Ergebnisse.
  - `src/core/matcher.py`: Regelbasiertes Matching (FR-007) + Hybrid ML gated.
  - `src/data_ingest/registry.py`: Dataset Registry Loader.
  - `src/data_ingest/adapters/`: Dataset-spezifische Adapter (Kaggle).
  - `scripts/data/ingest_kaggle_zips.py`: ZIP Ingestion -> JSONL.
  - `scripts/evaluate/evaluate_matching.py`: ML Evaluation und Bias Checks.
  - `scripts/train/train_from_processed.py`: Training aus processed JSONL (lokale Artifacts, ignored).

## 4) Aktuelle Implementierung (was existiert wirklich)
- Build/Run:
  - Lokales Setup via Python 3.12+, venv, `pip install -r requirements.txt`, Start via Streamlit. Quelle: `docs/00_overview/PROJECT_OVERVIEW.md`, `README.md`
- Tests/Qualitaet:
  - Unit- und Integrationstests in `tests/`. Quality Gates definieren ruff + pytest + coverage. Quelle: `tests/`, `docs/03_quality/QUALITY_GATES.md`
  - Registry/Adapter Tests vorhanden. Quelle: `tests/unit/test_registry_and_adapters.py`
- CI/CD:
  - GitHub Actions Workflow: Lint (ruff) + Tests (pytest) inkl. Coverage Report. Quelle: `.github/workflows/ci.yml`
- Dokumentation:
  - Knowledge Base (DE/EN): `docs/knowledge_base/`
  - Externe Datenquellen und Pipeline-Standard dokumentiert. Quelle: `docs/knowledge_base/en/external_data_sources.md`, `docs/knowledge_base/en/data_pipeline_standard.md`
- Konfiguration (ohne Secrets):
  - Abhaengigkeiten in `requirements.txt`. Quelle: `requirements.txt`
  - Model Artifacts in `models/` (ignored). Quelle: `.gitignore`

## 5) Backlog: Offene Punkte & naechste Schritte
### Top Next Steps (max 10)
1. Kaggle ZIPs ingestieren und Registry-Eintraege mit realen Lizenzdetails vervollstaendigen. Quelle: `data/processed/registry.json`, `docs/knowledge_base/en/07_data_sources_and_licensing.md`
2. Adapter-Logik anhand realer Dateiformate validieren/erweitern. Quelle: `src/data_ingest/adapters/`
3. Evaluation mit processed Kaggle-Daten ausfuehren (sofern Labels vorhanden). Quelle: `scripts/evaluate/evaluate_matching.py`
4. Pairing-Strategie fuer cv_only/jd_only Datensaetze definieren (optional). Quelle: `docs/knowledge_base/en/data_pipeline_standard.md`

### Risiken / Blocker
- Lizenz/PII-Status externer Datensaetze ist noch unklar. Quelle: `docs/knowledge_base/en/07_data_sources_and_licensing.md`
- Kaggle-Formate variieren stark; Adapter muessen je Dataset validiert werden. Quelle: `src/data_ingest/adapters/`
- ML Evaluation benoetigt Embedding-Modelle (Download/Runtime). Quelle: `src/core/ml/embedding_model.py`

## 6) To Clarify (Unbekannt im Repo)
- Konkrete Kaggle-URLs und Lizenztexte pro Dataset (Status: restricted bis verifiziert). Quelle: `docs/knowledge_base/en/07_data_sources_and_licensing.md`
- Welche externen Datensaetze wirklich fuer Training genutzt werden sollen. Quelle: `docs/04_evaluation/EVALUATION_PLAN.md`
- Deployment-Ziele fuer Demo-Hosting oder bleibt alles lokal? Quelle: `docs/00_overview/PROJECT_STATE.md`

## 7) Repo-Referenzen (wichtigste Dateien)
- README: `README.md`
- Projektueberblick: `docs/00_overview/PROJECT_OVERVIEW.md`
- Projektstatus: `docs/00_overview/PROJECT_STATE.md`
- Anforderungen: `docs/01_requirements/FR.en.md`
- NFR: `docs/01_requirements/NFR.en.md`
- Traceability: `docs/01_requirements/TRACEABILITY.en.md`
- Governance: `docs/03_quality/DEFINITION_OF_DONE.md`, `docs/03_quality/CHANGE_CONTROL.md`, `docs/03_quality/REVIEW_ACCEPTANCE.md`
- Architektur/ADRs: `docs/02_architecture/ADR/ADR-001-streamlit-mvp.md`, `docs/02_architecture/ADR/ADR-002-ml-matching.md`
- Quality Gates: `docs/03_quality/QUALITY_GATES.md`
- Evaluation Plan: `docs/04_evaluation/EVALUATION_PLAN.md`
- Evaluation Results: `docs/04_evaluation/EVALUATION_RESULTS.md`
- Explainable Scoring Spec: `docs/03_quality/EXPLAINABLE_SCORING_SPEC.md`
- Knowledge Base: `docs/knowledge_base/`
- External Data Sources: `docs/knowledge_base/en/external_data_sources.md`
- Data Pipeline Standard: `docs/knowledge_base/en/data_pipeline_standard.md`
- PDF Report Layout: `docs/knowledge_base/en/pdf_report_layout.md`
- Registry: `data/processed/registry.json`
- Ingestion Script: `scripts/data/ingest_kaggle_zips.py`
- Adapters: `src/data_ingest/adapters/`
- Tests: `tests/`
