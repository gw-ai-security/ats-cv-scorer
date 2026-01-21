from __future__ import annotations

from pathlib import Path
from typing import Iterable

from src.data_ingest.adapters.base import (
    canonical_record,
    detect_language,
    map_fields,
    normalize_text,
    read_rows,
)


MAPPING = {
    "jd_text": "description",
    "language": "language",
}


def parse(path: Path) -> Iterable[dict[str, object]]:
    for idx, row in enumerate(read_rows(path), start=1):
        fields = map_fields(row, MAPPING)
        if "job_description" in row:
            jd_text = normalize_text(row.get("job_description"))
        elif "Responsibilities" in row or "Skills" in row:
            parts = [
                row.get("Title", ""),
                row.get("Responsibilities", ""),
                row.get("Skills", ""),
                row.get("Keywords", ""),
            ]
            normalized_parts = [str(part) for part in parts if part]
            jd_text = normalize_text(" ".join(normalized_parts))
        else:
            jd_text = normalize_text(fields.get("jd_text"))
        if not jd_text:
            continue
        language = detect_language(jd_text, fields.get("language"))
        yield canonical_record(
            record_id=f"jd_2025_{idx:06d}",
            cv_text=None,
            jd_text=jd_text,
            label=None,
            language=language,
            source="kaggle:job_descriptions_2025",
            meta={"raw_fields": list(row.keys()), "dataset_type": "jd_only"},
        )
