from __future__ import annotations

from dataclasses import dataclass

from src.core.ats_criteria_extractor import ATSCriteria
from src.core.jd_parser import JDParseResult


@dataclass(frozen=True)
class FusionResult:
    score: float
    semantic_similarity: float
    skill_overlap_score: float
    section_coverage: float
    top_matched_skills: list[str]


def compute_skill_overlap(cv: ATSCriteria, jd: JDParseResult) -> tuple[float, list[str], list[str]]:
    cv_skills: set[str] = set()
    for group in cv.skills.values():
        cv_skills.update({skill.lower() for skill in group if skill})
    cv_skills.update({skill.lower() for skill in cv.certifications if skill})
    cv_skills.update({lang.lower() for lang in cv.languages if lang})

    jd_skills = {skill.lower() for skill in jd.skills + jd.keywords if skill}
    if not jd_skills:
        return 1.0, [], []
    matched = sorted(jd_skills & cv_skills)
    gaps = sorted(jd_skills - cv_skills)
    score = len(matched) / max(len(jd_skills), 1)
    return score, matched, gaps


def compute_section_coverage(cv: ATSCriteria) -> float:
    sections_present = 0
    total = 5
    if cv.summary != "not_found":
        sections_present += 1
    if cv.experience:
        sections_present += 1
    if cv.education:
        sections_present += 1
    if any(cv.skills.values()):
        sections_present += 1
    if cv.languages:
        sections_present += 1
    return sections_present / total


def fuse_features(
    semantic_similarity: float,
    cv: ATSCriteria,
    jd: JDParseResult,
    weights: dict[str, float] | None = None,
) -> FusionResult:
    weights = weights or {
        "semantic_similarity": 0.6,
        "skill_overlap": 0.25,
        "section_coverage": 0.15,
    }
    skill_score, matched, _gaps = compute_skill_overlap(cv, jd)
    coverage = compute_section_coverage(cv)
    total = (
        semantic_similarity * weights["semantic_similarity"]
        + skill_score * weights["skill_overlap"]
        + coverage * weights["section_coverage"]
    )
    return FusionResult(
        score=round(total * 100, 2),
        semantic_similarity=round(semantic_similarity, 4),
        skill_overlap_score=round(skill_score, 4),
        section_coverage=round(coverage, 4),
        top_matched_skills=matched[:10],
    )
