from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

MAX_UPLOAD_SIZE_BYTES = 10 * 1024 * 1024  # 10 MB
ALLOWED_MIME_TYPES = {"application/pdf"}


@dataclass(frozen=True)
class ValidationResult:
    ok: bool
    error: Optional[str] = None


def validate_upload(uploaded_file) -> ValidationResult:
    """
    FR-001: validate file type and size without raising exceptions.
    """
    try:
        if uploaded_file is None:
            return ValidationResult(ok=False, error="No file uploaded.")

        name = getattr(uploaded_file, "name", "") or ""
        mime_type = getattr(uploaded_file, "type", "") or ""
        size = _get_size(uploaded_file)

        if size is None:
            return ValidationResult(ok=False, error="Unable to determine file size.")

        if size > MAX_UPLOAD_SIZE_BYTES:
            return ValidationResult(ok=False, error="File too large. Max 10 MB.")

        if not _is_pdf(name, mime_type):
            return ValidationResult(ok=False, error="Invalid file type. PDF required.")

        return ValidationResult(ok=True, error=None)
    except Exception as exc:
        return ValidationResult(ok=False, error=f"Validation failed: {exc}")


def _is_pdf(name: str, mime_type: str) -> bool:
    if mime_type in ALLOWED_MIME_TYPES:
        return True
    return name.lower().endswith(".pdf")


def _get_size(uploaded_file) -> Optional[int]:
    size = getattr(uploaded_file, "size", None)
    if isinstance(size, int):
        return size

    if hasattr(uploaded_file, "getbuffer"):
        return len(uploaded_file.getbuffer())

    if hasattr(uploaded_file, "getvalue"):
        return len(uploaded_file.getvalue())

    return None
