# Projektueberblick (Case Study)

## Problemstellung
Recruiter und Kandidaten brauchen transparente, erklaerbare CV-Scorings. Viele
ATS-Systeme sind intransparent, und der Umgang mit CV-Daten ist oft unklar.
Dieses Projekt ist eine dokumentierte Engineering Case Study mit Fokus auf
Requirements, Traceability und Privacy-by-Design.

## Ziele
- deterministische PDF-Textextraktion als Basis
- reproduzierbare Pipeline fuer Struktur- und Skill-Analyse
- klare Dokumentation und Traceability fuer Portfolio-Reviews
- explizite Privacy-Constraints

## Nicht-Ziele
- kein produktionsreifer ATS-Ersatz
- keine persistente Speicherung von CV-Daten
- kein intransparentes Black-Box-Scoring

## Scope (MVP)
- PDF-Upload und Validierung (Typ und Groesse)
- Textextraktion mit deterministischem Verhalten
- Streamlit-UI mit Metadaten und Preview

## Privacy-by-Design
- Verarbeitung nur in der Session
- temporaere Dateien werden entfernt
- keine Speicherung oder Aufbewahrung von CV-Inhalten

## Lokal ausfuehren
Voraussetzungen: Python 3.12+, Windows PowerShell

```powershell
py -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe -m pytest -q
.venv\Scripts\python.exe -m ruff check .
.venv\Scripts\python.exe -m streamlit run frontend\streamlit_app.py
```

## Repo Map
- `frontend/` Streamlit UI
- `src/core/` Kernlogik (PDF-Extraktion)
- `src/utils/` Validierung und Helfer
- `tests/` Unit- und Integrationstests
- `docs/` Requirements, Architektur, Qualitaet, Evaluation
