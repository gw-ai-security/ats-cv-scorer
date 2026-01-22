from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path

from src.data_ingest.adapters import ADAPTERS
from src.data_ingest.registry import load_registry


FIXTURE_ROOT = Path("tests/fixtures/ingest")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate adapter health report.")
    parser.add_argument(
        "--report",
        type=Path,
        default=Path("docs/04_evaluation/ADAPTER_HEALTH_REPORT.md"),
        help="Output report path.",
    )
    return parser.parse_args()


def check_adapter(dataset_id: str, dataset_type: str) -> tuple[str, str]:
    adapter = ADAPTERS.get(dataset_id)
    if not adapter:
        return "fail", "adapter_missing"
    fixture_dir = FIXTURE_ROOT / dataset_id
    if not fixture_dir.exists():
        return "warn", "fixture_missing"
    fixture_files = list(fixture_dir.glob("*"))
    if not fixture_files:
        return "warn", "fixture_empty"
    records = list(adapter(fixture_files[0]))
    if not records:
        return "fail", "no_records_from_fixture"
    record = records[0]
    if record.get("meta", {}).get("dataset_type") != dataset_type:
        return "warn", "dataset_type_mismatch"
    if dataset_type == "paired" and not (record.get("cv_text") and record.get("jd_text")):
        return "fail", "missing_cv_or_jd"
    if dataset_type == "cv_only" and not record.get("cv_text"):
        return "fail", "missing_cv_text"
    if dataset_type == "jd_only" and not record.get("jd_text"):
        return "fail", "missing_jd_text"
    return "ok", "fixture_parsed"


def main() -> None:
    args = parse_args()
    registry = load_registry()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = [
        "# Adapter Health Report",
        "",
        f"Run timestamp: {timestamp} (Local)",
        "",
        "## Status",
    ]
    for dataset in registry.get("datasets", []):
        dataset_id = dataset.get("dataset_id")
        dataset_type = dataset.get("dataset_type", "unknown")
        status, reason = check_adapter(dataset_id, dataset_type)
        lines.append(f"- {dataset_id} ({dataset_type}): {status} ({reason})")
    lines.append("")
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {args.report}")


if __name__ == "__main__":
    main()
