from __future__ import annotations

import argparse
import json
import random
from pathlib import Path


def build_synthetic_pairs(seed: int, count: int) -> list[dict[str, object]]:
    random.seed(seed)
    skills = ["python", "sql", "aws", "docker", "ml", "nlp", "testing"]
    pairs = []
    for _ in range(count):
        jd = random.sample(skills, k=3)
        cv = jd[:2] + random.sample(skills, k=1)
        label = 1
        pairs.append(
            {
                "cv_text": f"Skills: {', '.join(cv)}",
                "jd_text": f"Requirements: {', '.join(jd)}",
                "label": label,
            }
        )
        jd = random.sample(skills, k=3)
        cv = random.sample([s for s in skills if s not in jd], k=2)
        pairs.append(
            {
                "cv_text": f"Skills: {', '.join(cv)}",
                "jd_text": f"Requirements: {', '.join(jd)}",
                "label": 0,
            }
        )
    return pairs


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="data/pairs.jsonl")
    parser.add_argument("--count", type=int, default=50)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    pairs = build_synthetic_pairs(seed=args.seed, count=args.count)
    path = Path(args.out)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for item in pairs:
            handle.write(json.dumps(item) + "\n")


if __name__ == "__main__":
    main()
