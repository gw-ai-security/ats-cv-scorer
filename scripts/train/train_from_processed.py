from __future__ import annotations

import argparse
from pathlib import Path
import json

import joblib
import numpy as np
from sklearn.linear_model import LogisticRegression

from datetime import datetime

from src.core.ats_criteria_extractor import ATSCriteriaExtractor
from src.core.jd_parser import JDParser
from src.core.matcher import BaselineMatcher
from src.core.ml.feature_fusion import compute_section_coverage, compute_skill_overlap
from src.core.ml.semantic_matcher import SemanticMatcher


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train calibrator from processed JSONL.")
    parser.add_argument("--input", type=Path, required=True, help="Processed JSONL dataset path.")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("models/calibrator.joblib"),
        help="Output model path (ignored by git).",
    )
    parser.add_argument(
        "--summary",
        type=Path,
        default=Path("docs/04_evaluation/TRAINING_SUMMARY.md"),
        help="Training summary output path.",
    )
    parser.add_argument("--positive-label", default="strong_match")
    return parser.parse_args()


def load_records(path: Path) -> list[dict[str, object]]:
    records = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            records.append(json.loads(line))
    return records


def build_features(records: list[dict[str, object]]) -> tuple[np.ndarray, np.ndarray]:
    matcher = SemanticMatcher()
    ats_extractor = ATSCriteriaExtractor()
    jd_parser = JDParser()
    baseline = BaselineMatcher()
    features = []
    labels = []
    for record in records:
        cv_text = record.get("cv_text") or ""
        jd_text = record.get("jd_text") or ""
        label = record.get("label")
        if not cv_text or not jd_text or label is None:
            continue
        cv = ats_extractor.extract(cv_text)
        jd = jd_parser.parse(jd_text)
        semantic = matcher.similarity(cv_text, jd_text)
        skill_overlap, _matched, _gaps = compute_skill_overlap(cv, jd)
        coverage = compute_section_coverage(cv)
        penalties = baseline._build_penalties(cv, jd)
        features.append(
            [
                semantic,
                skill_overlap,
                coverage,
                penalties.get("missing_required_count", 0),
                1.0 if penalties.get("keyword_stuffing_risk") else 0.0,
                penalties.get("evidence_ratio", 1.0),
            ]
        )
        labels.append(label)
    return np.array(features, dtype=float), np.array(labels)


def main() -> None:
    args = parse_args()
    if not args.input.exists():
        raise SystemExit("Input dataset not found.")
    records = load_records(args.input)
    features, labels = build_features(records)
    if features.size == 0:
        raise SystemExit("No labeled records available for training.")

    y = np.array([1 if label == args.positive_label else 0 for label in labels], dtype=int)
    model = LogisticRegression(max_iter=200)
    model.fit(features, y)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, args.output)
    write_summary(args.summary, args.input, len(features), args.positive_label, args.output)
    print(f"Saved calibrator to {args.output}")


def write_summary(
    summary_path: Path,
    input_path: Path,
    rows: int,
    positive_label: str,
    output_path: Path,
) -> None:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = [
        "# Training Summary",
        "",
        f"Run timestamp: {timestamp} (Local)",
        "",
        f"Input dataset: `{input_path}`",
        f"Rows used: {rows}",
        f"Positive label: {positive_label}",
        f"Output model: `{output_path}`",
        "",
        "Features: semantic_similarity, skill_overlap, section_coverage, missing_required_count,",
        "keyword_stuffing_risk, evidence_ratio",
    ]
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()
