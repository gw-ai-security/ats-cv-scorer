from __future__ import annotations

from dataclasses import dataclass
import re

from src.core.skill_extractor import SkillExtractor


@dataclass(frozen=True)
class ATSCriteria:
    contact: dict[str, str]
    summary: str
    experience: list[dict[str, str]]
    education: list[dict[str, str]]
    skills: dict[str, list[str]]
    certifications: list[str]
    languages: list[str]
    availability: str
    missing_fields: list[str]


class ATSCriteriaExtractor:
    """
    FR-005: Deterministic parsing of recruiter-facing criteria from CV text.
    """

    _SECTION_ALIASES = {
        "contact": [
            "contact",
            "kontakt",
            "personal info",
            "personal information",
            "personalia",
        ],
        "summary": [
            "summary",
            "profile",
            "profil",
            "about me",
            "ueber mich",
        ],
        "experience": [
            "experience",
            "work experience",
            "professional experience",
            "professional experience transfer skills",
            "employment",
            "work history",
            "berufserfahrung",
            "erfahrung",
        ],
        "education": [
            "education",
            "academic background",
            "ausbildung",
            "studium",
        ],
        "skills": [
            "skills",
            "technical skills",
            "soft skills",
            "core competencies",
            "competencies",
            "kenntnisse",
            "kompetenzen",
            "faehigkeiten",
        ],
        "projects": [
            "projects",
            "selected projects",
            "project experience",
            "projekte",
        ],
        "certifications": [
            "certifications",
            "certificates",
            "zertifikate",
        ],
        "languages": [
            "languages",
            "sprachen",
        ],
        "availability": [
            "availability",
            "verfuegbarkeit",
            "notice period",
            "start date",
            "start",
            "kuendigungsfrist",
        ],
    }

    _TOOL_TERMS = [
        "git",
        "github",
        "gitlab",
        "jira",
        "confluence",
        "docker",
        "kubernetes",
        "aws",
        "azure",
    ]
    _METHOD_TERMS = [
        "agile",
        "scrum",
        "kanban",
        "bpmn",
        "sdlc",
        "requirements engineering",
        "business process engineering",
    ]
    _LANGUAGE_TERMS = [
        "german",
        "english",
        "deutsch",
        "englisch",
        "french",
        "spanish",
    ]

    def __init__(self) -> None:
        self._section_lookup = self._build_section_lookup()
        self._skill_extractor = SkillExtractor()

    def extract(self, text: str) -> ATSCriteria:
        lines = self._lines(text)
        sections = self._split_sections(lines)

        contact = self._extract_contact(sections.get("contact", []), lines)
        summary = self._extract_summary(sections.get("summary", []))
        experience = self._extract_experience(sections.get("experience", []))
        education = self._extract_education(sections.get("education", []))
        skills = self._extract_skills(text, sections.get("skills", []))
        certifications = self._extract_certifications(sections.get("certifications", []), lines)
        languages = self._extract_languages(sections.get("languages", []), text)
        availability = self._extract_availability(sections.get("availability", []), lines)

        missing_fields = self._missing_fields(
            contact=contact,
            summary=summary,
            experience=experience,
            education=education,
            skills=skills,
            certifications=certifications,
            languages=languages,
            availability=availability,
        )

        return ATSCriteria(
            contact=contact,
            summary=summary,
            experience=experience,
            education=education,
            skills=skills,
            certifications=certifications,
            languages=languages,
            availability=availability,
            missing_fields=missing_fields,
        )

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

            if current_section is None:
                current_section = "contact"
            sections[current_section].append(line)

        return sections

    @staticmethod
    def _lines(text: str) -> list[str]:
        if not text:
            return []
        return [line.strip() for line in text.splitlines() if line.strip()]

    def _extract_contact(self, contact_lines: list[str], all_lines: list[str]) -> dict[str, str]:
        source = contact_lines if contact_lines else all_lines[:6]
        email = self._first_match(source, r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}")
        phone = self._first_match(source, r"\+?\d[\d\s\-()]{7,}\d")
        links = self._extract_links(source)
        name = self._extract_name(source)
        location = self._extract_location(all_lines)

        return {
            "name": name or "not_found",
            "email": email or "not_found",
            "phone": phone or "not_found",
            "location": location or "not_found",
            "links": ", ".join(links) if links else "not_found",
        }

    @staticmethod
    def _extract_summary(lines: list[str]) -> str:
        if not lines:
            return "not_found"
        return " ".join(lines).strip()

    def _extract_experience(self, lines: list[str]) -> list[dict[str, str]]:
        return self._extract_entries(lines)

    def _extract_education(self, lines: list[str]) -> list[dict[str, str]]:
        return self._extract_entries(lines)

    def _extract_skills(self, text: str, lines: list[str]) -> dict[str, list[str]]:
        skill_result = self._skill_extractor.extract(text)
        tools = self._find_terms(lines, self._TOOL_TERMS)
        methods = self._find_terms(lines, self._METHOD_TERMS)

        return {
            "hard": skill_result.skills["technical"],
            "soft": skill_result.skills["soft"],
            "languages": skill_result.skills["languages"],
            "certifications": skill_result.skills["certifications"],
            "tools": tools,
            "methods": methods,
        }

    def _extract_certifications(self, lines: list[str], all_lines: list[str]) -> list[str]:
        combined = lines if lines else all_lines
        results = []
        for line in combined:
            if re.search(r"(?i)\b(certified|certification|zertifikat|iso|aws)\b", line):
                results.append(line.strip())
        return self._dedupe(results)

    def _extract_languages(self, lines: list[str], text: str) -> list[str]:
        results = self._find_terms(lines, self._LANGUAGE_TERMS)
        results.extend(self._find_terms(self._lines(text), self._LANGUAGE_TERMS))
        return self._dedupe(results)

    def _extract_availability(self, lines: list[str], all_lines: list[str]) -> str:
        candidates = lines if lines else all_lines
        for line in candidates:
            if re.search(r"(?i)\b(availability|verfuegbarkeit|notice period|start)\b", line):
                return line.strip()
        if lines:
            return lines[0].strip()
        return "not_found"

    def _extract_entries(self, lines: list[str]) -> list[dict[str, str]]:
        if not lines:
            return []
        entries: list[dict[str, str]] = []
        current: dict[str, str] | None = None

        for line in lines:
            if self._looks_like_entry_header(line) or current is None:
                if current:
                    entries.append(current)
                current = {
                    "role": line,
                    "company": "",
                    "timeframe": self._extract_timeframe(line),
                    "responsibilities": "",
                }
            else:
                if not current["company"]:
                    current["company"] = line
                else:
                    current["responsibilities"] = (
                        f"{current['responsibilities']}\n{line}".strip()
                    )

        if current:
            entries.append(current)
        return entries

    @staticmethod
    def _looks_like_entry_header(line: str) -> bool:
        return bool(re.search(r"(?i)\b(19|20)\d{2}\b|since|present|ongoing", line))

    @staticmethod
    def _extract_timeframe(line: str) -> str:
        match = re.search(r"(?i)(\b(19|20)\d{2}\b.*)$", line)
        return match.group(1).strip() if match else ""

    @staticmethod
    def _first_match(lines: list[str], pattern: str) -> str:
        for line in lines:
            match = re.search(pattern, line, flags=re.IGNORECASE)
            if match:
                return match.group(0)
        return ""

    @staticmethod
    def _extract_links(lines: list[str]) -> list[str]:
        links = []
        for line in lines:
            for match in re.findall(r"https?://\S+", line):
                links.append(match.rstrip(").,"))
        return ATSCriteriaExtractor._dedupe(links)

    @staticmethod
    def _extract_name(lines: list[str]) -> str:
        for line in lines[:5]:
            if any(ch.isdigit() for ch in line) or "@" in line:
                continue
            if 2 <= len(line.split()) <= 4 and len(line) <= 60:
                return line.strip()
        return ""

    @staticmethod
    def _extract_location(lines: list[str]) -> str:
        for line in lines:
            if re.search(r"(?i)\b(location|standort|ort|based in)\b", line):
                parts = re.split(r"[:\-]", line, maxsplit=1)
                return parts[-1].strip()
        return ""

    @staticmethod
    def _find_terms(lines: list[str], terms: list[str]) -> list[str]:
        results = []
        text = " ".join(lines).lower()
        for term in terms:
            pattern = re.escape(term).replace(r"\ ", r"\s+")
            if re.search(rf"(?i)(?<!\w){pattern}(?!\w)", text):
                results.append(term.replace("deutsch", "german").replace("englisch", "english"))
        return ATSCriteriaExtractor._dedupe(results)

    def _missing_fields(
        self,
        contact: dict[str, str],
        summary: str,
        experience: list[dict[str, str]],
        education: list[dict[str, str]],
        skills: dict[str, list[str]],
        certifications: list[str],
        languages: list[str],
        availability: str,
    ) -> list[str]:
        missing = []
        for key, value in contact.items():
            if value == "not_found":
                missing.append(f"contact.{key}")
        if summary == "not_found":
            missing.append("summary")
        if not experience:
            missing.append("experience")
        if not education:
            missing.append("education")
        if not any(skills.values()):
            missing.append("skills")
        if not certifications:
            missing.append("certifications")
        if not languages:
            missing.append("languages")
        if availability == "not_found":
            missing.append("availability")
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
        text = self._replace_umlauts(text.strip().lower())
        text = re.sub(r"[^a-z0-9\s]", " ", text)
        text = re.sub(r"\s+", " ", text).strip()
        return text

    def _detect_inline_header(self, line: str) -> tuple[str | None, str]:
        if ":" not in line:
            return None, ""
        left, right = line.split(":", 1)
        section = self._section_lookup.get(self._normalize_header(left))
        if not section:
            return None, ""
        return section, right.strip()

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
