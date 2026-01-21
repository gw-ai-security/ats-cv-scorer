# External Evaluation Results

Run timestamp: 2026-01-21 16:29:19 (Local)

Command: `scripts\evaluate\evaluate_matching.py --dataset resume_data_ranking --summary-out docs\04_evaluation\EVALUATION_RESULTS_EXTERNAL.md --strategy baseline --limit 200`
Dataset ID: resume_data_ranking

## Summary
### baseline
- pairs_file: data\processed\datasets\resume_data_ranking.jsonl
- accuracy: 0.1799
- macro_f1: 0.177

## Limitations
- Run limited to first 200 records for runtime reasons.
- Hybrid ML evaluation not executed (embedding model download/runtime not available).
