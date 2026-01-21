# ML Evaluation & Bias Check (EN)

## Purpose
Systematic, reproducible evaluation of the ML matching approach and indicative bias checks using controlled scenarios.

## Evaluation Structure
### Goal
- Document quality, limits, and stability of ML matching.
- Enable comparison to the rule-based baseline.

### Evaluated Models
- Rule-based Baseline (deterministic)
- Hybrid ML Matcher (semantic similarity + feature fusion)

### Data Basis
- Synthetic data with ground truth (primary)
- Optional: weakly labeled data (only if documented)

### Versioning
- Model version (embedding model)
- Generator version (synthetic data)
- Seed (synthetic generator)

## Metrics (Why these?)
- **Classification (Precision/Recall/F1):** label quality for strong/partial/mismatch.
- **Score Error (MAE/RMSE vs expected_score_range):** deviation from expected score band.
- **Ranking (MRR/nDCG):** only relevant when ranking multiple JDs per CV.

## Bias Checks (indicative)
Compare model performance across controlled axes:
- job_family (backend/data/security)
- language (EN/DE)
- difficulty (easy/medium/hard)
- formatting_noise (clean/noisy)
- synonym_only (exact vs synonyms)

For each axis:
- verify ground truth distribution
- compare metrics (Accuracy/F1/MAE)
- flag significant deviations (indicative)

## Model Limits (explicit)
- Performance limited by synthetic coverage (no real CVs/JDs).
- Semantic similarity only partially captures implicit skills.
- Bias checks are indicative; no claims about real groups or sensitive attributes.
- Ranking metrics only valid with a ranking setup.

## Results (Summary)
- Summarize results from `metrics.json`, avoid raw numbers flood.
- Clearly state baseline vs hybrid strengths/weaknesses.

## Recommendations
- Expand synthetic taxonomy to improve coverage.
- Use hybrid models only when explainability stays traceable.
- Repeat bias checks for new seeds/versions.

## References
- `docs/04_evaluation/EVALUATION_PLAN.md`
- `docs/02_architecture/ADR/ADR-002-ml-matching.md`
- `docs/codex_skills/SKILL_SYNTHETIC_DATA_GENERATOR.md`

## Last Updated
2026-01-21 14:38:32 (Local)
