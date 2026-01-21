from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Iterable

from src.core.ats_criteria_extractor import ATSCriteriaExtractor
from src.core.jd_parser import JDParser
from src.core.matcher import match_with_strategy

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
        "--outdir",
        type=Path,
        default=Path("evaluation_outputs"),
        help="Output directory for metrics and confusion matrix.",
    )
    parser.add_argument(
        "--strategy",
        choices=["baseline", "hybrid_ml", "both"],
        default="both",
        help="Which matcher(s) to evaluate.",
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


def load_pairs(pairs_path: Path) -> list[dict[str, object]]:
    with pairs_path.open("r", encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


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
        cv_text = (base_dir / record["cv_file"]).read_text(encoding="utf-8")
        jd_text = (base_dir / record["jd_file"]).read_text(encoding="utf-8")
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
        true_label = record["expected_label"]

        true_labels.append(true_label)
        pred_labels.append(predicted_label)
        error = range_error(result.score, record["expected_score_range"])
        score_errors.append(error)

        flags = parse_flags(record.get("rationale", ""))
        details.append(
            {
                "pair_id": record["pair_id"],
                "expected_label": true_label,
                "predicted_label": predicted_label,
                "score": result.score,
                "expected_score_range": record["expected_score_range"],
                "error": error,
                "metadata": record.get("metadata", {}),
                "flags": flags,
            }
        )

    confusion = compute_confusion(true_labels, pred_labels)
    classification = precision_recall_f1(confusion)
    mae = sum(score_errors) / max(len(score_errors), 1)
    rmse = (sum(error**2 for error in score_errors) / max(len(score_errors), 1)) ** 0.5

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
        "confusion": confusion,
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
        true_labels = [item["expected_label"] for item in items]
        pred_labels = [item["predicted_label"] for item in items]
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


def main() -> None:
    args = parse_args()
    records = load_pairs(args.pairs)
    base_dir = args.pairs.parent
    args.outdir.mkdir(parents=True, exist_ok=True)

    strategies = []
    if args.strategy == "both":
        strategies = ["baseline", "hybrid_ml"]
    else:
        strategies = [args.strategy]

    metrics = {
        "evaluation_version": EVALUATION_VERSION,
        "pairs_file": str(args.pairs),
        "score_thresholds": {
            "strong": args.strong_threshold,
            "partial": args.partial_threshold,
        },
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

            confusion_path = args.outdir / f"confusion_matrix_{strategy}.csv"
            write_confusion_csv(result["confusion"], confusion_path, strategy)
        except Exception as exc:
            metrics["models"][strategy] = {"error": str(exc)}

    metrics_path = args.outdir / "metrics.json"
    with metrics_path.open("w", encoding="utf-8") as handle:
        json.dump(metrics, handle, indent=2)

    print(f"Wrote metrics to {metrics_path}")


if __name__ == "__main__":
    main()
