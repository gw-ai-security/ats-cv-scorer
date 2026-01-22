from __future__ import annotations

import hashlib
import re
from typing import Iterable

from src.core.ats_criteria_extractor import ATSCriteriaExtractor
from src.core.cv_analyzer import CVAnalyzer
from src.core.jd_parser import JDParser
from src.core.skill_extractor import SkillExtractor
from src.prompt_chain.models import Step1Result, Step2Result, Step3Result, Step4QA, Step4Result


def _normalize_terms(values: Iterable[str]) -> list[str]:
    terms = []
    for value in values:
        if value:
            terms.append(value.strip().lower())
    return sorted({term for term in terms if term})


def _extract_resume_evidence(resume_text: str) -> list[str]:
    lines = [line.strip() for line in resume_text.splitlines() if line.strip()]
    return lines[:15]


def _pad_keywords(keywords: list[str], target: int = 5) -> list[str]:
    padded = list(keywords)
    idx = 1
    while len(padded) < target:
        padded.append(f"keyword_gap_{idx}")
        idx += 1
    return padded[:target]


def step1_match(resume_text: str, jd_text: str, language: str) -> Step1Result:
    ats = ATSCriteriaExtractor().extract(resume_text)
    jd = JDParser().parse(jd_text)
    cv_skills = _normalize_terms(
        list(ats.skills.get("hard", []))
        + list(ats.skills.get("soft", []))
        + list(ats.skills.get("tools", []))
        + list(ats.languages)
    )
    jd_skills = _normalize_terms(jd.skills + jd.keywords)
    matched = sorted(set(cv_skills) & set(jd_skills))
    missing = sorted(set(jd_skills) - set(cv_skills))
    score = round((len(matched) / max(len(jd_skills), 1)) * 100, 2)
    missing_keywords = _pad_keywords(missing, 5)
    rationale = f"Matched {len(matched)} of {len(jd_skills)} JD terms."
    return Step1Result(score_0_100=score, missing_keywords=missing_keywords, rationale=rationale)


def step2_rewrite_suggestions(resume_text: str, jd_text: str, language: str) -> Step2Result:
    ats = ATSCriteriaExtractor().extract(resume_text)
    jd = JDParser().parse(jd_text)
    missing = _normalize_terms(set(jd.skills + jd.keywords) - set(ats.skills.get("hard", [])))
    evidence_refs = _extract_resume_evidence(resume_text)
    templates = []
    for skill in missing[:5]:
        templates.append(
            f"Accomplished [X] as measured by [Y] by doing [Z] (include '{skill}' evidence)."
        )
    if not templates:
        templates.append(
            "Accomplished [X] as measured by [Y] by doing [Z] (add concrete metrics)."
        )
    warnings = []
    if not ats.experience:
        warnings.append("No structured experience section found; provide role/company/timeframe.")
    return Step2Result(
        rewrite_mode="templates_only",
        templates=templates,
        evidence_refs=evidence_refs[:5],
        warnings=warnings,
    )


def step3_ats_risks(resume_text: str, jd_text: str, language: str) -> Step3Result:
    analyzer = CVAnalyzer()
    ats = ATSCriteriaExtractor().extract(resume_text)
    issues = []
    fixes = []
    section_result = analyzer.analyze_sections(resume_text)
    if len(section_result.headers_found) < 3:
        issues.append("Few detectable section headers; ATS may struggle to split sections.")
        fixes.append("Use clear section headings: Summary, Experience, Education, Skills.")
    if ats.missing_fields:
        issues.append(f"Missing fields: {', '.join(ats.missing_fields)}")
        fixes.append("Add missing contact and section details explicitly.")
    if re.search(r"\\t|\\|", resume_text):
        issues.append("Table-like formatting detected; ATS may skip columns.")
        fixes.append("Replace tables with plain text bullet lists.")
    return Step3Result(issues=issues or ["No major ATS issues detected."], fixes=fixes or [])


def step4_interview_questions(resume_text: str, jd_text: str, language: str) -> Step4Result:
    jd = JDParser().parse(jd_text)
    evidence = _extract_resume_evidence(resume_text)
    questions = []
    for idx, skill in enumerate(jd.skills[:3], start=1):
        question = f"Explain a complex project where you applied {skill}."
        answer = evidence[idx - 1] if idx - 1 < len(evidence) else "Insufficient evidence in resume."
        questions.append(
            Step4QA(
                question=question,
                answer=answer,
                evidence_refs=[answer] if "Insufficient" not in answer else [],
                insufficient_evidence="Insufficient" in answer,
            )
        )
    while len(questions) < 3:
        questions.append(
            Step4QA(
                question="Describe a challenging technical decision you made.",
                answer="Insufficient evidence in resume.",
                evidence_refs=[],
                insufficient_evidence=True,
            )
        )
    return Step4Result(questions=questions[:3])


def compute_pii_counts(text: str) -> dict[str, int]:
    email_hits = len(re.findall(r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\\.[A-Z]{2,}", text, flags=re.IGNORECASE))
    phone_hits = len(re.findall(r"\+?\d[\d\s\-()]{7,}\d", text))
    url_hits = len(re.findall(r"https?://\\S+", text))
    return {"email_hits": email_hits, "phone_hits": phone_hits, "url_hits": url_hits}


def hash_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()
