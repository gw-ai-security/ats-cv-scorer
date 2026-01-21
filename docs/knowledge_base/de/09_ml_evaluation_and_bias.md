# ML Evaluation & Bias Check (DE)

## Zweck
Systematische, reproduzierbare Evaluation des ML-Matching-Ansatzes sowie indikative Bias-Checks anhand kontrollierter Szenarien.

## Evaluationsstruktur
### Ziel
- Qualitaet, Grenzen und Stabilitaet des ML-Matchings dokumentieren.
- Vergleich zur rule-based Baseline ermoeglichen.

### Evaluierte Modelle
- Rule-based Baseline (deterministisch)
- Hybrid ML Matcher (semantische Aehnlichkeit + Feature Fusion)

### Datengrundlage
- Synthetic Data mit Ground Truth (primary)
- Optional: weakly labeled data (nur wenn dokumentiert)

### Versionierung
- Model-Version (Embedding Modell)
- Generator-Version (Synthetic Data)
- Seed (Synthetic Generator)

## Metriken (Warum diese?)
- **Classification (Precision/Recall/F1):** misst die Label-Qualitaet fuer strong/partial/mismatch.
- **Score-Error (MAE/RMSE gegen expected_score_range):** misst Abweichung vom erwarteten Score-Band.
- **Ranking (MRR/nDCG):** nur relevant, wenn pro CV mehrere JDs gerankt werden.

## Bias Checks (indikativ)
Vergleiche die Modellleistung entlang kontrollierter Achsen:
- job_family (backend/data/security)
- language (EN/DE)
- difficulty (easy/medium/hard)
- formatting_noise (clean/noisy)
- synonym_only (exact vs. synonyms)

Fuer jede Achse:
- gleiche Ground Truth Verteilung pruefen
- Metriken vergleichen (Accuracy/F1/MAE)
- signifikante Abweichungen markieren (indikativ)

## Modellgrenzen (explizit)
- Performance limitiert durch Synthetic Coverage (keine echten CVs/JDs).
- Semantische Aehnlichkeit deckt implizite Skills nur begrenzt ab.
- Bias Checks sind indikativ; keine Aussagen ueber reale Gruppen oder sensible Attribute.
- Ranking-Metriken nur gueltig, wenn Ranking-Setup vorhanden ist.

## Ergebnisse (Kurzfassung)
- Zusammenfassung basierend auf `docs/04_evaluation/EVALUATION_RESULTS.md` (2026-01-21):
  - Baseline: Accuracy 0.50, Macro F1 0.2222, MAE 0.0000 (synthetische Labels aus Baseline-Score).
  - Hybrid ML: Accuracy 0.00, Macro F1 0.0000, MAE 18.4830 (unkalibriert, aktuelle Thresholds).
  - Bias-Achsen indikativ; backend-Sample klein (n=2).
  - Keine mismatch-Faelle im synthetischen Set.

## Empfehlungen
- Synthetic Taxonomy erweitern, um Coverage zu erhoehen.
- Hybrid-Modelle nur einsetzen, wenn Explainability nachvollziehbar bleibt.
- Bias Checks regelmaessig wiederholen (bei neuen Seeds/Versionen).

## Verweise
- `docs/04_evaluation/EVALUATION_PLAN.md`
- `docs/04_evaluation/EVALUATION_RESULTS.md`
- `docs/03_quality/EXPLAINABLE_SCORING_SPEC.md`
- `docs/02_architecture/ADR/ADR-002-ml-matching.md`
- `docs/codex_skills/SKILL_SYNTHETIC_DATA_GENERATOR.md`

## Last Updated
2026-01-21 14:53:02 (Local)
