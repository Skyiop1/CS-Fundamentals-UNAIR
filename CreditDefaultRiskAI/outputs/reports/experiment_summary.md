# Experiment Summary - Credit Default Risk AI

## Dataset
- Total data: 29965
- Feature count: 23
- Missing value: 0
- Non-default distribution: 23335 (77.87%)
- Default distribution: 6630 (22.13%)

## Best Model
- Best model: Hybrid PCA-DNN
- Split scenario: 70/30
- Accuracy: 0.7874
- Precision: 0.5186
- Recall: 0.5455
- F1-score: 0.5317
- ROC-AUC: 0.7703

## Methodology Notes
SMOTE is applied only to the training data after train-test splitting and scaling.
PCA is used as a feature extraction stage for the Hybrid PCA-DNN pipeline, not as the primary deep learning model.
