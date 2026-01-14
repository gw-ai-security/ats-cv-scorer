# Project State (2026-01-14)

## Status Summary
- Phase: MVP (Case Study)
- Gesamtstatus: stabil, Scope klar
- Letztes Update: 2026-01-14

## Erledigt
- Projektueberblick und Scope dokumentiert
- Requirements (FR/NFR) und Traceability angelegt
- ADR-001 fuer Streamlit MVP festgelegt
- Quality Gates und Evaluation Plan dokumentiert
- Basisstruktur im Repo (frontend/src/tests/docs)

## In Arbeit
- deterministische PDF-Textextraktion (FR-002 Phase 1)
- Streamlit UI fuer Upload/Preview
- Tests fuer Extraktion und Validierung

## Naechste Schritte
- Struktur- und Skill-Analyse (geplant)
- Explainable Scoring Modellieren
- Traceability zu neuen Anforderungen erweitern

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
