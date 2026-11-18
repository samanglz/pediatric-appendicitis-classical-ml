# Final Research Results
## Pediatric Appendicitis — Classical Machine Learning

## 1. Evaluation protocol

- Dataset: 780 cases with valid target labels.
- Training set: 624 cases.
- Final Test set: 156 cases (93 positive, 63 negative).
- Positive class: `appendicitis`.
- Cross-validation: Stratified 10-Fold CV.
- CV folds were shared across the two experiments.
- Classification threshold: 0.5.
- Preprocessing was fitted within each CV training fold.
- Model selection used training-only CV results.
- Final Test was used only for final evaluation.
- No Test fitting or threshold tuning was performed.

## 2. Cross-validation results — all algorithms

All five algorithms are reported for both experiments.
Values are mean ± standard deviation across the ten folds.
OOF confusion matrix counts are pooled across all out-of-fold predictions.

| Experiment | Model | Accuracy | Precision | Recall | F1 | Balanced Accuracy | ROC-AUC | PR-AUC | Average Precision | OOF TN | OOF FP | OOF FN | OOF TP |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Experiment_1 | Dummy | 0.5930 ± 0.0049 | 0.5930 ± 0.0049 | 1.0000 ± 0.0000 | 0.7445 ± 0.0039 | 0.5000 ± 0.0000 | 0.5000 ± 0.0000 | 0.7965 ± 0.0024 | 0.5930 ± 0.0049 | 0 | 254 | 0 | 370 |
| Experiment_1 | LogisticRegression | 0.9007 ± 0.0327 | 0.9297 ± 0.0353 | 0.9027 ± 0.0587 | 0.9145 ± 0.0304 | 0.8998 ± 0.0314 | 0.9584 ± 0.0215 | 0.9707 ± 0.0176 | 0.9712 ± 0.0172 | 228 | 26 | 36 | 334 |
| Experiment_1 | DecisionTree | 0.8974 ± 0.0379 | 0.9296 ± 0.0428 | 0.8973 ± 0.0581 | 0.9116 ± 0.0341 | 0.8972 ± 0.0386 | 0.8972 ± 0.0386 | 0.9439 ± 0.0225 | 0.8946 ± 0.0408 | 228 | 26 | 38 | 332 |
| Experiment_1 | RandomForest | 0.9070 ± 0.0339 | 0.9232 ± 0.0366 | 0.9216 ± 0.0517 | 0.9213 ± 0.0296 | 0.9035 ± 0.0337 | 0.9673 ± 0.0228 | 0.9796 ± 0.0156 | 0.9792 ± 0.0161 | 225 | 29 | 29 | 341 |
| Experiment_1 | GradientBoosting | 0.9551 ± 0.0260 | 0.9755 ± 0.0198 | 0.9486 ± 0.0431 | 0.9613 ± 0.0231 | 0.9565 ± 0.0236 | 0.9857 ± 0.0158 | 0.9915 ± 0.0097 | 0.9916 ± 0.0096 | 245 | 9 | 19 | 351 |
| Experiment_2 | Dummy | 0.5930 ± 0.0049 | 0.5930 ± 0.0049 | 1.0000 ± 0.0000 | 0.7445 ± 0.0039 | 0.5000 ± 0.0000 | 0.5000 ± 0.0000 | 0.7965 ± 0.0024 | 0.5930 ± 0.0049 | 0 | 254 | 0 | 370 |
| Experiment_2 | LogisticRegression | 0.7933 ± 0.0452 | 0.8348 ± 0.0341 | 0.8135 ± 0.0810 | 0.8220 ± 0.0451 | 0.7884 ± 0.0407 | 0.8756 ± 0.0392 | 0.9163 ± 0.0278 | 0.9178 ± 0.0270 | 194 | 60 | 69 | 301 |
| Experiment_2 | DecisionTree | 0.7388 ± 0.0323 | 0.7752 ± 0.0231 | 0.7892 ± 0.0622 | 0.7809 ± 0.0329 | 0.7274 ± 0.0289 | 0.7274 ± 0.0289 | 0.8447 ± 0.0169 | 0.7369 ± 0.0224 | 169 | 85 | 78 | 292 |
| Experiment_2 | RandomForest | 0.8029 ± 0.0383 | 0.8392 ± 0.0308 | 0.8270 ± 0.0640 | 0.8318 ± 0.0363 | 0.7971 ± 0.0354 | 0.8734 ± 0.0420 | 0.9213 ± 0.0263 | 0.9206 ± 0.0260 | 195 | 59 | 64 | 306 |
| Experiment_2 | GradientBoosting | 0.7966 ± 0.0414 | 0.8411 ± 0.0482 | 0.8135 ± 0.0617 | 0.8253 ± 0.0373 | 0.7926 ± 0.0423 | 0.8769 ± 0.0346 | 0.9199 ± 0.0218 | 0.9212 ± 0.0213 | 196 | 58 | 69 | 301 |

