# Project State (2026-01-21)

## Status Summary
- Phase: MVP (Case Study)
- Gesamtstatus: stabil, Scope klar
- Letztes Update: 2026-01-21

## Erledigt
- Projektueberblick und Scope dokumentiert
- Requirements (FR/NFR) und Traceability angelegt
- ADR-001 fuer Streamlit MVP festgelegt
- Quality Gates und Evaluation Plan dokumentiert
- Definition of Done, Change Control und Review/Abnahme dokumentiert
- Requirement-Qualitaetsstandard, Traceability-Regeln und Scope-Guardrails definiert
- Project Snapshots fuer Kontextweitergabe angelegt
- Codex Skills fuer Requirements, Architektur, Kernmodule, Tests/CI und Snapshots dokumentiert
- Knowledge Base (DE/EN) angelegt und verlinkt
- Phase 0 formal signoff erstellt
- Basisstruktur im Repo (frontend/src/tests/docs)
- FR-002 Textextraktion (deterministisch) umgesetzt
- FR-003 CV-Strukturanalyse umgesetzt
- Tests fuer Extraktion und Strukturanalyse vorhanden
- FR-004 Skill-Extraktion und Kategorisierung umgesetzt
- Tests fuer Skill-Extraktion vorhanden
- FR-005 ATS-Recruiter-Kriterien aus CV extrahiert
- FR-006 JD Parsing umgesetzt (DE/EN)
- FR-007 Baseline Matching mit Explainability umgesetzt
- Tests fuer ATS-Extraktion, JD Parsing und Matching vorhanden
- Streamlit UI fuer Upload/Preview implementiert
- Optionales Hybrid-ML-Matching implementiert (Baseline bleibt Default)

## In Arbeit
- Evaluation ausfuehren und Ergebnisse dokumentieren
- Lern- und Portfolio-Artefakte mit Evaluationsergebnissen vervollstaendigen
- ML-Matching evaluieren (Ranking/F1)

## Naechste Schritte
- Explainable Scoring modellieren
- ML-Matching Roadmap evaluieren
- Traceability zu neuen Anforderungen erweitern
- Evaluationsergebnisse gem. `docs/04_evaluation/EVALUATION_PLAN.md` erfassen

## Risiken / Blocker
- PDF-Parsing kann variieren (Library/Platform)
- Datenqualitaet von CVs heterogen
- Scope Drift Richtung Produkt statt Case Study

## Entscheidungen
- Fokus auf Privacy-by-Design, keine Persistenz
- Deterministische Verarbeitung priorisiert vor ML-Experimenten

## Offene Fragen
- Welche Skill-Extraktion (Regeln vs. spaetere ML-Phase)?
- Welche Bewertungsmetrik fuer Erklaerbarkeit?

## Verweise
- Phasenplan & Skill-Orchestrierung: `docs/codex_skills/PHASE_PLAN.md`
- Skill-Uebersicht: `docs/codex_skills/OVERVIEW.md`
- Knowledge Base: `docs/knowledge_base/`
- Phase-1-Abschlussreport: `docs/codex_skills/PHASE_1_REPORT.md`
