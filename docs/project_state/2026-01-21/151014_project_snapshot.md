# Project Snapshot - ATS CV Scorer - 2026-01-21 15:10:14 (Local)

## 1) Kurzueberblick
- Zweck / Problem: Transparente, nachvollziehbare CV-Bewertung statt intransparenter ATS-Systeme. Quelle: `docs/00_overview/PROJECT_OVERVIEW.md`
- Zielgruppe / Nutzer: Recruiter und Kandidaten, Portfolio-Review fuer Engineering Case Study. Quelle: `docs/00_overview/PROJECT_OVERVIEW.md`, `README.md`
- Aktueller Stand in 5 Bulletpoints:
  - Evaluationsergebnisse fuer Baseline und Hybrid ML dokumentiert (synthetische Paare). Quelle: `docs/04_evaluation/EVALUATION_RESULTS.md`
  - Explainable Scoring Spec finalisiert inkl. Penalty-Signalen und Beispiele. Quelle: `docs/03_quality/EXPLAINABLE_SCORING_SPEC.md`
  - Evaluation Gate fuer Hybrid ML implementiert und UI-Strategie-Toggle angepasst. Quelle: `src/utils/config.py`, `src/core/matcher.py`, `frontend/streamlit_app.py`
  - Knowledge Base (DE/EN) um ML Evaluation Ergebnisse und Phase-2 Summary erweitert. Quelle: `docs/knowledge_base/de/09_ml_evaluation_and_bias.md`, `docs/knowledge_base/en/09_ml_evaluation_and_bias.md`, `docs/knowledge_base/de/phase_plan.md`, `docs/knowledge_base/en/phase_plan.md`
  - Phase 2 formal abgeschlossen (Signoff + Plan-Update). Quelle: `docs/codex_skills/PHASE_2_SIGNOFF.md`, `docs/codex_skills/PHASE_PLAN.md`

## 2) Scope & Nicht-Scope
- In Scope:
  - PDF Upload und Validierung, deterministische Textextraktion, strukturierte Analyse, Streamlit UI. Quelle: `README.md`, `docs/00_overview/PROJECT_OVERVIEW.md`
  - Synthetic Data fuer Tests und Evaluation (Ground Truth). Quelle: `src/data_synth/`, `tests/fixtures/synth/`
- Out of Scope:
  - Keine persistente Speicherung von CVs, kein produktionsreifer ATS-Ersatz, kein Black-Box-Scoring. Quelle: `README.md`, `docs/00_overview/PROJECT_OVERVIEW.md`
  - Keine realen personenbezogenen Daten (nur synthetisch). Quelle: `docs/knowledge_base/de/08_synthetic_data_generation.md`, `docs/knowledge_base/en/08_synthetic_data_generation.md`

## 3) Architektur & Komponenten (repo-basiert)
- High-level Architektur:
  - Streamlit UI -> Upload/Validation -> PDF-Verarbeitung -> Analyse/Extraktion -> Matching. Quelle: `frontend/streamlit_app.py`, `src/utils/validation.py`, `src/core/`
- Komponenten/Module (Pfad -> Verantwortung):
  - `frontend/streamlit_app.py`: UI, Upload, Anzeige der Extraktions- und Matching-Ergebnisse.
  - `src/utils/validation.py`: Upload-Validierung (Typ/Size) fuer FR-001.
  - `src/core/pdf_processor.py`: deterministische PDF-Textextraktion (FR-002).
  - `src/core/cv_analyzer.py`: CV-Strukturerkennung (FR-003).
  - `src/core/skill_extractor.py`: Skill-Extraktion und Kategorisierung (FR-004).
  - `src/core/ats_criteria_extractor.py`: ATS-Kriterien aus CV (FR-005).
  - `src/core/jd_parser.py`: Job-Description Parsing (FR-006).
  - `src/core/matcher.py`: Regelbasiertes Matching (FR-007) + Hybrid ML gated.
  - `src/data_synth/generator.py`: Synthetische CV/JD-Paare + Ground Truth.
  - `scripts/evaluate/evaluate_matching.py`: ML Evaluation und Bias Checks.

## 4) Aktuelle Implementierung (was existiert wirklich)
- Build/Run:
  - Lokales Setup via Python 3.12+, venv, `pip install -r requirements.txt`, Start via Streamlit. Quelle: `docs/00_overview/PROJECT_OVERVIEW.md`, `README.md`
- Tests/Qualitaet:
  - Unit- und Integrationstests in `tests/`. Quality Gates definieren ruff + pytest + coverage. Quelle: `tests/`, `docs/03_quality/QUALITY_GATES.md`
  - Synthetic Dataset Test vorhanden. Quelle: `tests/unit/test_synthetic_dataset.py`
