# Project Decision History

## Purpose

This document summarizes the major methodological decisions
that shaped the Pediatric Appendicitis Classical Machine
Learning project. Detailed records are available in the
accompanying `decisions/` and `doc/` directories.

## 1. Initial research and data-governance decisions

`EXP-TH-002.md` records the initial research design, target
definition, stratified train/test split, independent test-set
policy, feature eligibility principles, and data-preparation
constraints.

`EXP-TH-003.md` records the decision to assess usable clinical,
demographic, laboratory, and ultrasound features subject to
the project's feature eligibility and data-governance rules.

`EXP-TH-004.md` records the assessment of high-missingness
features and the resulting retained and excluded feature groups.

## 2. Classification and evaluation policy

`EXP-TH-001.md` establishes a fixed classification threshold
of 0.5 across both experiments.

`EXP-EVAL-001.md` formalizes the evaluation protocol, including
the positive class, training/test isolation, fold-local
preprocessing, evaluation metrics, and Stratified 10-Fold
Cross-Validation.

## 3. Experiment architecture

`EXP-ARCH-001.md` defines the two feature configurations,
the five candidate classifier families, independent
preprocessing pipelines, and shared cross-validation folds.

Both experiments use the same data partitions, candidate
algorithms, evaluation metrics, and fixed classification
threshold.

## 4. Official model selection

Following completion and audit of the official 10-Fold
Cross-Validation, `EXP-MODEL-SEL-001.md` records the selected
models:

- Experiment 1: GradientBoosting.
- Experiment 2: RandomForest.

Mean Recall was the primary selection criterion. Average
Precision, Precision, F1-score, and Recall stability were
considered as supporting criteria.

The held-out Test set was not used for model selection.

## 5. Final training and independent evaluation

The selected pipelines were fitted on the complete training
partition. Final evaluation was then performed on the reserved
held-out Test partition using the predefined threshold of 0.5.

Aggregate results and supporting artifacts are available in
the publication `cross_validation/` and `test_evaluation/`
directories.

## 6. Interpretation boundaries

The project reports descriptive experimental findings. It
does not claim inferential statistical significance,
prospective clinical effectiveness, or external generalizability.

The original internal decision records are retained separately
from these curated public-release copies. Where a later
approved decision supersedes an earlier pending item, the
publication copy identifies the subsequent implementation
status.

## 7. Source-of-truth hierarchy

For the completed project, readers should use:

1. Approved architecture and evaluation decisions for the
   experimental protocol.
2. The final model-selection decision for selected models.
3. Official cross-validation and final test artifacts for
   reported performance.
4. Research reports for consolidated interpretation and
   limitations.

Historical documents explain how the project evolved; they
should not be interpreted as overriding later approved
decisions or final archived results.
