# Discussion and Limitations
## Classical Machine Learning for Pediatric Appendicitis Prediction

# 1. Discussion

## 1.1. Overview of the Main Findings

This study investigated the performance of classical machine
learning algorithms for predicting pediatric appendicitis using
tabular demographic, clinical, laboratory, and ultrasound-related
data. Five classification approaches were evaluated: Dummy
Classifier, Logistic Regression, Decision Tree, Random Forest,
and Gradient Boosting.

Two feature configurations were compared. Experiment 1 included
Alvarado Score, Pediatric Appendicitis Score (PAS), and Appendix
Diameter, whereas Experiment 2 excluded these three features.

The results demonstrated differences in predictive performance
across algorithms and feature configurations. Overall, the
models evaluated in Experiment 1 achieved better cross-validation
performance than their corresponding models in Experiment 2.
The findings also showed that the magnitude of this performance
difference varied across algorithms.

## 1.2. Comparison of Model Performance

In Experiment 1, Gradient Boosting achieved the strongest
cross-validation performance among the evaluated learning
algorithms. It obtained a mean Recall of 0.9486 (SD = 0.0431),
mean Precision of 0.9755, mean F1-score of 0.9613, and mean
Average Precision (AP) of 0.9916.

In Experiment 2, Random Forest achieved the highest mean Recall
among the learning algorithms, with a value of 0.8270
(SD = 0.0640). Its mean Precision, F1-score, and AP were
0.8392, 0.8318, and 0.9206, respectively.

These findings indicate that the best-performing algorithm
depended on the feature configuration. Gradient Boosting was
the strongest model in Experiment 1, whereas Random Forest
achieved the highest mean Recall in Experiment 2.

The Dummy Classifier was retained as a baseline rather than
treated as a competing learning algorithm. Its high Recall
resulted from predicting the positive class for all observations
at the selected threshold. Its performance therefore illustrates
why Recall should not be interpreted in isolation.

## 1.3. Effect of the Three Additional Features

The comparison between the two experiments showed that removing
Alvarado Score, Pediatric Appendicitis Score, and Appendix
Diameter was associated with lower mean Recall and Average
Precision across all four learning algorithms.

The paired cross-validation comparisons showed positive
Experiment 1 minus Experiment 2 differences for both metrics
across the evaluated algorithms. For Recall, the mean differences
ranged from 0.0892 for Logistic Regression to 0.1351 for
Gradient Boosting. For AP, the differences ranged from 0.0534
for Logistic Regression to 0.1577 for Decision Tree.

These findings suggest that the three features, considered
together, provide useful predictive information to the evaluated
models. Their inclusion may help the algorithms distinguish
between patients with and without appendicitis.

However, the experimental design removed all three features
simultaneously. Consequently, the independent contribution
of each feature cannot be established from this comparison.

## 1.4. Differences in the Effect Across Algorithms

The magnitude of the performance reduction was not identical
across algorithms. Gradient Boosting showed the largest mean
Recall difference, whereas Decision Tree showed the largest
mean AP difference.

This variation suggests that different algorithms may benefit
from the additional information to different extents. However,
the current analysis is descriptive and does not establish
a statistically significant interaction between algorithm
choice and feature configuration.

## 1.5. Final Test Set Evaluation

After model selection using training-only cross-validation,
the selected pipelines were fitted on the complete training
set and evaluated once on the held-out test set.

The Experiment 1 Gradient Boosting model achieved:

- Accuracy: 0.9551
- Precision: 0.9778
- Recall: 0.9462
- F1-score: 0.9617
- Balanced Accuracy: 0.9572
- ROC-AUC: 0.9694
- Average Precision: 0.9840

Its confusion matrix contained 61 true negatives, 2 false
positives, 5 false negatives, and 88 true positives.

The Experiment 2 Random Forest model achieved:

- Accuracy: 0.8590
- Precision: 0.8817
- Recall: 0.8817
- F1-score: 0.8817
- Balanced Accuracy: 0.8536
- ROC-AUC: 0.8980
- Average Precision: 0.9392

Its confusion matrix contained 52 true negatives, 11 false
positives, 11 false negatives, and 82 true positives.

The Experiment 1 selected model achieved higher values across
the reported test metrics. Nevertheless, the selected models
were different algorithms: Gradient Boosting in Experiment 1
and Random Forest in Experiment 2. Therefore, this test-set
comparison evaluates the two selected pipelines and cannot
isolate the effect of the three features alone.

