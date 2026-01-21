from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
import sys


@dataclass(frozen=True)
class KaggleDataset:
    name: str
    dataset_id: str
    output_dir: Path


DATASETS = [
    KaggleDataset(
        name="ATS Scoring Dataset",
        dataset_id="TBD/ats-scoring-dataset",
        output_dir=Path("data/raw/kaggle/ats_scoring"),
    ),
    KaggleDataset(
        name="Resume-Job Matching Dataset",
        dataset_id="TBD/resume-job-matching",
        output_dir=Path("data/raw/kaggle/resume_job_matching"),
    ),
    KaggleDataset(
        name="Resume Data for Ranking",
        dataset_id="TBD/resume-data-ranking",
        output_dir=Path("data/raw/kaggle/resume_ranking"),
    ),
    KaggleDataset(
        name="Job Descriptions 2025",
        dataset_id="TBD/job-descriptions-2025",
        output_dir=Path("data/raw/kaggle/job_descriptions_2025"),
    ),
    KaggleDataset(
        name="Job Skill Set Dataset",
        dataset_id="TBD/job-skill-set",
        output_dir=Path("data/raw/kaggle/job_skill_set"),
    ),
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Download Kaggle datasets (placeholder IDs).")
    parser.add_argument(
        "--dataset-id",
        action="append",
        default=[],
        help="Override dataset IDs (repeatable).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print actions without downloading.",
    )
    return parser.parse_args()


def ensure_kaggle() -> object:
    try:
        from kaggle.api.kaggle_api_extended import KaggleApi
    except Exception as exc:  # pragma: no cover - optional dependency
        raise RuntimeError(
            "Kaggle API not available. Install kaggle and configure credentials."
        ) from exc

    api = KaggleApi()
    api.authenticate()
    return api


def download_dataset(api: object, dataset: KaggleDataset, dry_run: bool) -> None:
    dataset.output_dir.mkdir(parents=True, exist_ok=True)
    if dry_run:
        print(f"[DRY-RUN] {dataset.name}: {dataset.dataset_id} -> {dataset.output_dir}")
        return
    if dataset.dataset_id.startswith("TBD/"):
        print(f"[SKIP] {dataset.name}: dataset_id not set")
        return
    print(f"[DOWNLOAD] {dataset.name}: {dataset.dataset_id}")
    api.dataset_download_files(dataset.dataset_id, path=str(dataset.output_dir), unzip=True)


def main() -> None:
    args = parse_args()
    datasets = DATASETS
    if args.dataset_id:
        if len(args.dataset_id) != len(DATASETS):
            print("Provide override IDs for all datasets in DATASETS order.", file=sys.stderr)
            sys.exit(1)
        datasets = [
            KaggleDataset(name=entry.name, dataset_id=override, output_dir=entry.output_dir)
            for entry, override in zip(DATASETS, args.dataset_id)
        ]

    api = None
    if not args.dry_run:
        api = ensure_kaggle()

    for dataset in datasets:
        download_dataset(api, dataset, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
