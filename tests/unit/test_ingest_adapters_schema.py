from __future__ import annotations

from pathlib import Path

from src.data_ingest.adapters import ADAPTERS


FIXTURES = {
    "ats_scoring_dataset": {
        "path": Path("tests/fixtures/ingest/ats_scoring_dataset/train_data.json"),
        "dataset_type": "cv_only",
    },
    "resume_job_matching": {
        "path": Path("tests/fixtures/ingest/resume_job_matching/train.csv"),
        "dataset_type": "paired",
    },
    "resume_data_ranking": {
        "path": Path("tests/fixtures/ingest/resume_data_ranking/resume_data_for_ranking.csv"),
        "dataset_type": "paired",
    },
    "job_descriptions_2025": {
        "path": Path("tests/fixtures/ingest/job_descriptions_2025/job_dataset.csv"),
        "dataset_type": "jd_only",
    },
    "job_skill_set": {
        "path": Path("tests/fixtures/ingest/job_skill_set/resume_extraction.csv"),
        "dataset_type": "skills_only",
    },
}


def test_adapter_fixtures_schema() -> None:
    for dataset_id, spec in FIXTURES.items():
        adapter = ADAPTERS[dataset_id]
        records = list(adapter(spec["path"]))
        assert records, f"{dataset_id} produced no records"
        record = records[0]
        assert "id" in record
        assert "source" in record
        assert "meta" in record
        assert record["meta"].get("dataset_type") == spec["dataset_type"]
        if spec["dataset_type"] == "paired":
            assert record.get("cv_text")
            assert record.get("jd_text")
        if spec["dataset_type"] == "cv_only":
            assert record.get("cv_text")
        if spec["dataset_type"] == "jd_only":
            assert record.get("jd_text")
