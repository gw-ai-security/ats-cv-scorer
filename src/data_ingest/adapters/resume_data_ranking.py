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
    "cv_text": "resume",
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
        if "career_objective" in row or "job_position_name" in row:
            cv_parts = [
                row.get("career_objective", ""),
                row.get("skills", ""),
                row.get("educational_institution_name", ""),
                row.get("degree_names", ""),
                row.get("major_field_of_studies", ""),
                row.get("positions", ""),
                row.get("responsibilities", ""),
                row.get("languages", ""),
                row.get("certification_skills", ""),
            ]
            jd_parts = [
                row.get("job_position_name", ""),
                row.get("educationaL_requirements", ""),
                row.get("experiencere_requirement", ""),
                row.get("responsibilities.1", ""),
                row.get("skills_required", ""),
                row.get("related_skils_in_job", ""),
            ]
            cv_text = normalize_text(" ".join([part for part in cv_parts if part]))
            jd_text = normalize_text(" ".join([part for part in jd_parts if part]))
            label_raw = row.get("matched_score")
        else:
            cv_text = normalize_text(fields.get("cv_text"))
            jd_text = normalize_text(fields.get("jd_text"))
            label_raw = fields.get("label")
        if not cv_text and not jd_text:
            continue
        label = normalize_label(label_raw)
        language = detect_language(f"{cv_text} {jd_text}", fields.get("language"))
        yield canonical_record(
            record_id=f"resume_rank_{idx:06d}",
            cv_text=cv_text or None,
            jd_text=jd_text or None,
            label=label,
            language=language,
            source="kaggle:resume_data_ranking",
            meta={
                "dataset_type": "paired",
                "raw_fields": list(row.keys()),
                "label_original": label_raw,
            },
        )
