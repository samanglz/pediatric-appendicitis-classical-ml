from pathlib import Path
import pickle
import pandas as pd


def load_prepared_datasets(project_root):
    """
    Load and validate the four prepared project DataFrames.
    """

    project_root = Path(project_root)

    dataset_path = (
        project_root
        / "data"
        / "processed"
        / "prepared_datasets.pkl"
    )

    if not dataset_path.exists():
        raise FileNotFoundError(
            f"Dataset file not found: {dataset_path}"
        )

    # Only load pickle files from trusted project storage.
    with open(dataset_path, "rb") as file:
        datasets = pickle.load(file)

    required_names = [
        "train_df_original",
        "test_df_original",
        "train_df_clean",
        "test_df_clean",
    ]

    for name in required_names:
        if name not in datasets:
            raise KeyError(
                f"Required dataset missing: {name}"
            )

        if not isinstance(datasets[name], pd.DataFrame):
            raise TypeError(
                f"{name} is not a pandas DataFrame."
            )

    # Verify expected dataset dimensions.
    expected_shapes = {
        "train_df_original": (624, 58),
        "test_df_original": (156, 58),
        "train_df_clean": (624, 48),
        "test_df_clean": (156, 48),
    }

    for name, expected_shape in expected_shapes.items():
        actual_shape = datasets[name].shape

        if actual_shape != expected_shape:
            raise ValueError(
                f"{name}: expected {expected_shape}, "
                f"got {actual_shape}"
            )

    # Verify that the cleaned Test remains identical
    # to its original version on retained columns.
    test_reference = datasets["test_df_original"].loc[
        datasets["test_df_clean"].index,
        datasets["test_df_clean"].columns
    ]

    pd.testing.assert_frame_equal(
        datasets["test_df_clean"],
        test_reference,
        check_exact=True,
        check_dtype=True,
        check_names=True
    )

    return datasets
