# ATS CV Scorer - Phasenplan & Skill-Orchestrierung

Statusgrundlage: Project Snapshot `docs/project_state/2026-01-21/144012_project_snapshot.md`.
Hinweis: Status in diesem Plan reflektiert den Snapshot, nicht spaetere Aenderungen.

## 1) Gesamt-Phasenuebersicht
| Phase | Name | Ziel | Status |
|-------|------|------|--------|
| Phase 0 | Projektgrundlagen | Repo, Scope, Privacy, Basis-Dokumentation | erledigt |
| Phase 1 | Requirements & Governance | Anforderungen, Traceability, Qualitaets- und Evaluationsregeln | erledigt |
| Phase 2 | ML Integration & Demo Readiness | Hybrid ML, Explainability, Evaluation Gate, UI Demo | erledigt |
| Phase 3 | Implementierung | Kernmodule, Matching, UI | erledigt |
| Phase 4 | Qualitaet & Evaluation | Tests/CI, Evaluation | erledigt |
| Phase 5 | Reflektion & Portfolio | Projektkontext, Lern- und Portfolio-Artefakte | in Arbeit |
| vNext | External Data & Reporting | Kaggle Ingestion, Externe Evaluation, Exports, Demo | in Arbeit |

## 2) Phase 0 - Projektgrundlagen (ERLEDIGT)
### Ziel
Grundlagen, Scope und Privacy-by-Design im Repo verankern.
### Rollen
Projektowner, Tech Lead
### Aufgaben
| Aufgabe | Rolle | Status | Begruendung | Referenz |
|---------|-------|--------|-------------|----------|
| Projektueberblick und Scope dokumentieren | Projektowner | erledigt | Dokument existiert | `docs/00_overview/PROJECT_OVERVIEW.md` |
| Repo-Basisstruktur anlegen (docs/src/tests/frontend) | Tech Lead | erledigt | Struktur im Repo dokumentiert | `docs/00_overview/PROJECT_STATE.md` |
| Privacy-by-Design Grundsaetze festhalten | Projektowner | erledigt | Privacy-Abschnitte dokumentiert | `README.md`, `docs/00_overview/PROJECT_OVERVIEW.md` |
| Phase-0-Signoff erstellen | Projektowner | erledigt | Signoff-Datei vorhanden | `docs/codex_skills/PHASE_0_SIGNOFF.md` |
### Abschlusskriterien
- Scope und Privacy sind dokumentiert.
- Basisstruktur ist vorhanden.

## 3) Phase 1 - Requirements & Governance (ERLEDIGT)
### Ziel
Anforderungen und Governance nachvollziehbar dokumentieren.
### Rollen
Requirements Engineer, QA Lead
### Aufgaben
| Aufgabe | Rolle | Status | Begruendung | Referenz |
|---------|-------|--------|-------------|----------|
| FR/NFR definieren und versionieren | Requirements Engineer | erledigt | FR/NFR Dokumente vorhanden | `docs/01_requirements/FR.en.md`, `docs/01_requirements/NFR.en.md` |
| Traceability-Matrix pflegen | Requirements Engineer | erledigt | Matrix vorhanden | `docs/01_requirements/TRACEABILITY.en.md` |
| Quality Gates definieren | QA Lead | erledigt | Quality Gates dokumentiert | `docs/03_quality/QUALITY_GATES.md` |
| Evaluation Plan definieren | QA Lead | erledigt | Evaluation Plan dokumentiert | `docs/04_evaluation/EVALUATION_PLAN.md` |
| Definition of Done dokumentieren | QA Lead | erledigt | Dokument vorhanden | `docs/03_quality/DEFINITION_OF_DONE.md` |
| Change Control Regeln definieren | QA Lead | erledigt | Dokument vorhanden | `docs/03_quality/CHANGE_CONTROL.md` |
| Review- und Abnahmeprozess definieren | QA Lead | erledigt | Dokument vorhanden | `docs/03_quality/REVIEW_ACCEPTANCE.md` |
| Requirement-Qualitaetsstandard definieren | Requirements Engineer | erledigt | Dokument vorhanden | `docs/01_requirements/REQUIREMENTS_QUALITY.md` |
| Traceability-Regeln definieren | Requirements Engineer | erledigt | Dokument vorhanden | `docs/01_requirements/TRACEABILITY_RULES.md` |
| Scope- und Drift-Guardrails definieren | Projektowner | erledigt | Dokument vorhanden | `docs/01_requirements/SCOPE_GUARDRAILS.md` |
### Abschlusskriterien
- FR/NFR und Traceability sind vorhanden.
- Quality Gates und Evaluation Plan sind dokumentiert.

