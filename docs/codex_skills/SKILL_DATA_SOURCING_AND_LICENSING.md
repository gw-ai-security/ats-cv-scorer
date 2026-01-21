# Skill: Data Sourcing & Licensing Checklist

## Zweck
Sicherstellen, dass externe Datenquellen (z. B. Kaggle, O*NET, Synthetic Data) vor Nutzung strukturiert bewertet, dokumentiert und in der Knowledge Base (DE/EN) nachvollziehbar festgehalten werden.

## Wann anwenden
- Vor jeder neuen externen Datenquelle (Training, Evaluation, Tests).
- Bei Aenderung der Lizenzbedingungen oder des Nutzungszwecks.
- Bei Erweiterung von bestehenden Datenquellen (neue Versionen, Subsets).

## Vorgehen (Schritt-fuer-Schritt)
1) Knowledge-Base-first: Pruefe `docs/knowledge_base/de/07_data_sources_and_licensing.md` und `docs/knowledge_base/en/07_data_sources_and_licensing.md` auf bestehende Eintraege.
2) Sammle nur dokumentierbare Fakten zur Quelle (Name, URL, Typ, Lizenz, Zweck, Speicherstrategie) ohne personenbezogene Daten zu speichern.
3) Fuehre die Licensing- und Compliance-Checklist pro Quelle aus (siehe KB-Template).
4) Entscheide den Status `approved`, `restricted` oder `rejected` inkl. Begruendung.
5) Dokumentiere die Quelle gespiegelt in DE/EN in der Knowledge Base.
6) Verlinke relevante Artefakte (Evaluation Plan, ML ADR, Project Snapshot-Verzeichnis).

## Dokumentationsergebnis
- Jede Quelle hat eine explizite Entscheidung + Begruendung.
- Keine Datensaetze werden im Repo gespeichert; nur Referenzen und Verarbeitungslogik.
- Wenn Lizenz unklar: Status = `restricted` und Begruendung dokumentieren.

## Qualitaetskriterien
- **Approved:** Lizenz erlaubt beabsichtigte Nutzung, keine unzulaessige PII, Scope passt, Speicherstrategie konform.
- **Restricted:** Lizenz oder Datenschutz unklar, nur Test-/Evaluationsnutzung erlaubt, klare Limits dokumentiert.
- **Rejected:** Lizenz untersagt Nutzung, PII-Risiko nicht beherrschbar, Scope Drift oder Zweckkonflikt.

## Repo-Referenzen
- `docs/knowledge_base/de/07_data_sources_and_licensing.md`
- `docs/knowledge_base/en/07_data_sources_and_licensing.md`
- `docs/04_evaluation/EVALUATION_PLAN.md`
- `docs/02_architecture/ADR/ADR-002-ml-matching.md`
- `docs/project_state/`

## Last Updated
2026-01-21 14:08:05 (Local)
