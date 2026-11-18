from sklearn.base import clone
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (
    RandomForestClassifier,
    GradientBoostingClassifier,
)

from sklearn.model_selection import StratifiedKFold


def get_model_templates():
    return {
        "Dummy": DummyClassifier(strategy="prior"),

        "LogisticRegression": LogisticRegression(
            max_iter=2000,
            random_state=42,
        ),

        "DecisionTree": DecisionTreeClassifier(
            random_state=42,
        ),

        "RandomForest": RandomForestClassifier(
            random_state=42,
            n_jobs=-1,
        ),

        "GradientBoosting": GradientBoostingClassifier(
            random_state=42,
        ),
    }


def build_model_pipeline(preprocessor, estimator, scale=False):
    steps = [
        ("preprocessor", clone(preprocessor)),
    ]

    if scale:
        steps.append(
            ("scaler", StandardScaler(with_mean=False))
        )

    steps.append(
        ("classifier", clone(estimator))
    )

    return Pipeline(steps=steps)


def build_experiment_pipelines(preprocessor):
    templates = get_model_templates()
    pipelines = {}

    for model_name, estimator in templates.items():
        pipelines[model_name] = build_model_pipeline(
            preprocessor=preprocessor,
            estimator=estimator,
            scale=(model_name == "LogisticRegression"),
        )

    return pipelines


def build_shared_cv(n_splits=10, random_state=42):
    return StratifiedKFold(
        n_splits=n_splits,
        shuffle=True,
        random_state=random_state,
    )


def generate_cv_splits(cv, X_train, y_train):
    return list(cv.split(X_train, y_train))
