# ADR-002: ML Matching Roadmap (Plan)

## Status
Accepted (Optional Hybrid ML)

## Context
The current baseline will be rules-based matching for transparency and determinism.
We plan an ML-based matcher only after baseline stability and evaluation data exist.

Recruiter-focused criteria to prioritize:
- role/seniority, location/remote, work authorization
- years of experience and relevant domains
- required skills and tools
- certifications and languages
- education requirements
- clear gaps vs. must-have requirements

## Decision
Implement an optional hybrid ML matcher that uses semantic similarity (bi-encoder)
and feature fusion, while keeping the deterministic baseline as default.

## Implementation (Current)
- Optional ML modules live under `src/core/ml/` (embedding model, semantic matcher, feature fusion).
- Strategy selection in `src/core/matcher.py` with env flag `MATCHING_STRATEGY=hybrid_ml`.
- Explainability includes semantic similarity, skill overlap, section coverage, and top matched chunks.
- Optional calibrator hook via `ML_CALIBRATOR_PATH` (logistic regression) without breaking baseline.

## ML Plan (High Level)
1) Data collection
   - Curate CV and JD pairs with labeled outcomes (match / no match / partial).
   - Prefer synthetic or consented samples; no persistent storage of personal data.
2) Feature strategy
   - Structured fields from the rules-based extractor (skills, experience, edu).
   - Text embeddings for JD and CV sections (e.g., skills, experience summaries).
   - Hybrid scoring: rules-based constraints + ML similarity.
3) Model families
   - Baseline: cosine similarity on sentence embeddings.
   - Candidate models: bi-encoder embeddings; optional cross-encoder re-ranker.
4) Evaluation
   - Precision/recall, ranking metrics (MRR, nDCG).
   - Human review of explanations for top matches and false positives.
5) Privacy and bias
   - No external API calls for sensitive data.
   - Document bias risks (name, gender signals) and mitigation strategies.
6) Rollout
   - Keep baseline as default.
   - Run ML in shadow mode, compare to baseline, then gate for optional use.

## Consequences
- Baseline remains default and deterministic.
- ML path is optional and explainable; requires evaluation data to be completed.
