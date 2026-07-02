# Feature Extraction & Selection

Implementation of feature extraction (PCA) and feature selection (ANOVA) techniques on Diabetes and Performance datasets.

## 📋 Description

### Feature Extraction — PCA (Principal Component Analysis)
- Dimensions reduction using PCA with a 95% explained variance threshold.
- Generates scree plots and 2D PCA visualization projections.
- Evaluated on the Diabetes dataset.

### Feature Selection — ANOVA (Analysis of Variance)
- Statistical feature selection for classification (categorical target).
- Identifies statistically significant features based on a p-value < 0.05.
- Evaluated on both Diabetes and Performance datasets.

## 📁 Datasets

| Dataset | File | Description |
|---------|------|-----------|
| Diabetes | `Diabetes.csv` | Diabetes patient records for classification. |
| Performance | `performance.csv` | Student academic performance records. |

## 🚀 Getting Started

```bash
pip install pandas numpy matplotlib scikit-learn scipy
python "Ekstraksi Fitur/ekstraksi_fitur_diabetes.py"
python "Seleksi Fitur/seleksi_fitur_diabetes.py"
```

## 📂 Directory Structure

```
Feature Extraction & Selection/
├── Diabetes.csv
├── performance.csv
├── Ekstraksi Fitur/
│   ├── ekstraksi_fitur_diabetes.py     # PCA script
│   ├── hasil_pca_diabetes.csv
│   ├── pca_plot_diabetes.png
│   ├── pca_plot_performance.png
│   ├── scree_plot_diabetes.png
│   └── scree_plot_performance.png
└── Seleksi Fitur/
    ├── seleksi_fitur_diabetes.py       # ANOVA script for Diabetes
    ├── seleksi_fitur_performance.py    # ANOVA script for Performance
    ├── hasil_seleksi_fitur_diabetes.csv
    └── hasil_seleksi_fitur_performance.csv
```
