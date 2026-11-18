<!-- Curated public-release copy. Original internal record preserved. -->

### Decision: Using a Consistent Classification Threshold Across All Models

**Decision ID:** EXP-TH-001

**Status:** Accepted

**Decision:**

All classification models in both experiments will be evaluated using the same fixed decision threshold of `0.5`.

For the positive class (`Appendicitis`), a predicted probability greater than or equal to `0.5` will be classified as `Appendicitis`. Otherwise, the prediction will be classified as `No Appendicitis`.

**Rationale:**

1. Ensuring consistent evaluation conditions across all models.
2. Avoiding unnecessary experimental complexity.
3. Simplifying result analysis and interpretation.
4. Maintaining the project's focus on comparing classification algorithms and investigating the impact of selected features.

**Evaluation Metrics:**

- **Primary metric:** Recall for the `Appendicitis` class.
- **Secondary metrics:** Precision, F1-score, Accuracy, Balanced Accuracy, ROC-AUC, PR-AUC, and Confusion Matrix.

**Methodological Constraints:**

No model-specific threshold optimization or threshold tuning will be performed. The test set will remain untouched during model development and will be used exclusively for final evaluation.

**Scope:**

This decision applies to both experiments:

- **Experiment 1:** Models trained using the three selected features: `Alvarado_Score`, `Paedriatic_Appendicitis_Score`, and `Appendix_Diameter`.
- **Experiment 2:** Models trained without these three features.