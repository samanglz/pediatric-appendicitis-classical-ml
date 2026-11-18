# Classical Machine Learning for Pediatric Appendicitis Prediction

A reproducible-oriented research project comparing classical machine learning models for pediatric appendicitis prediction using structured clinical and imaging-related features.

The project investigates model performance under two feature configurations and evaluates the contribution of three selected predictors through controlled, same-algorithm comparisons.

> **Research use only.** This project is not a clinical decision-support system and must not be used to diagnose patients or replace professional medical judgment.

## Research objectives

1. Compare five classical machine learning algorithms for binary appendicitis prediction.
2. Evaluate model performance using stratified cross-validation and a held-out test set.
3. Examine how performance changes when three selected predictors are excluded.
4. Report recall as the primary evaluation metric, with complementary metrics for a broader assessment.

## Dataset and data governance

The project uses the Regensburg Pediatric Appendicitis dataset.

- 782 original records.
- 780 records with a valid target label.
- Stratified train/test split: 624 training records and 156 test records.
- Positive class: `appendicitis`.
- The test set was kept separate from preprocessing fitting, cross-validation, and model selection.
- Patient-level data and prepared dataset files are intentionally not included in this public repository.

The original dataset and patient-level records may be subject to their own access and licensing conditions. The MIT license in this repository applies to the project code, not to the dataset.

## Experimental design

Two feature configurations were evaluated using the same five model families.

| Experiment | Predictors | Number of features |
|---|---|---:|
| Experiment 1 | Full approved predictor set | 40 |
| Experiment 2 | Excludes Alvarado Score, Pediatric Appendicitis Score, and Appendix Diameter | 37 |

Models:

- Dummy Classifier
- Logistic Regression
- Decision Tree
- Random Forest
- Gradient Boosting

The positive class is `appendicitis`. Recall was the pre-specified primary metric. Precision, F1-score, Average Precision (AP), and recall variability were also considered.

### Preprocessing

Preprocessing is implemented within scikit-learn pipelines so that transformations are fitted on training data within each cross-validation fold.

The implemented components include:

- Median imputation and missingness indicators for numeric variables.
- Most-frequent imputation and ordinal encoding for ordinal variables.
- Constant missing-value handling and one-hot encoding for nominal variables.
- Standard scaling for Logistic Regression.

### Cross-validation protocol

- Stratified 10-Fold Cross-Validation.
- Shuffling enabled.
- Random seed: 42.
- Shared fold splits across model comparisons.
- No test-set use for cross-validation or model selection.
- Classification threshold: 0.5.
- No threshold tuning.

The project contains the model templates, preprocessing pipeline integration, and shared CV split-generation utilities in `src/pipelines.py`.

**Reproducibility note:** The current source tree does not contain a standalone script that independently executes the complete 10-Fold CV loop and regenerates all fold-level results. The CV results presented in this repository are archived experiment outputs. The presence of pipeline construction and split-generation utilities should not be interpreted as a claim that the entire CV experiment can currently be reproduced with a single command.

## Cross-validation results

The selected models were chosen using the pre-specified primary metric, mean Recall.

| Experiment | Selected model | Mean Recall | Recall SD | Precision | F1 | AP |
|---|---|---:|---:|---:|---:|---:|
| Experiment 1 | Gradient Boosting | 0.9486 | 0.0431 | 0.9755 | 0.9613 | 0.9916 |
| Experiment 2 | Random Forest | 0.8270 | 0.0640 | 0.8392 | 0.8318 | 0.9206 |

Random Forest was selected for Experiment 2 because it achieved the highest mean Recall in that experiment. Gradient Boosting had a slightly higher AP, but AP was not the primary selection criterion.

## Final held-out test results

The selected model for each experiment was trained on the complete training partition and evaluated on the held-out test set.

| Metric | Experiment 1: Gradient Boosting | Experiment 2: Random Forest |
|---|---:|---:|
| Accuracy | 0.9551 | 0.8590 |
| Precision | 0.9778 | 0.8817 |
| Recall | 0.9462 | 0.8817 |
| F1-score | 0.9617 | 0.8817 |
| Balanced Accuracy | 0.9572 | 0.8536 |
| ROC-AUC | 0.9694 | 0.8980 |
| Average Precision | 0.9840 | 0.9392 |

The two final test models are different algorithms. Therefore, the difference between their test scores cannot be attributed exclusively to the removal of the three predictors. Same-algorithm paired cross-validation comparisons provide a more appropriate descriptive assessment of feature-set differences.

These results are descriptive. No inferential statistical significance is claimed.

## Main findings

- Experiment 1 achieved higher mean Recall than Experiment 2 in the selected-model cross-validation results.
- Same-algorithm paired fold comparisons showed higher Recall and AP for Experiment 1 across the four non-baseline algorithms.
- The final held-out test results were consistent with the overall CV pattern.
- The results support the importance of the evaluated feature configuration in this dataset, but do not establish clinical effectiveness or generalization to other hospitals or populations.

## Project structure

```text
ML_Classic_appendicit/
├── src/
│   ├── data_io.py
│   ├── preprocessing.py
│   ├── pipelines.py
│   ├── train_final_models.py
│   └── evaluate_final_models.py
├── reports/
│   └── publication/
│       ├── README.md
│       ├── research/
│       ├── cross_validation/
│       └── test_evaluation/
├── data/                 # Excluded from public repository
├── models/               # Excluded from public repository
├── README.md
├── requirements.txt
├── .gitignore
└── LICENSE
```

Only the curated `reports/publication/` directory is intended for
public release. Internal experiment archives and intermediate
evaluation outputs are retained locally and excluded from the
public repository.

## Environment

The recorded environment used for final model training and test evaluation:

| Package | Version |
|---|---:|
| Python | 3.13.18 |
| NumPy | 2.4.6 |
| pandas | 2.2.3 |
| scikit-learn | 1.6.1 |
| joblib | 1.6.0 |
| tabulate | 0.9.0 |

Install the listed dependencies:

```bash
pip install -r requirements.txt
```

## Running the available scripts

The prepared dataset file and trained model artifacts are not distributed in this repository. The scripts require the corresponding local project artifacts.

### Train final models

From the project root:

```bash
python src/train_final_models.py
```

The training script uses the prepared datasets and saves model artifacts and a training manifest under a run-specific directory.

### Evaluate final models

From the project root, provide the project root and the relevant training run ID:

```bash
python src/evaluate_final_models.py \
  --project-root . \
  --training-run-id final_models_20261118_091523
```

The evaluation script expects the prepared datasets and corresponding trained model artifacts to be available locally.

These commands describe the available final-training and test-evaluation workflow. They do not regenerate the archived 10-Fold CV results.

## Limitations

- The analysis is based on one dataset and does not include external validation.
- The sample size is limited.
- The results are retrospective and do not demonstrate prospective clinical utility.
- Model performance may change across institutions, populations, data collection practices, and clinical workflows.
- The archived CV results are not currently regenerated by a standalone end-to-end CV execution script in the repository.
- The final selected models differ between experiments; consequently, their test-score difference does not isolate the effect of the three excluded predictors.
- No clinical deployment, diagnostic recommendation, or patient-management use is claimed.

## License

The project code is released under the MIT License. See [LICENSE](LICENSE).

The dataset, patient-level records, and third-party materials are not covered by this repository's code license.
