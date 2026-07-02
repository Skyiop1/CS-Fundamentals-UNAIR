# Data Normalization

Implementation of data normalization techniques using three different scaling methods on two datasets.

## 📋 Description

This coursework demonstrates the application of preprocessing normalization techniques:
- **Min-Max Scaling** — transforms data into the [0, 1] range.
- **Standard Scaling (Z-Score)** — scales data so that mean = 0 and std = 1.
- **Robust Scaling** — scales data based on median & IQR, making it robust to outliers.

## 📁 Datasets

| Dataset | File | Description |
|---------|------|-----------|
| Lung Cancer Prediction | `Lung Cancer Prediction.csv` | Dataset for lung cancer prediction. |
| Shopping Mall Customers | `Shopping.csv` | Customer data from shopping malls. |

## 🚀 Getting Started

```bash
pip install pandas scikit-learn
python TugasTM2.py
```

## 📂 Directory Structure

```
Data Normalization/
├── TugasTM2.py                  # Main scaling script
├── Lung Cancer Prediction.csv   # Lung cancer dataset
└── Shopping.csv                 # Customer dataset
```
