# Codex Skills - ATS CV Scorer

## 1) Skill-Uebersicht
| Skill Name | Zweck | Wann verwenden | Datei |
|-----------|-------|----------------|------|
| requirements-traceability | Anforderungen und Traceability pflegen | Bei Aenderungen an FR/NFR oder Mapping | `.codex/skills/requirements-traceability/SKILL.md` |
| architecture-adr | Architekturentscheidungen dokumentieren | Bei neuen oder geaenderten Architekturentscheidungen | `.codex/skills/architecture-adr/SKILL.md` |
| pdf-processing | PDF-Upload/Extraktion pflegen | Bei Anpassungen an Upload-Regeln oder Parsing | `.codex/skills/pdf-processing/SKILL.md` |
| cv-structure-analysis | CV-Strukturerkennung pflegen | Bei neuen Abschnitts- oder Header-Regeln | `.codex/skills/cv-structure-analysis/SKILL.md` |
| skill-extraction | Skill-Extraktion pflegen | Bei neuen Skills, Synonymen, Kategorien | `.codex/skills/skill-extraction/SKILL.md` |
| ats-criteria-extraction | ATS-Kriterien extrahieren | Bei neuen ATS-Feldern oder Regeln | `.codex/skills/ats-criteria-extraction/SKILL.md` |
| jd-parsing | JD-Parsing pflegen | Bei neuen JD-Feldern oder Parsing-Regeln | `.codex/skills/jd-parsing/SKILL.md` |
| matching-baseline | Regelbasiertes Matching pflegen | Bei Scoring-/Explainability-Aenderungen | `.codex/skills/matching-baseline/SKILL.md` |
| streamlit-ui | Streamlit UI pflegen | Bei UI- oder Workflow-Aenderungen | `.codex/skills/streamlit-ui/SKILL.md` |
| testing-quality-gates | Tests/CI/Quality pflegen | Bei neuen Features oder CI-Updates | `.codex/skills/testing-quality-gates/SKILL.md` |
| evaluation-plan | Evaluation planen | Bei neuen Metriken/Schwellen | `.codex/skills/evaluation-plan/SKILL.md` |
| project-state-snapshot | Project Snapshot erzeugen | Bei Status-Updates oder Kontextweitergabe | `.codex/skills/project-state-snapshot/SKILL.md` |
| project-phase-planner | Phasenplan pflegen | Bei Aenderungen am Projektplan | `.codex/skills/project-phase-planner/SKILL.md` |
| project-orchestration | Skill-Orchestrierung | Bei Phasenwechsel oder Laufplanung | `.codex/skills/project-orchestration/SKILL.md` |

## 2) Skill-Dateien (einzeln erstellt)
Jede Skill-Datei folgt diesem Template:

```
# Skill: <SKILL_NAME>

## Zweck
Was dieser Skill tut.

## Wann anwenden
Typische Situationen im Projektverlauf.

## Vorgehen (Schritt-fuer-Schritt)
1. ...
2. ...

## Lernperspektive
- Warum wurde das so geloest?
- Welche Alternativen gaebe es?
- Warum wurden sie hier bewusst nicht gewaehlt?

## Repo-Referenzen
- Datei / Pfad / Abschnitt

## Qualitaetscheck
- Welche Kriterien muessen erfuellt sein?
```

## 3) Empfohlene Skill-Reihenfolge (Lernpfad)
1. requirements-traceability
2. architecture-adr
3. pdf-processing
4. cv-structure-analysis
5. skill-extraction
6. ats-criteria-extraction
7. jd-parsing
8. matching-baseline
9. streamlit-ui
10. testing-quality-gates
11. evaluation-plan
12. project-state-snapshot
13. project-phase-planner
14. project-orchestration
