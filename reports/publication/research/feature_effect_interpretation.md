# Interpretation of the Effect of Three Clinical Features
## Classical ML for Pediatric Appendicitis Prediction

## 1. Main Finding

The results showed that including the following three features
was associated with better predictive performance:

- `Alvarado_Score`
- `Paedriatic_Appendicitis_Score`
- `Appendix_Diameter`

This pattern was observed across all four evaluated learning
algorithms. Removing these features resulted in lower mean Recall
and Average Precision for every algorithm.

Overall, these features provided useful predictive information
to the evaluated models.

## 2. Interpretation of the Performance Reduction

Alvarado Score and Pediatric Appendicitis Score summarize
information related to clinical signs and findings.

Appendix Diameter provides additional information derived
from ultrasound assessment.

By including these features, models receive additional clinical
and ultrasound-related information alongside the other available
demographic, clinical, laboratory, and ultrasound predictors.

Removing them reduces the information available to the models,
which may explain the observed reduction in predictive performance.

## 3. Independent Contribution of Each Feature

The three features were removed simultaneously in Experiment 2.
Therefore, the current experimental design does not allow us
to determine the independent contribution of each feature.

It is not possible to conclude from these experiments that
Alvarado Score, Pediatric Appendicitis Score, or Appendix
Diameter individually contributes more than the others.

## 4. Differences Across Algorithms

The magnitude of the observed performance reduction varied
across algorithms:

- Gradient Boosting showed the largest Recall reduction.
- Decision Tree showed the largest Average Precision reduction.
- Logistic Regression and Random Forest showed smaller
  Average Precision reductions.

These descriptive differences suggest that learning algorithms
may benefit from the additional information to different extents.

However, the current results do not establish a specific internal
mechanism explaining these differences.

## 5. Research Interpretation — Final Draft

The comparative results indicate that including Alvarado Score,
Pediatric Appendicitis Score, and Appendix Diameter was associated
with improved predictive performance across all four evaluated
learning algorithms. These features provide additional clinical
and ultrasound-related information that may help models
distinguish between patients with and without appendicitis.
Their removal resulted in consistent reductions in mean Recall
and Average Precision across the evaluated algorithms. However,
since the three features were removed simultaneously, the
independent contribution of each feature cannot be determined
from the current experimental design. Furthermore, the magnitude
of performance reduction varied across algorithms, suggesting
that different learning algorithms may benefit from the additional
information to different extents.

## 6. Scope and Interpretation Notes

- The findings describe associations observed in the experiments.
- The results do not establish the independent importance
  of each of the three features.
- No additional experiments or model fitting were performed
  for this interpretation.
- No causal claims are made.
- The interpretation is based on the official 10-Fold
  Cross-Validation results.

## Provenance

- Experiment 1: Three additional features included.
- Experiment 2: Three additional features excluded.
- Cross-validation: Stratified 10-Fold.
- Official CV run: `10fold_official_20261118_083752`
- Related hypothesis record:
  `HYPOTHESES_H1_H2_H3_EVALUATION_20261118.md`
