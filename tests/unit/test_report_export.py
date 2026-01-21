from __future__ import annotations

from src.core.ats_criteria_extractor import ATSCriteriaExtractor
from src.core.jd_parser import JDParser
from src.core.matcher import BaselineMatcher
from src.core.report_export import build_report_payload, render_report_markdown, json_dumps


def test_report_export_payload_and_markdown() -> None:
    cv_text = "Profile: Data engineer with Python and SQL. Experience: ETL pipelines."
    jd_text = "Data Engineer role. Required: Python, SQL."

    ats = ATSCriteriaExtractor().extract(cv_text)
    jd = JDParser().parse(jd_text)
    match = BaselineMatcher().match(ats, jd)

    payload = build_report_payload(match=match, ats=ats, jd=jd, strategy="rule_based")
    assert "meta" in payload
    assert "summary" in payload
    assert "score_breakdown" in payload

    md_text = render_report_markdown(payload)
    assert "ATS CV Scorer - Match Report" in md_text

    json_text = json_dumps(payload)
    assert "\"summary\"" in json_text
