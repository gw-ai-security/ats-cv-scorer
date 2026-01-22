from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Apply license overrides to registry.json.")
    parser.add_argument(
        "--registry",
        type=Path,
        default=Path("data/processed/registry.json"),
        help="Registry JSON path.",
    )
    parser.add_argument(
        "--overrides",
        type=Path,
        default=Path("data/processed/registry_licenses_overrides.json"),
        help="Overrides JSON path.",
    )
    parser.add_argument(
        "--changelog",
        type=Path,
        default=Path("data/processed/REGISTRY_CHANGELOG.md"),
        help="Changelog output path.",
    )
    return parser.parse_args()


def validate_entry(entry: dict[str, object]) -> list[str]:
    errors = []
    status = entry.get("usage_status")
    if status in {"approved", "approved_local_only"}:
        for key in ("source_url", "license_label"):
            value = entry.get(key)
            if not value or value == "unknown":
                errors.append(f"missing_{key}")
    return errors


def apply_overrides(registry: dict[str, object], overrides: dict[str, object]) -> list[str]:
    changed = []
    override_map = overrides.get("datasets", {})
    for dataset in registry.get("datasets", []):
        dataset_id = dataset.get("dataset_id")
        if dataset_id not in override_map:
            continue
        updates = override_map[dataset_id]
        if not isinstance(updates, dict):
            continue
        for key, value in updates.items():
            if dataset.get(key) != value:
                dataset[key] = value
                changed.append(f"{dataset_id}:{key}")
    return changed


def write_changelog(path: Path, changed: list[str]) -> None:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = [
        "# Registry Changelog",
        "",
        f"Run timestamp: {timestamp} (Local)",
        "",
    ]
    if changed:
        lines.append("## Updated Fields")
        for item in changed:
            lines.append(f"- {item}")
    else:
        lines.append("## Updated Fields")
        lines.append("- none")
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    args = parse_args()
    registry = json.loads(args.registry.read_text(encoding="utf-8"))
    overrides = json.loads(args.overrides.read_text(encoding="utf-8"))
    changed = apply_overrides(registry, overrides)

    errors = []
    for dataset in registry.get("datasets", []):
        errors.extend([f"{dataset.get('dataset_id')}:{err}" for err in validate_entry(dataset)])
    if errors:
        error_text = "\n".join(errors)
        raise SystemExit(f"License validation failed:\n{error_text}")

    args.registry.write_text(json.dumps(registry, indent=2) + "\n", encoding="utf-8")
    write_changelog(args.changelog, changed)
    print(f"Updated {args.registry}")
    print(f"Wrote {args.changelog}")


if __name__ == "__main__":
    main()