- CI/CD:
  - GitHub Actions Workflow: Lint (ruff) + Tests (pytest) inkl. Coverage Report. Quelle: `.github/workflows/ci.yml`
- Dokumentation:
  - Knowledge Base (DE/EN): `docs/knowledge_base/`
  - Phasenplan & Skills: `docs/codex_skills/`
  - Reflektion/Portfolio: `docs/05_reflection/`
- Konfiguration (ohne Secrets):
  - Abhaengigkeiten in `requirements.txt`. Quelle: `requirements.txt`

## 5) Backlog: Offene Punkte & naechste Schritte
### Top Next Steps (max 10)
1. Explainable Scoring weiter modellieren (Penalty-Logik implementieren). Quelle: `docs/03_quality/EXPLAINABLE_SCORING_SPEC.md`
2. ML-Matching Roadmap evaluieren. Quelle: `docs/00_overview/PROJECT_STATE.md`, `docs/02_architecture/ADR/ADR-002-ml-matching.md`
3. Lern- und Portfolio-Artefakte mit Evaluationsergebnissen vervollstaendigen. Quelle: `docs/05_reflection/`

### Risiken / Blocker
- PDF-Parsing variiert je nach Library/Platform. Quelle: `docs/00_overview/PROJECT_STATE.md`
- Datenqualitaet von CVs heterogen. Quelle: `docs/00_overview/PROJECT_STATE.md`
- ML Evaluation benoetigt Embedding-Modelle (Download/Runtime). Quelle: `src/core/ml/embedding_model.py`

## 6) To Clarify (Unbekannt im Repo)
- Welche konkreten Scoring-Gewichte und Erklaerungslogiken sollen offiziell dokumentiert werden? -> wichtig fuer Nachvollziehbarkeit -> moeglich in `docs/02_architecture/` oder `docs/00_overview/`.
- Welche Beispiel- oder Evaluationsdatensaetze werden genutzt? -> wichtig fuer Evaluation Plan -> moeglich in `docs/04_evaluation/`.
- Gibt es geplante Deployment-Ziele (z.B. Demo-Hosting) oder bleibt alles lokal? -> wichtig fuer Betriebsanforderungen -> moeglich in `docs/00_overview/`.
- Gibt es definierte Security/Compliance-Anforderungen ueber Privacy hinaus? -> wichtig fuer Risikoanalyse -> moeglich in `docs/03_quality/` oder `docs/01_requirements/`.

## 7) Repo-Referenzen (wichtigste Dateien)
- README: `README.md`
- Projektueberblick: `docs/00_overview/PROJECT_OVERVIEW.md`
- Projektstatus: `docs/00_overview/PROJECT_STATE.md`
- Anforderungen: `docs/01_requirements/FR.en.md`
- NFR: `docs/01_requirements/NFR.en.md`
- Traceability: `docs/01_requirements/TRACEABILITY.en.md`
- Governance: `docs/03_quality/DEFINITION_OF_DONE.md`, `docs/03_quality/CHANGE_CONTROL.md`, `docs/03_quality/REVIEW_ACCEPTANCE.md`
- Requirements-Qualitaet: `docs/01_requirements/REQUIREMENTS_QUALITY.md`, `docs/01_requirements/TRACEABILITY_RULES.md`, `docs/01_requirements/SCOPE_GUARDRAILS.md`
- Architektur/ADRs: `docs/02_architecture/ADR/ADR-001-streamlit-mvp.md`, `docs/02_architecture/ADR/ADR-002-ml-matching.md`
- Quality Gates: `docs/03_quality/QUALITY_GATES.md`
- Evaluation Plan: `docs/04_evaluation/EVALUATION_PLAN.md`
- Evaluation Results: `docs/04_evaluation/EVALUATION_RESULTS.md`
- Explainable Scoring Spec: `docs/03_quality/EXPLAINABLE_SCORING_SPEC.md`
- Knowledge Base: `docs/knowledge_base/`
- Phasenplan: `docs/codex_skills/PHASE_PLAN.md`
- Skill-Uebersicht: `docs/codex_skills/OVERVIEW.md`
- Phase-2-Signoff: `docs/codex_skills/PHASE_2_SIGNOFF.md`
- Reflektion: `docs/05_reflection/`
- Project Snapshots: `docs/project_state/`
- CI/CD: `.github/workflows/ci.yml`
- UI: `frontend/streamlit_app.py`
- Core: `src/core/`
- Tests: `tests/`
