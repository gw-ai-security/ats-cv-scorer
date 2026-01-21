from __future__ import annotations

import argparse
from pathlib import Path

from src.data_pipeline.parsers import parse_skillset_records


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Parse skill datasets to JSONL.")
    parser.add_argument("--input", type=Path, required=True, help="Path to source CSV/JSONL.")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("data/processed/skill_sets.jsonl"),
        help="Output JSONL path.",
    )
    parser.add_argument("--skill-field", required=True, help="Field name containing skill name.")
    parser.add_argument("--category-field", default=None, help="Optional category field name.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    parse_skillset_records(args.input, args.output, args.skill_field, args.category_field)


if __name__ == "__main__":
    main()
