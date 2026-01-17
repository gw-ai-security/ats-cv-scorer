from src.core.cv_analyzer import CVAnalyzer


def test_detects_de_en_section_headers():
    text = "\n".join(
        [
            "Max Mustermann",
            "max@example.com",
            "Berufserfahrung",
            "Company A - Developer",
            "Ausbildung",
            "TU Berlin",
            "Skills: Python, SQL",
            "Projects",
            "ATS CV Scorer",
        ]
    )

    analyzer = CVAnalyzer()
    result = analyzer.analyze_sections(text)

    assert "Max Mustermann" in result.sections["contact"]
    assert "Company A - Developer" in result.sections["experience"]
    assert "TU Berlin" in result.sections["education"]
    assert "Python, SQL" in result.sections["skills"]
    assert "ATS CV Scorer" in result.sections["projects"]


def test_graceful_degradation_without_headers():
    text = "Jane Doe\njane@example.com\nData Analyst"

    analyzer = CVAnalyzer()
    result = analyzer.analyze_sections(text)

    assert "Jane Doe" in result.sections["contact"]
    assert result.sections["experience"] == ""
    assert result.sections["education"] == ""
    assert result.sections["skills"] == ""
    assert result.sections["projects"] == ""
