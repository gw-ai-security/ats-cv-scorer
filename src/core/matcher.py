from __future__ import annotations

from dataclasses import dataclass
import os
import re

from src.core.ml.calibration import Calibrator
from src.core.ml.feature_fusion import FusionResult, fuse_features
from src.core.ml.semantic_matcher import SemanticMatcher

from src.core.ats_criteria_extractor import ATSCriteria
from src.core.jd_parser import JDParseResult
from src.utils.config import is_evaluation_gate_open


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
        penalties = self._build_penalties(cv, jd)

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
            "penalties": penalties,
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
        evidence = BaselineMatcher._skill_evidence(cv, matched)
        evidence_ratio = evidence["evidence_ratio"]
        if matched:
            score *= evidence_ratio

        return score, {
            "matched": matched,
            "gaps": gaps,
            "evidence_ratio": evidence_ratio,
            "unverified_skills": evidence["unverified_skills"],
            "evidence_snippets": evidence["evidence_snippets"],
        }

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

    @staticmethod
    def _build_penalties(cv: ATSCriteria, jd: JDParseResult) -> dict[str, object]:
        cv_skills = BaselineMatcher._collect_cv_skills(cv)
        jd_skills = BaselineMatcher._collect_jd_skills(jd)
        missing_required = sorted(jd_skills - cv_skills)
        has_skills = bool(cv_skills)
        keyword_stuffing_risk = has_skills and not cv.experience
        evidence = BaselineMatcher._skill_evidence(cv, sorted(cv_skills & jd_skills))
        return {
            "missing_required_skills": missing_required,
            "missing_required_count": len(missing_required),
            "keyword_stuffing_risk": keyword_stuffing_risk,
            "unverified_skill_count": len(evidence["unverified_skills"]),
            "evidence_ratio": evidence["evidence_ratio"],
        }

    @staticmethod
    def _skill_evidence(cv: ATSCriteria, matched: list[str]) -> dict[str, object]:
        if not matched:
            return {"evidence_ratio": 1.0, "unverified_skills": [], "evidence_snippets": {}}
        evidence_snippets: dict[str, str] = {}
        unverified = []
        experience_lines = []
        for entry in cv.experience:
            for key in ("role", "company", "responsibilities"):
                value = entry.get(key, "")
                if value:
                    experience_lines.append(value)
        if cv.summary and cv.summary != "not_found":
            experience_lines.append(cv.summary)
        combined = " ".join(experience_lines).lower()
        for skill in matched:
            skill_lower = skill.lower()
            if skill_lower in combined:
                snippet = ""
                for line in experience_lines:
                    if re.search(rf"(?i)\\b{re.escape(skill_lower)}\\b", line):
                        snippet = line.strip()
                        break
                evidence_snippets[skill] = snippet[:140] if snippet else "evidence_found"
            else:
                unverified.append(skill)
        evidence_ratio = (len(matched) - len(unverified)) / max(len(matched), 1)
        return {
            "evidence_ratio": round(evidence_ratio, 4),
            "unverified_skills": unverified,
            "evidence_snippets": evidence_snippets,
        }


class HybridMLMatcher:
    """
    Optional ML matcher that keeps the baseline intact and adds explainable signals.
    """

    def __init__(
        self,
        calibrator_path: str | None = None,
        top_k_chunks: int = 3,
    ) -> None:
        self.semantic_matcher = SemanticMatcher(top_k=top_k_chunks)
        self.calibrator = Calibrator(calibrator_path) if calibrator_path else None

    def match(self, cv: ATSCriteria, jd: JDParseResult, cv_text: str, jd_text: str) -> MatchResult:
        semantic = self.semantic_matcher.match(cv_text, jd_text)
        fusion: FusionResult = fuse_features(
            semantic_similarity=semantic.semantic_similarity,
            cv=cv,
            jd=jd,
        )
        penalties = BaselineMatcher._build_penalties(cv, jd)
        evidence = BaselineMatcher._skill_evidence(cv, fusion.top_matched_skills)

        score = fusion.score
        if self.calibrator:
            import numpy as np

            features = np.array(
                [
                    [
                        fusion.semantic_similarity,
                        fusion.skill_overlap_score,
                        fusion.section_coverage,
                        penalties.get("missing_required_count", 0),
                        1.0 if penalties.get("keyword_stuffing_risk") else 0.0,
                        penalties.get("evidence_ratio", 1.0),
                    ]
                ]
            )
            calibrated = self.calibrator.predict(features)
            score = round(calibrated * 100, 2)

        breakdown = {
            "semantic_similarity": fusion.semantic_similarity,
            "skill_overlap_score": fusion.skill_overlap_score,
            "section_coverage": fusion.section_coverage,
            "top_matched_skills": fusion.top_matched_skills,
            "top_matched_chunks": semantic.top_matched_chunks,
            "penalties": penalties,
            "evidence_snippets": evidence["evidence_snippets"],
        }
        return MatchResult(score=score, breakdown=breakdown)


def match_with_strategy(
    strategy: str,
    cv: ATSCriteria,
    jd: JDParseResult,
    cv_text: str | None = None,
    jd_text: str | None = None,
) -> MatchResult:
    if strategy == "hybrid_ml":
        if not is_evaluation_gate_open():
            raise ValueError("Evaluation gate is closed; hybrid_ml is disabled.")
        if not cv_text or not jd_text:
            raise ValueError("cv_text and jd_text are required for hybrid_ml matching.")
        calibrator_path = os.getenv("ML_CALIBRATOR_PATH")
        return HybridMLMatcher(calibrator_path=calibrator_path).match(
            cv=cv, jd=jd, cv_text=cv_text, jd_text=jd_text
        )
    return BaselineMatcher().match(cv, jd)
