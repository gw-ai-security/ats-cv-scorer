# Project Snapshot - ATS CV Scorer - 2026-01-21 12:23:24 (Local)

## 1) Kurzueberblick
- Zweck / Problem: Transparente, nachvollziehbare CV-Bewertung statt intransparenter ATS-Systeme. Quelle: `docs/00_overview/PROJECT_OVERVIEW.md`
- Zielgruppe / Nutzer: Recruiter und Kandidaten, Portfolio-Review fuer Engineering Case Study. Quelle: `docs/00_overview/PROJECT_OVERVIEW.md`, `README.md`
- Aktueller Stand in 5 Bulletpoints:
  - Knowledge Base (DE/EN) als Single Source of Truth angelegt. Quelle: `docs/knowledge_base/`
  - Governance-Artefakte fuer Phase 1 definiert (DoD, Change Control, Review, Requirements-Qualitaet, Traceability-Regeln, Scope-Guardrails). Quelle: `docs/03_quality/`, `docs/01_requirements/`
  - Phasenplan erweitert inkl. Begruendungen und Phase-0-Signoff. Quelle: `docs/codex_skills/PHASE_PLAN.md`, `docs/codex_skills/PHASE_0_SIGNOFF.md`
  - Deterministische PDF-Textextraktion umgesetzt (FR-002) inkl. Tests. Quelle: `docs/01_requirements/FR.en.md`, `src/core/pdf_processor.py`, `tests/unit/test_pdf_processor.py`
  - JD-Parsing und regelbasiertes Matching umgesetzt (FR-006/FR-007). Quelle: `docs/01_requirements/FR.en.md`, `src/core/jd_parser.py`, `src/core/matcher.py`, `tests/unit/`

## 2) Scope & Nicht-Scope
- In Scope:
  - PDF Upload und Validierung, deterministische Textextraktion, strukturierte Analyse, Streamlit UI. Quelle: `README.md`, `docs/00_overview/PROJECT_OVERVIEW.md`
- Out of Scope:
  - Keine persistente Speicherung von CVs, kein produktionsreifer ATS-Ersatz, kein Black-Box-Scoring. Quelle: `README.md`, `docs/00_overview/PROJECT_OVERVIEW.md`

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
  - `src/core/matcher.py`: Regelbasiertes Matching (FR-007).
- Datenfluesse / Integrationen:
  - Upload von CV/JD (PDF oder Text), lokale Verarbeitung, temporaere Dateien werden geloescht. Quelle: `frontend/streamlit_app.py`, `docs/00_overview/PROJECT_OVERVIEW.md`
  - Keine externen APIs/Integrationen dokumentiert. Quelle: Repo-Suche

## 4) Aktuelle Implementierung (was existiert wirklich)
- Build/Run:
  - Lokales Setup via Python 3.12+, venv, `pip install -r requirements.txt`, Start via Streamlit. Quelle: `docs/00_overview/PROJECT_OVERVIEW.md`, `README.md`
- Tests/Qualitaet:
  - Unit- und Integrationstests in `tests/`. Quality Gates definieren ruff + pytest + coverage. Quelle: `tests/`, `docs/03_quality/QUALITY_GATES.md`
- CI/CD:
  - GitHub Actions Workflow: Lint (ruff) + Tests (pytest) inkl. Coverage Report. Quelle: `.github/workflows/ci.yml`
- Dokumentation:
  - Knowledge Base (DE/EN): `docs/knowledge_base/`
  - Phasenplan & Skills: `docs/codex_skills/`
- Konfiguration (ohne Secrets):
  - Abhaengigkeiten in `requirements.txt`. Keine weiteren Konfigurationsdateien fuer Umgebungen dokumentiert. Quelle: `requirements.txt`

## 5) Backlog: Offene Punkte & naechste Schritte
### Top Next Steps (max 10)
1. Streamlit UI fuer Upload/Preview vervollstaendigen (Status: in Arbeit). Quelle: `docs/00_overview/PROJECT_STATE.md`
2. Explainable Scoring weiter modellieren. Quelle: `docs/00_overview/PROJECT_STATE.md`
3. ML-Matching Roadmap evaluieren. Quelle: `docs/00_overview/PROJECT_STATE.md`, `docs/02_architecture/ADR/ADR-002-ml-matching.md`
4. Evaluationsergebnisse dokumentieren. Quelle: `docs/04_evaluation/EVALUATION_PLAN.md`

### Risiken / Blocker
- PDF-Parsing variiert je nach Library/Platform. Quelle: `docs/00_overview/PROJECT_STATE.md`
- Datenqualitaet von CVs ist heterogen. Quelle: `docs/00_overview/PROJECT_STATE.md`
- Scope Drift Richtung Produkt statt Case Study. Quelle: `docs/01_requirements/SCOPE_GUARDRAILS.md`

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
- Knowledge Base: `docs/knowledge_base/`
- Phasenplan: `docs/codex_skills/PHASE_PLAN.md`
- Skill-Uebersicht: `docs/codex_skills/OVERVIEW.md`
- Phase-0-Signoff: `docs/codex_skills/PHASE_0_SIGNOFF.md`
- Project Snapshots: `docs/project_state/`
- CI/CD: `.github/workflows/ci.yml`
- UI: `frontend/streamlit_app.py`
- Core: `src/core/`
- Tests: `tests/`