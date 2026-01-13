# ATS CV Scoring System  
Engineering Case Study – Consumer Usability & Data Science

## 🇩🇪 Projektüberblick (Deutsch)

Dieses Repository dokumentiert die Entwicklung eines **ATS CV Scoring Systems**
als **Engineering Case Study** mit Fokus auf:

- Requirements Engineering
- Data Science & NLP
- Software Architecture
- Consumer Usability
- Open Source Engineering Practices

Ziel ist **nicht** ein Produkt, sondern ein **nachvollziehbar dokumentiertes
End-to-End-Engineering-Projekt** für Portfolio- und Bewerbungszwecke.

---

## 🇬🇧 Project Overview (English)

This repository documents the development of an **ATS CV Scoring System**
as an **engineering case study**, focusing on:

- Requirements Engineering
- Data Science & NLP
- Software Architecture
- Consumer Usability
- Open Source engineering practices

The goal is **not** to build a commercial product, but a **transparent,
well-documented end-to-end engineering project** for portfolio and career use.

---

## 🎯 Engineering Objectives

- Demonstrate structured **requirements engineering**
- Design a reproducible **data science pipeline**
- Apply **NLP techniques** to real-world documents (CVs)
- Translate technical results into **user-facing insights**
- Follow **professional repository and documentation standards**

---

## 🧩 Scope (MVP)

- PDF CV upload and text extraction
- NLP-based structure & skill analysis
- ATS-style scoring (0–100)
- Explainable recommendations
- Streamlit-based user interface

---

## ⚠️ Non-Goals

- No commercial ATS replacement
- No storage of personal data
- No opaque black-box scoring

---

## 🛠 Tech Stack

- Python 3.10+
- spaCy, sentence-transformers
- scikit-learn, pandas, numpy
- Streamlit
- Docker (later phase)

---

## 📐 Architecture (High-Level)

PDF → Text Extraction → NLP Analysis → Feature Engineering → Scoring → UI

---

## 📄 Documentation

- `docs/` – Requirements, architecture, decisions
- `src/` – Core implementation
- `tests/` – Automated tests
- `frontend/` – Streamlit application

---

## 🔐 Privacy & Ethics

All processing is session-based.
No CV data is stored permanently.

---

## 🚧 Project Status

**Phase:** Setup & Requirements Engineering  
**Next Step:** Core pipeline implementation
