# Car Price Prediction

Prediksi harga mobil bekas menggunakan ensemble machine learning models (XGBoost & LightGBM) dengan Streamlit dashboard.

## 📋 Deskripsi

Project ini membangun model prediksi harga mobil bekas menggunakan:
- **XGBoost Regressor** — gradient boosting untuk regresi
- **LightGBM Regressor** — gradient boosting yang lebih efisien
- **Streamlit Dashboard** — interface interaktif untuk eksplorasi dan prediksi

Fitur utama:
- Analisis distribusi harga dan fitur kategorik
- Correlation heatmap
- Perbandingan evaluasi model (MAE, RMSE, R²)
- Feature importance analysis
- Actual vs Predicted plot & Residual plot

## 📁 Dataset

| Dataset | File | Deskripsi |
|---------|------|-----------|
| Car Details v3 | `Car details v3.csv` | Dataset mobil bekas (8128 sampel) |

## 🚀 Cara Menjalankan

```bash
pip install streamlit pandas numpy matplotlib seaborn scikit-learn xgboost lightgbm
streamlit run streamlit_app.py
```

## 📂 Struktur File

```
Car Price Prediction/
├── streamlit_app.py                # Streamlit web app
├── car_price_prediction.ipynb      # Jupyter notebook analisis
├── Car details v3.csv              # Dataset
├── model_metadata.json             # Metadata model
├── report-car-price-prediction.pdf # Laporan tugas
├── actual_vs_predicted.png         # Visualisasi prediksi
├── correlation_heatmap.png         # Heatmap korelasi
├── distribusi_harga.png            # Distribusi harga
├── distribusi_kategorik.png        # Distribusi fitur kategorik
├── evaluasi_model.png              # Perbandingan model
├── feature_importance.png          # Feature importance
└── residual_plot.png               # Residual plot
```
