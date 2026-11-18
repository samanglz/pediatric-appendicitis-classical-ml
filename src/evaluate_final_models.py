
from pathlib import Path
import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone

import joblib
import numpy as np
import pandas as pd
import sklearn

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    balanced_accuracy_score,
    roc_auc_score,
    precision_recall_curve,
    auc,
    average_precision_score,
    confusion_matrix,
)

def sha256_file(path):
    digest = hashlib.sha256()
    with open(path, "rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--project-root",
        type=Path,
        required=True,
    )
    parser.add_argument(
        "--training-run-id",
        default="final_models_20261118_091523",
    )
    args = parser.parse_args()

    project_root = args.project_root.resolve()

    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

    from src.data_io import load_prepared_datasets

    training_model_dir = (
        project_root / "models" / args.training_run_id
    )
    training_manifest_path = (
        training_model_dir / "training_manifest.json"
    )

    if not training_manifest_path.exists():
        raise FileNotFoundError(training_manifest_path)

    with open(training_manifest_path, "r", encoding="utf-8") as file:
        training_manifest = json.load(file)

    # Verify the original dataset and model artifacts.
    dataset_path = project_root / training_manifest["dataset_file"]

    if sha256_file(dataset_path) != training_manifest["dataset_sha256"]:
        raise ValueError("Dataset SHA256 mismatch.")

    for experiment, record in training_manifest["models"].items():
        model_path = training_model_dir / record["model_file"]

        if sha256_file(model_path) != record["model_sha256"]:
            raise ValueError(
                f"Model SHA256 mismatch: {experiment}"
            )

    # Load datasets. The loader also performs its read-only
    # integrity verification of the cleaned Test dataset.
    datasets = load_prepared_datasets(project_root)

    test_df = datasets["test_df_clean"]

    if test_df.shape != (156, 48):
        raise ValueError(
            f"Unexpected Test shape: {test_df.shape}"
        )

    if test_df["Diagnosis"].isna().any():
        raise ValueError("Missing Test targets detected.")

    y_test = test_df["Diagnosis"].copy()

    positive_class = "appendicitis"
    negative_class = "no appendicitis"
    threshold = 0.5

    if set(y_test.unique()) != {
        positive_class,
        negative_class,
    }:
        raise ValueError("Unexpected Test target classes.")

    selected_models = {
        "Experiment_1": "GradientBoosting",
        "Experiment_2": "RandomForest",
    }

    output_run_id = (
        "final_test_evaluation_"
        + datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    )

    output_dir = (
        project_root / "reports" / "evaluation" / output_run_id
    )

    if output_dir.exists():
        raise FileExistsError(output_dir)

    output_dir.mkdir(parents=True, exist_ok=False)

    metric_records = []
    prediction_data = {
        "test_index": test_df.index,
        "y_true": y_test.values,
    }
    confusion_records = {}

    for experiment, expected_model_name in selected_models.items():

        record = training_manifest["models"][experiment]

        if record["selected_model"] != expected_model_name:
            raise ValueError(
                f"Unexpected selected model for {experiment}."
            )

        if record["threshold"] != threshold:
            raise ValueError(
                f"Unexpected threshold for {experiment}."
            )

        feature_columns = record["feature_columns"]

        if len(feature_columns) != record["feature_count"]:
            raise ValueError(
                f"Feature count mismatch in {experiment}."
            )

        missing_columns = (
            set(feature_columns) - set(test_df.columns)
        )

        if missing_columns:
            raise ValueError(
                f"Missing Test features: {missing_columns}"
            )

        X_test = test_df.loc[:, feature_columns]

        model_path = training_model_dir / record["model_file"]
        pipeline = joblib.load(model_path)

        classifier = pipeline.named_steps["classifier"]
        classes = list(classifier.classes_)

        if positive_class not in classes:
            raise ValueError(
                f"Positive class missing in {experiment}."
            )

        positive_index = classes.index(positive_class)

        probabilities = pipeline.predict_proba(X_test)[
            :, positive_index
        ]

        predictions = np.where(
            probabilities >= threshold,
            positive_class,
            negative_class,
        )

        y_binary = (
            y_test == positive_class
        ).astype(int)

        pred_binary = (
            predictions == positive_class
        ).astype(int)

        tn, fp, fn, tp = confusion_matrix(
            y_binary,
            pred_binary,
            labels=[0, 1],
        ).ravel()

        precision_curve, recall_curve, _ = (
            precision_recall_curve(
                y_binary,
                probabilities,
            )
        )

        pr_auc = auc(
            recall_curve,
            precision_curve,
        )

        metrics = {
            "experiment": experiment,
            "model": expected_model_name,
            "test_samples": len(y_test),
            "feature_count": len(feature_columns),
            "threshold": threshold,
            "accuracy": accuracy_score(
                y_binary, pred_binary
            ),
            "precision": precision_score(
                y_binary, pred_binary, zero_division=0
            ),
            "recall": recall_score(
                y_binary, pred_binary, zero_division=0
            ),
            "f1": f1_score(
                y_binary, pred_binary, zero_division=0
            ),
            "balanced_accuracy": balanced_accuracy_score(
                y_binary, pred_binary
            ),
            "roc_auc": roc_auc_score(
                y_binary, probabilities
            ),
            "pr_auc": pr_auc,
            "average_precision": average_precision_score(
                y_binary, probabilities
            ),
            "tn": int(tn),
            "fp": int(fp),
            "fn": int(fn),
            "tp": int(tp),
        }

        metric_records.append(metrics)

        prediction_data[
            f"{experiment}_probability"
        ] = probabilities

        prediction_data[
            f"{experiment}_prediction"
        ] = predictions

        confusion_records[experiment] = {
            "TN": int(tn),
            "FP": int(fp),
            "FN": int(fn),
            "TP": int(tp),
        }

        print()
        print("-" * 65)
        print(experiment)
        print(f"Model: {expected_model_name}")
        print(f"Test samples: {len(y_test)}")
        print(f"Features: {len(feature_columns)}")
        print("Evaluation: PASS")
        print("-" * 65)

    metrics_df = pd.DataFrame(metric_records)
    predictions_df = pd.DataFrame(prediction_data)

    metrics_path = output_dir / "test_metrics.csv"
    predictions_path = output_dir / "test_predictions.csv"
    confusion_path = output_dir / "confusion_matrices.json"
    manifest_path = output_dir / "evaluation_manifest.json"
    report_path = output_dir / "final_test_evaluation_report.md"

    metrics_df.to_csv(metrics_path, index=False)
    predictions_df.to_csv(predictions_path, index=False)

    with open(confusion_path, "w", encoding="utf-8") as file:
        json.dump(
            confusion_records,
            file,
            indent=2,
            ensure_ascii=False,
        )

    manifest = {
        "run_id": output_run_id,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "training_run_id": args.training_run_id,
        "training_selection_decision": (
            training_manifest["selection_decision"]
        ),
        "test_samples": len(y_test),
        "test_class_counts": {
            str(key): int(value)
            for key, value in y_test.value_counts().items()
        },
        "positive_class": positive_class,
        "negative_class": negative_class,
        "classification_threshold": threshold,
        "test_used_for_final_evaluation": True,
        "test_used_for_training": False,
        "test_used_for_model_selection": False,
        "fit_performed": False,
        "threshold_tuning_performed": False,
        "models": selected_models,
        "training_manifest_sha256": sha256_file(
            training_manifest_path
        ),
        "dataset_sha256": training_manifest["dataset_sha256"],
        "model_sha256": {
            experiment: record["model_sha256"]
            for experiment, record
            in training_manifest["models"].items()
        },
        "metrics_file": metrics_path.name,
        "predictions_file": predictions_path.name,
        "confusion_matrices_file": confusion_path.name,
        "python_version": sys.version,
        "numpy_version": np.__version__,
        "pandas_version": pd.__version__,
        "scikit_learn_version": sklearn.__version__,
        "joblib_version": joblib.__version__,
    }

    with open(manifest_path, "w", encoding="utf-8") as file:
        json.dump(
            manifest,
            file,
            indent=2,
            ensure_ascii=False,
        )

    report_lines = [
        "# Final Test Evaluation",
        "",
        f"- Run ID: `{output_run_id}`",
        f"- Training run: `{args.training_run_id}`",
        f"- Test samples: {len(y_test)}",
        f"- Positive class: `{positive_class}`",
        f"- Threshold: {threshold}",
        "- Fit performed: No",
        "- Threshold tuning: No",
        "",
        "## Results",
        "",
        metrics_df.to_markdown(index=False),
        "",
        "## Confusion Matrices",
        "",
    ]

    for experiment, matrix in confusion_records.items():
        report_lines.extend([
            f"### {experiment}",
            "",
            f"- TN: {matrix['TN']}",
            f"- FP: {matrix['FP']}",
            f"- FN: {matrix['FN']}",
            f"- TP: {matrix['TP']}",
            "",
        ])

    report_path.write_text(
        "\n".join(report_lines),
        encoding="utf-8",
    )

    # Verify persisted evaluation artifacts.
    for path in [
        metrics_path,
        predictions_path,
        confusion_path,
        manifest_path,
        report_path,
    ]:
        if not path.exists() or path.stat().st_size == 0:
            raise RuntimeError(
                f"Evaluation artifact verification failed: {path}"
            )

    print()
    print("=" * 65)
    print("FINAL TEST EVALUATION COMPLETED")
    print("=" * 65)
    print(metrics_df.to_string(index=False))
    print()
    print("Run ID:", output_run_id)
    print("Output directory:", output_dir)
    print("Manifest:", manifest_path)
    print("Report:", report_path)
    print("Fit performed: NO")
    print("Threshold tuning: NO")
    print("Test used for final evaluation: YES")


if __name__ == "__main__":
    main()
