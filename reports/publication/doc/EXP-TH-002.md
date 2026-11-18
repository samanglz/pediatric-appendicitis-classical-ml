<!-- Curated public-release copy. Original internal record preserved. -->

# Decision: Experimental Design, Dataset Splitting, and Data Preparation Policies

**Decision ID:** EXP-TH-002

**Status:** Accepted (for the decisions explicitly marked as accepted below)

## 1. Research Design

The project will compare classical machine-learning classification algorithms for predicting pediatric appendicitis using the Regensburg Pediatric Appendicitis dataset.

The project will use two experiments to investigate the effect of three selected clinical variables on model performance.

### Experiment 1 — Including the Selected Clinical Features

Models will be trained using the eligible predictor features, including:

- `Alvarado_Score`
- `Paedriatic_Appendicitis_Score`
- `Appendix_Diameter`

### Experiment 2 — Excluding the Selected Clinical Features

Models will be trained using the same eligible predictor features, but without the three variables listed above.

All other experimental conditions will remain consistent between the two experiments, including the data split, algorithms, evaluation metrics, and classification threshold.

**Rationale:**

This design allows the project to investigate how the inclusion or exclusion of these three variables affects model performance while keeping the comparison as consistent as possible.

## 2. Target Variable and Positive Class

**Target variable:** `Diagnosis`

The target variable contains two classes:

- `Appendicitis`
- `No Appendicitis`

The positive class is defined as `Appendicitis`.

Records with missing values in the target variable will be excluded from supervised model development and evaluation.

The two records with missing `Diagnosis` values will therefore be excluded.

## 3. Train/Test Split Strategy

**Decision ID:** EXP-SPLIT-001

**Status:** Accepted

The dataset will be divided into training and testing sets using a stratified train/test split.

**Decision:**

- Training set: 80%
- Test set: 20%
- Random state: `42`
- Stratification variable: `Diagnosis`

Stratification will preserve approximately the same class distribution in both subsets.

**Rationale:**

1. Maintaining a representative distribution of both target classes in the training and test sets.
2. Reducing the risk of an unrepresentative split caused by random sampling.
3. Supporting a fair comparison of classification algorithms.
4. Ensuring that both experiments use exactly the same training and test records.

### Actual Split Results

After excluding the two records with missing target values, the dataset contained 780 labelled records.

| Partition | Appendicitis | No Appendicitis | Total |
|---|---:|---:|---:|
| Training | 370 (59.29%) | 254 (40.71%) | 624 |
| Testing | 93 (59.62%) | 63 (40.38%) | 156 |
| Total | 463 | 317 | 780 |

The split was successfully performed, and the verification confirmed:

- No overlapping row indices between training and testing sets.
- The class proportions were approximately preserved.
- All 780 labelled records were assigned to one of the two subsets.

## 4. Independent Test Set Policy

**Decision ID:** EXP-TEST-001

**Status:** Accepted

The test set will be reserved exclusively for final model evaluation.

It must not be used during model development for:

- Feature selection.
- Data preprocessing parameter fitting.
- Hyperparameter tuning.
- Threshold optimization.
- Model selection.
- Any iterative decisions intended to improve model performance.

All preprocessing transformations must be fitted using training data only.

The test set will be used only after the model-development process has been completed.

## 5. Feature Exclusion Policy

**Decision ID:** EXP-FEATURE-EXCL-001

**Status:** Accepted

The following variables will not be used as model predictors:

| Feature | Reason for Exclusion |
|---|---|
| `Diagnosis` | Target variable, not a predictor. |
| `Diagnosis_Presumptive` | Contains presumptive diagnostic information strongly associated with the final diagnosis and may introduce target leakage. |
| `Management` | Represents a clinical management decision that is strongly associated with the diagnosis and may contain downstream information. |
| `Severity` | Strongly associated with the diagnosis and may represent information unavailable at the intended prediction point. |
| `Length_of_Stay` | Represents information recorded at discharge and is not appropriate as a predictor. |
| `US_Performed` | Excluded from the final model input feature set. |
| `Appendix_on_US` | Excluded from the final model input feature set. |
| `US_Number` | Identifier/reference field rather than a clinical predictor. |

The remaining eligible features will be reviewed before the final predictor list is approved.

## 6. Unit of Analysis and Identifier Handling

**Status:** Accepted with a documented limitation

Each labelled row in the tabular dataset will be treated as one modelling record for the current train/test split.

`US_Number` will not be used as a predictor.

Although the non-missing `US_Number` values were unique in the dataset, this fact alone does not conclusively establish patient-level independence across all records.

If reliable evidence of repeated patients or a suitable patient-level grouping identifier becomes available, the splitting strategy should be reconsidered.

## 7. Decision Regarding test_set_codes.csv

**Decision ID:** EXP-DATA-001

**Status:** Accepted

The `test_set_codes.csv` file will not be used to define the train/test split for this tabular machine-learning project.

The file contained 71 unique codes. A comparison with the non-missing `US_Number` values identified 57 matching codes and 14 unmatched codes.