The paired comparisons between identical algorithms in
cross-validation provide the more appropriate evidence for
examining the effect associated with the feature configuration.

## 1.6. Overall Interpretation

Taken together, the findings indicate that classical machine
learning algorithms can achieve promising predictive performance
on this pediatric appendicitis dataset. The results also suggest
that including the three additional clinical and ultrasound-related
features is associated with improved predictive performance.

Gradient Boosting provided the strongest overall results in
Experiment 1, while Random Forest was the strongest model in
Experiment 2 according to the primary Recall criterion.

These findings should be interpreted as an evaluation of
predictive performance on the available dataset. They do not
establish clinical effectiveness or demonstrate that the models
can replace clinical assessment.

# 2. Limitations

Several limitations should be considered when interpreting
the findings of this study.

## 2.1. Dataset Size

The study used 780 observations with valid target labels,
including 624 training observations and 156 test observations.
Although this dataset allowed a structured comparison of
multiple algorithms, its size remains limited for establishing
broad generalizability. Performance estimates may vary when
the models are evaluated on substantially larger populations.

## 2.2. Missing Data

Several clinical and ultrasound-related variables contained
missing values. Missing values were handled through
preprocessing pipelines using training-fold imputation and
missingness indicators where appropriate.

Although this approach allowed the models to use the available
information without discarding large numbers of observations,
imputation cannot fully recover information that was not
recorded. Missingness may also reflect differences in clinical
data collection and examination practices.

## 2.3. Retrospective Dataset

The analysis was based on an existing retrospective dataset
rather than a prospectively designed data collection process.
Consequently, the available variables and their completeness
were determined by the original data collection procedures.

The findings should therefore be interpreted within the
context of this dataset and its data collection setting.

## 2.4. Lack of External Validation

The models were evaluated using a held-out test subset from
the same dataset. No external validation was performed using
an independent hospital, institution, or patient population.

Therefore, the ability of the selected models to generalize
to other clinical settings remains unknown.

## 2.5. Feature Ablation Design

The three additional features were removed simultaneously
in Experiment 2. This design allowed an evaluation of their
combined contribution but did not identify the independent
effect of each feature.

Further experiments would be required to estimate the
individual contribution of each feature. Such experiments
were outside the scope of the current study.

## 2.6. Model and Evaluation Scope

The study focused on five classical classification approaches
and used a fixed classification threshold of 0.5. Threshold
optimization, probability calibration, and broader model
optimization were not part of the experimental protocol.

The reported results therefore describe performance under
the selected algorithms, preprocessing procedures, and
evaluation settings rather than the maximum achievable
performance of every possible model configuration.

## 2.7. Clinical Applicability

The study evaluated predictive performance using retrospective
tabular data. It did not assess clinical workflow integration,
prospective clinical outcomes, or the impact of model-assisted
decisions on patient care.

Accordingly, the models should not be considered substitutes
for clinical judgment or established diagnostic procedures.
Further validation would be necessary before considering
any clinical application.

# 3. Conclusion

This study compared classical machine learning algorithms
for pediatric appendicitis prediction under two feature
configurations. The results showed that Gradient Boosting
achieved the strongest cross-validation and test performance
in Experiment 1, while Random Forest achieved the highest
mean Recall in Experiment 2.

The inclusion of Alvarado Score, Pediatric Appendicitis Score,
and Appendix Diameter was associated with improved Recall
and Average Precision across the evaluated learning algorithms.
However, their individual contributions could not be separated
because they were removed as a group.

Despite the promising results, the limited dataset size,
missing values, retrospective nature of the data, and absence
of external validation restrict the generalizability of the
findings. Further evaluation on independent patient populations
is necessary before considering clinical application.

# 4. Reporting Notes

- Positive class: appendicitis.
- Primary metric for model selection: Recall.
- Cross-validation: Stratified 10-Fold Cross-Validation.
- Classification threshold: 0.5.
- Average Precision (AP) and trapezoidal PR-AUC are distinct
  evaluation metrics and are reported separately.
- Model selection was based on training-only cross-validation.
- The held-out test set was used for final evaluation only.
- No additional model fitting or statistical testing was
  performed for this report.

## Provenance

- Official CV run: `10fold_official_20261118_083752`
- Final training run: `final_models_20261118_091523`
- Final test evaluation: `final_test_evaluation_20261118_091752`
- Hypothesis evaluation:
  `HYPOTHESES_H1_H2_H3_EVALUATION_20261118.md`
- Feature interpretation:
  `FEATURE_EFFECT_INTERPRETATION_20261118.md`
