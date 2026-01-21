from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from joblib import dump
from sklearn.linear_model import LogisticRegression


def load_pairs(path: Path) -> tuple[np.ndarray, np.ndarray]:
    features = []
    labels = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            row = json.loads(line)
            if "features" in row and "label" in row:
                features.append(row["features"])
                labels.append(row["label"])
    return np.asarray(features, dtype=float), np.asarray(labels, dtype=int)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pairs", default="data/pairs_with_features.jsonl")
    parser.add_argument("--out", default="data/semantic_calibrator.joblib")
    args = parser.parse_args()

    pairs_path = Path(args.pairs)
    if not pairs_path.exists():
        raise SystemExit("Missing pairs_with_features.jsonl")

    X, y = load_pairs(pairs_path)
    if X.size == 0:
        raise SystemExit("No features found in input file.")

    model = LogisticRegression(max_iter=200, random_state=42)
    model.fit(X, y)
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    dump(model, out_path)


if __name__ == "__main__":
    main()
