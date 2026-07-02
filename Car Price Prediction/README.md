# Car Price Prediction

Predicting used car pricing using ensemble machine learning models (XGBoost & LightGBM) coupled with an interactive Streamlit dashboard.

## 📋 Description

This project implements used car price estimation algorithms employing:
- **XGBoost Regressor** — extreme gradient boosting optimized for regression.
- **LightGBM Regressor** — a highly efficient, tree-based gradient boosting framework.
- **Streamlit Dashboard** — user interface for data exploration and prediction.

Key metrics and displays:
- Price distribution and categorical features analysis.
- Feature correlation heatmaps.
- Model performance evaluations (MAE, RMSE, R²).
- Feature importance ranking.
- Actual vs. Predicted values plots and Residual diagnostics.

## 📁 Datasets

| Dataset | File | Description |
|---------|------|-----------|
| Car Details v3 | `Car details v3.csv` | Dataset containing information on 8,128 used cars. |

## 🚀 Getting Started

```bash
pip install streamlit pandas numpy matplotlib seaborn scikit-learn xgboost lightgbm
streamlit run streamlit_app.py
```

## 📂 Directory Structure

```
Car Price Prediction/
├── streamlit_app.py                # Streamlit app script
├── car_price_prediction.ipynb      # Analytical notebook
├── Car details v3.csv              # Car specifications dataset
├── model_metadata.json             # JSON file containing hyperparameters
├── report-car-price-prediction.pdf # Final project report
├── actual_vs_predicted.png         # Regression plot
├── correlation_heatmap.png         # Correlation plot
├── distribusi_harga.png            # Distribution plot
├── distribusi_kategorik.png        # Categorical plot
├── evaluasi_model.png              # Comparison bar plot
├── feature_importance.png          # Importance chart
└── residual_plot.png               # Residual chart
```
