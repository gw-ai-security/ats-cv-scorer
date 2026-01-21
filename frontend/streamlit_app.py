from __future__ import annotations

import os
import tempfile

import streamlit as st

from src.core.ats_criteria_extractor import ATSCriteriaExtractor, ATSCriteria
from src.core.cv_analyzer import CVAnalyzer
from src.core.jd_parser import JDParser, JDParseResult
from src.core.matcher import BaselineMatcher, MatchResult, match_with_strategy
from src.core.pdf_processor import PDFProcessor
from src.core.skill_extractor import SkillExtractor
from src.utils.config import get_matching_strategy
from src.utils.validation import validate_upload


st.set_page_config(page_title="ATS CV Scorer", layout="wide")
st.title("ATS CV Scorer")
st.caption("Upload a CV PDF to preview extraction, structure, and skills.")

with st.sidebar:
    st.header("Upload")
    st.write("Accepted file type: PDF")
    st.write("Max size: 10 MB")
    cv_input_mode = st.radio("CV input", ["PDF upload", "Paste text"], horizontal=True)
    uploader = None
    cv_text_input = ""
    if cv_input_mode == "PDF upload":
        uploader = st.file_uploader("Choose a CV file", type=["pdf"])
    else:
        cv_text_input = st.text_area("Paste CV text", height=200)

    jd_input_mode = st.radio("JD input", ["PDF upload", "Paste text"], horizontal=True)
    jd_uploader = None
    jd_text_input = ""
    if jd_input_mode == "PDF upload":
        jd_uploader = st.file_uploader("Choose a job description", type=["pdf"])
    else:
        jd_text_input = st.text_area("Paste JD text", height=200)
    run_analysis = st.toggle("Run analysis", value=True)
    run_matching = st.toggle("Run matching (CV vs JD)", value=True)
    default_strategy = get_matching_strategy()
    matching_strategy = st.selectbox(
        "Matching strategy",
        ["rule_based", "hybrid_ml"],
        index=0 if default_strategy == "rule_based" else 1,
        help="hybrid_ml uses semantic similarity and feature fusion; rule_based is deterministic baseline.",
    )

status_slot = st.empty()


def _build_match_explanations(match: MatchResult, ats: ATSCriteria) -> list[str]:
    explanations: list[str] = []
    breakdown = match.breakdown

    skill_gaps = breakdown["skills"].get("gaps", [])
    if skill_gaps:
        explanations.append(f"Missing JD skills: {', '.join(skill_gaps)}")

    language_gaps = breakdown["language"].get("gaps", [])
    if language_gaps:
        explanations.append(f"Missing language(s): {', '.join(language_gaps)}")

    if breakdown["experience"].get("has_experience") is False:
        explanations.append("Experience section not detected for required seniority.")

    if breakdown["education"].get("requires_degree") and not breakdown["education"].get("has_education"):
        explanations.append("Education section missing while degree is required.")

    if breakdown["location"].get("jd_location") and breakdown["location"].get("cv_location") == "":
        explanations.append("Location missing in CV for a non-remote JD.")
    elif breakdown["location"].get("jd_location") and breakdown["location"].get("cv_location"):
        if breakdown["location"].get("jd_location") not in breakdown["location"].get("cv_location"):
            explanations.append("Location does not match the JD requirement.")

    if ats.missing_fields:
        explanations.append(f"Missing CV fields: {', '.join(ats.missing_fields)}")

    if not explanations:
        explanations.append("All criteria matched based on current rules.")

    return explanations


def _build_optimized_cv_text(
    match: MatchResult, ats: ATSCriteria, jd: JDParseResult
) -> str:
    contact = ats.contact
    name = contact.get("name", "not_found")
    email = contact.get("email", "not_found")
    phone = contact.get("phone", "not_found")
    location = contact.get("location", "not_found")
    links = contact.get("links", "not_found")

    skills = []
    for group in ats.skills.values():
        skills.extend(group)
    skills = [skill for skill in skills if skill]
    missing_skills = match.breakdown["skills"].get("gaps", [])

    lines = [
        f"{name if name != 'not_found' else '[Your Name]'}",
        f"Email: {email if email != 'not_found' else '[Add Email]'}",
        f"Phone: {phone if phone != 'not_found' else '[Add Phone]'}",
        f"Location: {location if location != 'not_found' else '[Add Location]'}",
        f"Links: {links if links != 'not_found' else '[Add Links]'}",
        "",
        "Summary",
        ats.summary if ats.summary != "not_found" else "[Add a concise professional summary aligned to the JD.]",
        "",
        "Skills",
        ", ".join(sorted(skills)) if skills else "[Add key skills]",
    ]

    if missing_skills:
        lines.extend(["", "JD Skill Gaps to Consider", ", ".join(missing_skills)])

    if jd.requirements:
        lines.extend(["", "JD Requirements (reference)"])
        lines.extend([f"- {item}" for item in jd.requirements])

    if jd.responsibilities:
        lines.extend(["", "JD Responsibilities (reference)"])
        lines.extend([f"- {item}" for item in jd.responsibilities])

    lines.extend(["", "Experience"])
    if ats.experience:
        for entry in ats.experience:
            role = entry.get("role", "")
            company = entry.get("company", "")
            timeframe = entry.get("timeframe", "")
            responsibilities = entry.get("responsibilities", "")
            lines.append(f"- {role} | {company} | {timeframe}".strip())
            if responsibilities:
                lines.append(f"  {responsibilities}")
    else:
        lines.append("[Add experience entries aligned to the JD requirements.]")

    lines.extend(["", "Education"])
    if ats.education:
        for entry in ats.education:
            role = entry.get("role", "")
            company = entry.get("company", "")
            timeframe = entry.get("timeframe", "")
            lines.append(f"- {role} | {company} | {timeframe}".strip())
    else:
        lines.append("[Add education entries if required by the JD.]")

    if ats.languages:
        lines.extend(["", "Languages", ", ".join(sorted({lang for lang in ats.languages if lang}))])

    if ats.certifications:
        lines.extend(["", "Certifications", ", ".join(ats.certifications)])

    if ats.availability and ats.availability != "not_found":
        lines.extend(["", "Availability", ats.availability])

    return "\n".join(lines).strip()


