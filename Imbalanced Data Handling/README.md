# Imbalanced Data Handling

Implementation of data resampling techniques to handle class imbalance issues in datasets.

## 📋 Description

This coursework demonstrates two primary resampling approaches to address class imbalance:
- **Random Oversampling (ROS)** — duplicates samples from the minority class to balance distributions.
- **Random Undersampling (RUS)** — reduces samples from the majority class to prevent model bias.

Evaluated on the Wine Quality dataset for binary classification tasks.

## 📁 Datasets

| Dataset | File | Description |
|---------|------|-----------|
| Wine Quality | `WineQT.csv` | Red wine chemical composition and quality records. |

## 🚀 Getting Started

```bash
pip install pandas scikit-learn imbalanced-learn
python random_oversampling.py
python random_undersampling.py
```

## 📂 Directory Structure

```
Imbalanced Data Handling/
├── random_oversampling.py          # ROS implementation script
├── random_undersampling.py         # RUS implementation script
├── DATASERWINE.ipynb               # Data exploration notebook
├── WineQT.csv                      # Wine quality dataset
└── report-imbalanced-data.pdf      # Coursework report
```
