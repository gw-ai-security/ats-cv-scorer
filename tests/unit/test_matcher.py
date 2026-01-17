from src.core.ats_criteria_extractor import ATSCriteria
from src.core.jd_parser import JDParseResult
from src.core.matcher import BaselineMatcher


def test_baseline_matching_scores_and_explanations():
    cv = ATSCriteria(
        contact={"name": "Jane", "email": "jane@example.com", "phone": "123", "location": "Vienna", "links": "not_found"},
        summary="Profile text",
        experience=[{"role": "Analyst", "company": "ACME", "timeframe": "2021-2023", "responsibilities": ""}],
        education=[{"role": "BSc", "company": "FH", "timeframe": "2020-2023", "responsibilities": ""}],
        skills={
            "hard": ["python", "sql"],
            "soft": ["communication"],
            "languages": ["english", "german"],
            "certifications": [],
            "tools": ["git"],
            "methods": [],
        },
        certifications=[],
        languages=["english", "german"],
        availability="Start: 2026",
        missing_fields=[],
    )

    jd = JDParseResult(
        role="Data Analyst",
        seniority="senior",
        location="Vienna",
        remote="no",
        requirements=["Python", "SQL"],
        nice_to_have=[],
        responsibilities=["Build dashboards"],
        skills=["python", "sql"],
        keywords=["python", "sql", "dashboards"],
        missing_fields=[],
    )

    matcher = BaselineMatcher()
    result = matcher.match(cv, jd)

    assert result.score > 0
    assert "skills" in result.breakdown
    assert result.breakdown["location"]["score"] in (0.0, 1.0)
