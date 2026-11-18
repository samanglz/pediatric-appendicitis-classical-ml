<!-- Curated public-release copy. Original internal record preserved. -->

# EXP-ARCH-001
## Experiment Architecture and Shared Cross-Validation Design

**Status:** Approved

### 1. Objective

Define a consistent architecture for the two experimental
configurations used to compare classical machine learning
classification algorithms for pediatric appendicitis prediction.

### 2. Experiment 1

Experiment 1 includes the following three additional predictors:

- Alvarado_Score
- Paedriatic_Appendicitis_Score
- Appendix_Diameter

Five classifiers will be evaluated:

1. DummyClassifier
2. LogisticRegression
3. DecisionTree
4. RandomForest
5. GradientBoosting

### 3. Experiment 2

Experiment 2 excludes the following predictors:

- Alvarado_Score
- Paedriatic_Appendicitis_Score
- Appendix_Diameter

The same five classifiers will be evaluated.

### 4. Pipeline Architecture

Each experiment contains five independent model pipelines.

Every pipeline uses an independently cloned instance of
the corresponding experiment's preprocessing pipeline.

The architecture is:

#### DummyClassifier

Preprocessing -> Model

#### LogisticRegression

Preprocessing -> Scaling -> Model

Scaling uses StandardScaler(with_mean=False) to preserve
sparse matrix compatibility.

#### DecisionTree

Preprocessing -> Model

#### RandomForest

Preprocessing -> Model

#### GradientBoosting

Preprocessing -> Model

Scaling is applied only to LogisticRegression.

The DummyClassifier remains part of the same pipeline
structure for consistent data-flow and evaluation handling.

Total number of independent pipelines: 10.

### 5. Shared Cross-Validation Strategy

A single StratifiedKFold configuration will be shared
across both experiments and all classifiers.

Configuration:

- n_splits = 10
- shuffle = True
- random_state = 42

The fold indices will be generated once from the training
data and reused for all ten pipelines.

This ensures that model comparisons are performed using
identical training and validation partitions.

### 6. Data Isolation and Leakage Prevention

- Only training data will be used during cross-validation.
- Preprocessing will be fitted independently within each
  training fold through the model pipelines.
- Validation folds will only be transformed using the
  preprocessing fitted on their corresponding training folds.
- The independent test dataset will not be used for
  preprocessing fitting, cross-validation, feature selection,
  model selection, or hyperparameter tuning.
- The test dataset will be reserved for final independent
  evaluation after model selection.

### 7. Experiment Comparison

The two experiments will use the same classifiers,
cross-validation strategy, evaluation metrics, and
decision threshold.

This design allows the effect of excluding the three
specified predictors to be compared consistently.

### 8. Approval

This architecture is approved as the implementation
reference for the project's experimental pipelines
and shared cross-validation procedure.
