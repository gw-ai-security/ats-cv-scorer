from __future__ import annotations

from pathlib import Path
from typing import Iterable

from src.data_ingest.adapters.base import canonical_record, map_fields, normalize_text, read_rows


MAPPING = {
    "skill": "skill",
    "category": "category",
}


def parse(path: Path) -> Iterable[dict[str, object]]:
    for idx, row in enumerate(read_rows(path), start=1):
        fields = map_fields(row, MAPPING)
        raw_skill = fields.get("skill") or row.get("skills ") or row.get("skills") or row.get("job_skill_set")
        if not raw_skill:
            continue
        skills = [normalize_text(item) for item in str(raw_skill).split(",") if normalize_text(item)]
        category = fields.get("category") or row.get("Job_title") or row.get("category")
        for offset, skill in enumerate(skills):
            yield canonical_record(
                record_id=f"skill_{idx:06d}_{offset:02d}",
                cv_text=None,
                jd_text=None,
                label=None,
                language="unknown",
                source="kaggle:job_skill_set",
                meta={
                    "skill": skill,
                    "category": category,
                    "dataset_type": "skills_only",
                    "raw_fields": list(row.keys()),
                },
            )
