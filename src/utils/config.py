from __future__ import annotations

import os
from pathlib import Path


EVALUATION_RESULTS_PATH = Path("docs/04_evaluation/EVALUATION_RESULTS.md")
EVALUATION_GATE_MARKER = "Status: Completed"


def is_evaluation_gate_open() -> bool:
    if not EVALUATION_RESULTS_PATH.exists():
        return False
    content = EVALUATION_RESULTS_PATH.read_text(encoding="utf-8", errors="ignore")
    return EVALUATION_GATE_MARKER in content


def get_matching_strategy() -> str:
    strategy = os.getenv("MATCHING_STRATEGY", "rule_based").strip().lower()
    if strategy not in {"rule_based", "hybrid_ml"}:
        return "rule_based"
    if strategy == "hybrid_ml" and not is_evaluation_gate_open():
        return "rule_based"
    return strategy
