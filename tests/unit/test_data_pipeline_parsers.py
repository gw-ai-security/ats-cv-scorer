from __future__ import annotations

import csv
import json
from pathlib import Path

from src.data_pipeline.parsers import parse_jd_records, parse_resume_records, parse_skillset_records


def _read_jsonl(path: Path) -> list[dict[str, object]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def test_parsers_write_jsonl(tmp_path: Path) -> None:
    resumes_csv = tmp_path / "resumes.csv"
    jds_csv = tmp_path / "jds.csv"
    skills_csv = tmp_path / "skills.csv"

    with resumes_csv.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["text", "language"])
        writer.writeheader()
        writer.writerow({"text": "Profile: Python developer", "language": "en"})

    with jds_csv.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["description", "language"])
        writer.writeheader()
        writer.writerow({"description": "Required: Python", "language": "en"})

    with skills_csv.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["skill", "category"])
        writer.writeheader()
        writer.writerow({"skill": "python", "category": "technical"})

    resume_out = tmp_path / "resumes.jsonl"
    jd_out = tmp_path / "jds.jsonl"
    skill_out = tmp_path / "skills.jsonl"

    parse_resume_records(resumes_csv, resume_out, "text")
    parse_jd_records(jds_csv, jd_out, "description")
    parse_skillset_records(skills_csv, skill_out, "skill", "category")

    resumes = _read_jsonl(resume_out)
    jds = _read_jsonl(jd_out)
    skills = _read_jsonl(skill_out)

    assert resumes[0]["record_id"].startswith("resume_")
    assert jds[0]["record_id"].startswith("jd_")
    assert skills[0]["record_id"].startswith("skill_")
