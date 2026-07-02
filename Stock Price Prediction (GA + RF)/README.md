# Stock Price Direction Prediction — GA + Random Forest

Prediksi arah harga saham BBCA (Bank Central Asia) menggunakan **Genetic Algorithm** untuk seleksi fitur optimal dan **Random Forest** sebagai model klasifikasi, dilengkapi threshold tuning untuk optimasi keputusan.

## 📋 Deskripsi

Project ini merupakan implementasi lengkap pipeline machine learning untuk prediksi arah pergerakan harga saham, dengan fitur:

### 🧬 Genetic Algorithm (Feature Selection)
- Seleksi fitur optimal dari indikator teknikal
- Multi-seed evaluation untuk konsistensi
- Ablation study untuk validasi kontribusi fitur

### 🌲 Random Forest (Classification)
- Prediksi arah harga (naik/turun) dengan threshold 0.5%
- Hyperparameter tuning via RandomizedSearchCV
- Time Series cross-validation

### 📊 Comprehensive Evaluation
- Multi-split scenario (80/20, 75/25, 70/30)
- ROC-AUC, F1-Score, Balanced Accuracy
- Confusion matrix comparison
- Threshold tuning untuk optimasi precision/recall trade-off

### 📈 Visualisasi
- Price history & recent estimation charts
- GA fitness evolution
- Model comparison & split scenario analysis
- Feature importance & selection frequency

## 🚀 Cara Menjalankan

```bash
pip install yfinance pandas numpy scikit-learn matplotlib
python main.py
```

> ⚠️ Script membutuhkan koneksi internet untuk mengambil data saham via Yahoo Finance API.

## 📂 Struktur File

```
Stock Price Prediction (GA + RF)/
├── main.py                    # Script utama (pipeline lengkap)
├── DOCUMENTATION.md           # Dokumentasi progress & parameter tuning
├── experiment_log.md          # Log output terminal eksperimen
└── output/
    ├── charts/                # Semua visualisasi (.png)
    │   ├── bbca_price_history_chart.png
    │   ├── confusion_matrix_comparison.png
    │   ├── ga_fitness_chart.png
    │   ├── roc_curve_chart.png
    │   └── ...
    └── data/                  # Semua hasil eksperimen (.csv)
        ├── experiment_results.csv
        ├── ga_fitness_history.csv
        ├── split_scenario_results.csv
        └── ...
```

## 🛠️ Tech Stack

- **Data Source**: Yahoo Finance (`yfinance`)
- **ML**: scikit-learn (RandomForest, SVM, DummyClassifier)
- **Optimization**: Custom Genetic Algorithm
- **Visualization**: matplotlib
