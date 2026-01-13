from src.core.pdf_processor import PDFProcessor, ExtractionResult


def test_imports_and_types():
    processor = PDFProcessor()
    assert processor is not None


def test_extract_text_returns_result_even_on_failure(tmp_path):
    # Provide a non-pdf file path; extraction should not crash
    fake_pdf = tmp_path / "not_a_pdf.pdf"
    fake_pdf.write_text("this is not a pdf")

    processor = PDFProcessor()
    result = processor.extract_text(str(fake_pdf))

    assert isinstance(result, ExtractionResult)
    assert result.method == "pdfplumber"
    assert result.quality in ("high", "low")
    assert result.text == ""  # on failure, empty string
    assert result.error is not None
