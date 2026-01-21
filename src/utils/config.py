from __future__ import annotations

import os


def get_matching_strategy() -> str:
    strategy = os.getenv("MATCHING_STRATEGY", "rule_based").strip().lower()
    if strategy not in {"rule_based", "hybrid_ml"}:
        return "rule_based"
    return strategy
