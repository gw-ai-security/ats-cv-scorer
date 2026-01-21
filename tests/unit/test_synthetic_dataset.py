from __future__ import annotations

import json
from pathlib import Path

from src.core.ats_criteria_extractor import ATSCriteriaExtractor
from src.core.jd_parser import JDParser
from src.core.matcher import BaselineMatcher


def _load_pairs(fixtures_dir: Path) -> list[dict[str, object]]:
    pairs_path = fixtures_dir / "pairs.jsonl"
    with pairs_path.open("r", encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def test_synthetic_pairs_matcher_scores_and_explainability() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    fixtures_dir = repo_root / "tests" / "fixtures" / "synth"
    pairs = _load_pairs(fixtures_dir)

    matcher = BaselineMatcher()
    cv_extractor = ATSCriteriaExtractor()
    jd_parser = JDParser()

    for record in pairs:
        cv_text = (fixtures_dir / record["cv_file"]).read_text(encoding="utf-8")
        jd_text = (fixtures_dir / record["jd_file"]).read_text(encoding="utf-8")

        cv = cv_extractor.extract(cv_text)
        jd = jd_parser.parse(jd_text)
        result = matcher.match(cv, jd)

        expected_min, expected_max = record["expected_score_range"]
        assert expected_min <= result.score <= expected_max

        breakdown = result.breakdown["skills"]
        matched = {skill.lower() for skill in breakdown["matched"]}
        gaps = {skill.lower() for skill in breakdown["gaps"]}

        expected_matched = {skill.lower() for skill in record["matched_skills"]}
        expected_missing = {skill.lower() for skill in record["missing_required_skills"]}

        assert expected_matched.issubset(matched)
        assert expected_missing.issubset(gaps)
