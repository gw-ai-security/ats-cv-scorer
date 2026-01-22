# Project Snapshot - ATS CV Scorer - 2026-01-22 20:42:49 (Local)

## 1) Kurzueberblick
- Zweck / Problem: Transparente, nachvollziehbare CV-Bewertung statt intransparenter ATS-Systeme. Quelle: `docs/00_overview/PROJECT_OVERVIEW.md`
- Zielgruppe / Nutzer: Recruiter und Kandidaten, Portfolio-Review fuer Engineering Case Study. Quelle: `docs/00_overview/PROJECT_OVERVIEW.md`, `README.md`
- Aktueller Stand in 5 Bulletpoints:
  - Prompt Chain Workflow (4 Schritte) implementiert inkl. Offline-Fallback und optionalem Provider. Quelle: `src/prompt_chain/`, `frontend/streamlit_app.py`
  - Prompt Chain Ergebnisse in PDF/JSON/MD Export eingebunden. Quelle: `src/core/report_export.py`, `src/core/pdf_layout.py`, `src/core/templates/score_report.txt.j2`
  - Lizenz-Registry Workflow + Overrides + Changelog vorhanden. Quelle: `data/processed/registry_licenses_overrides.json`, `scripts/data/update_registry_licenses.py`, `data/processed/REGISTRY_CHANGELOG.md`
  - Adapter-Validation Framework mit Fixtures + Health Report. Quelle: `tests/fixtures/ingest/`, `tests/unit/test_ingest_adapters_schema.py`, `docs/04_evaluation/ADAPTER_HEALTH_REPORT.md`
  - External Evaluation Summary (baseline; hybrid optional mit Skip-Note) dokumentiert. Quelle: `docs/04_evaluation/EVALUATION_RESULTS_EXTERNAL.md`

## 2) Scope & Nicht-Scope
- In Scope:
  - Lokale Ingestion externer Datensaetze (Kaggle ZIPs, offline). Quelle: `scripts/data/ingest_kaggle_zips.py`
  - Externe Evaluation mit Quality/PII Reports und Adapter Health. Quelle: `docs/04_evaluation/`
  - Prompt Chain Workflow (Recruiter Match -> Rewrite -> ATS Check -> Interview Q&A). Quelle: `src/prompt_chain/`
- Out of Scope:
  - Keine Rohdaten im Repo (ZIPs/unzipped/processed datasets ignoriert). Quelle: `.gitignore`
  - Keine PII im Repo (nur Counts/Reports). Quelle: `docs/04_evaluation/PII_SCAN_REPORT.md`

## 3) Architektur & Komponenten (repo-basiert)
- High-level Architektur:
  - Streamlit UI -> Upload/Validation -> Analyse/Extraktion -> Matching -> Prompt Chain -> Exports. Quelle: `frontend/streamlit_app.py`, `src/core/`, `src/prompt_chain/`
- Komponenten/Module (Pfad -> Verantwortung):
  - `src/prompt_chain/`: Prompt Chain Engine, Heuristics, Provider Interface.
  - `src/core/report_export.py`: Report Payload inkl. Prompt Chain Results.
  - `scripts/data/update_registry_licenses.py`: Lizenz-Overrides fuer Registry.
  - `scripts/data/adapter_health_report.py`: Adapter Health Report.

## 4) Aktuelle Implementierung (was existiert wirklich)
- Tests/Qualitaet:
  - Prompt Chain Tests vorhanden (fallback + schema). Quelle: `tests/unit/test_prompt_chain_fallback.py`, `tests/unit/test_prompt_chain_schema.py`
  - Adapter Schema Tests vorhanden. Quelle: `tests/unit/test_ingest_adapters_schema.py`
- Dokumentation:
  - Prompt Chain Skill + KB-Seiten (DE/EN). Quelle: `docs/codex_skills/SKILL_PROMPT_CHAIN_WORKFLOW.md`, `docs/knowledge_base/en/10_prompt_chain_workflow.md`

## 5) Backlog: Offene Punkte & naechste Schritte
1. Lizenz/URL-Details pro Kaggle Dataset verifizieren und `registry_licenses_overrides.json` pflegen. Quelle: `data/processed/registry.json`
2. Hybrid ML External Eval ausfuehren, falls Embedding-Cache lokal vorhanden. Quelle: `scripts/evaluate/evaluate_matching.py`
3. Prompt Chain LLM Provider anbinden (optional, wenn API Key vorhanden). Quelle: `src/prompt_chain/providers/openai_provider.py`

## 6) Risiken / Blocker
- Kaggle-Formate variieren stark; Adapter brauchen laufende Pflege. Quelle: `src/data_ingest/adapters/`
- Hybrid ML Evaluation benoetigt Embedding-Modelle (Download/Runtime). Quelle: `src/core/ml/embedding_model.py`
- LLM Provider optional; ohne API Key bleibt Fallback aktiv. Quelle: `src/prompt_chain/providers/openai_provider.py`

## 7) Repo-Referenzen (wichtigste Dateien)
- Prompt Chain Engine: `src/prompt_chain/engine.py`
- Prompt Chain Heuristics: `src/prompt_chain/heuristics.py`
- Prompt Chain UI: `frontend/streamlit_app.py`
- Prompt Chain Skill: `docs/codex_skills/SKILL_PROMPT_CHAIN_WORKFLOW.md`
- External Evaluation Results: `docs/04_evaluation/EVALUATION_RESULTS_EXTERNAL.md`
- Adapter Health Report: `docs/04_evaluation/ADAPTER_HEALTH_REPORT.md`
