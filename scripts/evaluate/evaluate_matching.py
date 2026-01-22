from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
import sys
from typing import Iterable

from src.core.ats_criteria_extractor import ATSCriteriaExtractor
from src.core.jd_parser import JDParser
from src.core.matcher import match_with_strategy
from src.core.ml.embedding_runtime import get_default_embedding_status

EVALUATION_VERSION = "1.0.0"
LABELS = ["strong_match", "partial_match", "mismatch"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Evaluate matching models on synthetic pairs.")
    parser.add_argument(
        "--pairs",
        type=Path,
        default=Path("tests/fixtures/synth/pairs.jsonl"),
        help="Path to synthetic pairs.jsonl.",
    )
    parser.add_argument(
        "--processed-dir",
        type=Path,
        default=None,
        help="Optional processed data directory containing pairs.jsonl.",
    )
    parser.add_argument(
        "--dataset",
        type=str,
        default=None,
        help="Dataset ID under data/processed/datasets/<dataset_id>.jsonl",
    )
    parser.add_argument(
        "--outdir",
        type=Path,
        default=Path("evaluation_outputs"),
        help="Output directory for metrics and confusion matrix.",
    )
    parser.add_argument(
        "--summary-out",
        type=Path,
        default=None,
        help="Optional markdown summary output path.",
    )
    parser.add_argument(
        "--strategy",
        choices=["baseline", "hybrid_ml", "both"],
        default="both",
        help="Which matcher(s) to evaluate.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Optional limit on number of records evaluated.",
    )
    parser.add_argument(
        "--strong-threshold",
        type=float,
        default=80.0,
        help="Score threshold for strong_match.",
    )
    parser.add_argument(
        "--partial-threshold",
        type=float,
        default=60.0,
        help="Score threshold for partial_match.",
    )
    return parser.parse_args()


def load_pairs(pairs_path: Path, limit: int | None = None) -> list[dict[str, object]]:
    records = []
    with pairs_path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            records.append(json.loads(line))
            if limit and len(records) >= limit:
                break
    return records


def score_to_label(score: float, strong_threshold: float, partial_threshold: float) -> str:
    if score >= strong_threshold:
        return "strong_match"
    if score >= partial_threshold:
        return "partial_match"
    return "mismatch"


def compute_confusion(
    true_labels: Iterable[str], pred_labels: Iterable[str]
) -> dict[tuple[str, str], int]:
    confusion: dict[tuple[str, str], int] = {}
    for true_label, pred_label in zip(true_labels, pred_labels):
        key = (true_label, pred_label)
        confusion[key] = confusion.get(key, 0) + 1
    return confusion


def precision_recall_f1(confusion: dict[tuple[str, str], int]) -> dict[str, object]:
    metrics = {}
    totals = {label: 0 for label in LABELS}
    for (true_label, _pred_label), count in confusion.items():
        totals[true_label] += count

    per_label = {}
    for label in LABELS:
        tp = confusion.get((label, label), 0)
        fp = sum(confusion.get((other, label), 0) for other in LABELS if other != label)
        fn = sum(confusion.get((label, other), 0) for other in LABELS if other != label)
        precision = tp / (tp + fp) if (tp + fp) else 0.0
        recall = tp / (tp + fn) if (tp + fn) else 0.0
        f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) else 0.0
        per_label[label] = {
            "precision": round(precision, 4),
            "recall": round(recall, 4),
            "f1": round(f1, 4),
            "support": totals[label],
        }

    macro_f1 = sum(per_label[label]["f1"] for label in LABELS) / len(LABELS)
    accuracy = sum(confusion.get((label, label), 0) for label in LABELS) / max(
        sum(totals.values()), 1
    )

    metrics["per_label"] = per_label
    metrics["macro_f1"] = round(macro_f1, 4)
    metrics["accuracy"] = round(accuracy, 4)
    return metrics


def range_error(score: float, expected_range: list[float]) -> float:
    low, high = expected_range
    if score < low:
        return low - score
    if score > high:
        return score - high
    return 0.0


def parse_flags(rationale: str) -> dict[str, bool]:
    text = rationale.lower()
    return {
        "formatting_noise": "noisy_formatting" in text,
        "synonym_only": "synonym_only" in text,
    }


def _load_text(record: dict[str, object], base_dir: Path, key: str, file_key: str) -> str:
    if file_key in record:
        return (base_dir / record[file_key]).read_text(encoding="utf-8")
    return str(record.get(key) or "")


