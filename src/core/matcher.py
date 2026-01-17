from __future__ import annotations

from dataclasses import dataclass

from src.core.ats_criteria_extractor import ATSCriteria
from src.core.jd_parser import JDParseResult


@dataclass(frozen=True)
class MatchResult:
    score: float
    breakdown: dict[str, dict[str, object]]


class BaselineMatcher:
    """
    FR-007: Deterministic, explainable baseline matching.
    """

    def __init__(self, weights: dict[str, float] | None = None) -> None:
        self.weights = weights or {
            "skills": 0.5,
            "experience": 0.2,
            "education": 0.15,
            "language": 0.1,
            "location": 0.05,
        }

    def match(self, cv: ATSCriteria, jd: JDParseResult) -> MatchResult:
        skill_score, skill_detail = self._match_skills(cv, jd)
        experience_score, experience_detail = self._match_experience(cv, jd)
        education_score, education_detail = self._match_education(cv, jd)
        language_score, language_detail = self._match_language(cv, jd)
        location_score, location_detail = self._match_location(cv, jd)

        total = (
            skill_score * self.weights["skills"]
            + experience_score * self.weights["experience"]
            + education_score * self.weights["education"]
            + language_score * self.weights["language"]
            + location_score * self.weights["location"]
        )

        breakdown = {
            "skills": skill_detail | {"score": skill_score},
            "experience": experience_detail | {"score": experience_score},
            "education": education_detail | {"score": education_score},
            "language": language_detail | {"score": language_score},
            "location": location_detail | {"score": location_score},
        }

        return MatchResult(score=round(total * 100, 2), breakdown=breakdown)

    @staticmethod
    def _match_skills(cv: ATSCriteria, jd: JDParseResult) -> tuple[float, dict[str, object]]:
        cv_skills = BaselineMatcher._collect_cv_skills(cv)
        jd_skills = BaselineMatcher._collect_jd_skills(jd)

        if not jd_skills:
            return 1.0, {"matched": [], "gaps": [], "note": "no_jd_skills"}

        matched = sorted(cv_skills & jd_skills)
        gaps = sorted(jd_skills - cv_skills)
        score = len(matched) / max(len(jd_skills), 1)

        return score, {"matched": matched, "gaps": gaps}

    @staticmethod
    def _match_experience(cv: ATSCriteria, jd: JDParseResult) -> tuple[float, dict[str, object]]:
        if jd.seniority == "not_found":
            return 1.0, {"note": "no_seniority_requirement"}
        score = 1.0 if cv.experience else 0.0
        return score, {"seniority": jd.seniority, "has_experience": bool(cv.experience)}

    @staticmethod
    def _match_education(cv: ATSCriteria, jd: JDParseResult) -> tuple[float, dict[str, object]]:
        jd_text = " ".join(jd.requirements + jd.nice_to_have + jd.responsibilities).lower()
        requires_degree = any(term in jd_text for term in ("bachelor", "master", "phd"))
        if not requires_degree:
            return 1.0, {"note": "no_degree_requirement"}
        score = 1.0 if cv.education else 0.0
        return score, {"requires_degree": True, "has_education": bool(cv.education)}

    @staticmethod
    def _match_language(cv: ATSCriteria, jd: JDParseResult) -> tuple[float, dict[str, object]]:
        jd_lang = {skill for skill in jd.skills if skill in {"german", "english"}}
        cv_lang = {lang.lower() for lang in cv.languages}
        if not jd_lang:
            return 1.0, {"note": "no_language_requirement"}
        matched = sorted(jd_lang & cv_lang)
        gaps = sorted(jd_lang - cv_lang)
        score = len(matched) / max(len(jd_lang), 1)
        return score, {"matched": matched, "gaps": gaps}

    @staticmethod
    def _match_location(cv: ATSCriteria, jd: JDParseResult) -> tuple[float, dict[str, object]]:
        if jd.remote == "yes":
            return 1.0, {"note": "remote_role"}
        if jd.location == "not_found":
            return 1.0, {"note": "no_location_requirement"}
        cv_location = cv.contact.get("location", "").lower()
        match = jd.location.lower() in cv_location if cv_location else False
        return 1.0 if match else 0.0, {"jd_location": jd.location, "cv_location": cv_location}

    @staticmethod
    def _collect_cv_skills(cv: ATSCriteria) -> set[str]:
        values = []
        for group in cv.skills.values():
            values.extend(group)
        values.extend(cv.certifications)
        values.extend(cv.languages)
        return {value.lower() for value in values if value}

    @staticmethod
    def _collect_jd_skills(jd: JDParseResult) -> set[str]:
        values = jd.skills + jd.keywords
        return {value.lower() for value in values if value}
