# Feature Extraction & Selection

Implementasi teknik ekstraksi fitur (PCA) dan seleksi fitur (ANOVA) pada dataset Diabetes dan Performance.

## 📋 Deskripsi

### Ekstraksi Fitur — PCA (Principal Component Analysis)
- Reduksi dimensi menggunakan PCA dengan threshold 95% explained variance
- Menghasilkan scree plot dan visualisasi PCA 2D
- Diterapkan pada dataset Diabetes

### Seleksi Fitur — ANOVA (Analysis of Variance)
- Seleksi fitur statistik untuk klasifikasi (target kategorikal)
- Mengidentifikasi fitur signifikan berdasarkan p-value < 0.05
- Diterapkan pada dataset Diabetes dan Performance

## 📁 Dataset

| Dataset | File | Deskripsi |
|---------|------|-----------|
| Diabetes | `Diabetes.csv` | Dataset diabetes untuk klasifikasi |
| Performance | `performance.csv` | Dataset performa akademik |

## 🚀 Cara Menjalankan

```bash
pip install pandas numpy matplotlib scikit-learn scipy
python "Ekstraksi Fitur/ekstraksi_fitur_diabetes.py"
python "Seleksi Fitur/seleksi_fitur_diabetes.py"
```

## 📂 Struktur File

```
Feature Extraction & Selection/
├── Diabetes.csv
├── performance.csv
├── Ekstraksi Fitur/
│   ├── ekstraksi_fitur_diabetes.py
│   ├── hasil_pca_diabetes.csv
│   ├── pca_plot_diabetes.png
│   ├── pca_plot_performance.png
│   ├── scree_plot_diabetes.png
│   └── scree_plot_performance.png
└── Seleksi Fitur/
    ├── seleksi_fitur_diabetes.py
    ├── seleksi_fitur_performance.py
    ├── hasil_seleksi_fitur_diabetes.csv
    └── hasil_seleksi_fitur_performance.csv
```
