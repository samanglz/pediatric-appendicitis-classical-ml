<!-- Curated public-release copy. Original internal record preserved. -->

# Decision: Final Assessment of High-Missingness Features

**Decision ID:** EXP-FEATURE-MISSING-001  
**Status:** Accepted  
**Scope:** 17 features with more than 70% missing values in the training dataset  
**Dataset:** Regensburg Pediatric Appendicitis Dataset  
**Decision stage:** Exploratory Data Analysis (EDA) and feature assessment

## 1. Background

Seventeen features were identified as having more than 70% missing values in the training dataset.

Rather than automatically excluding these features based on their missingness percentages, their observed values were examined separately for the Appendicitis and No Appendicitis classes.

The assessment considered:

- The number of observed values in each diagnosis class.
- The representation of both classes.
- The distribution and diversity of observed categories.
- The feasibility of using each feature in the planned machine learning pipeline.
- Potential information value despite substantial missingness.

## 2. Accepted Decision: Excluded Features

The following ten features are excluded from the model input feature set:

| Feature | Reason for exclusion |
|---|---|
| `Abscess_Location` | Only 8 observed values in the Appendicitis class and none in the No Appendicitis class. There is insufficient representation for a meaningful comparison. |
| `Gynecological_Findings` | Only 20 observed values in the Appendicitis class and 1 in the No Appendicitis class. The feature also contains diverse free-text categories that would require substantial normalization. |
| `Lymph_Nodes_Location` | Contains numerous textual location categories and variations, making consistent representation difficult. Its usefulness as a predictor is unclear in the current dataset. |
| `Appendicolith` | Only 52 observed values in the Appendicitis class and 1 in the No Appendicitis class, providing inadequate representation of both classes. |
| `Appendicular_Abscess` | Only 59 observed values in the Appendicitis class and 8 in the No Appendicitis class. Class representation is highly limited. |
| `Conglomerate_of_Bowel_Loops` | Only 30 observed values in the Appendicitis class and 5 in the No Appendicitis class. |
| `Ileus` | Only 40 observed values in the Appendicitis class and 6 in the No Appendicitis class. |
| `Perforation` | Only 62 observed values in the Appendicitis class and 5 in the No Appendicitis class. |
| `Perfusion` | Only 48 observed values in the Appendicitis class and 1 in the No Appendicitis class. |
| `Segmented_Neutrophils` | Only 26 observed numeric values in the Appendicitis class and 15 in the No Appendicitis class. The available observations are insufficient for reliable use in the planned modelling process. |

### Rationale

These features were excluded because their observed data were too sparse, one or both diagnosis classes were inadequately represented, or their current representation would require disproportionate data preparation relative to the available information.

The decision is not based solely on missingness percentage. It also considers the reliability of class comparisons and the practical feasibility of using the features in the current modelling workflow.

## 3. Accepted Decision: Retained Features

The following seven features will remain eligible as candidate model inputs:

| Feature | Reason for retention |
|---|---|
| `Appendix_Wall_Layers` | Shows potentially informative differences in observed category distributions between the diagnosis classes. |
| `Target_Sign` | Observed category distributions suggest potentially useful differences between the classes. |
| `Bowel_Wall_Thickening` | Both classes have observed values, with potentially informative differences in category distributions. |
| `Pathological_Lymph_Nodes` | Has a comparatively better number of observations in both classes and representation of both Yes and No categories. |
| `Meteorism` | Has a reasonable number of observed values in both classes and remains eligible for model-based evaluation. |
| `Enteritis` | Observed category distributions differ between the classes, making the feature potentially informative despite substantial missingness. |
| `Coprostasis` | Observed values suggest a possible difference between classes, although the distribution requires cautious interpretation. |

### Rationale

These features were retained because their observed values provide potentially useful information and their class representation is more adequate for further evaluation.

Retention does not establish that these features are statistically significant or improve predictive performance. Their actual contribution must be assessed during model development and validation.

## 4. Missing-Value Handling Policy

The following rules apply to the retained features:

1. A missing value must not automatically be interpreted as a negative clinical finding.
2. Missing values must remain distinguishable from observed Yes/No values.
3. Missing-value imputation, if required, must be performed within the machine learning preprocessing pipeline.
4. Imputation parameters must be learned exclusively from the training portion of each validation fold.
5. The test set must not be used to determine imputation values or preprocessing decisions.

## 5. Scope and Limitations

This decision applies only to the 17 features assessed for high missingness.

It does not constitute the final selection of all model predictors. Other candidate features remain subject to the previously accepted project decisions and subsequent data-quality and preprocessing assessments.

The observed category distributions are descriptive findings. They do not independently establish predictive value, statistical significance, or causal relationships.

## 6. Final Decision Summary

- **Excluded:** 10 features.
- **Retained for further evaluation:** 7 features.
- **Automatic exclusion based solely on missingness:** Not adopted.
- **Missing values interpreted as negative findings:** Not permitted.
- **Final predictive usefulness:** To be assessed during model development and validation.

**Final status: ACCEPTED**