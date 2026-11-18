from pathlib import Path
from datetime import datetime, timezone
import argparse
import hashlib
import json
import time
import sys

# Resolve the project root before importing internal project modules.
SCRIPT_PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(SCRIPT_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPT_PROJECT_ROOT))

import joblib
import numpy as np
import pandas as pd
import sklearn

from src.data_io import load_prepared_datasets
from src.preprocessing import prepare_training_experiment
from src.pipelines import (
    get_model_templates,
    build_model_pipeline,
)


def calculate_sha256(path):
    """Return SHA256 hash of a file."""
    digest = hashlib.sha256()

    with open(path, "rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)

    return digest.hexdigest()


def write_json(path, data):
    """Write JSON with reproducible formatting."""
    path.write_text(
        json.dumps(
            data,
            indent=4,
            ensure_ascii=False,
            default=str,
        ),
        encoding="utf-8",
    )


def main():
    parser = argparse.ArgumentParser(
        description="Train the two officially selected final ML models."
    )

    parser.add_argument(
        "--project-root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
    )

    args = parser.parse_args()
    project_root = args.project_root.resolve()

    if not project_root.is_dir():
        raise FileNotFoundError(
            f"Project root does not exist: {project_root}"
        )

    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

    # -----------------------------------------------------
    # 1. Load and validate prepared datasets
    # -----------------------------------------------------

    print("=" * 70)
    print("FINAL MODEL TRAINING")
    print("=" * 70)

    datasets = load_prepared_datasets(project_root)

    # Only the cleaned training DataFrame is used below.
    # The loader separately verifies Test-data integrity.
    train_df = datasets["train_df_clean"]

    if train_df.shape != (624, 48):
        raise ValueError(
            f"Unexpected training shape: {train_df.shape}"
        )

    if "Diagnosis" not in train_df.columns:
        raise KeyError("Diagnosis target is missing.")

    if train_df["Diagnosis"].isna().any():
        raise ValueError("Training target contains missing values.")

    expected_classes = {
        "appendicitis",
        "no appendicitis",
    }

    if set(train_df["Diagnosis"].unique()) != expected_classes:
        raise ValueError("Unexpected target classes.")

    # -----------------------------------------------------
    # 2. Prepare the two approved experiments
    # -----------------------------------------------------

    experiments = {
        1: prepare_training_experiment(
            train_df=train_df,
            experiment=1,
        ),
        2: prepare_training_experiment(
            train_df=train_df,
            experiment=2,
        ),
    }

    exp1 = experiments[1]
    exp2 = experiments[2]

    if len(exp1["feature_columns"]) != 40:
        raise ValueError("Experiment 1 must contain 40 features.")

    if len(exp2["feature_columns"]) != 37:
        raise ValueError("Experiment 2 must contain 37 features.")

    if not exp1["X_train"].index.equals(
        exp2["X_train"].index
    ):
        raise ValueError("Training sample indices differ.")

    if not exp1["y_train"].equals(exp2["y_train"]):
        raise ValueError("Training targets differ.")

    expected_removed = {
        "Alvarado_Score",
        "Paedriatic_Appendicitis_Score",
        "Appendix_Diameter",
    }

    actual_removed = (
        set(exp1["feature_columns"])
        - set(exp2["feature_columns"])
    )

    if actual_removed != expected_removed:
        raise ValueError(
            f"Unexpected Experiment 2 exclusions: {actual_removed}"
        )

    # -----------------------------------------------------
    # 3. Define officially selected models
    # -----------------------------------------------------

    templates = get_model_templates()

    selected = {
        1: "GradientBoosting",
        2: "RandomForest",
    }

    # -----------------------------------------------------
    # 4. Create unique output directories
    # -----------------------------------------------------

    run_id = datetime.now(timezone.utc).strftime(
        "final_models_%Y%m%d_%H%M%S"
    )

    model_dir = project_root / "models" / run_id
    report_dir = (
        project_root / "reports" / "training" / run_id
    )

    if model_dir.exists() or report_dir.exists():
        raise FileExistsError(
            f"Run directory already exists: {run_id}"
        )

    model_dir.mkdir(parents=True, exist_ok=False)
    report_dir.mkdir(parents=True, exist_ok=False)

    # -----------------------------------------------------
    # 5. Fit and save selected models
    # -----------------------------------------------------

    records = {}
    training_start = datetime.now(timezone.utc).isoformat()

    for experiment_number, model_name in selected.items():

        data = experiments[experiment_number]

        X_train = data["X_train"]
        y_train = data["y_train"]

        print()
        print("-" * 65)
        print(f"Experiment {experiment_number}")
        print(f"Model: {model_name}")
        print(f"Samples: {len(X_train)}")
        print(f"Features: {len(data['feature_columns'])}")
        print("-" * 65)

        pipeline = build_model_pipeline(
            preprocessor=data["preprocessor"],
            estimator=templates[model_name],
            scale=False,
        )

        start_time = time.perf_counter()

        # The only model-fitting operation in this script.
        pipeline.fit(X_train, y_train)

        fit_seconds = time.perf_counter() - start_time

        classifier = pipeline.named_steps["classifier"]

        if "appendicitis" not in classifier.classes_:
            raise ValueError(
                "Positive class missing from fitted classifier."
            )

        filename = (
            f"experiment_{experiment_number}_"
            f"{model_name.lower()}.joblib"
        )

        model_path = model_dir / filename

        joblib.dump(
            pipeline,
            model_path,
            compress=3,
        )

        model_hash = calculate_sha256(model_path)

        # Verify that the saved artifact can be reloaded.
        restored_pipeline = joblib.load(model_path)

        restored_classifier = (
            restored_pipeline.named_steps["classifier"]
        )

        if not hasattr(restored_classifier, "classes_"):
            raise RuntimeError(
                "Saved model did not retain fitted state."
            )

        if list(restored_classifier.classes_) != list(
            classifier.classes_
        ):
            raise RuntimeError(
                "Saved model classes do not match."
            )

        records[f"Experiment_{experiment_number}"] = {
            "experiment": experiment_number,
            "selected_model": model_name,
            "model_file": filename,
            "model_sha256": model_hash,
            "training_samples": len(X_train),
            "feature_count": len(data["feature_columns"]),
            "feature_columns": data["feature_columns"],
            "numeric_columns": data["numeric_columns"],
            "ordinal_columns": data["ordinal_columns"],
            "nominal_columns": data["nominal_columns"],
            "target_column": "Diagnosis",
            "positive_class": "appendicitis",
            "classes": classifier.classes_.tolist(),
            "threshold": 0.5,
            "scaling": False,
            "fit_duration_seconds": round(fit_seconds, 4),
            "estimator_parameters": classifier.get_params(
                deep=False
            ),
        }

        print("Fit: PASS")
        print("Save: PASS")
        print("Reload verification: PASS")
        print(f"SHA256: {model_hash}")

        del restored_pipeline

    # -----------------------------------------------------
    # 6. Create training manifest
    # -----------------------------------------------------

    training_end = datetime.now(timezone.utc).isoformat()

    data_path = (
        project_root
        / "data"
        / "processed"
        / "prepared_datasets.pkl"
    )

    source_files = [
        project_root / "src" / "data_io.py",
        project_root / "src" / "preprocessing.py",
        project_root / "src" / "pipelines.py",
        project_root / "src" / "train_final_models.py",
    ]

    source_hashes = {
        str(path.relative_to(project_root)): calculate_sha256(path)
        for path in source_files
    }

    manifest = {
        "run_id": run_id,
        "training_started_utc": training_start,
        "training_completed_utc": training_end,
        "selection_decision": "EXP-MODEL-SEL-001",
        "cross_validation_reference": (
            "10fold_official_20261118_083752"
        ),
        "training_method": "Full training set fit",
        "training_samples": len(train_df),
        "test_used_for_training": False,
        "test_used_for_model_selection": False,
        "test_integrity_check": (
            "Performed by load_prepared_datasets"
        ),
        "positive_class": "appendicitis",
        "classification_threshold": 0.5,
        "random_state": 42,
        "python_version": sys.version,
        "numpy_version": np.__version__,
        "pandas_version": pd.__version__,
        "scikit_learn_version": sklearn.__version__,
        "joblib_version": joblib.__version__,
        "dataset_file": str(data_path.relative_to(project_root)),
        "dataset_sha256": calculate_sha256(data_path),
        "source_sha256": source_hashes,
        "models": records,
    }

    manifest_path = model_dir / "training_manifest.json"

    write_json(manifest_path, manifest)

    # -----------------------------------------------------
    # 7. Create human-readable training report
    # -----------------------------------------------------

    report_lines = [
        "# Final Model Training Report",
        "",
        f"- Run ID: `{run_id}`",
        f"- Training started (UTC): `{training_start}`",
        f"- Training completed (UTC): `{training_end}`",
        "- Selection decision: `EXP-MODEL-SEL-001`",
        "- Training samples per experiment: 624",
        "- Test used for fitting: No",
        "- Test used for model selection: No",
        "- Test integrity validation: Performed by data loader",
        "- Positive class: `appendicitis`",
        "- Classification threshold: `0.5`",
        "",
        "## Trained Models",
        "",
    ]

    for key, record in records.items():
        report_lines.extend([
            f"### {key}",
            "",
            f"- Model: `{record['selected_model']}`",
            f"- Features: {record['feature_count']}",
            f"- Training samples: {record['training_samples']}",
            f"- Fit duration: {record['fit_duration_seconds']} seconds",
            f"- Model file: `{record['model_file']}`",
            f"- SHA256: `{record['model_sha256']}`",
            "",
        ])

    report_lines.extend([
        "## Reproducibility",
        "",
        f"- Manifest: `{manifest_path}`",
        f"- Dataset SHA256: `{manifest['dataset_sha256']}`",
        "- Source-file SHA256 hashes are recorded in the manifest.",
        "- Both saved models passed reload verification.",
        "",
        "## Evaluation Status",
        "",
        "The held-out Test dataset has not been used for model fitting,",
        "model selection, threshold tuning, or performance evaluation.",
        "Final Test evaluation is a separate subsequent stage.",
        "",
    ])

    report_path = report_dir / "final_training_report.md"

    report_path.write_text(
        "\n".join(report_lines),
        encoding="utf-8",
    )

    # -----------------------------------------------------
    # 8. Final artifact verification
    # -----------------------------------------------------

    for record in records.values():
        path = model_dir / record["model_file"]

        if calculate_sha256(path) != record["model_sha256"]:
            raise RuntimeError(
                f"Model hash verification failed: {path}"
            )

    if not manifest_path.is_file():
        raise RuntimeError("Manifest was not created.")

    if not report_path.is_file():
        raise RuntimeError("Training report was not created.")

    print()
    print("=" * 70)
    print("FINAL TRAINING COMPLETED")
    print("=" * 70)
    print(f"Run ID: {run_id}")
    print(f"Models: {model_dir}")
    print(f"Manifest: {manifest_path}")
    print(f"Report: {report_path}")
    print("Model hashes: VERIFIED")
    print("Saved model reload checks: VERIFIED")
    print("Test used for fitting: NO")
    print("Test used for model selection: NO")


if __name__ == "__main__":
    main()