### Baseline interpretation

Dummy is retained as a baseline, not treated as a competitive
learning algorithm. Its high Recall must be interpreted alongside
its pooled confusion matrix and other metrics.

## 3. Final Test results — selected models

The selected models were GradientBoosting for Experiment 1 and
RandomForest for Experiment 2.

| Experiment | Selected Model | Accuracy | Precision | Recall | F1 | Balanced Accuracy | ROC-AUC | PR-AUC | Average Precision | TN | FP | FN | TP |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Experiment_1 | GradientBoosting | 0.9551 | 0.9778 | 0.9462 | 0.9617 | 0.9572 | 0.9694 | 0.9840 | 0.9840 | 61 | 2 | 5 | 88 |
| Experiment_2 | RandomForest | 0.8590 | 0.8817 | 0.8817 | 0.8817 | 0.8536 | 0.8980 | 0.9401 | 0.9392 | 52 | 11 | 11 | 82 |

## 4. Paired same-algorithm CV comparison

Differences are calculated as Experiment 1 minus Experiment 2
within each shared fold. Positive values favor Experiment 1.
The standard deviation is calculated across the ten paired
fold-level differences using sample standard deviation.

| Model | Metric | Mean Difference | SD of Differences | Positive Folds | Negative Folds | Equal Folds | Minimum | Maximum |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DecisionTree | Recall | 0.1081 | 0.0979 | 8 | 0 | 2 | 0.0000 | 0.2703 |
| DecisionTree | Average_Precision | 0.1577 | 0.0564 | 10 | 0 | 0 | 0.0488 | 0.2540 |
| Dummy | Recall | 0.0000 | 0.0000 | 0 | 0 | 10 | 0.0000 | 0.0000 |
| Dummy | Average_Precision | 0.0000 | 0.0000 | 0 | 0 | 10 | 0.0000 | 0.0000 |
| GradientBoosting | Recall | 0.1351 | 0.0477 | 10 | 0 | 0 | 0.0541 | 0.2162 |
| GradientBoosting | Average_Precision | 0.0703 | 0.0210 | 10 | 0 | 0 | 0.0327 | 0.1003 |
| LogisticRegression | Recall | 0.0892 | 0.0598 | 9 | 0 | 1 | 0.0000 | 0.1622 |
| LogisticRegression | Average_Precision | 0.0534 | 0.0216 | 10 | 0 | 0 | 0.0188 | 0.0888 |
| RandomForest | Recall | 0.0946 | 0.0464 | 10 | 0 | 0 | 0.0270 | 0.1622 |
| RandomForest | Average_Precision | 0.0586 | 0.0197 | 10 | 0 | 0 | 0.0333 | 0.0874 |

## 5. Interpretation boundaries

1. The paired CV comparison keeps the algorithm fixed and is
   therefore more informative about the effect of changing the
   feature set than comparing two different selected algorithms.

2. The final Test comparison evaluates the two selected pipelines.
   Since the selected algorithms differ, the Test performance
   difference cannot be attributed solely to the three removed
   predictors.

3. The three predictors are Alvarado_Score,
   Paedriatic_Appendicitis_Score, and Appendix_Diameter.

4. PR-AUC and Average Precision are distinct metrics and must
   not be treated as interchangeable.

6. These retrospective results do not establish clinical
   readiness. External validation is required, and the models
   are not substitutes for clinician judgment.

## 6. Source and audit provenance

- Official CV run: `10fold_official_20261118_083752`
- Final training run: `final_models_20261118_091523`
- Final Test evaluation: `final_test_evaluation_20261118_091752`
- Independent Test audit: PASS
- Original source result files: read-only
- Model fitting during report generation: NO
- Test fitting or threshold tuning: NO