def evaluate_records(
    records: list[dict[str, object]],
    base_dir: Path,
    strategy: str,
    strong_threshold: float,
    partial_threshold: float,
) -> dict[str, object]:
    cv_extractor = ATSCriteriaExtractor()
    jd_parser = JDParser()

    true_labels: list[str] = []
    pred_labels: list[str] = []
    score_errors: list[float] = []
    details: list[dict[str, object]] = []

    for record in records:
        cv_text = _load_text(record, base_dir, "cv_text", "cv_file")
        jd_text = _load_text(record, base_dir, "jd_text", "jd_file")
        cv = cv_extractor.extract(cv_text)
        jd = jd_parser.parse(jd_text)

        result = match_with_strategy(
            strategy=strategy,
            cv=cv,
            jd=jd,
            cv_text=cv_text,
            jd_text=jd_text,
        )
        predicted_label = score_to_label(result.score, strong_threshold, partial_threshold)
        true_label = record.get("expected_label") or record.get("label")

        if true_label:
            true_labels.append(str(true_label))
            pred_labels.append(predicted_label)
            expected_range = record.get("expected_score_range")
            if expected_range:
                error = range_error(result.score, expected_range)
                score_errors.append(error)
            else:
                score_errors.append(0.0)

        flags = parse_flags(record.get("rationale", ""))
        details.append(
            {
                "pair_id": record.get("pair_id") or record.get("id") or "unknown",
                "expected_label": true_label,
                "predicted_label": predicted_label,
                "score": result.score,
                "expected_score_range": record.get("expected_score_range"),
                "error": score_errors[-1] if score_errors else 0.0,
                "metadata": record.get("metadata", {}),
                "flags": flags,
            }
        )

    classification = None
    confusion_rows = []
    mae = sum(score_errors) / max(len(score_errors), 1)
    rmse = (sum(error**2 for error in score_errors) / max(len(score_errors), 1)) ** 0.5
    if true_labels:
        confusion = compute_confusion(true_labels, pred_labels)
        classification = precision_recall_f1(confusion)
        confusion_rows = confusion_to_rows(confusion)

    descriptive = None
    if not true_labels:
        scores = [item["score"] for item in details]
        if scores:
            scores_sorted = sorted(scores)
            descriptive = {
                "count": len(scores),
                "min": round(scores_sorted[0], 4),
                "p50": round(scores_sorted[len(scores_sorted) // 2], 4),
                "p90": round(scores_sorted[int(len(scores_sorted) * 0.9) - 1], 4)
                if len(scores_sorted) >= 2
                else round(scores_sorted[0], 4),
                "max": round(scores_sorted[-1], 4),
            }

    return {
        "classification": classification,
        "score_error": {
            "mae": round(mae, 4),
            "rmse": round(rmse, 4),
        },
        "ranking": {
            "mrr": None,
            "ndcg": None,
            "note": "not_applicable_single_pair",
        },
        "confusion_rows": confusion_rows,
        "descriptive": descriptive,
        "details": details,
    }


def group_metrics(details: list[dict[str, object]], axis: str) -> dict[str, object]:
    grouped: dict[str, list[dict[str, object]]] = {}
    for item in details:
        if axis in {"job_family", "difficulty", "language"}:
            value = item.get("metadata", {}).get(axis, "unknown")
        elif axis in {"formatting_noise", "synonym_only"}:
            value = "yes" if item.get("flags", {}).get(axis) else "no"
        else:
            value = "unknown"
        grouped.setdefault(value, []).append(item)

    results = {}
    for value, items in grouped.items():
        filtered = [item for item in items if item.get("expected_label")]
        true_labels = [item["expected_label"] for item in filtered]
        pred_labels = [item["predicted_label"] for item in filtered]
        if not true_labels:
            results[value] = {"count": len(items), "note": "no_labels"}
            continue
        confusion = compute_confusion(true_labels, pred_labels)
        classification = precision_recall_f1(confusion)
        errors = [item["error"] for item in items]
        mae = sum(errors) / max(len(errors), 1)
        rmse = (sum(error**2 for error in errors) / max(len(errors), 1)) ** 0.5
        results[value] = {
            "count": len(items),
            "accuracy": classification["accuracy"],
            "macro_f1": classification["macro_f1"],
            "mae": round(mae, 4),
            "rmse": round(rmse, 4),
        }
    return results


def write_confusion_csv(confusion: dict[tuple[str, str], int], path: Path, model: str) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["model", "label_true", "label_pred", "count"])
        for true_label in LABELS:
            for pred_label in LABELS:
                writer.writerow([model, true_label, pred_label, confusion.get((true_label, pred_label), 0)])


def confusion_to_rows(confusion: dict[tuple[str, str], int]) -> list[dict[str, object]]:
    rows = []
    for true_label in LABELS:
        for pred_label in LABELS:
            rows.append(
                {
                    "label_true": true_label,
                    "label_pred": pred_label,
                    "count": confusion.get((true_label, pred_label), 0),
                }
            )
    return rows


def main() -> None:
    args = parse_args()
    pairs_path = args.pairs
    dataset_id = None
    if args.dataset:
        dataset_id = args.dataset
        pairs_path = Path("data/processed/datasets") / f"{args.dataset}.jsonl"
    elif args.processed_dir:
        candidate = args.processed_dir / "pairs.jsonl"
        if candidate.exists():
            pairs_path = candidate
    records = load_pairs(pairs_path, args.limit)
    base_dir = pairs_path.parent
    args.outdir.mkdir(parents=True, exist_ok=True)

    strategies = []
    if args.strategy == "both":
        strategies = ["baseline", "hybrid_ml"]
    else:
        strategies = [args.strategy]
    notes: list[str] = []
    embedding_status = get_default_embedding_status()
    if "hybrid_ml" in strategies and not embedding_status.available:
        notes.append(f"hybrid_skipped: {embedding_status.message}")
        if args.strategy == "hybrid_ml":
            strategies = ["baseline"]
        else:
            strategies = [s for s in strategies if s != "hybrid_ml"]

    metrics = {
        "evaluation_version": EVALUATION_VERSION,
        "pairs_file": str(pairs_path),
        "score_thresholds": {
            "strong": args.strong_threshold,
            "partial": args.partial_threshold,
        },
        "notes": notes,
        "models": {},
    }

    for strategy in strategies:
        try:
            result = evaluate_records(
                records=records,
                base_dir=base_dir,
                strategy=strategy,
                strong_threshold=args.strong_threshold,
                partial_threshold=args.partial_threshold,
            )
            details = result.pop("details")
            metrics["models"][strategy] = {
                **result,
                "by_scenario": {
                    "job_family": group_metrics(details, "job_family"),
                    "difficulty": group_metrics(details, "difficulty"),
                    "language": group_metrics(details, "language"),
                    "formatting_noise": group_metrics(details, "formatting_noise"),
                    "synonym_only": group_metrics(details, "synonym_only"),
                },
            }

            if result["confusion_rows"]:
                confusion_path = args.outdir / f"confusion_matrix_{strategy}.csv"
                write_confusion_csv(
                    compute_confusion(
                        [item["expected_label"] for item in details if item["expected_label"]],
                        [item["predicted_label"] for item in details if item["expected_label"]],
                    ),
                    confusion_path,
                    strategy,
                )
        except Exception as exc:
            metrics["models"][strategy] = {"error": str(exc)}

    metrics_path = args.outdir / "metrics.json"
    with metrics_path.open("w", encoding="utf-8") as handle:
        json.dump(metrics, handle, indent=2)

    if args.summary_out:
        write_summary(
            summary_path=args.summary_out,
            metrics=metrics,
            dataset_id=dataset_id,
            strategies=strategies,
            notes=notes,
        )

    print(f"Wrote metrics to {metrics_path}")


def write_summary(
    summary_path: Path,
    metrics: dict[str, object],
    dataset_id: str | None,
    strategies: list[str],
    notes: list[str],
) -> None:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    command = " ".join(sys.argv)
    lines = [
        "# External Evaluation Results",
        "",
        f"Run timestamp: {timestamp} (Local)",
        "",
        f"Command: `{command}`",
        f"Dataset ID: {dataset_id or 'n/a'}",
        "",
        "## Summary",
    ]
    if notes:
        lines.append("## Environment Notes")
        for note in notes:
            lines.append(f"- {note}")
        lines.append("")
    for strategy in strategies:
        model = metrics.get("models", {}).get(strategy, {})
        lines.append(f"### {strategy}")
        if "error" in model:
            lines.append(f"- error: {model['error']}")
            lines.append("")
            continue
        classification = model.get("classification")
        descriptive = model.get("descriptive")
        lines.append(f"- pairs_file: {metrics.get('pairs_file')}")
        if classification:
            lines.append(f"- accuracy: {classification.get('accuracy')}")
            lines.append(f"- macro_f1: {classification.get('macro_f1')}")
        if descriptive:
            lines.append(f"- descriptive_count: {descriptive.get('count')}")
            lines.append(f"- score_min: {descriptive.get('min')}")
            lines.append(f"- score_p50: {descriptive.get('p50')}")
            lines.append(f"- score_p90: {descriptive.get('p90')}")
            lines.append(f"- score_max: {descriptive.get('max')}")
        if not classification:
            lines.append("- limitation: labels not available; metrics are descriptive only.")
        lines.append("")
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()
