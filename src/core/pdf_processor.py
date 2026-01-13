from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import pdfplumber


@dataclass(frozen=True)
class ExtractionResult:
    text: str
    method: str  # "pdfplumber" (OCR deferred)
    quality: str  # "high" | "low"
    page_count: int
    word_count: int
    error: Optional[str] = None


class PDFProcessor:
    """
    FR-002 (Phase 1): text extraction with pdfplumber + metadata.
    OCR fallback is explicitly out of scope here.
    """

    def __init__(self, min_words_quality_high: int = 50) -> None:
        self.min_words_quality_high = min_words_quality_high

    def extract_text(self, pdf_path: str) -> ExtractionResult:
        try:
            text, page_count = self._extract_with_pdfplumber(pdf_path)
            word_count = self._count_words(text)
            quality = "high" if word_count >= self.min_words_quality_high else "low"

            return ExtractionResult(
                text=text,
                method="pdfplumber",
                quality=quality,
                page_count=page_count,
                word_count=word_count,
                error=None,
            )
        except Exception as exc:
            # FR-002: no crash to user; return empty + low quality + error string
            return ExtractionResult(
                text="",
                method="pdfplumber",
                quality="low",
                page_count=0,
                word_count=0,
                error=str(exc),
            )

    def _extract_with_pdfplumber(self, pdf_path: str) -> tuple[str, int]:
        chunks: list[str] = []
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text() or ""
                page_text = page_text.strip()
                if page_text:
                    chunks.append(page_text)
            page_count = len(pdf.pages)
        return "\n".join(chunks).strip(), page_count

    @staticmethod
    def _count_words(text: str) -> int:
        if not text:
            return 0
        return len(text.split())
