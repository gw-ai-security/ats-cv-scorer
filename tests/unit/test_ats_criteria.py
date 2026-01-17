from src.core.ats_criteria_extractor import ATSCriteriaExtractor


def test_extracts_core_ats_fields():
    text = "\n".join(
        [
            "Jane Doe",
            "jane.doe@example.com",
            "+43 650 1234567",
            "Location: Vienna",
            "Profile",
            "Business Informatics student with interest in AI.",
            "Professional Experience",
            "Data Analyst",
            "ACME Corp | 2021-2023",
            "Built dashboards and reports",
            "Education",
            "BSc Business Informatics",
            "FH Technikum Wien | 2020-2023",
            "Skills",
            "Python, SQL, Git",
            "Languages",
            "German, English",
            "Availability",
            "Start: January 2026",
        ]
    )

    extractor = ATSCriteriaExtractor()
    result = extractor.extract(text)

    assert result.contact["name"] == "Jane Doe"
    assert result.contact["email"] == "jane.doe@example.com"
    assert result.contact["phone"].startswith("+43")
    assert result.contact["location"] == "Vienna"
    assert result.summary != "not_found"
    assert result.experience
    assert result.education
    assert "python" in result.skills["hard"]
    assert "git" in result.skills["tools"]
    assert "german" in result.languages
    assert result.availability != "not_found"


def test_missing_fields_marked_not_found():
    extractor = ATSCriteriaExtractor()
    result = extractor.extract("")

    assert result.contact["name"] == "not_found"
    assert result.summary == "not_found"
    assert result.experience == []
    assert result.education == []
    assert result.availability == "not_found"
