from __future__ import annotations

from pathlib import Path

from src.data_ingest.adapters import ADAPTERS
from src.data_ingest.registry import list_dataset_ids, load_registry
from src.data_ingest.schema import validate_canonical_record


def test_registry_loader() -> None:
    registry = load_registry()
    assert "datasets" in registry
    ids = list_dataset_ids()
    assert "resume_job_matching" in ids


def test_resume_job_matching_adapter_fixture() -> None:
    fixture = Path("tests/fixtures/kaggle/resume_job_matching_sample.csv")
    adapter = ADAPTERS["resume_job_matching"]
    records = list(adapter(fixture))
    assert records
    errors = validate_canonical_record(records[0])
    assert errors == []


def test_schema_validation_flags_invalid_label() -> None:
    record = {
        "id": "x",
        "cv_text": "cv",
        "jd_text": "jd",
        "label": "invalid",
        "language": "en",
        "source": "kaggle:test",
        "meta": {},
    }
    errors = validate_canonical_record(record)
    assert "invalid_label" in errors
