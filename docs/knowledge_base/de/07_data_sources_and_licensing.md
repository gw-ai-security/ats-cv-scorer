# Data Sources & Licensing (DE)

## Zweck
Dokumentation externer Datenquellen inkl. Lizenz- und Compliance-Bewertung vor Nutzung im Projekt.

## Checklist (pro Datenquelle)
- Name der Quelle:
- URL:
- Art der Daten (CV, JD, Skills, Synthetic):
- Lizenztyp (z. B. CC, Kaggle License, Public Domain):
- Nutzungszweck im Projekt (Training, Evaluation, Tests):
- Speicherung (lokal, transient, nicht gespeichert):
- Risiken (PII, Bias, Scope Drift):
- Entscheidung: approved / restricted / rejected:
- Begruendung:

## Entscheidungslogik (Kurzfassung)
- **approved**: Lizenz passt zum Zweck, keine unzulaessige PII, Scope konform, Speicherstrategie erlaubt.
- **restricted**: Lizenz/Datenschutz unklar oder nur eingeschraenkte Nutzung; nur Test/Evaluation mit klaren Limits.
- **rejected**: Lizenz untersagt Nutzung, PII-Risiko nicht beherrschbar, oder Scope Drift.
- Wenn Lizenz unklar ist: `restricted` und Begruendung dokumentieren.

## Kaggle Local ZIP Workflow
- ZIPs nach `data/external/kaggle/_incoming_zips/` legen (git-ignored).
- Entpacken nach `data/external/kaggle/_unzipped/` (git-ignored).
- `scripts/data/ingest_kaggle_zips.py` ausfuehren -> `data/processed/datasets/<dataset_id>.jsonl`.
- Datasets in `data/processed/registry.json` registrieren.
- Aktuelle Dataset-IDs (restricted bis Lizenz verifiziert):
  - `ats_scoring_dataset`
  - `resume_job_matching`
  - `resume_data_ranking`
  - `job_descriptions_2025`
  - `job_skill_set`

### Registry Felder (Compliance)
- `source_url`: Dataset-URL (unknown bis verifiziert).
- `license_label`: explizite Lizenz (Default `unknown`).
- `license_url`: Link zu Lizenz/Terms (optional; Default `unknown`).
- `usage_status`: `restricted`, bis Lizenz + PII Status dokumentiert sind.
- `dataset_type`: `paired|cv_only|jd_only|skills_only` fuer Verarbeitung.

### Bedeutung von usage_status
- `restricted`: Lizenz/PII nicht verifiziert; nur lokale Analyse mit klaren Limits.
- `approved_local_only`: Lizenz verifiziert, aber nur lokale Nutzung; keine Weitergabe.
- `approved`: Lizenz verifiziert und fuer Projekt freigegeben (keine Rohdaten im Repo).

### Lizenzinfos aktualisieren
1) `data/processed/registry_licenses_overrides.json` bearbeiten.
2) `scripts/data/update_registry_licenses.py` ausfuehren.
3) `data/processed/REGISTRY_CHANGELOG.md` pruefen.

## Aktuelle Bewertungen (initial)
### Kaggle Resume / Job Description Dataset (konkrete Quelle ausstehend)
- Name der Quelle: Kaggle Resume / Job Description (Datensatz noch nicht definiert)
- URL: TBD (dataset-spezifisch)
- Art der Daten: CV, JD
- Lizenztyp: TBD (dataset-spezifisch)
- Nutzungszweck im Projekt: Evaluation/Test (geplant)
- Speicherung: transient (kein persistenter Speicher)
- Risiken: PII, Bias, Lizenzklarheit
- Entscheidung: restricted
- Begruendung: Datensatz noch nicht ausgewaehlt; Lizenzbedingungen und PII-Status unklar.

### O*NET Skills & Occupations Data
- Name der Quelle: O*NET Skills & Occupations Data
- URL: https://www.onetcenter.org/database.html
- Art der Daten: Skills, Occupations
- Lizenztyp: TBD (Lizenzbedingungen muessen verifiziert werden)
- Nutzungszweck im Projekt: Referenz/Taxonomie
- Speicherung: lokal (nur abgeleitete Strukturen, keine Rohdaten committen)
- Risiken: Lizenzklarheit, Scope Drift
- Entscheidung: restricted
- Begruendung: Lizenzbedingungen sind noch nicht validiert und dokumentiert.

### Synthetic / Generated Data (intern)
- Name der Quelle: Synthetic / Generated Data (intern)
- URL: N/A
- Art der Daten: Synthetic
- Lizenztyp: Interne Generierung (dokumentierter Generator)
- Nutzungszweck im Projekt: Tests/Evaluation
- Speicherung: transient oder lokal (ohne PII)
- Risiken: Bias durch Prompting, Realitaetsferne
- Entscheidung: approved
- Begruendung: Prozess und Guardrails sind dokumentiert; keine PII und kontrollierte Generierung (siehe `docs/knowledge_base/de/08_synthetic_data_generation.md`).

## Beispielbewertungen (Templates)
### Kaggle Resume Dataset (Beispiel)
- Name der Quelle: Kaggle Resume Dataset (Beispiel)
- URL: https://www.kaggle.com/datasets/<dataset-name>
- Art der Daten: CV
- Lizenztyp: Unklar (Beispiel)
- Nutzungszweck im Projekt: Evaluation/Test
- Speicherung: transient (kein persistenter Speicher)
- Risiken: PII, Bias, Lizenzklarheit
- Entscheidung: restricted
- Begruendung: Lizenz und PII-Status nicht eindeutig dokumentiert; nur Testnutzung bis Klaerung.

### O*NET Skills Data (Beispiel)
- Name der Quelle: O*NET Skills Data (Beispiel)
- URL: https://www.onetcenter.org/database.html
- Art der Daten: Skills
- Lizenztyp: Unklar (Beispiel)
- Nutzungszweck im Projekt: Referenz/Taxonomie
- Speicherung: lokal (nur abgeleitete Strukturen, keine Rohdaten committen)
- Risiken: Lizenzklarheit, Scope Drift
- Entscheidung: restricted
- Begruendung: Lizenz und Nutzungsrechte muessen fuer Projektzweck validiert werden.

### Synthetic Data (Beispiel)
- Name der Quelle: Synthetic Data (Beispiel)
- URL: N/A (intern generiert)
- Art der Daten: Synthetic
- Lizenztyp: Eigene Generierung (Beispiel)
- Nutzungszweck im Projekt: Tests/Evaluation
- Speicherung: transient oder lokal (ohne PII)
- Risiken: Bias durch Prompting, Realitaetsferne
- Entscheidung: approved
- Begruendung: Keine PII, Zweck klar, Nutzung und Speicherung kontrollierbar.

## Verweise
- `docs/04_evaluation/EVALUATION_PLAN.md`
- `docs/02_architecture/ADR/ADR-002-ml-matching.md`
- `docs/knowledge_base/de/external_data_sources.md`
- `docs/project_state/`

## Last Updated
2026-01-22 20:21:30 (Local)
