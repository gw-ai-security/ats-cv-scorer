# External Evaluation Results

Run timestamp: 2026-01-22 20:20:32 (Local)

Command: `scripts\evaluate\evaluate_matching.py --dataset resume_data_ranking --strategy both --limit 50 --summary-out docs\04_evaluation\EVALUATION_RESULTS_EXTERNAL.md`
Dataset ID: resume_data_ranking

## Summary
## Environment Notes
- hybrid_skipped: model_cache_not_found

### baseline
- pairs_file: data\processed\datasets\resume_data_ranking.jsonl
- accuracy: 0.1489
- macro_f1: 0.153

## Limitations
- Labels are normalized from numeric `matched_score`; thresholds may not match dataset intent.
- Hybrid ML skipped due to missing local model cache.
- Run limited to 50 records for runtime reasons.
