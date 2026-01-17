from __future__ import annotations

from dataclasses import dataclass
import re

SECTION_KEYS = ("contact", "experience", "education", "skills", "projects")

_HEADER_ALIASES = {
    "contact": [
        "contact",
        "kontakt",
        "personal info",
        "personal information",
        "profil",
        "summary",
    ],
    "experience": [
        "experience",
        "work experience",
        "professional experience",
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
        "kenntnisse",
        "kompetenzen",
        "faehigkeiten",
    ],
    "projects": [
        "projects",
        "project experience",
        "projekte",
    ],
}


def _replace_umlauts(text: str) -> str:
    return (
        text.replace("\u00e4", "ae")
        .replace("\u00f6", "oe")
        .replace("\u00fc", "ue")
        .replace("\u00df", "ss")
    )


def _normalize_header(text: str) -> str:
    text = _replace_umlauts(text.strip().lower())
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


_HEADER_LOOKUP = {
    _normalize_header(alias): section
    for section, aliases in _HEADER_ALIASES.items()
    for alias in aliases
}


@dataclass(frozen=True)
class CVSectionResult:
    sections: dict[str, str]
    headers_found: list[str]


class CVAnalyzer:
    """
    FR-003: Best-effort section detection for common CV headers in DE/EN.
    """

    def analyze_sections(self, text: str) -> CVSectionResult:
        sections: dict[str, list[str]] = {key: [] for key in SECTION_KEYS}
        headers_found: list[str] = []
        current_section: str | None = None

        if not text:
            return CVSectionResult(
                sections={key: "" for key in SECTION_KEYS},
                headers_found=[],
            )

        for raw_line in text.splitlines():
            line = raw_line.strip()
            if not line:
                continue

            inline_section, inline_content = self._detect_inline_header(line)
            if inline_section:
                current_section = inline_section
                headers_found.append(inline_section)
                if inline_content:
                    sections[current_section].append(inline_content)
                continue

            normalized = _normalize_header(line)
            section = _HEADER_LOOKUP.get(normalized)
            if section:
                current_section = section
                headers_found.append(section)
                continue

            if current_section is None:
                current_section = "contact"
            sections[current_section].append(line)

        return CVSectionResult(
            sections={key: "\n".join(lines).strip() for key, lines in sections.items()},
            headers_found=headers_found,
        )

    @staticmethod
    def _detect_inline_header(line: str) -> tuple[str | None, str]:
        if ":" not in line:
            return None, ""
        left, right = line.split(":", 1)
        section = _HEADER_LOOKUP.get(_normalize_header(left))
        if not section:
            return None, ""
        return section, right.strip()
