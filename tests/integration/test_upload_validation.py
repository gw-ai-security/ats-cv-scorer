from dataclasses import dataclass

from src.utils.validation import MAX_UPLOAD_SIZE_BYTES, validate_upload

@dataclass
class FakeUpload:
    name: str
    type: str
    size: int


def test_invalid_file_type_returns_error():
    upload = FakeUpload(name="resume.txt", type="text/plain", size=1234)
    result = validate_upload(upload)
    assert result.ok is False
    assert result.error is not None


def test_file_too_large_returns_error():
    upload = FakeUpload(
        name="resume.pdf",
        type="application/pdf",
        size=MAX_UPLOAD_SIZE_BYTES + 1,
    )
    result = validate_upload(upload)
    assert result.ok is False
    assert result.error is not None


def test_valid_pdf_returns_ok():
    upload = FakeUpload(name="resume.pdf", type="application/pdf", size=1024)
    result = validate_upload(upload)
    assert result.ok is True
    assert result.error is None
