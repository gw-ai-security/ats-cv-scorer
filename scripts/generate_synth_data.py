from __future__ import annotations

import argparse
import json
from pathlib import Path

from src.data_synth.generator import DEFAULT_TAXONOMY_PATH, SyntheticGenerator, load_taxonomy


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate synthetic CV/JD pairs.")
    parser.add_argument("--n", type=int, default=10, help="Number of pairs to generate.")
    parser.add_argument("--seed", type=int, default=7, help="Random seed for reproducibility.")
    parser.add_argument(
        "--lang",
        choices=["en", "de", "mixed"],
        default="en",
        help="Language for generated texts.",
    )
    parser.add_argument(
        "--job-family",
        dest="job_family",
        default="mixed",
        help="Job family to generate (backend, data, security, mixed).",
    )
    parser.add_argument(
        "--difficulty",
        choices=["easy", "medium", "hard", "mixed"],
        default="mixed",
        help="Difficulty profile.",
    )
    parser.add_argument(
        "--outdir",
        type=Path,
        default=Path("tests/fixtures/synth"),
        help="Output directory.",
    )
    parser.add_argument(
        "--taxonomy",
        type=Path,
        default=DEFAULT_TAXONOMY_PATH,
        help="Path to skill taxonomy JSON.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    taxonomy = load_taxonomy(args.taxonomy)
    generator = SyntheticGenerator(taxonomy=taxonomy, seed=args.seed)

    outdir = args.outdir
    outdir.mkdir(parents=True, exist_ok=True)
    pairs_path = outdir / "pairs.jsonl"

    with pairs_path.open("w", encoding="utf-8") as pairs_file:
        for idx in range(1, args.n + 1):
            lang = args.lang
            if lang == "mixed":
                lang = "en" if idx % 2 == 1 else "de"
            pair = generator.generate_pair(
                pair_index=idx,
                lang=lang,
                job_family=args.job_family,
                difficulty=args.difficulty,
            )
            cv_path = outdir / f"{pair.pair_id}_cv.txt"
            jd_path = outdir / f"{pair.pair_id}_jd.txt"
            cv_path.write_text(pair.cv_text, encoding="utf-8")
            jd_path.write_text(pair.jd_text, encoding="utf-8")

            record = {
                "pair_id": pair.pair_id,
                "cv_file": cv_path.name,
                "jd_file": jd_path.name,
                **pair.ground_truth,
            }
            pairs_file.write(json.dumps(record, ensure_ascii=False) + "\n")

    print(f"Wrote {args.n} pairs to {outdir}")


if __name__ == "__main__":
    main()