Although the official dataset files were verified against the Zenodo version 1.03 files using MD5 hashes, the available documentation does not unambiguously establish that these codes correspond directly to the rows in the tabular Excel dataset.

Therefore, the project will use its own stratified 80/20 train/test split.

No definitive assumption will be made about the exact meaning of all codes in `test_set_codes.csv`.

## 8. Dataset Integrity and Missing-Value Considerations

**Status:** Initial audit findings accepted; final feature and preprocessing policies subsequently implemented

The initial dataset contained 782 rows and 58 columns.

After excluding the two records with missing `Diagnosis`, 780 labelled records remained.

The target distribution was:

- Appendicitis: 463 records.
- No Appendicitis: 317 records.

No severe class imbalance was identified. Therefore, SMOTE is not currently planned.

The dataset contains missing values, including substantial missingness in several ultrasound-derived features.

Missing ultrasound findings must not automatically be interpreted as negative findings.

The following observations were identified during the dataset audit:

- `Appendix_Diameter` has 284 missing values (36.32%).
- `Alvarado_Score` and `Paedriatic_Appendicitis_Score` each have 52 missing values (6.65%).
- Several ultrasound-related variables have more than 90% missing values.
- Missingness patterns differ across management groups and may partly reflect clinical workflow.

The subsequent feature audit documented in `EXP-TH-004.md` assessed 17 high-missingness features: ten were excluded and seven were retained as eligible candidates. The final model input configuration was then implemented and is documented in the source preprocessing module.

No suspicious numerical values will be silently modified or removed without further investigation and supporting evidence.

## 9. Evaluated Classical Machine-Learning Algorithms

The initial model comparison will include:

1. DummyClassifier as a baseline.
2. Logistic Regression.
3. Decision Tree.
4. Random Forest.
5. Gradient Boosting.

The project will remain focused on classical machine-learning classification methods.

Deep-learning models and ultrasound-image analysis are outside the scope of this project.

## 10. Preprocessing and Leakage Prevention

**Status:** Implemented and verified in the final training pipelines

Preprocessing must be performed without allowing information from the test set to influence model development.

The implemented approach uses scikit-learn pipelines and a shared preprocessing module.

The final implementation follows these principles:

1. Numeric features use median imputation.
2. Missingness indicators are generated for numeric and ordinal features.
3. The ordinal urine features `Ketones_in_Urine`, `RBC_in_Urine`, and `WBC_in_Urine` use most-frequent imputation followed by an `OrdinalEncoder` with explicitly defined category order and an unknown-value code of -1.
4. Nominal categorical features use constant imputation with the `__MISSING__` marker followed by one-hot encoding.
5. Preprocessing transformations are fitted within each training fold during cross-validation.
6. Final selected pipelines are fitted on the training partition; the held-out test partition is reserved for final evaluation.
7. The same preprocessing design is used for both experiments, with the experiment-specific predictor list determining the input columns.

The final feature configuration is implemented in `src/preprocessing.py`. Experiment 1 uses 40 predictors. Experiment 2 uses 37 predictors after excluding the three experiment-specific clinical variables.

## 11. Relationship with EXP-TH-001

This decision is complementary to `EXP-TH-001`, which establishes a fixed classification threshold of 0.5 for all models in both experiments.

The two decisions jointly define the current experimental framework:

- `EXP-TH-001`: Classification threshold and evaluation policy.
- `EXP-TH-002`: Experimental design, target definition, dataset splitting, feature exclusions, data integrity considerations, and leakage-prevention policies.

In case of overlap, the specific threshold rules defined in `EXP-TH-001` remain authoritative.

## 12. Subsequent Implementation Status

The following items were pending when this initial decision
document was written. They were subsequently addressed during
the project's implementation:

1. **Eligible predictor features:** Finalized and implemented
   through the approved 40-feature and 37-feature experiment
   configurations.
2. **High-missingness features:** Reviewed and documented in
   `EXP-TH-004.md`; ten features were excluded and seven were
   retained.
3. **Feature typing:** Finalized in the implemented
   preprocessing pipeline.
4. **Missing-value handling:** Implemented using training-fold
   preprocessing pipelines, including numeric median
   imputation, ordinal most-frequent imputation, and nominal
   missing-value handling.
5. **Preprocessing configuration:** Implemented in the shared
   preprocessing module and fitted within each training fold.
6. **Cross-validation:** Finalized as shared Stratified
   10-Fold Cross-Validation with shuffling and random state 42.
7. **Model selection:** Based on mean positive-class Recall as
   the primary criterion, with complementary metrics and
   Recall stability considered. No threshold tuning was used.

The later approved evaluation and model-selection records,
together with the archived official results, are the references
for the completed implementation.

This section records subsequent project status; it does not
rewrite the historical decisions that were pending at the time
of the original document.

---

**Final Scope**

This decision applies to both experiments and establishes the methodological rules for dataset preparation, splitting, feature eligibility, and leakage prevention.

The purpose is to ensure a consistent, reproducible, and scientifically defensible comparison of classical machine-learning algorithms for pediatric appendicitis prediction.