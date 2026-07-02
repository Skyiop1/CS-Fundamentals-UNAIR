# Wine Quality Classification

Aplikasi web interaktif untuk prediksi kualitas wine menggunakan Decision Tree Classifier dengan Streamlit.

## 📋 Deskripsi

Aplikasi ini menyediakan:
- **Eksplorasi Data** — overview dataset, distribusi kelas, dan correlation heatmap interaktif (Plotly)
- **Evaluasi Model** — accuracy, confusion matrix, classification report, dan visualisasi Decision Tree
- **Prediksi Real-time** — form interaktif untuk memprediksi kualitas wine berdasarkan komposisi kimiawi

Kualitas wine diklasifikasikan menjadi:
- **Bad** (quality score 3, 4, 5)
- **Good** (quality score 6, 7, 8)

## 📁 Dataset

| Dataset | File | Deskripsi |
|---------|------|-----------|
| Wine Quality | `WineQT.csv` | Dataset kualitas wine merah (1143 sampel, 11 fitur) |

## 🚀 Cara Menjalankan

```bash
pip install streamlit pandas numpy matplotlib seaborn plotly scikit-learn
streamlit run app.py
```

## 📂 Struktur File

```
Wine Quality Classification/
├── app.py                          # Streamlit web app
├── WineQT.csv                      # Dataset wine quality
└── report-wine-quality.pdf         # Laporan tugas
```

## 🖥️ Screenshot

Aplikasi menggunakan dark maroon theme dengan desain premium:
- Metric cards dengan animasi hover
- Plotly interactive charts
- Custom styled prediction form
