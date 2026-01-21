from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Iterable


def _read_rows(path: Path) -> Iterable[dict[str, str]]:
    if path.suffix.lower() in {".jsonl", ".json"}:
        with path.open("r", encoding="utf-8") as handle:
            for line in handle:
                if line.strip():
                    yield json.loads(line)
        return
    with path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            yield row


def parse_resume_records(source_path: Path, output_path: Path, text_field: str) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    records = []
    for idx, row in enumerate(_read_rows(source_path), start=1):
        text = (row.get(text_field) or "").strip()
        if not text:
            continue
        records.append(
            {
                "record_id": f"resume_{idx:06d}",
                "text": text,
                "language": row.get("language", "unknown"),
                "source": source_path.name,
                "metadata": {"raw_fields": list(row.keys())},
            }
        )
    with output_path.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")
