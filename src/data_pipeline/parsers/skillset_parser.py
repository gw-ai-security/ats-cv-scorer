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


def parse_skillset_records(
    source_path: Path,
    output_path: Path,
    skill_field: str,
    category_field: str | None = None,
) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    records = []
    for idx, row in enumerate(_read_rows(source_path), start=1):
        skill = (row.get(skill_field) or "").strip()
        if not skill:
            continue
        record = {
            "record_id": f"skill_{idx:06d}",
            "skill": skill,
            "category": (row.get(category_field) if category_field else "unknown"),
            "source": source_path.name,
            "metadata": {"raw_fields": list(row.keys())},
        }
        records.append(record)
    with output_path.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")
