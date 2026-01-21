from __future__ import annotations

import argparse
import json
import re
from datetime import datetime
from pathlib import Path


EMAIL_RE = re.compile(r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}", re.IGNORECASE)
PHONE_RE = re.compile(r"\+?\d[\d\s\-()]{7,}\d")
URL_RE = re.compile(r"https?://\S+")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Scan processed JSONL for PII patterns.")
    parser.add_argument(
        "--processed-dir",
        type=Path,
        default=Path("data/processed/datasets"),
        help="Directory with processed JSONL files.",
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=Path("docs/04_evaluation/PII_SCAN_REPORT.md"),
        help="Output report path.",
    )
    return parser.parse_args()


def scan_text(text: str) -> dict[str, int]:
    return {
        "email_hits": len(EMAIL_RE.findall(text)),
        "phone_hits": len(PHONE_RE.findall(text)),
        "url_hits": len(URL_RE.findall(text)),
    }


def scan_dataset(path: Path) -> dict[str, int]:
    totals = {"records": 0, "records_with_hits": 0, "email_hits": 0, "phone_hits": 0, "url_hits": 0}
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            record = json.loads(line)
            text = f"{record.get('cv_text') or ''} {record.get('jd_text') or ''}"
            hits = scan_text(text)
            totals["records"] += 1
            totals["email_hits"] += hits["email_hits"]
            totals["phone_hits"] += hits["phone_hits"]
            totals["url_hits"] += hits["url_hits"]
            if any(hits.values()):
                totals["records_with_hits"] += 1
    return totals


def write_report(results: dict[str, dict[str, int]], report_path: Path) -> None:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = [
        "# PII Scan Report",
        "",
        f"Run timestamp: {timestamp} (Local)",
        "",
        "Scan scope: processed JSONL under `data/processed/datasets/`.",
        "Raw content is not stored in this report.",
        "",
        "## Results",
    ]
    for dataset_id, stats in results.items():
        lines.append(f"### {dataset_id}")
        lines.append(f"- records: {stats['records']}")
        lines.append(f"- records_with_hits: {stats['records_with_hits']}")
        lines.append(f"- email_hits: {stats['email_hits']}")
        lines.append(f"- phone_hits: {stats['phone_hits']}")
        lines.append(f"- url_hits: {stats['url_hits']}")
        lines.append("")
    report_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    args = parse_args()
    results: dict[str, dict[str, int]] = {}
    if not args.processed_dir.exists():
        raise SystemExit("Processed directory not found.")
    for path in sorted(args.processed_dir.glob("*.jsonl")):
        results[path.stem] = scan_dataset(path)
    write_report(results, args.report)
    print(f"Wrote {args.report}")


if __name__ == "__main__":
    main()
