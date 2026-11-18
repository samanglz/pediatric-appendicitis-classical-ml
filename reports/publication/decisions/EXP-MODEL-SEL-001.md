<!-- Curated public-release copy. Original internal record preserved. -->

# EXP-MODEL-SEL-001 — Final Model Selection Decision

## 1. Decision Status

Approved model selection based on the completed official Stratified 10-Fold
Cross-Validation and its read-only audit.

## 2. Selection Policy

Mean Recall is the primary model-selection criterion.

The following supporting criteria are also considered:
- Mean Average Precision (AP)
- Mean Precision
- Mean F1-score
- Recall stability across the ten validation folds, assessed using
  standard deviation and observed range.

The Dummy classifier is retained as a baseline and is not considered
a candidate for final model selection.

The held-out Test dataset is not used for model selection.

## 3. Selected Models

### Experiment 1

- Selected model: GradientBoosting
- Number of predictors: 40
- Mean Recall: 0.9486
- Recall standard deviation: 0.0431
- Recall range: 0.8649–1.0000
- Mean Precision: 0.9755
- Mean F1-score: 0.9613
- Mean Average Precision: 0.9916

Rationale:
GradientBoosting achieved the highest mean Recall among the learning
algorithms in Experiment 1. It also showed the lowest Recall standard
deviation and range among the learning algorithms in this experiment.

### Experiment 2

- Selected model: RandomForest
- Number of predictors: 37
- Mean Recall: 0.8270
- Recall standard deviation: 0.0640
- Recall range: 0.7568–0.9189
- Mean Precision: 0.8392
- Mean F1-score: 0.8318
- Mean Average Precision: 0.9206

Rationale:
RandomForest achieved the highest mean Recall among the learning
algorithms in Experiment 2. GradientBoosting had slightly higher mean
AP and slightly lower Recall standard deviation, but Recall remains
the primary selection criterion.

## 4. Final Selection

- Experiment 1: GradientBoosting
- Experiment 2: RandomForest

These selections are based exclusively on training-set cross-validation
results and the previously approved selection policy.

## 5. Next Step

Rebuild the two selected preprocessing/model Pipelines and fit each
Pipeline using all 624 training samples.

The 156-sample held-out Test dataset must remain untouched until the
final evaluation stage.

No threshold tuning or model selection using Test data is permitted.

## 6. Reproducibility

- Cross-validation: Stratified 10-Fold
- Shuffle: True
- Random state: 42
- Classification threshold: 0.5
- Positive class: appendicitis
- Original official CV results must remain unchanged.
