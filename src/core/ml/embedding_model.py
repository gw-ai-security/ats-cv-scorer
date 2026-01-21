from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np

_MODEL_CACHE: dict[str, object] = {}


@dataclass
class EmbeddingConfig:
    model_name: str = "sentence-transformers/all-MiniLM-L6-v2"
    normalize: bool = True


class EmbeddingModel:
    def __init__(self, config: EmbeddingConfig | None = None) -> None:
        self.config = config or EmbeddingConfig()
        self._model = None

    def _load(self) -> object:
        if self.config.model_name in _MODEL_CACHE:
            return _MODEL_CACHE[self.config.model_name]
        from sentence_transformers import SentenceTransformer

        model = SentenceTransformer(self.config.model_name)
        _MODEL_CACHE[self.config.model_name] = model
        return model

    def encode(self, texts: Iterable[str]) -> np.ndarray:
        if self._model is None:
            self._model = self._load()
        batch = list(texts)
        if not batch:
            return np.empty((0, 0))
        embeddings = self._model.encode(batch, normalize_embeddings=self.config.normalize)
        return np.asarray(embeddings, dtype=float)
