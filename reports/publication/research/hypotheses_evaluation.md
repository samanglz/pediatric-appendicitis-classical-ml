# Research Hypotheses Evaluation
## Classical ML for Pediatric Appendicitis Prediction

Evaluation date: 2026-11-18

---

# H1 — Differences Between Learning Algorithms

## Hypothesis

The performance of different classical machine learning algorithms
for predicting pediatric appendicitis is not identical.

## Evaluation protocol

- Stratified 10-Fold Cross-Validation.
- Four learning algorithms compared separately in each experiment.
- DummyClassifier retained as a baseline, not as a competing learning algorithm.
- Recall was the primary selection metric.
- Precision, F1, Average Precision, and Recall stability were also examined.
- No statistical significance test was performed.

## Experiment 1 — Three additional features included

| Model | Mean Recall | Mean Precision | Mean F1 | Mean AP | Recall Std |
|---|---:|---:|---:|---:|---:|
| Logistic Regression | 0.9027 | 0.9297 | 0.9145 | 0.9712 | 0.0587 |
| Decision Tree | 0.8973 | 0.9296 | 0.9116 | 0.8946 | 0.0581 |
| Random Forest | 0.9216 | 0.9232 | 0.9213 | 0.9792 | 0.0517 |
| Gradient Boosting | 0.9486 | 0.9755 | 0.9613 | 0.9916 | 0.0431 |

Gradient Boosting achieved the highest mean Recall, Precision,
F1, and Average Precision in Experiment 1.

## Experiment 2 — Three additional features excluded

| Model | Mean Recall | Mean Precision | Mean F1 | Mean AP | Recall Std |
|---|---:|---:|---:|---:|---:|
| Logistic Regression | 0.8135 | 0.8348 | 0.8220 | 0.9178 | 0.0810 |
| Decision Tree | 0.7892 | 0.7752 | 0.7809 | 0.7369 | 0.0622 |
| Random Forest | 0.8270 | 0.8392 | 0.8318 | 0.9206 | 0.0640 |
| Gradient Boosting | 0.8135 | 0.8411 | 0.8253 | 0.9212 | 0.0617 |

Random Forest achieved the highest mean Recall and F1 in
Experiment 2. Gradient Boosting achieved slightly higher
Precision and Average Precision.

## H1 conclusion

**H1 is supported by descriptive evidence.**

The evaluated algorithms showed different performance levels
in both experiments. The best-performing algorithm also differed
depending on the experiment and evaluation metric.

No statistical significance test was performed. Therefore,
this conclusion does not establish statistically significant
differences between algorithms.

---

# H2 — Effect of Removing Three Features

## Hypothesis

Removing `Alvarado_Score`, `Paedriatic_Appendicitis_Score`,
and `Appendix_Diameter` changes the predictive performance
of the classical machine learning models.

## Evaluation protocol

- Experiment 1 includes all three features.
- Experiment 2 excludes all three features.
- The same four learning algorithms were compared across experiments.
- Stratified 10-Fold Cross-Validation was used.
- Paired fold comparisons were examined.
- Recall was the primary metric.
- Average Precision was examined as a complementary metric.
- No statistical significance test was performed.

## Recall comparison

Difference = Experiment 1 - Experiment 2.

| Model | Experiment 1 | Experiment 2 | Difference |
|---|---:|---:|---:|
| Logistic Regression | 0.9027 | 0.8135 | +0.0892 |
| Decision Tree | 0.8973 | 0.7892 | +0.1081 |
| Random Forest | 0.9216 | 0.8270 | +0.0946 |
| Gradient Boosting | 0.9486 | 0.8135 | +0.1351 |

All four algorithms achieved higher mean Recall in Experiment 1.

## Average Precision comparison

| Model | Experiment 1 | Experiment 2 | Difference |
|---|---:|---:|---:|
| Logistic Regression | 0.9712 | 0.9178 | +0.0534 |
| Decision Tree | 0.8946 | 0.7369 | +0.1577 |
| Random Forest | 0.9792 | 0.9206 | +0.0586 |
| Gradient Boosting | 0.9916 | 0.9212 | +0.0703 |

