from __future__ import annotations

import json
from pathlib import Path


REGISTRY_PATH = Path("data/processed/registry.json")


def load_registry(path: Path | None = None) -> dict:
    target = path or REGISTRY_PATH
    data = json.loads(target.read_text(encoding="utf-8"))
    if "datasets" not in data:
        raise ValueError("Registry missing datasets key.")
    return data


def list_dataset_ids(path: Path | None = None) -> list[str]:
    registry = load_registry(path)
    return [entry["dataset_id"] for entry in registry["datasets"]]
