from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate external data quality report.")
    parser.add_argument(
        "--processed-dir",
        type=Path,
        default=Path("data/processed/datasets"),
        help="Directory with processed JSONL files.",
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=Path("docs/04_evaluation/EXTERNAL_DATA_QUALITY.md"),
        help="Output report path.",
    )
    return parser.parse_args()


def summarize_dataset(path: Path) -> dict[str, object]:
    rows = 0
    missing_cv = 0
    missing_jd = 0
    missing_label = 0
    lengths_cv = []
    lengths_jd = []
    hashes = set()
    dupes = 0
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            rows += 1
            record = json.loads(line)
            cv_text = record.get("cv_text") or ""
            jd_text = record.get("jd_text") or ""
            label = record.get("label")
            if not cv_text:
                missing_cv += 1
            if not jd_text:
                missing_jd += 1
            if label in (None, ""):
                missing_label += 1
            if cv_text:
                lengths_cv.append(len(cv_text))
            if jd_text:
                lengths_jd.append(len(jd_text))
            key = hashlib.sha256(f"{cv_text}::{jd_text}".encode("utf-8")).hexdigest()
            if key in hashes:
                dupes += 1
            else:
                hashes.add(key)
    return {
        "rows": rows,
        "missing_cv": missing_cv,
        "missing_jd": missing_jd,
        "missing_label": missing_label,
        "avg_cv_length": round(sum(lengths_cv) / max(len(lengths_cv), 1), 2),
        "avg_jd_length": round(sum(lengths_jd) / max(len(lengths_jd), 1), 2),
        "duplicate_estimate": dupes,
    }


def write_report(results: dict[str, dict[str, object]], report_path: Path) -> None:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = [
        "# External Data Quality Report",
        "",
        f"Run timestamp: {timestamp} (Local)",
        "",
        "Scope: processed JSONL datasets under `data/processed/datasets/`.",
        "",
        "## Summary",
    ]
    for dataset_id, stats in results.items():
        lines.append(f"### {dataset_id}")
        lines.append(f"- rows: {stats['rows']}")
        lines.append(f"- missing_cv: {stats['missing_cv']}")
        lines.append(f"- missing_jd: {stats['missing_jd']}")
        lines.append(f"- missing_label: {stats['missing_label']}")
        lines.append(f"- avg_cv_length: {stats['avg_cv_length']}")
        lines.append(f"- avg_jd_length: {stats['avg_jd_length']}")
        lines.append(f"- duplicate_estimate: {stats['duplicate_estimate']}")
        lines.append("")
    report_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    args = parse_args()
    results: dict[str, dict[str, object]] = {}
    if not args.processed_dir.exists():
        raise SystemExit("Processed directory not found.")
    for path in sorted(args.processed_dir.glob("*.jsonl")):
        results[path.stem] = summarize_dataset(path)
    write_report(results, args.report)
    print(f"Wrote {args.report}")


if __name__ == "__main__":
    main()
