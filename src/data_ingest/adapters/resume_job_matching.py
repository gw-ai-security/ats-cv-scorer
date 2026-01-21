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
    "label": "match_label",
    "language": "language",
}


def parse(path: Path) -> Iterable[dict[str, object]]:
    for idx, row in enumerate(read_rows(path), start=1):
        fields = map_fields(row, MAPPING)
        cv_text = ""
        jd_text = ""
        if "skills_cv" in row or "vacancyName" in row:
            cv_parts = [
                row.get("positionName", ""),
                row.get("skills_cv", ""),
                row.get("hardSkills_cv", ""),
                row.get("softSkills_cv", ""),
                row.get("workExperienceList", ""),
                row.get("educationList", ""),
                row.get("experience", ""),
            ]
            jd_parts = [
                row.get("vacancyName", ""),
                row.get("skills_vacancy", ""),
                row.get("hardSkills_vacancy", ""),
                row.get("softSkills_vacancy", ""),
                row.get("positionRequirements", ""),
                row.get("responsibilities", ""),
            ]
            cv_text = normalize_text(" ".join([part for part in cv_parts if part]))
            jd_text = normalize_text(" ".join([part for part in jd_parts if part]))
        else:
            cv_text = normalize_text(fields.get("cv_text"))
            jd_text = normalize_text(fields.get("jd_text"))
        if not cv_text and not jd_text:
            continue
        label = (fields.get("label") or "").strip().lower() or None
        language = detect_language(f"{cv_text} {jd_text}", fields.get("language"))
        yield canonical_record(
            record_id=f"resume_job_{idx:06d}",
            cv_text=cv_text or None,
            jd_text=jd_text or None,
            label=label,
            language=language,
            source="kaggle:resume_job_matching",
            meta={
                "dataset_type": "paired",
                "raw_fields": list(row.keys()),
            },
        )
