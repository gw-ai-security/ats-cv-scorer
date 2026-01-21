from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Callable, Iterable


CANONICAL_LABELS = {"strong_match", "partial_match", "mismatch", None}
CANONICAL_LANGUAGES = {"en", "de", "unknown"}


def read_rows(path: Path) -> Iterable[dict[str, str]]:
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


def write_jsonl(records: Iterable[dict[str, object]], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")


def canonical_record(
    record_id: str,
    cv_text: str | None,
    jd_text: str | None,
    label: str | None,
    language: str,
    source: str,
    meta: dict[str, object],
) -> dict[str, object]:
    if label not in CANONICAL_LABELS:
        label = None
    if language not in CANONICAL_LANGUAGES:
        language = "unknown"
    return {
        "id": record_id,
        "cv_text": cv_text,
        "jd_text": jd_text,
        "label": label,
        "language": language,
        "source": source,
        "meta": meta,
    }


AdapterFn = Callable[[Path], Iterable[dict[str, object]]]


def ingest_dataset(input_path: Path, output_path: Path, adapter: AdapterFn) -> None:
    records = adapter(input_path)
    write_jsonl(records, output_path)
