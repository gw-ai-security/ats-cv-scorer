# ATS CV Scorer (Engineering Case Study)

## Project Overview (EN)
This repository documents an end-to-end engineering case study for an ATS-style
CV scoring system. The goal is not a commercial product, but a transparent,
portfolio-ready project with clear requirements, traceability, and tests.

Objectives:
- demonstrate requirements engineering and traceability
- build a reproducible NLP pipeline on real-world CVs
- deliver explainable scoring and user-facing insights
- keep privacy and data handling explicit

Scope (MVP):
- PDF upload and validation
- deterministic text extraction (FR-002 Phase 1)
- structure and skill analysis (planned)
- Streamlit UI

Non-goals:
- no persistent storage of CVs
- no opaque, unexplainable scoring
- no production-grade ATS replacement

Privacy:
- all processing is session-based
- temporary files are deleted after processing

## Projektueberblick (DE)
Dieses Repository dokumentiert eine Engineering Case Study fuer ein
ATS-aehnliches CV-Scoring-System. Ziel ist kein Produkt, sondern ein
transparentes, portfolio-faehiges Projekt mit klaren Anforderungen,
Traceability und Tests.

Ziele:
- Requirements Engineering und Traceability sichtbar machen
- reproduzierbare NLP-Pipeline auf CVs
- erklaerbare Scoring-Ergebnisse
- klare Privacy-Grenzen

Scope (MVP):
- PDF-Upload und Validierung
- deterministische Textextraktion (FR-002 Phase 1)
- Struktur- und Skill-Analyse (geplant)
- Streamlit UI

Nicht-Ziele:
- keine persistente Speicherung von CVs
- kein intransparenter Black-Box-Score
- kein produktionsreifer ATS-Ersatz

Datenschutz:
- Verarbeitung nur innerhalb der Session
- temporaere Dateien werden geloescht