def _build_improvements(match: MatchResult, ats: ATSCriteria, jd: JDParseResult) -> list[str]:
    improvements: list[str] = []
    skill_gaps = match.breakdown["skills"].get("gaps", [])
    if skill_gaps:
        improvements.append(f"Add missing JD skills: {', '.join(skill_gaps)}")

    language_gaps = match.breakdown["language"].get("gaps", [])
    if language_gaps:
        improvements.append(f"Add language evidence: {', '.join(language_gaps)}")

    if match.breakdown["education"].get("requires_degree") and not match.breakdown["education"].get(
        "has_education"
    ):
        improvements.append("Add education section aligned to JD degree requirement.")

    if match.breakdown["experience"].get("has_experience") is False:
        improvements.append("Add experience entries that match the JD seniority.")

    if match.breakdown["location"].get("jd_location") and not match.breakdown["location"].get(
        "cv_location"
    ):
        improvements.append("Add location details to match the JD requirement.")

    if ats.missing_fields:
        improvements.append(f"Fill missing CV fields: {', '.join(ats.missing_fields)}")

    if jd.requirements:
        improvements.append("Mirror JD requirements with concrete bullet points in the CV.")
    if jd.responsibilities:
        improvements.append("Align experience bullets to JD responsibilities.")

    if not improvements:
        improvements.append("No obvious improvements detected by current rules.")

    return improvements


def _render_ml_explanation(match: MatchResult) -> None:
    st.subheader("ML explanation")
    st.write(f"Semantic similarity: {match.breakdown.get('semantic_similarity')}")
    st.write(f"Skill overlap score: {match.breakdown.get('skill_overlap_score')}")
    st.write(f"Section coverage: {match.breakdown.get('section_coverage')}")
    top_skills = match.breakdown.get("top_matched_skills", [])
    if top_skills:
        st.write("Top matched skills:")
        for skill in top_skills:
            st.write(f"- {skill}")
    top_chunks = match.breakdown.get("top_matched_chunks", [])
    if top_chunks:
        st.write("Top matched chunks:")
        for chunk in top_chunks:
            st.write(f"- {chunk.get('chunk')} (sim {chunk.get('similarity')})")

def _pdf_bytes_from_text(text: str) -> bytes | None:
    try:
        from io import BytesIO
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas
    except Exception:
        return None

    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    y = height - 72
    for line in text.splitlines():
        if y < 72:
            pdf.showPage()
            y = height - 72
        pdf.drawString(72, y, line[:120])
        y -= 14
    pdf.save()
    buffer.seek(0)
    return buffer.read()


if uploader is None and not cv_text_input.strip():
    st.info("Upload a PDF or paste CV text to start.")
