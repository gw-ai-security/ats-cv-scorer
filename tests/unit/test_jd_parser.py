from src.core.jd_parser import JDParser


def test_parses_jd_sections_and_metadata():
    text = "\n".join(
        [
            "Senior Data Analyst",
            "Location: Vienna",
            "Remote possible",
            "Requirements",
            "- Python",
            "- SQL",
            "Nice to have",
            "- AWS",
            "Responsibilities",
            "- Build dashboards",
            "- Support stakeholders",
        ]
    )

    parser = JDParser()
    result = parser.parse(text)

    assert result.role == "Senior Data Analyst"
    assert result.seniority == "senior"
    assert result.location == "Vienna"
    assert result.remote == "yes"
    assert "Python" in result.requirements
    assert "AWS" in result.nice_to_have
    assert result.responsibilities
    assert "python" in result.skills
    assert result.missing_fields == []


def test_parses_german_headers_and_numbered_lists():
    text = "\n".join(
        [
            "Data Analyst (m/w/d)",
            "Standort: Wien",
            "Dein Profil",
            "1. SQL",
            "2. Python",
            "Aufgaben",
            "- Reports erstellen",
            "Nice to have",
            "- AWS",
        ]
    )

    parser = JDParser()
    result = parser.parse(text)

    assert result.location == "Wien"
    assert "SQL" in result.requirements
    assert "Reports erstellen" in result.responsibilities
    assert "AWS" in result.nice_to_have
