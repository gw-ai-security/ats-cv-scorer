# Skill: ML Evaluation & Bias Check

## Zweck
Evaluiere ML-Matching (Hybrid) gegen die rule-based Baseline und dokumentiere indikative Bias Checks reproduzierbar.

## Wann anwenden
- Vor oder nach Aenderungen am ML-Matching (Embedding/Feature Fusion).
- Wenn Synthetic Data Generator oder Taxonomie aktualisiert wurden.
- Vor Review/Audit der ML-Ergebnisse.

## Vorgehen (Schritt-fuer-Schritt)
1) Verifiziere Synthetic Pairs unter `tests/fixtures/synth/pairs.jsonl`.
2) Fuehre die Evaluation aus (Baseline und Hybrid):
   - `py scripts/evaluate/evaluate_matching.py --pairs tests/fixtures/synth/pairs.jsonl --outdir evaluation_outputs`
3) Pruefe `metrics.json` und `confusion_matrix_*.csv` auf Plausibilitaet.
4) Dokumentiere Zusammenfassung und Limits in der Knowledge Base (DE/EN).
5) Vergleiche Szenarien (job_family, language, difficulty, formatting_noise, synonym_only).

## Outputs
- `evaluation_outputs/metrics.json`
- `evaluation_outputs/confusion_matrix_baseline.csv`
- `evaluation_outputs/confusion_matrix_hybrid_ml.csv`

## Qualitaetskriterien
- Reproduzierbar (Seed + Versionen dokumentiert).
- Metriken passend zum Setup (kein Ranking ohne Ranking-Setup).
- Bias Checks indikativ, keine pauschalen Fairness-Aussagen.
- Explizite Dokumentation von Grenzen.

## Repo-Referenzen
- `scripts/evaluate/evaluate_matching.py`
- `tests/fixtures/synth/pairs.jsonl`
- `docs/knowledge_base/de/09_ml_evaluation_and_bias.md`
- `docs/knowledge_base/en/09_ml_evaluation_and_bias.md`
- `docs/04_evaluation/EVALUATION_PLAN.md`
- `docs/02_architecture/ADR/ADR-002-ml-matching.md`

## Last Updated
2026-01-21 14:38:32 (Local)
