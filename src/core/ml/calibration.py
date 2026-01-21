from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np


@dataclass
class Calibrator:
    model_path: str
    _model: object | None = None

    def _load(self) -> object | None:
        path = Path(self.model_path)
        if not path.exists():
            return None
        from joblib import load

        return load(path)

    def predict(self, features: np.ndarray) -> float:
        if self._model is None:
            self._model = self._load()
        if self._model is None:
            return float(features[0][0]) if features.size else 0.0
        prob = self._model.predict_proba(features)[:, 1]
        return float(prob[0])
