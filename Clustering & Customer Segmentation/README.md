# Clustering & Customer Segmentation

Analisis segmentasi pelanggan menggunakan algoritma K-Means dan K-Modes clustering.

## 📋 Deskripsi

Project ini mengimplementasikan dua algoritma clustering:
- **K-Means Clustering** — untuk data numerik (Mall Customers dataset)
- **K-Modes Clustering** — untuk data campuran numerik & kategorikal (Credit Card dataset)

Analisis mencakup:
- Penentuan jumlah cluster optimal (Elbow Method, Silhouette Score)
- Visualisasi cluster
- Profiling dan interpretasi segmen pelanggan

## 📁 Dataset

| Dataset | File | Deskripsi |
|---------|------|-----------|
| Mall Customers | `Mall_Customers.csv` | Data pelanggan mall (200 sampel) |
| Credit Card | `CC GENERAL.csv` | Data penggunaan kartu kredit (8950 sampel) |

## 🚀 Cara Menjalankan

Buka notebook di Jupyter:
```bash
pip install pandas numpy matplotlib seaborn scikit-learn kmodes
jupyter notebook TM10_Clustering_KModes.ipynb
```

## 📂 Struktur File

```
Clustering & Customer Segmentation/
├── TM10_Clustering_KModes.ipynb            # Notebook K-Modes utama
├── TM10_KModes_Clustering.ipynb            # Notebook K-Modes alternatif
├── Mall_Customers.csv                       # Dataset Mall
├── CC GENERAL.csv                           # Dataset Credit Card
├── CC_GENERAL_KModes_Result.csv             # Hasil clustering
└── report-customer-segmentation.pdf         # Laporan akhir
```
