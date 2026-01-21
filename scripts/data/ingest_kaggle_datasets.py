from __future__ import annotations

import argparse
from pathlib import Path

from src.data_pipeline.adapters import kaggle_adapters
from src.data_pipeline.ingest import ingest_dataset


ADAPTERS = {
    "ats_scoring": kaggle_adapters.ats_scoring_adapter,
    "resume_job_matching": kaggle_adapters.resume_job_matching_adapter,
    "resume_ranking": kaggle_adapters.resume_ranking_adapter,
    "job_descriptions_2025": kaggle_adapters.job_descriptions_2025_adapter,
    "job_skill_set": kaggle_adapters.job_skill_set_adapter,
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Ingest Kaggle datasets into canonical JSONL.")
    parser.add_argument("--input", type=Path, required=True, help="Path to dataset file.")
    parser.add_argument("--adapter", choices=ADAPTERS.keys(), required=True)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("data/processed/datasets/kaggle_pairs.jsonl"),
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    adapter = ADAPTERS[args.adapter]
    ingest_dataset(args.input, args.output, adapter)


if __name__ == "__main__":
    main()
