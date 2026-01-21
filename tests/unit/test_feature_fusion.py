from __future__ import annotations

from src.core.ats_criteria_extractor import ATSCriteria
from src.core.jd_parser import JDParseResult
from src.core.ml.feature_fusion import fuse_features


def test_feature_fusion_output_schema() -> None:
    cv = ATSCriteria(
        contact={"name": "A", "email": "a@b.com", "phone": "1", "location": "Vienna", "links": ""},
        summary="summary",
        experience=[{"role": "Engineer", "company": "X", "timeframe": "", "responsibilities": ""}],
        education=[{"role": "BSc", "company": "Y", "timeframe": "", "responsibilities": ""}],
        skills={"hard": ["python"], "soft": [], "languages": [], "certifications": [], "tools": [], "methods": []},
        certifications=[],
        languages=["english"],
        availability="not_found",
        missing_fields=[],
    )
    jd = JDParseResult(
        role="Engineer",
        seniority="junior",
        location="Vienna",
        remote="no",
        requirements=["Python"],
        nice_to_have=[],
        responsibilities=[],
        skills=["python"],
        keywords=["python"],
        missing_fields=[],
    )
    fusion = fuse_features(semantic_similarity=0.8, cv=cv, jd=jd)
    assert 0.0 <= fusion.score <= 100.0
    assert fusion.semantic_similarity == 0.8
    assert fusion.skill_overlap_score >= 0.0
