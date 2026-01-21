# Project Overview (Case Study)

## Problem Statement
Recruiters and candidates need transparent, explainable CV scoring. Most ATS
systems are opaque, and CV data handling is often unclear. This project is a
documented engineering case study that focuses on requirements, traceability,
and privacy-first processing.

## Goals
- deliver deterministic PDF text extraction as a foundation
- build a reproducible pipeline for CV structure and skill analysis
- provide clear documentation and traceability for portfolio review
- keep privacy constraints explicit and enforced

## Non-Goals
- no production-grade ATS replacement
- no persistent storage of CV data
- no opaque or unexplainable scoring

## Scope (MVP)
- upload and validate PDF CVs (type and size)
- extract text with deterministic behavior
- expose metadata and preview in a Streamlit UI

## Privacy-by-Design
- processing is session-based
- temporary files are removed after use
- no storage or retention of CV contents

## How to Run (Local)
Prereqs: Python 3.12+, Windows PowerShell

```powershell
py -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe -m pytest -q
.venv\Scripts\python.exe -m ruff check .
.venv\Scripts\python.exe -m streamlit run frontend\streamlit_app.py
```

## Optional ML Matching
Enable the hybrid ML matcher (semantic similarity + feature fusion):

```powershell
$env:MATCHING_STRATEGY="hybrid_ml"
.venv\Scripts\python.exe -m streamlit run frontend\streamlit_app.py
```

Notes:
- The baseline matcher remains the default.
- ML downloads the embedding model on first use.

## Repo Map
- `frontend/` Streamlit UI
- `src/core/` core processing (PDF extraction)
- `src/utils/` validation and helpers
- `tests/` unit and integration tests
- `docs/` requirements, architecture, quality, evaluation
- `docs/codex_skills/PHASE_PLAN.md` phasenbasierter Projektplan
- `docs/codex_skills/OVERVIEW.md` Skill-Uebersicht
