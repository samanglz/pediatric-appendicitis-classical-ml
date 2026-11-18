from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer, MissingIndicator
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder


EXCLUDED_COLUMNS = [
    "US_Number",
    "Diagnosis_Presumptive",
    "Management",
    "Severity",
    "Length_of_Stay",
    "US_Performed",
    "Appendix_on_US",
]

EXPERIMENT_2_EXCLUDED = [
    "Alvarado_Score",
    "Paedriatic_Appendicitis_Score",
    "Appendix_Diameter",
]

ORDINAL_COLUMNS = [
    "Ketones_in_Urine",
    "RBC_in_Urine",
    "WBC_in_Urine",
]

ORDINAL_CATEGORIES = [
    ["no", "+", "++", "+++"],
    ["no", "+", "++", "+++"],
    ["no", "+", "++", "+++"],
]


def build_preprocessor(
    numeric_columns,
    ordinal_columns,
    ordinal_levels,
    nominal_columns,
):
    numeric_pipeline = Pipeline([
        (
            "imputer",
            SimpleImputer(strategy="median"),
        ),
    ])

    ordinal_pipeline = Pipeline([
        (
            "imputer",
            SimpleImputer(strategy="most_frequent"),
        ),
        (
            "encoder",
            OrdinalEncoder(
                categories=ordinal_levels,
                handle_unknown="use_encoded_value",
                unknown_value=-1,
            ),
        ),
    ])

    nominal_pipeline = Pipeline([
        (
            "imputer",
            SimpleImputer(
                strategy="constant",
                fill_value="__MISSING__",
            ),
        ),
        (
            "encoder",
            OneHotEncoder(handle_unknown="ignore"),
        ),
    ])

    return ColumnTransformer(
        transformers=[
            ("numerical", numeric_pipeline, numeric_columns),
            (
                "numerical_missing",
                MissingIndicator(features="all"),
                numeric_columns,
            ),
            ("ordinal", ordinal_pipeline, ordinal_columns),
            (
                "ordinal_missing",
                MissingIndicator(features="all"),
                ordinal_columns,
            ),
            ("nominal", nominal_pipeline, nominal_columns),
        ],
        remainder="drop",
    )


def prepare_training_experiment(train_df, experiment=1):
    if experiment not in (1, 2):
        raise ValueError("Experiment must be 1 or 2.")

    feature_columns = [
        col for col in train_df.columns
        if col not in EXCLUDED_COLUMNS + ["Diagnosis"]
    ]

    if experiment == 2:
        feature_columns = [
            col for col in feature_columns
            if col not in EXPERIMENT_2_EXCLUDED
        ]

    X_train = train_df[feature_columns].copy()
    y_train = train_df["Diagnosis"].copy()

    numeric_columns = X_train.select_dtypes(
        include=["number"]
    ).columns.tolist()

    categorical_columns = X_train.select_dtypes(
        include=["object", "category", "bool"]
    ).columns.tolist()

    ordinal_columns = [
        col for col in ORDINAL_COLUMNS
        if col in categorical_columns
    ]

    nominal_columns = [
        col for col in categorical_columns
        if col not in ordinal_columns
    ]

    ordinal_levels = [
        ORDINAL_CATEGORIES[ORDINAL_COLUMNS.index(col)]
        for col in ordinal_columns
    ]

    preprocessor = build_preprocessor(
        numeric_columns=numeric_columns,
        ordinal_columns=ordinal_columns,
        ordinal_levels=ordinal_levels,
        nominal_columns=nominal_columns,
    )

    return {
        "X_train": X_train,
        "y_train": y_train,
        "feature_columns": feature_columns,
        "numeric_columns": numeric_columns,
        "ordinal_columns": ordinal_columns,
        "nominal_columns": nominal_columns,
        "preprocessor": preprocessor,
    }
