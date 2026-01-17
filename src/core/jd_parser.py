from __future__ import annotations

from dataclasses import dataclass
import re

from src.core.skill_extractor import SkillExtractor


@dataclass(frozen=True)
class JDParseResult:
    role: str
    seniority: str
    location: str
    remote: str
    requirements: list[str]
    nice_to_have: list[str]
    responsibilities: list[str]
    skills: list[str]
    keywords: list[str]
    missing_fields: list[str]


class JDParser:
    """
    FR-006: Deterministic parsing of job descriptions (DE/EN headers).
    """

    _SECTION_ALIASES = {
        "requirements": [
            "requirements",
            "qualifications",
            "must have",
            "must-have",
            "anforderungen",
            "profil",
            "ihr profil",
            "dein profil",
            "was du mitbringst",
            "was sie mitbringen",
            "qualifikationen",
        ],
        "nice_to_have": [
            "nice to have",
            "nice-to-have",
            "preferred",
            "optional",
            "wuensche",
            "bonus",
            "wuensche und pluspunkte",
            "nice to have skills",
        ],
        "responsibilities": [
            "responsibilities",
            "duties",
            "what you will do",
            "what you do",
            "aufgaben",
            "verantwortlichkeiten",
            "deine aufgaben",
            "ihr aufgabengebiet",
        ],
    }

    _SENIORITY_TERMS = [
        "internship",
        "intern",
        "werkstudent",
        "trainee",
        "student",
        "junior",
        "mid",
        "senior",
        "lead",
        "principal",
    ]

    def __init__(self) -> None:
        self._section_lookup = self._build_section_lookup()
        self._skill_extractor = SkillExtractor()

    def parse(self, text: str) -> JDParseResult:
        lines = self._lines(text)
        normalized_text = self._normalize_text(text)
        sections = self._split_sections(lines)

        role = self._extract_role(lines)
        seniority = self._extract_seniority(normalized_text)
        location = self._extract_location(lines)
        remote = "yes" if self._is_remote(normalized_text) else "no"

        requirements = self._extract_list(sections.get("requirements", []))
        nice_to_have = self._extract_list(sections.get("nice_to_have", []))
        responsibilities = self._extract_list(sections.get("responsibilities", []))

        skills = self._extract_skills(text)
        keywords = self._extract_keywords(requirements + nice_to_have + responsibilities)

        missing_fields = self._missing_fields(
            role=role,
            seniority=seniority,
            location=location,
            requirements=requirements,
            responsibilities=responsibilities,
        )

        return JDParseResult(
            role=role or "not_found",
            seniority=seniority or "not_found",
            location=location or "not_found",
            remote=remote,
            requirements=requirements,
            nice_to_have=nice_to_have,
            responsibilities=responsibilities,
            skills=skills,
            keywords=keywords,
            missing_fields=missing_fields,
        )

    @staticmethod
    def _lines(text: str) -> list[str]:
        if not text:
            return []
        return [line.strip() for line in text.splitlines() if line.strip()]

    def _split_sections(self, lines: list[str]) -> dict[str, list[str]]:
        sections: dict[str, list[str]] = {key: [] for key in self._SECTION_ALIASES}
        current_section: str | None = None

        for raw_line in lines:
            line = raw_line.strip()
            if not line:
                continue

            inline_section, inline_content = self._detect_inline_header(line)
            if inline_section:
                current_section = inline_section
                if inline_content:
                    sections[current_section].append(inline_content)
                continue

            normalized = self._normalize_header(line)
            section = self._section_lookup.get(normalized)
            if section:
                current_section = section
                continue

            if current_section:
                sections[current_section].append(line)

        return sections

    def _extract_role(self, lines: list[str]) -> str:
        for line in lines[:8]:
            if re.search(r"(?i)\b(role|position|job title|stellenbezeichnung)\b", line):
                parts = re.split(r"[:\-]", line, maxsplit=1)
                return parts[-1].strip()
        for line in lines[:5]:
            if len(line.split()) <= 8 and not self._looks_like_header(line):
                return line
        return ""

    def _extract_seniority(self, normalized_text: str) -> str:
        for term in self._SENIORITY_TERMS:
            if re.search(rf"(?i)(?<!\w){re.escape(term)}(?!\w)", normalized_text):
                return term
        return ""

    @staticmethod
    def _extract_location(lines: list[str]) -> str:
        for line in lines:
            if re.search(r"(?i)\b(location|standort|ort|based in)\b", line):
                parts = re.split(r"[:\-]", line, maxsplit=1)
                return parts[-1].strip()
        return ""

    def _extract_list(self, lines: list[str]) -> list[str]:
        bullets = []
        for line in lines:
            if re.match(r"^\s*[-*\u2022]\s+", line):
                bullets.append(re.sub(r"^\s*[-*\u2022]\s+", "", line).strip())
            elif re.match(r"^\s*\d+[\).]\s+", line):
                bullets.append(re.sub(r"^\s*\d+[\).]\s+", "", line).strip())
        return bullets if bullets else lines

    def _extract_skills(self, text: str) -> list[str]:
        skill_result = self._skill_extractor.extract(text)
        combined = (
            skill_result.skills["technical"]
            + skill_result.skills["soft"]
            + skill_result.skills["languages"]
            + skill_result.skills["certifications"]
        )
        return self._dedupe(combined)

    @staticmethod
    def _extract_keywords(lines: list[str]) -> list[str]:
        if not lines:
            return []
        text = " ".join(lines).lower()
        tokens = re.split(r"[^a-z0-9]+", text)
        stop_words = {
            "and",
            "or",
            "the",
            "with",
            "for",
            "a",
            "an",
            "of",
            "to",
            "in",
            "und",
            "oder",
            "mit",
            "fuer",
            "ein",
            "eine",
            "von",
            "zu",
        }
        results = [token for token in tokens if len(token) > 2 and token not in stop_words]
        return JDParser._dedupe(results)

    @staticmethod
    def _missing_fields(
        role: str,
        seniority: str,
        location: str,
        requirements: list[str],
        responsibilities: list[str],
    ) -> list[str]:
        missing = []
        if not role:
            missing.append("role")
        if not seniority:
            missing.append("seniority")
        if not location:
            missing.append("location")
        if not requirements:
            missing.append("requirements")
        if not responsibilities:
            missing.append("responsibilities")
        return missing

    def _build_section_lookup(self) -> dict[str, str]:
        lookup: dict[str, str] = {}
        for section, aliases in self._SECTION_ALIASES.items():
            for alias in aliases:
                lookup[self._normalize_header(alias)] = section
        return lookup

    @staticmethod
    def _replace_umlauts(text: str) -> str:
        return (
            text.replace("\u00e4", "ae")
            .replace("\u00f6", "oe")
            .replace("\u00fc", "ue")
            .replace("\u00df", "ss")
        )

    def _normalize_header(self, text: str) -> str:
        return self._normalize_text(text)

    def _detect_inline_header(self, line: str) -> tuple[str | None, str]:
        if ":" not in line:
            return None, ""
        left, right = line.split(":", 1)
        section = self._section_lookup.get(self._normalize_header(left))
        if not section:
            return None, ""
        return section, right.strip()

    def _normalize_text(self, text: str) -> str:
        text = self._replace_umlauts(text.strip().lower())
        text = re.sub(r"[^a-z0-9\s]", " ", text)
        text = re.sub(r"\s+", " ", text).strip()
        return text

    def _looks_like_header(self, line: str) -> bool:
        normalized = self._normalize_header(line)
        return normalized in self._section_lookup

    @staticmethod
    def _is_remote(text: str) -> bool:
        return bool(
            re.search(
                r"(?i)\b(remote|hybrid|home office|homeoffice|fully remote)\b",
                text,
            )
        )

    @staticmethod
    def _dedupe(values: list[str]) -> list[str]:
        seen = set()
        result = []
        for value in values:
            key = value.strip().lower()
            if not key or key in seen:
                continue
            seen.add(key)
            result.append(value.strip())
        return result
