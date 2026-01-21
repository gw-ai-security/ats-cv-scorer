from __future__ import annotations

import argparse
from pathlib import Path

from src.data_pipeline.parsers import parse_jd_records


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Parse job description datasets to JSONL.")
    parser.add_argument("--input", type=Path, required=True, help="Path to source CSV/JSONL.")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("data/processed/job_descriptions.jsonl"),
        help="Output JSONL path.",
    )
    parser.add_argument("--text-field", required=True, help="Field name containing JD text.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    parse_jd_records(args.input, args.output, args.text_field)


if __name__ == "__main__":
    main()
