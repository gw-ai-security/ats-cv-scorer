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
    "cv_text": "resume_text",
    "jd_text": "job_description",
    "label": "label",
    "language": "language",
}


def normalize_label(raw: str | None) -> str | None:
    if not raw:
        return None
    value = raw.strip().lower()
    if value in {"strong_match", "partial_match", "mismatch"}:
        return value
    if value in {"strong", "high", "good", "match", "yes"}:
        return "strong_match"
    if value in {"partial", "medium", "mid"}:
        return "partial_match"
    if value in {"weak", "low", "no", "mismatch"}:
        return "mismatch"
    try:
        score = float(value)
    except ValueError:
        return None
    if score >= 0.8:
        return "strong_match"
    if score >= 0.5:
        return "partial_match"
    return "mismatch"


def parse(path: Path) -> Iterable[dict[str, object]]:
    for idx, row in enumerate(read_rows(path), start=1):
        fields = map_fields(row, MAPPING)
        cv_text = normalize_text(fields.get("cv_text") or row.get("text"))
        jd_text = normalize_text(fields.get("jd_text"))
        if not cv_text and not jd_text:
            continue
        label = normalize_label(fields.get("label"))
        language = detect_language(f"{cv_text} {jd_text}", fields.get("language"))
        yield canonical_record(
            record_id=f"ats_scoring_{idx:06d}",
            cv_text=cv_text or None,
            jd_text=jd_text or None,
            label=label,
            language=language,
            source="kaggle:ats_scoring_dataset",
            meta={
                "dataset_type": "cv_only",
                "raw_fields": list(row.keys()),
                "label_original": fields.get("label"),
            },
        )
