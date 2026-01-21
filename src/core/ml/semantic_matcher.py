from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np

from src.core.ml.embedding_model import EmbeddingModel


@dataclass(frozen=True)
class SemanticMatchResult:
    semantic_similarity: float
    top_matched_chunks: list[dict[str, object]]


class SemanticMatcher:
    def __init__(self, embedder: EmbeddingModel | None = None, top_k: int = 3) -> None:
        self.embedder = embedder or EmbeddingModel()
        self.top_k = top_k

    def similarity(self, left: str, right: str) -> float:
        embeddings = self.embedder.encode([left, right])
        if embeddings.size == 0:
            return 0.0
        left_vec, right_vec = embeddings
        return float(self._cosine(left_vec, right_vec))

    def top_chunks(self, cv_text: str, jd_text: str) -> list[dict[str, object]]:
        chunks = self._split_chunks(cv_text)
        if not chunks:
            return []
        embeddings = self.embedder.encode([jd_text] + chunks)
        jd_vec = embeddings[0]
        scores = []
        for idx, chunk_vec in enumerate(embeddings[1:], start=0):
            score = float(self._cosine(jd_vec, chunk_vec))
            scores.append((idx, score))
        scores.sort(key=lambda item: item[1], reverse=True)
        results = []
        for idx, score in scores[: self.top_k]:
            results.append({"chunk": chunks[idx], "similarity": round(score, 4)})
        return results

    def match(self, cv_text: str, jd_text: str) -> SemanticMatchResult:
        return SemanticMatchResult(
            semantic_similarity=round(self.similarity(cv_text, jd_text), 4),
            top_matched_chunks=self.top_chunks(cv_text, jd_text),
        )

    @staticmethod
    def _split_chunks(text: str) -> list[str]:
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        if not lines:
            return []
        chunks: list[str] = []
        current: list[str] = []
        current_len = 0
        for line in lines:
            if current_len + len(line) > 400 and current:
                chunks.append(" ".join(current))
                current = []
                current_len = 0
            current.append(line)
            current_len += len(line)
        if current:
            chunks.append(" ".join(current))
        return chunks

    @staticmethod
    def _cosine(left: Iterable[float], right: Iterable[float]) -> float:
        left_vec = np.asarray(left, dtype=float)
        right_vec = np.asarray(right, dtype=float)
        denom = np.linalg.norm(left_vec) * np.linalg.norm(right_vec)
        if denom == 0.0:
            return 0.0
        return float(np.dot(left_vec, right_vec) / denom)
