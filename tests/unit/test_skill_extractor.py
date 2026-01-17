from src.core.skill_extractor import SkillExtractor


def test_extracts_skills_with_synonyms_and_categories():
    text = "Experienced in Python, JS, and SQL. Strong teamwork. Deutsch, English."
    extractor = SkillExtractor()
    result = extractor.extract(text)

    assert result.skills["technical"] == ["javascript", "python", "sql"]
    assert result.skills["soft"] == ["teamwork"]
    assert result.skills["languages"] == ["english", "german"]
    assert result.skills["certifications"] == []


def test_empty_text_returns_empty_sets():
    extractor = SkillExtractor()
    result = extractor.extract("")

    assert result.skills["technical"] == []
    assert result.skills["soft"] == []
    assert result.skills["languages"] == []
    assert result.skills["certifications"] == []
