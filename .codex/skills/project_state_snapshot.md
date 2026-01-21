# Skill: project_state_snapshot

Zweck: Erzeuge bei jedem Run einen repo-basierten Project Snapshot als Markdown und versioniere ihn mit Timestamp. Keine Annahmen ausserhalb des Repos.

## Ablauf
1) Repository-Inventur
   - Suche zentrale Artefakte: `README.md`, `docs/00_overview/`, `docs/01_requirements/`, `docs/02_architecture/`, `docs/03_quality/`, `docs/04_evaluation/`, `.github/workflows/`, `src/`, `frontend/`, `tests/`.
   - Lies nur die relevanten Dateien. Keine externen Quellen.
2) Faktenextraktion
   - Zweck/Scope/Nicht-Scope, Status, Architektur, Module, Datenfluesse, Build/Run, Tests/Qualitaet, CI/CD.
   - Jede Aussage muss mit einem Dateipfad belegbar sein.
   - Wenn Informationen fehlen: als "Unbekannt im Repo" markieren und in "To Clarify" aufnehmen.
3) Snapshot schreiben
   - Zielpfad: `docs/project_state/YYYY-MM-DD/HHmmss_project_snapshot.md`
   - Timestamp lokale Zeit (Systemzeit).
   - Niemals vorhandene Snapshots ueberschreiben.
4) Qualitaetscheck
   - Keine unbegruendeten Behauptungen.
   - Keine Secrets ausgeben (nur Hinweis + Pfad, falls entdeckt).
   - Snapshot 1-3 Seiten, copy-paste-tauglich.

## Output-Template (Markdown)
```
# Project Snapshot - <PROJECT_NAME> - <TIMESTAMP_LOCAL>

## 1) Kurzueberblick
- Zweck / Problem
- Zielgruppe / Nutzer
- Aktueller Stand in 5 Bulletpoints

## 2) Scope & Nicht-Scope
- In Scope:
- Out of Scope:

## 3) Architektur & Komponenten (repo-basiert)
- High-level Architektur (Datei-Referenzen)
- Komponenten/Module (Pfad -> Verantwortung)
- Datenfluesse / Integrationen (falls vorhanden)

## 4) Aktuelle Implementierung (was existiert wirklich)
- Build/Run (aus README/Config)
- Tests/Qualitaet (Testordner, Coverage-Hinweise)
- CI/CD (Workflow-Dateien)
- Konfiguration (ohne Secrets)

## 5) Backlog: Offene Punkte & naechste Schritte
### Top Next Steps (max 10)
1. ...
### Risiken / Blocker
- ...

## 6) To Clarify (Unbekannt im Repo)
- Frage -> Warum noetig -> Wo koennte es stehen

## 7) Repo-Referenzen (wichtigste Dateien)
- README: <pfad>
- Architektur: <pfad>
- CI/CD: <pfad>
- ...
```

## Checkliste vor Abschluss
- Alle MUST-Regeln erfuellt
- Keine Geheimnisse im Text
- Dateipfad korrekt versioniert
- Top-Referenzen genannt