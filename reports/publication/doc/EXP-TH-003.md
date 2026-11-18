<!-- Curated public-release copy. Original internal record preserved. -->

# Decision: Comprehensive Use of Available Dataset Features

**Decision ID:** EXP-FEATURE-001

**Status:** Accepted

## Decision

All usable information available in the `All cases` sheet of the Regensburg Pediatric Appendicitis dataset will be considered as candidate input features for the machine-learning experiments.

The candidate feature scope includes:

- Demographic and anthropometric information.
- Clinical symptoms and examination findings.
- Blood and urine laboratory results.
- Ultrasound-related variables and findings.
- The three selected clinical variables: `Alvarado_Score`, `Paedriatic_Appendicitis_Score`, and `Appendix_Diameter`.

Features will not be excluded solely because they contain missing values. Their suitability will be assessed before finalizing the predictor set.

## Constraints

This decision does not authorize the use of:

- The target variable `Diagnosis` as an input feature.
- Identifier fields such as `US_Number`.
- Variables that directly encode the diagnosis or introduce substantial target leakage.
- Downstream or post-outcome information that would not be appropriate for the intended prediction setting.

Previously agreed exclusions remain in effect:

- `Diagnosis_Presumptive`
- `Management`
- `Severity`
- `Length_of_Stay`
- `US_Performed`
- `Appendix_on_US`
- `US_Number`

## Missing-Value Considerations

Features with substantial missingness will first be reviewed for:

1. Clinical relevance.
2. Amount and pattern of missing data.
3. Whether missingness reflects the clinical workflow.
4. Whether a defensible preprocessing strategy is available.

No feature will be automatically discarded based only on its missing-value percentage.

## Scope

This decision applies to both experiments.

- **Experiment 1:** Includes the three selected clinical variables.
- **Experiment 2:** Excludes only those three variables from the otherwise eligible feature set.

The final predictor list will be established after the feature audit and before preprocessing and model training.

## Rationale

The project aims to investigate the predictive value of the broad range of demographic, clinical, laboratory, and ultrasound-derived information available in the dataset, rather than restricting the analysis to a small predefined group of variables.

This approach also allows the project to assess the contribution of different types of clinical information while maintaining the previously established leakage-prevention constraints.