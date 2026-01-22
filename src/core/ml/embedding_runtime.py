from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path


@dataclass(frozen=True)
class EmbeddingRuntimeStatus:
    available: bool
    message: str


def _candidate_cache_dirs() -> list[Path]:
    candidates = []
    env_keys = [
        "SENTENCE_TRANSFORMERS_HOME",
        "HF_HOME",
        "TRANSFORMERS_CACHE",
    ]
    for key in env_keys:
        value = os.getenv(key)
        if value:
            candidates.append(Path(value))
    home = Path.home()
    candidates.append(home / ".cache" / "torch" / "sentence_transformers")
    candidates.append(home / ".cache" / "huggingface" / "hub")
    return [path for path in candidates if path.exists()]


def check_embedding_availability(model_name: str) -> EmbeddingRuntimeStatus:
    try:
        import sentence_transformers  # noqa: F401
    except Exception as exc:
        return EmbeddingRuntimeStatus(False, f"sentence_transformers_import_failed: {exc}")

    for cache_dir in _candidate_cache_dirs():
        if model_name in str(cache_dir):
            return EmbeddingRuntimeStatus(True, f"found_cache:{cache_dir}")
        if any(model_name.replace("/", "") in part.name for part in cache_dir.rglob("*")):
            return EmbeddingRuntimeStatus(True, f"found_cache:{cache_dir}")

    return EmbeddingRuntimeStatus(False, "model_cache_not_found")


def get_default_embedding_status() -> EmbeddingRuntimeStatus:
    model_name = os.getenv("ATS_EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
    return check_embedding_availability(model_name)
