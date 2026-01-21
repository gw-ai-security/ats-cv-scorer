from __future__ import annotations

from src.core.ats_criteria_extractor import ATSCriteriaExtractor
from src.core.jd_parser import JDParser
from src.core.matcher import BaselineMatcher
from src.core.pdf_layout import render_score_report_pdf


def test_render_score_report_pdf() -> None:
    cv_text = "\n".join(
        [
            "Contact: Jordan Taylor",
            "Profile: Backend engineer with Python and SQL.",
            "Experience: 2021-2024 Backend Engineer",
            "Skills: Python, SQL, Communication",
        ]
    )
    jd_text = "\n".join(
        [
            "Backend Engineer",
            "Responsibilities:",
            "- Build services",
            "Required:",
            "- Python",
            "- SQL",
        ]
    )

    ats = ATSCriteriaExtractor().extract(cv_text)
    jd = JDParser().parse(jd_text)
    match = BaselineMatcher().match(ats, jd)

    pdf_bytes = render_score_report_pdf(match=match, ats=ats, jd=jd, strategy="rule_based")
    assert pdf_bytes[:4] == b"%PDF"
