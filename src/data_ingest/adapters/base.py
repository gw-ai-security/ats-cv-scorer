from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Iterable


def read_rows(path: Path) -> Iterable[dict[str, str]]:
    if path.suffix.lower() == ".jsonl":
        with path.open("r", encoding="utf-8") as handle:
            for line in handle:
                if line.strip():
                    yield json.loads(line)
        return
    if path.suffix.lower() == ".json":
        payload = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(payload, list):
            for row in payload:
                if isinstance(row, dict):
                    yield row
        elif isinstance(payload, dict):
            yield payload
        return
    with path.open("r", encoding="utf-8") as handle:
        sample = handle.read(4096)
        handle.seek(0)
        try:
            dialect = csv.Sniffer().sniff(sample)
        except csv.Error:
            dialect = csv.excel
        if sample.count("|") > sample.count(","):
            dialect = csv.excel
            dialect.delimiter = "|"
        reader = csv.DictReader(handle, dialect=dialect)
        for row in reader:
            yield row


def normalize_text(text: str | None) -> str:
    if not text:
        return ""
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    return " ".join(normalized.split()).strip()


def detect_language(text: str, fallback: str | None = None) -> str:
    if fallback:
        candidate = fallback.strip().lower()
        if candidate in {"en", "de", "unknown"}:
            return candidate
    lowered = f" {text.lower()} "
    en_hits = sum(token in lowered for token in (" the ", " and ", " with ", " for ", " experience "))
    de_hits = sum(token in lowered for token in (" und ", " der ", " die ", " das ", " mit ", " fuer "))
    if de_hits > en_hits:
        return "de"
    if en_hits > 0:
        return "en"
    return "unknown"


def canonical_record(
    record_id: str,
    cv_text: str | None,
    jd_text: str | None,
    label: str | None,
    language: str | None,
    source: str,
    meta: dict[str, object],
) -> dict[str, object]:
    label = label if label in {"strong_match", "partial_match", "mismatch"} else None
    language = (language or "unknown").lower()
    if language not in {"en", "de", "unknown"}:
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


def map_fields(row: dict[str, str], mapping: dict[str, str]) -> dict[str, str]:
    return {target: row.get(source, "") for target, source in mapping.items()}