All four algorithms achieved higher mean Average Precision
in Experiment 1.

## Paired fold comparison

### Recall

- Logistic Regression: Experiment 1 better in 9 folds, equal in 1.
- Decision Tree: Experiment 1 better in 8 folds, equal in 2.
- Random Forest: Experiment 1 better in all 10 folds.
- Gradient Boosting: Experiment 1 better in all 10 folds.

### Average Precision

Experiment 1 performed better in all 10 folds for each
of the four learning algorithms.

## H2 conclusion

**H2 is supported by descriptive evidence.**

Removing the three features was consistently associated with
lower Recall and Average Precision across all four learning
algorithms. Paired fold comparisons support the consistency
of this observed pattern.

No statistical significance test was performed. Therefore,
the conclusion is descriptive and does not establish statistical
significance.

The observed differences should not be interpreted as proof
that the three features alone caused the entire performance
difference. Potential overlap between these predictors and
the dataset's label-generation process must be considered.

---

# Provenance

- Official CV run: `10fold_official_20261118_083752`
- CV summary: `model_summary.csv`
- Fold-level results: `fold_results.csv`
- Paired comparison: `paired_fold_comparison_20261118.csv`
- CV folds: 10
- Test set was not used for hypothesis evaluation or model selection.
- No new model fitting or statistical testing was performed
  for this hypothesis evaluation.


---

# H3 — Differences in Feature Effects Across Algorithms

## Hypothesis

The effect of removing `Alvarado_Score`,
`Paedriatic_Appendicitis_Score`, and `Appendix_Diameter`
on predictive performance is not identical across algorithms.

## Evaluation protocol

- The same four learning algorithms were compared across both experiments.
- Differences were calculated as Experiment 1 minus Experiment 2.
- Mean Recall and Mean Average Precision were examined.
- Paired 10-fold results were reviewed for consistency.
- No statistical interaction test was performed.

## Recall differences

| Model | Experiment 1 - Experiment 2 |
|---|---:|
| Logistic Regression | +0.0892 |
| Decision Tree | +0.1081 |
| Random Forest | +0.0946 |
| Gradient Boosting | +0.1351 |

The largest observed Recall difference was for Gradient Boosting.

## Average Precision differences

| Model | Experiment 1 - Experiment 2 |
|---|---:|
| Logistic Regression | +0.0534 |
| Decision Tree | +0.1577 |
| Random Forest | +0.0586 |
| Gradient Boosting | +0.0703 |

The largest observed Average Precision difference was for Decision Tree.

## Paired fold consistency

- Recall: Experiment 1 was better in 9 folds for Logistic Regression,
  8 folds for Decision Tree, and all 10 folds for Random Forest
  and Gradient Boosting. Remaining folds were equal.
- Average Precision: Experiment 1 was better in all 10 folds
  for each of the four algorithms.

The magnitude of the observed differences varied across algorithms,
although the direction of the difference was consistently in favor
of Experiment 1.

## H3 conclusion

**H3 is supported by descriptive evidence.**

The observed effect associated with removing the three features
was not identical across algorithms. Gradient Boosting showed
the largest Recall difference, whereas Decision Tree showed
the largest Average Precision difference.

No statistical interaction test was performed. Therefore,
these results do not establish a statistically significant
interaction between algorithm choice and feature set.

The findings should be interpreted descriptively and do not
establish that the three features alone caused the observed
differences.

---

# Consolidated Hypothesis Conclusions

| Hypothesis | Conclusion |
|---|---|
| H1 — Differences between algorithms | Supported by descriptive evidence |
| H2 — Effect of removing three features | Supported by descriptive evidence |
| H3 — Differences in feature effects across algorithms | Supported by descriptive evidence |

All three hypotheses received descriptive support.
No inferential statistical significance claims are made.

## Overall methodological note

These conclusions are based on the official Stratified 10-Fold
Cross-Validation results and paired fold comparisons.
No additional model fitting, threshold tuning, or statistical
significance testing was performed for this hypothesis assessment.