else:
    if uploader is not None:
        validation = validate_upload(uploader)
        if not validation.ok:
            st.error(validation.error or "Upload validation failed.")
            st.stop()

    if not run_analysis:
        st.warning("Enable 'Run analysis' to process the uploaded file.")
        st.stop()

    processor = PDFProcessor()
    analyzer = CVAnalyzer()
    extractor = SkillExtractor()
    ats_extractor = ATSCriteriaExtractor()
    jd_parser = JDParser()
    matcher = BaselineMatcher()
    temp_path = None
    jd_temp_path = None

    try:
        if uploader is not None:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(uploader.getbuffer())
                temp_path = tmp.name
            status_slot.info("Extracting text...")
            result = processor.extract_text(temp_path)
        else:
            status_slot.info("Using provided CV text...")
            result = processor.extract_text(temp_path) if temp_path else None
            if result is None:
                class _TextResult:
                    def __init__(self, text: str) -> None:
                        self.text = text
                        self.method = "text"
                        self.quality = "high" if text.strip() else "low"
                        self.page_count = 0
                        self.word_count = len(text.split())
                        self.error = None
                result = _TextResult(cv_text_input)

        left, right = st.columns([2, 1], gap="large")
        with right:
            st.subheader("Extraction metadata")
            st.write(
                {
                    "method": result.method,
                    "quality": result.quality,
                    "page_count": result.page_count,
                    "word_count": result.word_count,
                    "error": result.error,
                }
            )
            ats_preview = ats_extractor.extract(result.text)
            st.subheader("Match summary")
            st.write("Upload or paste a JD to calculate the score.")

        with left:
            tabs = st.tabs(["Text", "Structure", "Skills", "ATS Criteria", "Job Description", "Match", "Optimization"])

            with tabs[0]:
                st.subheader("Text preview")
                preview = result.text[:4000]
                st.text(preview if preview else "(no text extracted)")

            with tabs[1]:
                st.subheader("Structure preview")
                section_result = analyzer.analyze_sections(result.text)
                st.write({"headers_found": section_result.headers_found})
                for section_name, content in section_result.sections.items():
                    label = section_name.capitalize()
                    with st.expander(label, expanded=bool(content)):
                        st.text(content if content else "(empty)")

            with tabs[2]:
                st.subheader("Skill preview")
                skill_result = extractor.extract(result.text)
                st.write(skill_result.skills)

            with tabs[3]:
                st.subheader("ATS criteria preview")
                ats_result = ats_extractor.extract(result.text)
                st.write(
                    {
                        "contact": ats_result.contact,
                        "summary": ats_result.summary,
                        "experience": ats_result.experience,
                        "education": ats_result.education,
                        "skills": ats_result.skills,
                        "certifications": ats_result.certifications,
                        "languages": ats_result.languages,
                        "availability": ats_result.availability,
                        "missing_fields": ats_result.missing_fields,
                    }
                )

            jd_text = None
            parsed_jd = None
            if jd_uploader is not None:
                jd_validation = validate_upload(jd_uploader)
                if not jd_validation.ok:
                    st.error(jd_validation.error or "JD upload validation failed.")
                else:
                    if jd_temp_path is None:
                        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                            tmp.write(jd_uploader.getbuffer())
                            jd_temp_path = tmp.name
                    jd_result = processor.extract_text(jd_temp_path)
                    jd_text = jd_result.text
            elif jd_text_input.strip():
                jd_text = jd_text_input

            if jd_text:
                parsed_jd = jd_parser.parse(jd_text)

            with tabs[4]:
                if parsed_jd is None:
                    st.info("Upload a JD PDF or paste JD text to parse it.")
                else:
                    st.write(parsed_jd.__dict__)

            with tabs[5]:
                if not run_matching:
                    st.info("Enable matching in the sidebar to compare CV vs JD.")
                elif parsed_jd is None:
                    st.info("Upload a JD PDF or paste JD text to compute the match.")
                else:
                    ats_result = ats_extractor.extract(result.text)
                    if matching_strategy == "hybrid_ml":
                        match_result = match_with_strategy(
                            matching_strategy,
                            ats_result,
                            parsed_jd,
                            cv_text=result.text,
                            jd_text=jd_text or "",
                        )
                        st.metric("Match score (ML)", f"{match_result.score}%")
                    else:
                        match_result = matcher.match(ats_result, parsed_jd)
                        st.metric("Match score", f"{match_result.score}%")
                    st.write(match_result.breakdown)

                    with right:
                        if matching_strategy == "hybrid_ml":
                            _render_ml_explanation(match_result)
                        else:
                            st.subheader("Score explanation")
                            for item in _build_match_explanations(match_result, ats_result):
                                st.write(f"- {item}")
                            st.subheader("Improvements")
                            for item in _build_improvements(match_result, ats_result, parsed_jd):
                                st.write(f"- {item}")

            with tabs[6]:
                if parsed_jd is None or not run_matching:
                    st.info("Provide a JD and enable matching to generate an optimized CV.")
                else:
                    ats_result = ats_extractor.extract(result.text)
                    match_result = matcher.match(ats_result, parsed_jd)
                    optimized_text = _build_optimized_cv_text(match_result, ats_result, parsed_jd)
                    st.subheader("Optimized CV (plain text)")
                    st.text_area("Copy-ready CV", optimized_text, height=300)
                    st.download_button(
                        "Download optimized CV (TXT)",
                        data=optimized_text.encode("utf-8"),
                        file_name="optimized_cv.txt",
                        mime="text/plain",
                    )
                    pdf_bytes = _pdf_bytes_from_text(optimized_text)
                    if pdf_bytes:
                        st.download_button(
                            "Download optimized CV (PDF)",
                            data=pdf_bytes,
                            file_name="optimized_cv.pdf",
                            mime="application/pdf",
                        )
                    else:
                        st.info("PDF download requires reportlab to be installed.")
        status_slot.success("Done.")
    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)
        if jd_temp_path and os.path.exists(jd_temp_path):
            os.remove(jd_temp_path)
