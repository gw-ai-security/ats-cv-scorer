from __future__ import annotations

import os
import tempfile

import streamlit as st

from src.core.pdf_processor import PDFProcessor
from src.utils.validation import validate_upload


st.set_page_config(page_title="ATS CV Scorer", layout="centered")
st.title("ATS CV Scorer - FR-002 Extraction Demo")

uploader = st.file_uploader(
    "Upload a PDF CV",
    type=["pdf"],
    help="Max file size: 10 MB"
)


if uploader is not None:
    validation = validate_upload(uploader)
    if not validation.ok:
        st.error(validation.error or "Upload validation failed.")
        st.stop()

    processor = PDFProcessor()
    temp_path = None

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(uploader.getbuffer())
            temp_path = tmp.name

        result = processor.extract_text(temp_path)

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

        st.subheader("Text preview")
        preview = result.text[:4000]
        st.text(preview if preview else "(no text extracted)")
    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)