## 4) Phase 2 - ML Integration & Demo Readiness (ERLEDIGT)
### Ziel
Hybrid ML optional integrieren, Explainability sicherstellen, Evaluation Gate und UI Demo absichern.
### Rollen
Software Architect, ML Engineer, Frontend Engineer
### Aufgaben
| Aufgabe | Rolle | Status | Begruendung | Referenz |
|---------|-------|--------|-------------|----------|
| Hybrid ML Matcher integrieren (optional) | ML Engineer | erledigt | Hybrid-Strategie vorhanden, Baseline bleibt Default | `src/core/matcher.py`, `src/core/ml/` |
| Evaluation Gate fuer ML implementieren | Software Architect | erledigt | Gate in Config + UI dokumentiert | `src/utils/config.py`, `frontend/streamlit_app.py`, `docs/04_evaluation/EVALUATION_RESULTS.md` |
| Explainable Scoring Spezifikation finalisieren | Software Architect | erledigt | Spezifikation dokumentiert | `docs/03_quality/EXPLAINABLE_SCORING_SPEC.md` |
| Streamlit Demo-UI fuer Strategy + Explainability | Frontend Engineer | erledigt | Toggle + Breakdown vorhanden | `frontend/streamlit_app.py` |
| ADR-002 aktualisieren (Evaluation Gate, Explainability) | Software Architect | erledigt | ADR aktualisiert | `docs/02_architecture/ADR/ADR-002-ml-matching.md` |
### Abschlusskriterien
- Hybrid ML ist optional und gated.
- Explainability ist dokumentiert und in der UI sichtbar.
- ADR-002 reflektiert die Umsetzung.

## 5) Phase 3 - Implementierung (ERLEDIGT)
### Ziel
Kernfunktionalitaet implementieren und integrieren.
### Rollen
Backend Engineer, Frontend Engineer
### Aufgaben
| Aufgabe | Rolle | Status | Begruendung | Referenz |
|---------|-------|--------|-------------|----------|
| PDF Upload und Validierung (FR-001) | Backend Engineer | erledigt | Implementierung und Test vorhanden | `src/utils/validation.py`, `tests/integration/test_upload_validation.py` |
| PDF Textextraktion (FR-002) | Backend Engineer | erledigt | Implementierung und Test vorhanden | `src/core/pdf_processor.py`, `tests/unit/test_pdf_processor.py` |
| CV-Strukturanalyse (FR-003) | Backend Engineer | erledigt | Implementierung und Test vorhanden | `src/core/cv_analyzer.py`, `tests/unit/test_cv_sections.py` |
| Skill-Extraktion (FR-004) | Backend Engineer | erledigt | Implementierung und Test vorhanden | `src/core/skill_extractor.py`, `tests/unit/test_skill_extractor.py` |
| ATS-Kriterien-Extraktion (FR-005) | Backend Engineer | erledigt | Implementierung und Test vorhanden | `src/core/ats_criteria_extractor.py`, `tests/unit/test_ats_criteria.py` |
| JD Parsing (FR-006) | Backend Engineer | erledigt | Implementierung und Test vorhanden | `src/core/jd_parser.py`, `tests/unit/test_jd_parser.py` |
| Baseline Matching (FR-007) | Backend Engineer | erledigt | Implementierung und Test vorhanden | `src/core/matcher.py`, `tests/unit/test_matcher.py` |
| Streamlit UI fuer Upload/Preview | Frontend Engineer | erledigt | UI implementiert (Upload, Preview, Matching) | `frontend/streamlit_app.py` |
| Optionales Hybrid-ML-Matching implementieren | Backend Engineer | erledigt | ML-Module vorhanden, Baseline bleibt Default | `src/core/ml/`, `src/core/matcher.py` |
### Abschlusskriterien
- FR-001 bis FR-007 sind implementiert und getestet.
- UI ist funktionsfaehig fuer Upload, Preview und Matching.

