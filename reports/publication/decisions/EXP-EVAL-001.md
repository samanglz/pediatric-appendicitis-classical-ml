<!-- Curated public-release copy. Original internal record preserved. -->

# EXP-EVAL-001: Model Evaluation Policy

## 1. Purpose

This document defines the evaluation protocol for the
Pediatric Appendicitis Classical Machine Learning project.

The objective is to compare five classical machine learning
algorithms across two feature experiments under a consistent
and leakage-controlled evaluation strategy.

## 2. Dataset and Target

- Training set: 624 samples.
- Independent Test set: 156 samples.
- Target column: `Diagnosis`.
- Positive class: `appendicitis`.
- Negative class: `no appendicitis`.

The Test dataset must remain untouched during preprocessing
design, cross-validation, model selection, and any other
training-stage decisions.

## 3. Experiments

### Experiment 1

Includes all approved predictors, including:

- `Alvarado_Score`
- `Paedriatic_Appendicitis_Score`
- `Appendix_Diameter`

Total raw predictors: 40.

### Experiment 2

Excludes the three predictors listed above.

Total raw predictors: 37.

All other previously approved feature eligibility and
exclusion decisions remain unchanged.

## 4. Candidate Algorithms

The following five algorithms will be evaluated in both
experiments:

1. DummyClassifier (strategy="prior")
2. LogisticRegression
3. DecisionTreeClassifier
4. RandomForestClassifier
5. GradientBoostingClassifier

Total candidate pipelines: 10.

The Dummy classifier is retained as a baseline.

## 5. Preprocessing and Pipeline Isolation

Each candidate pipeline must contain its own independent
clone of the experiment-specific preprocessor.

Preprocessing must be fitted only on the training partition
of each cross-validation fold.

The corresponding validation partition must only be
transformed using the fitted training-fold preprocessor.

Scaling policy:

- Logistic Regression: StandardScaler(with_mean=False).
- Dummy and tree-based models: no scaling.

All preprocessing and model fitting must occur inside
the sklearn Pipeline to prevent information leakage.

## 6. Cross-Validation Strategy

Use Stratified 10-Fold Cross-Validation with:

- n_splits = 10
- shuffle = True
- random_state = 42

The ten folds must be generated once from the training
dataset and reused unchanged across all ten pipelines.

This ensures that every candidate model is evaluated on
the same training and validation partitions.

Each training sample must appear in a validation partition
exactly once.

## 7. Training-Stage Restrictions

Only the Training dataset may be used for:

- Preprocessing fitting.
- Cross-validation.
- Model comparison and selection.
- Hyperparameter decisions, if explicitly approved.
- Any training-stage evaluation decisions.

The independent Test dataset must not be used for:

- Feature selection.
- Preprocessing design or fitting.
- Hyperparameter tuning.
- Model selection.
- Threshold selection.
- Repeated experimentation or optimization.

No threshold tuning is planned.

## 8. Classification Threshold

The classification threshold is fixed at 0.5.

For the positive class:

- Probability >= 0.5: appendicitis.
- Probability < 0.5: no appendicitis.

The positive-class probability must be extracted by
identifying the `appendicitis` class in `classes_`.
Its column position must not be assumed.

ROC-AUC, PR-AUC, and Average Precision (AP) must use
continuous prediction scores or probabilities for the
positive class, not binary labels.

Average Precision (AP) must be calculated using
`sklearn.metrics.average_precision_score` for the positive
class (`appendicitis`).

AP and PR-AUC must be reported as separate metrics.
Although both are derived from the Precision-Recall
relationship, they are not necessarily numerically
identical because their calculation methods differ.

## 9. Evaluation Metrics

The following metrics will be reported:

1. Accuracy
2. Precision
3. Recall
4. F1-score
5. Balanced Accuracy
6. ROC-AUC
7. PR-AUC
8. Average Precision (AP)
9. Confusion Matrix

Recall for the positive class (`appendicitis`) is the
primary metric.

Precision, F1-score, Balanced Accuracy, ROC-AUC, PR-AUC,
Average Precision (AP), and Confusion Matrix provide
complementary information.

## 10. Model Selection and Final Evaluation

Candidate pipelines will first be compared using only
Training-set cross-validation results.

After model selection:

1. The selected pipeline for each experiment will be
   fitted on the complete Training dataset.
2. The fitted pipeline will be evaluated on the independent
   Test dataset.
3. The fixed classification threshold of 0.5 will be used.
4. All approved evaluation metrics will be reported.

The Test set is reserved for this final evaluation.

## 11. GradientBoosting Compatibility Check

Before official cross-validation, GradientBoostingClassifier
was tested independently in both experiments using
120-sample stratified subsets drawn from Training data.

Results:

- Experiment 1: Fit, Predict, and Predict Proba passed.
- Experiment 2: Fit, Predict, and Predict Proba passed.
- Preprocessor output was Dense in both experiments.
- No Test samples were used.
- No official cross-validation or model selection was performed.

This was a technical compatibility check only and its
results are not part of the official model comparison.

## 12. Reproducibility

The following settings must remain fixed unless a formally
documented decision changes them:

- Random state: 42.
- Cross-validation: StratifiedKFold, 10 splits, shuffle=True.
- Classification threshold: 0.5.
- Shared folds across all ten candidate pipelines.
- Independent preprocessing pipelines.

## 13. Scope

This evaluation is a retrospective tabular machine learning
study using information recorded during clinical assessment.

The models are not intended to replace clinical judgment
or serve as autonomous diagnostic systems.

The dataset's reference standard is heterogeneous:
operated patients have histological confirmation, while
conservatively managed patients may have labels based on
clinical criteria. This limitation must be considered when
interpreting model performance.

## 14. Status

Evaluation policy approved and locked before official
cross-validation.

No official cross-validation results are included in this
document.
