# ATS CV Scorer - Phasenplan & Skill-Orchestrierung

Statusgrundlage: Project Snapshot `docs/project_state/2026-01-21/122540_project_snapshot.md`.
Hinweis: Status in diesem Plan reflektiert den Snapshot, nicht spaetere Aenderungen.

## 1) Gesamt-Phasenuebersicht
| Phase | Name | Ziel | Status |
|-------|------|------|--------|
| Phase 0 | Projektgrundlagen | Repo, Scope, Privacy, Basis-Dokumentation | erledigt |
| Phase 1 | Requirements & Governance | Anforderungen, Traceability, Qualitaets- und Evaluationsregeln | erledigt |
| Phase 2 | Architektur & Design | Architekturentscheidungen und ADRs | erledigt |
| Phase 3 | Implementierung | Kernmodule, Matching, UI | in Arbeit |
| Phase 4 | Qualitaet & Evaluation | Tests/CI, Evaluation | in Arbeit |
| Phase 5 | Reflektion & Portfolio | Projektkontext, Lern- und Portfolio-Artefakte | offen |

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

## 4) Phase 2 - Architektur & Design (ERLEDIGT)
### Ziel
Architekturentscheidungen dokumentieren und begruenden.
### Rollen
Software Architect, Tech Lead
### Aufgaben
| Aufgabe | Rolle | Status | Begruendung | Referenz |
|---------|-------|--------|-------------|----------|
| Streamlit als MVP UI entscheiden (ADR-001) | Software Architect | erledigt | ADR dokumentiert | `docs/02_architecture/ADR/ADR-001-streamlit-mvp.md` |
| ML-Matching Plan dokumentieren (ADR-002) | Software Architect | erledigt | ADR dokumentiert (Proposed) | `docs/02_architecture/ADR/ADR-002-ml-matching.md` |
### Abschlusskriterien
- ADRs sind dokumentiert und referenzierbar.

## 5) Phase 3 - Implementierung (IN ARBEIT)
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
| Streamlit UI fuer Upload/Preview | Frontend Engineer | in Arbeit | UI vorhanden, Status laut Project State | `frontend/streamlit_app.py`, `docs/00_overview/PROJECT_STATE.md` |
### Abschlusskriterien
- FR-001 bis FR-007 sind implementiert und getestet.
- UI ist funktionsfaehig fuer Upload, Preview und Matching.

## 6) Phase 4 - Qualitaet & Evaluation (IN ARBEIT)
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
| Evaluation ausfuehren und Ergebnisse dokumentieren | Evaluation Lead | offen | Keine Ergebnisse im Repo | Unbekannt im Repo |
### Abschlusskriterien
- Tests und CI laufen stabil.
- Evaluationsergebnisse sind dokumentiert.

## 7) Phase 5 - Reflektion & Portfolio (OFFEN)
### Ziel
Projekt als Lern- und Portfolio-Artefakt abschliessen.
### Rollen
Learning Engineer, Projektowner
### Aufgaben
| Aufgabe | Rolle | Status | Begruendung | Referenz |
|---------|-------|--------|-------------|----------|
| Projekt-Status-Snapshot erstellen und pflegen | Learning Engineer | erledigt | Snapshot-Dateien vorhanden | `docs/project_state/` |
| Lern- und Entscheidungsnarrativ dokumentieren | Learning Engineer | offen | Kein Narrativ im Repo | Unbekannt im Repo |
| Portfolio-Zusammenfassung erstellen | Projektowner | offen | Keine Portfolio-Datei im Repo | Unbekannt im Repo |
### Abschlusskriterien
- Aktueller Snapshot ist vorhanden.
- Lern- und Portfolio-Artefakte sind dokumentiert.

---

# Skill: Project Phase Planner
Siehe `.codex/skills/project-phase-planner/SKILL.md`.

# Skill: Project Orchestration
Siehe `.codex/skills/project-orchestration/SKILL.md`.

---

# Ergaenzung bestehender Skills
Jeder Skill enthaelt eine Sektion `## Phasenbezug` mit Aufgaben und Status.