## 6) Phase 4 - Qualitaet & Evaluation (ERLEDIGT)
### Ziel
Qualitaet sichern und Evaluation messbar machen.
### Rollen
QA Engineer, Evaluation Lead
### Aufgaben
| Aufgabe | Rolle | Status | Begruendung | Referenz |
|---------|-------|--------|-------------|----------|
| Testsuite und CI etablieren | QA Engineer | erledigt | Tests und CI Workflow vorhanden | `tests/`, `.github/workflows/ci.yml` |
| Quality Gates dokumentieren | QA Engineer | erledigt | Dokument vorhanden | `docs/03_quality/QUALITY_GATES.md` |
| Evaluation Plan definieren | Evaluation Lead | erledigt | Dokument vorhanden | `docs/04_evaluation/EVALUATION_PLAN.md` |
| Evaluation ausfuehren und Ergebnisse dokumentieren | Evaluation Lead | erledigt | Ergebnisse dokumentiert | `docs/04_evaluation/EVALUATION_RESULTS.md` |
| ML-Matching evaluieren (Ranking/F1) | Evaluation Lead | erledigt | Baseline/Hybrid dokumentiert, Ranking nicht anwendbar | `docs/04_evaluation/EVALUATION_RESULTS.md` |
### Abschlusskriterien
- Tests und CI laufen stabil.
- Evaluationsergebnisse sind dokumentiert.

## 7) Phase 5 - Reflektion & Portfolio (IN ARBEIT)
### Ziel
Projekt als Lern- und Portfolio-Artefakt abschliessen.
### Rollen
Learning Engineer, Projektowner
### Aufgaben
| Aufgabe | Rolle | Status | Begruendung | Referenz |
|---------|-------|--------|-------------|----------|
| Projekt-Status-Snapshot erstellen und pflegen | Learning Engineer | erledigt | Snapshot-Dateien vorhanden | `docs/project_state/` |
| Lern- und Entscheidungsnarrativ dokumentieren | Learning Engineer | in Arbeit | Dokument angelegt, Ergebnisdaten fehlen | `docs/05_reflection/LEARNING_NARRATIVE.md` |
| Portfolio-Zusammenfassung erstellen | Projektowner | in Arbeit | Dokument angelegt, Evaluationsergebnisse fehlen | `docs/05_reflection/PORTFOLIO_SUMMARY.md` |
### Abschlusskriterien
- Aktueller Snapshot ist vorhanden.
- Lern- und Portfolio-Artefakte sind dokumentiert.

## 8) vNext - External Data & Reporting (IN ARBEIT)
### Ziel
External Data Support, Reporting-Exports und Demo-Flow auf Release-Niveau.
### Rollen
Data Engineer, ML Engineer, Frontend Engineer, QA Lead
### Aufgaben
| Aufgabe | Rolle | Status | Begruendung | Referenz |
|---------|-------|--------|-------------|----------|
| Local ZIP Ingestion + Registry | Data Engineer | in Arbeit | Pipeline und Registry implementiert | `scripts/data/ingest_kaggle_zips.py`, `data/processed/registry.json` |
| External Data Quality + PII Scan | QA Lead | in Arbeit | Reports erstellt, weitere Validierung offen | `docs/04_evaluation/EXTERNAL_DATA_QUALITY.md`, `docs/04_evaluation/PII_SCAN_REPORT.md` |
| External Evaluation Summary | Evaluation Lead | in Arbeit | Baseline-Run dokumentiert | `docs/04_evaluation/EVALUATION_RESULTS_EXTERNAL.md` |
| Report Exports (PDF/JSON/MD) | Frontend Engineer | in Arbeit | Exports integriert | `src/core/report_export.py`, `frontend/streamlit_app.py` |
### Abschlusskriterien
- External Dataset Workflow ist reproduzierbar dokumentiert.
- Reports sind exportierbar und UI-Demo laeuft stabil.

---

# Skill: Project Phase Planner
Siehe `.codex/skills/project-phase-planner/SKILL.md`.

# Skill: Project Orchestration
Siehe `.codex/skills/project-orchestration/SKILL.md`.

---

# Ergaenzung bestehender Skills
Jeder Skill enthaelt eine Sektion `## Phasenbezug` mit Aufgaben und Status.
