from __future__ import annotations

import json
from pathlib import Path
import zipfile

from src.data_ingest.adapters import ADAPTERS
from src.data_ingest.registry import load_registry
from src.data_ingest.schema import validate_canonical_record


INCOMING_DIR = Path("data/external/kaggle/_incoming_zips")
UNZIPPED_DIR = Path("data/external/kaggle/_unzipped")
OUTPUT_DIR = Path("data/processed/datasets")
REPORT_PATH = Path("data/processed/INGEST_REPORT.md")


def unzip_all() -> list[Path]:
    UNZIPPED_DIR.mkdir(parents=True, exist_ok=True)
    extracted = []
    for zip_path in INCOMING_DIR.glob("*.zip"):
        target_dir = UNZIPPED_DIR / zip_path.stem
        if target_dir.exists() and any(target_dir.iterdir()):
            extracted.append(target_dir)
            continue
        target_dir.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(zip_path, "r") as handle:
            handle.extractall(target_dir)
        extracted.append(target_dir)
    return extracted


def find_dataset_files(patterns: list[str]) -> list[Path]:
    matches: list[Path] = []
    for pattern in patterns:
        matches.extend(UNZIPPED_DIR.glob(pattern))
    return sorted({match.resolve() for match in matches})


def ingest_dataset(dataset: dict) -> dict[str, object]:
    dataset_id = dataset["dataset_id"]
    patterns = dataset.get("expected_files", [])
    adapter_name = dataset.get("adapter")
    adapter = ADAPTERS.get(adapter_name)
    output_path = OUTPUT_DIR / f"{dataset_id}.jsonl"
    dataset_type = dataset.get("dataset_type", "unknown")
    license_label = dataset.get("license_label", "unknown")
    usage_status = dataset.get("usage_status", "restricted")
    source_url = dataset.get("source_url", "unknown")

    if not adapter:
        return {"dataset_id": dataset_id, "status": "error", "message": "adapter_missing"}

    files = find_dataset_files(patterns)
    if not files:
        return {"dataset_id": dataset_id, "status": "missing", "message": "no_matching_files"}

    records = []
    errors = []
    for source_path in files:
        for record in adapter(source_path):
            if dataset_type and "dataset_type" not in record.get("meta", {}):
                record.setdefault("meta", {})["dataset_type"] = dataset_type
            record_errors = validate_canonical_record(record)
            if record_errors:
                errors.append({"id": record.get("id"), "errors": record_errors})
                continue
            records.append(record)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")

    return {
        "dataset_id": dataset_id,
        "status": "ok",
        "source_files": [str(path) for path in files],
        "records_written": len(records),
        "invalid_records": len(errors),
        "dataset_type": dataset_type,
        "license_label": license_label,
        "usage_status": usage_status,
        "source_url": source_url,
    }


def write_report(results: list[dict[str, object]]) -> None:
    lines = ["# Ingest Report", "", "## Summary"]
    for result in results:
        lines.append(
            f"- {result['dataset_id']}: {result['status']} (records={result.get('records_written', 0)})"
        )
    lines.append("")
    lines.append("## Details")
    for result in results:
        lines.append(f"### {result['dataset_id']}")
        for key, value in result.items():
            lines.append(f"- {key}: {value}")
        lines.append("")
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    INCOMING_DIR.mkdir(parents=True, exist_ok=True)
    unzip_all()
    registry = load_registry()
    results = [ingest_dataset(entry) for entry in registry["datasets"]]
    write_report(results)
    print(f"Wrote {REPORT_PATH}")


if __name__ == "__main__":
    main()
