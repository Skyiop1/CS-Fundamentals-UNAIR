# Clustering & Customer Segmentation

Customer market segmentation analysis using K-Means and K-Modes clustering algorithms.

## 📋 Description

This project implements two clustering approaches:
- **K-Means Clustering** — applied to numerical dimensions (Mall Customers dataset).
- **K-Modes Clustering** — applied to categorical and mixed dimensions (Credit Card dataset).

Key analytical steps:
- Defining the optimal number of clusters (Elbow Method, Silhouette Score).
- Cluster distributions visualization.
- Market profiling and characteristics mapping.

## 📁 Datasets

| Dataset | File | Description |
|---------|------|-----------|
| Mall Customers | `Mall_Customers.csv` | Numerical shopper parameters (200 records). |
| Credit Card | `CC GENERAL.csv` | Mixed credit card customer parameters (8,950 records). |

## 🚀 Getting Started

To launch the notebooks:
```bash
pip install pandas numpy matplotlib seaborn scikit-learn kmodes
jupyter notebook TM10_Clustering_KModes.ipynb
```

## 📂 Directory Structure

```
Clustering & Customer Segmentation/
├── TM10_Clustering_KModes.ipynb            # Main K-Modes notebook
├── TM10_KModes_Clustering.ipynb            # Alternative clustering notebook
├── Mall_Customers.csv                       # Customer dataset
├── CC GENERAL.csv                           # Credit Card dataset
├── CC_GENERAL_KModes_Result.csv             # Clustering output records
└── report-customer-segmentation.pdf         # Final project report
```
