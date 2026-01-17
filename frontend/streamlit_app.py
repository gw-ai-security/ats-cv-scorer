from __future__ import annotations

import os
import tempfile

import streamlit as st

from src.core.ats_criteria_extractor import ATSCriteriaExtractor
from src.core.cv_analyzer import CVAnalyzer
from src.core.jd_parser import JDParser
from src.core.matcher import BaselineMatcher
from src.core.pdf_processor import PDFProcessor
from src.core.skill_extractor import SkillExtractor
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

status_slot = st.empty()

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

        with left:
            tabs = st.tabs(["Text", "Structure", "Skills", "ATS Criteria", "Job Description", "Match"])

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

            with tabs[4]:
                if jd_uploader is None and not jd_text_input.strip():
                    st.info("Upload a JD PDF or paste JD text to parse it.")
                else:
                    if jd_uploader is not None:
                        jd_validation = validate_upload(jd_uploader)
                        if not jd_validation.ok:
                            st.error(jd_validation.error or "JD upload validation failed.")
                            jd_validation = None
                        if jd_validation:
                            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                                tmp.write(jd_uploader.getbuffer())
                                jd_temp_path = tmp.name
                            jd_result = processor.extract_text(jd_temp_path)
                            parsed_jd = jd_parser.parse(jd_result.text)
                            st.write(parsed_jd.__dict__)
                    else:
                        parsed_jd = jd_parser.parse(jd_text_input)
                        st.write(parsed_jd.__dict__)

            with tabs[5]:
                if not run_matching:
                    st.info("Enable matching in the sidebar to compare CV vs JD.")
                elif jd_uploader is None and not jd_text_input.strip():
                    st.info("Upload a JD PDF or paste JD text to compute the match.")
                else:
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
                            parsed_jd = jd_parser.parse(jd_result.text)
                            ats_result = ats_extractor.extract(result.text)
                            match_result = matcher.match(ats_result, parsed_jd)
                            st.metric("Match score", f"{match_result.score}%")
                            st.write(match_result.breakdown)
                    else:
                        parsed_jd = jd_parser.parse(jd_text_input)
                        ats_result = ats_extractor.extract(result.text)
                        match_result = matcher.match(ats_result, parsed_jd)
                        st.metric("Match score", f"{match_result.score}%")
                        st.write(match_result.breakdown)
        status_slot.success("Done.")
    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)
        if jd_temp_path and os.path.exists(jd_temp_path):
            os.remove(jd_temp_path)
