from __future__ import annotations

from dataclasses import dataclass

import pytest

from src.core.ats_criteria_extractor import ATSCriteria
from src.core.jd_parser import JDParseResult
from src.core.matcher import HybridMLMatcher


@dataclass(frozen=True)
class DummySemanticResult:
    semantic_similarity: float
    top_matched_chunks: list[dict[str, object]]


class DummySemanticMatcher:
    def __init__(self, *args, **kwargs) -> None:
        pass

    def match(self, cv_text: str, jd_text: str) -> DummySemanticResult:
        return DummySemanticResult(
            semantic_similarity=0.75,
            top_matched_chunks=[{"chunk": "match", "similarity": 0.75}],
        )


def test_hybrid_matcher_explainability_keys(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("src.core.matcher.SemanticMatcher", DummySemanticMatcher)
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
    matcher = HybridMLMatcher()
    result = matcher.match(cv=cv, jd=jd, cv_text="cv", jd_text="jd")
    assert "semantic_similarity" in result.breakdown
    assert "top_matched_chunks" in result.breakdown
