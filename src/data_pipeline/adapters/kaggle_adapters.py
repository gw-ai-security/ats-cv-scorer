from __future__ import annotations

from pathlib import Path
from typing import Iterable

from src.data_pipeline.ingest import canonical_record, read_rows


def ats_scoring_adapter(dataset_path: Path) -> Iterable[dict[str, object]]:
    for idx, row in enumerate(read_rows(dataset_path), start=1):
        cv_text = (row.get("resume_text") or "").strip()
        jd_text = (row.get("job_description") or "").strip()
        label = (row.get("label") or "").strip().lower() or None
        if not cv_text and not jd_text:
            continue
        yield canonical_record(
            record_id=f"ats_scoring_{idx:06d}",
            cv_text=cv_text or None,
            jd_text=jd_text or None,
            label=label,
            language=(row.get("language") or "unknown").lower(),
            source="kaggle:ats_scoring_dataset",
            meta={"raw_fields": list(row.keys())},
        )


def resume_job_matching_adapter(dataset_path: Path) -> Iterable[dict[str, object]]:
    for idx, row in enumerate(read_rows(dataset_path), start=1):
        cv_text = (row.get("resume") or row.get("cv_text") or "").strip()
        jd_text = (row.get("job_description") or row.get("jd_text") or "").strip()
        label = (row.get("match_label") or row.get("label") or "").strip().lower() or None
        if not cv_text and not jd_text:
            continue
        yield canonical_record(
            record_id=f"resume_job_{idx:06d}",
            cv_text=cv_text or None,
            jd_text=jd_text or None,
            label=label,
            language=(row.get("language") or "unknown").lower(),
            source="kaggle:resume_job_matching",
            meta={"raw_fields": list(row.keys())},
        )


def resume_ranking_adapter(dataset_path: Path) -> Iterable[dict[str, object]]:
    for idx, row in enumerate(read_rows(dataset_path), start=1):
        cv_text = (row.get("resume") or row.get("cv_text") or "").strip()
        jd_text = (row.get("job_description") or row.get("jd_text") or "").strip()
        label = (row.get("label") or row.get("rank") or "").strip().lower() or None
        if not cv_text and not jd_text:
            continue
        yield canonical_record(
            record_id=f"resume_rank_{idx:06d}",
            cv_text=cv_text or None,
            jd_text=jd_text or None,
            label=label if label in {"strong_match", "partial_match", "mismatch"} else None,
            language=(row.get("language") or "unknown").lower(),
            source="kaggle:resume_data_ranking",
            meta={"raw_fields": list(row.keys())},
        )


def job_descriptions_2025_adapter(dataset_path: Path) -> Iterable[dict[str, object]]:
    for idx, row in enumerate(read_rows(dataset_path), start=1):
        jd_text = (row.get("description") or row.get("job_description") or "").strip()
        if not jd_text:
            continue
        yield canonical_record(
            record_id=f"jd_2025_{idx:06d}",
            cv_text=None,
            jd_text=jd_text,
            label=None,
            language=(row.get("language") or "unknown").lower(),
            source="kaggle:job_descriptions_2025",
            meta={"raw_fields": list(row.keys())},
        )


def job_skill_set_adapter(dataset_path: Path) -> Iterable[dict[str, object]]:
    for idx, row in enumerate(read_rows(dataset_path), start=1):
        skill = (row.get("skill") or row.get("name") or "").strip()
        if not skill:
            continue
        yield canonical_record(
            record_id=f"skill_{idx:06d}",
            cv_text=None,
            jd_text=None,
            label=None,
            language="unknown",
            source="kaggle:job_skill_set",
            meta={"skill": skill, "category": row.get("category")},
        )
