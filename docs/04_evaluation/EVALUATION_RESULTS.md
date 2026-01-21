# Evaluation Results

## Purpose
Document reproducible evaluation results for the baseline and hybrid ML matchers.

## Status
Status: Completed
Evaluation date: 2026-01-21 (Local)

## Dataset & Setup
- Dataset: synthetic CV↔JD pairs with ground truth
- Input file: `tests/fixtures/synth/pairs.jsonl`
- Pair count: 10 (labels: 5 strong_match, 5 partial_match, 0 mismatch)
- Metrics output: `evaluation_outputs/metrics.json` (ignored by git)
- Environment: Python 3.12.3 on Windows 11

## Reproducible Runs
```bash
$env:PYTHONPATH='.'; py scripts/evaluate/evaluate_matching.py --pairs tests/fixtures/synth/pairs.jsonl --outdir evaluation_outputs --strategy both --strong-threshold 80 --partial-threshold 60
```

## Versions
- Git commit: `5ad32cef941dc616257d2d05fb5b7dda0fc2b207`
- Synthetic generator version: `1.0.0` (from `tests/fixtures/synth/pairs.jsonl`)
- Seeds: 10 per-pair seeds stored in `tests/fixtures/synth/pairs.jsonl`
- Hybrid model: `sentence-transformers/all-MiniLM-L6-v2` (downloaded on first run)

## Results Summary (Synthetic, n=10)
| Model | Accuracy | Macro F1 | MAE | RMSE |
| --- | --- | --- | --- | --- |
| Baseline | 0.50 | 0.2222 | 0.0000 | 0.0000 |
| Hybrid ML | 0.00 | 0.0000 | 18.4830 | 19.2561 |

Notes:
- Baseline MAE/RMSE are zero because expected score ranges were generated from baseline matcher output.
- Hybrid ML uses semantic similarity + feature fusion weights without a calibrator.

## Bias-Axis Checks (Indicative)
Baseline:
- job_family: data accuracy 0.6667, security 0.6, backend 0.0 (n=2)
- language: EN 0.6 vs DE 0.4
- formatting_noise: identical accuracy 0.5 (yes/no)
- synonym_only: 0.6 (yes) vs 0.4 (no)

Hybrid ML:
- job_family: 0.0 accuracy across all families (MAE ranges 11.085–21.892)
- language: 0.0 accuracy in EN/DE (MAE ~17.756–19.21)
- formatting_noise: 0.0 accuracy for clean/noisy
- synonym_only: 0.0 accuracy for exact/synonym-only

## Interpretation (Evidence-Based)
- Baseline classifies all strong_match as partial_match due to JD keyword gaps in skill overlap.
- Hybrid ML underperforms on this synthetic set and predicts mismatch for all pairs at the current thresholds.
- Synthetic labels include no mismatch cases, limiting classification diagnostics for that class.
- Bias axes are indicative only; some groups have low sample counts (e.g., backend n=2).
- Results reflect the current scoring thresholds (80/60) and uncalibrated hybrid weights.

## Limitations
- Synthetic-only dataset; no real CV/JD distributions.
- No mismatch class examples, so precision/recall for that class are not meaningful.
- Hybrid ML performance depends on embedding downloads and may vary with model updates.
- Bias checks are controlled and indicative; no claims about real-world fairness.

## References
- `docs/04_evaluation/EVALUATION_PLAN.md`
- `docs/03_quality/EXPLAINABLE_SCORING_SPEC.md`
- `scripts/evaluate/evaluate_matching.py`
