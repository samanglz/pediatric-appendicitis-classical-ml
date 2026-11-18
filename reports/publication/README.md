# Publication Reports

This directory contains the curated, non-patient-level research
artifacts selected for public release.

The original internal experiment archives are retained separately
under `reports/` and are not part of this curated publication set.

## Directory structure

```text
publication/
├── README.md
├── PROJECT_DECISION_HISTORY.md
├── decisions/
│   ├── EXP-ARCH-001.md
│   ├── EXP-EVAL-001.md
│   └── EXP-MODEL-SEL-001.md
├── doc/
│   ├── EXP-TH-001.md
│   ├── EXP-TH-002.md
│   ├── EXP-TH-003.md
│   └── EXP-TH-004.md
├── research/
│   ├── final_research_results.md
│   ├── hypotheses_evaluation.md
│   ├── feature_effect_interpretation.md
│   └── discussion_and_limitations.md
├── cross_validation/
│   ├── fold_results.csv
│   ├── model_summary.csv
│   ├── paired_fold_comparison.csv
│   ├── model_stability.csv
│   └── figures/
└── test_evaluation/
    ├── test_metrics.csv
    └── confusion_matrices.json
```

## Research documents

- `final_research_results.md`: consolidated cross-validation and
  held-out test results.
- `hypotheses_evaluation.md`: descriptive evaluation of H1, H2, and H3.
- `feature_effect_interpretation.md`: interpretation of the evaluated
  feature configurations.
- `discussion_and_limitations.md`: discussion, limitations, and
  interpretation boundaries.

## Cross-validation artifacts

The cross-validation artifacts correspond to the official run:

`10fold_official_20261118_083752`

They include:

- Fold-level metrics for the five evaluated model families and both
  feature configurations.
- Aggregated model summaries.
- Same-algorithm paired fold comparisons.
- Model stability summaries.
- Recall and Average Precision comparison figures.

The official protocol used Stratified 10-Fold Cross-Validation,
shared fold splits, shuffling, and random seed 42.

The archived fold-level results are experiment outputs. The source
repository contains pipeline construction and split-generation
utilities, but does not currently provide a standalone end-to-end
script that independently regenerates the complete CV results.

## Final test artifacts

The final held-out test artifacts correspond to:

`final_test_evaluation_20261118_091752`

The selected models were trained using the training partition and
evaluated on the held-out test partition.

Published test artifacts include aggregate metrics and confusion
matrices. Row-level predictions and patient-level records are not
included.

## Metric definitions

- **Recall:** proportion of actual positive cases correctly identified.
- **Precision:** proportion of predicted positive cases that are
  actually positive.
- **F1-score:** harmonic mean of precision and recall.
- **Accuracy:** proportion of all predictions that are correct.
- **Balanced Accuracy:** average recall across the classes.
- **ROC-AUC:** area under the receiver operating characteristic curve.
- **Average Precision (AP):** summary of the precision-recall ranking
  performance across score thresholds.
- **Recall SD:** standard deviation of fold-level recall values.

Average Precision and area under a plotted precision-recall curve
(PR-AUC) are related but are not interchangeable definitions.

## Interpretation

Recall was the pre-specified primary model-selection metric.
Other metrics provide complementary information.

The reported hypothesis conclusions are descriptive. They do not
claim inferential statistical significance.

The results come from one retrospective dataset and do not establish
clinical effectiveness, prospective utility, or external
generalizability.

## Data governance

This directory intentionally excludes:

- Patient-level datasets.
- Prepared dataset files.
- Row-level test predictions.
- Trained model binaries.
- Private or intermediate audit artifacts.

The dataset may have separate access and licensing conditions.
The repository's MIT License applies to project code and does not
grant rights to the dataset or third-party materials.

## Decision records and project history

The `decisions/` directory contains the approved architecture,
evaluation, and model-selection records. The `doc/` directory
contains the project's methodological and data-preparation
decisions, including their subsequent implementation status.

`PROJECT_DECISION_HISTORY.md` provides an overview of how
these decisions relate to the completed experiments.

These are curated public-release copies. Original internal
records remain preserved separately. Where an initial
document contains pending items, the public copy identifies
their subsequent implementation status.

The official evaluation protocol uses Stratified 10-Fold
Cross-Validation with shared folds, shuffling, and random
state 42.
