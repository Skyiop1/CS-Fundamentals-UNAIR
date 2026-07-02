# Imbalanced Data Handling

Implementasi teknik penanganan data tidak seimbang (imbalanced data) menggunakan metode resampling.

## 📋 Deskripsi

Tugas ini mendemonstrasikan dua pendekatan resampling untuk menangani class imbalance:
- **Random Oversampling (ROS)** — menduplikasi sampel dari kelas minoritas
- **Random Undersampling (RUS)** — mengurangi sampel dari kelas mayoritas

Diterapkan pada dataset Wine Quality untuk klasifikasi kualitas wine.

## 📁 Dataset

| Dataset | File | Deskripsi |
|---------|------|-----------|
| Wine Quality | `WineQT.csv` | Dataset kualitas wine merah |

## 🚀 Cara Menjalankan

```bash
pip install pandas scikit-learn imbalanced-learn
python random_oversampling.py
python random_undersampling.py
```

## 📂 Struktur File

```
Imbalanced Data Handling/
├── random_oversampling.py          # Script Random Oversampling
├── random_undersampling.py         # Script Random Undersampling
├── DATASERWINE.ipynb               # Notebook eksplorasi data
├── WineQT.csv                      # Dataset wine quality
└── report-imbalanced-data.pdf      # Laporan tugas
```
