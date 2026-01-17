from __future__ import annotations

from dataclasses import dataclass
import re


@dataclass(frozen=True)
class SkillExtractionResult:
    skills: dict[str, list[str]]


class SkillExtractor:
    """
    FR-004: Extract skills using a small in-memory database with synonyms.
    """

    _SKILL_DB: dict[str, list[str]] = {
        "technical": [
            "python",
            "javascript",
            "sql",
            "streamlit",
            "pandas",
            "numpy",
        ],
        "soft": [
            "communication",
            "leadership",
            "teamwork",
        ],
        "languages": [
            "german",
            "english",
        ],
        "certifications": [
            "aws certified solutions architect",
        ],
    }

    _SYNONYMS: dict[str, str] = {
        "js": "javascript",
        "py": "python",
        "aws sa": "aws certified solutions architect",
        "aws solutions architect": "aws certified solutions architect",
        "deutsch": "german",
        "englisch": "english",
    }

    def __init__(self) -> None:
        self._canonical_to_category = self._build_category_lookup()
        self._patterns = self._build_patterns()

    def extract(self, text: str) -> SkillExtractionResult:
        if not text:
            return SkillExtractionResult(skills=self._empty_result())

        found: dict[str, set[str]] = {key: set() for key in self._SKILL_DB}
        for pattern, canonical in self._patterns:
            if pattern.search(text):
                category = self._canonical_to_category.get(canonical)
                if category:
                    found[category].add(canonical)

        return SkillExtractionResult(
            skills={key: sorted(values) for key, values in found.items()}
        )

    def _empty_result(self) -> dict[str, list[str]]:
        return {key: [] for key in self._SKILL_DB}

    def _build_category_lookup(self) -> dict[str, str]:
        lookup: dict[str, str] = {}
        for category, skills in self._SKILL_DB.items():
            for skill in skills:
                lookup[skill] = category
        return lookup

    def _build_patterns(self) -> list[tuple[re.Pattern[str], str]]:
        patterns: list[tuple[re.Pattern[str], str]] = []

        def add_pattern(term: str, canonical: str) -> None:
            escaped = re.escape(term).replace(r"\ ", r"\s+")
            regex = re.compile(rf"(?i)(?<!\w){escaped}(?!\w)")
            patterns.append((regex, canonical))

        for category, skills in self._SKILL_DB.items():
            for skill in skills:
                add_pattern(skill, skill)

        for alias, canonical in self._SYNONYMS.items():
            add_pattern(alias, canonical)

        return patterns
