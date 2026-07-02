# Data Normalization

Implementasi teknik normalisasi data menggunakan tiga metode berbeda pada dua dataset.

## 📋 Deskripsi

Tugas ini mendemonstrasikan penerapan preprocessing data berupa normalisasi menggunakan:
- **Min-Max Scaling** — mentransformasi data ke rentang [0, 1]
- **Standard Scaling (Z-Score)** — mentransformasi data agar mean = 0 dan std = 1
- **Robust Scaling** — normalisasi berbasis median & IQR, tahan terhadap outlier

## 📁 Dataset

| Dataset | File | Deskripsi |
|---------|------|-----------|
| Lung Cancer Prediction | `Lung Cancer Prediction.csv` | Dataset prediksi kanker paru-paru |
| Shopping Mall Customers | `Shopping.csv` | Data pelanggan mall untuk segmentasi |

## 🚀 Cara Menjalankan

```bash
pip install pandas scikit-learn
python TugasTM2.py
```

## 📂 Struktur File

```
Data Normalization/
├── TugasTM2.py                  # Script utama normalisasi
├── Lung Cancer Prediction.csv   # Dataset kanker paru
└── Shopping.csv                 # Dataset pelanggan mall
```
