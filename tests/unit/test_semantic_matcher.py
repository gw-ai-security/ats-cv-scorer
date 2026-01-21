from __future__ import annotations

import numpy as np

from src.core.ml.semantic_matcher import SemanticMatcher


class FakeEmbedder:
    def encode(self, texts):
        vectors = []
        for text in texts:
            length = len(text)
            count_a = text.lower().count("a")
            vectors.append([length, count_a, 1.0])
        return np.asarray(vectors, dtype=float)


def test_semantic_matcher_similarity_and_chunks() -> None:
    matcher = SemanticMatcher(embedder=FakeEmbedder(), top_k=1)
    cv_text = "Alpha beta.\nExperience in analytics.\nSkills: Python, SQL."
    jd_text = "Looking for analytics skills."
    result = matcher.match(cv_text, jd_text)
    assert 0.0 <= result.semantic_similarity <= 1.0
    assert len(result.top_matched_chunks) == 1
    assert "chunk" in result.top_matched_chunks[0]
