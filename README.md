# CS-Fundamentals-UNAIR

📚 **Academic Projects & Development Portofolio** — Information Systems, Universitas Airlangga (UNAIR)
  
[![Python Version](https://img.shields.io/badge/Python-3.9+-blue.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Flutter](https://img.shields.io/badge/Flutter-3.x-02569B.svg?style=for-the-badge&logo=flutter&logoColor=white)](https://flutter.dev/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B.svg?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Docker](https://img.shields.io/badge/Docker-Container-2496ED.svg?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)

Repositori ini berfungsi sebagai portofolio akademik untuk mata kuliah pemrograman, ilmu data (Data Science), dan pengembangan aplikasi yang dikerjakan selama masa studi di Program Studi **Sistem Informasi, Universitas Airlangga**. Repositori ini terbagi menjadi tugas-tugas terstruktur (*assignments*) dan proyek-proyek mandiri skala besar (*primary projects*).

---

## 🗺️ Peta Repositori (Repository Map)

```mermaid
flowchart TD
    Root[CS-Fundamentals-UNAIR] --> ClassTasks[Tugas Terstruktur / Coursework]
    Root --> PrimaryProjects[Proyek Utama / Primary Projects]

    ClassTasks --> T1[Data Preprocessing & Scaling]
    T1 --> D1["`**Data Normalization**`
    *Min-Max, Standard, & Robust Scaling*"]
    
    ClassTasks --> T2[Dimensionality & Selection]
    T2 --> D2["`**Feature Extraction & Selection**`
    *PCA & ANOVA-based statistical selection*"]
    
    ClassTasks --> T3[Resampling & Imbalance]
    T3 --> D3["`**Imbalanced Data Handling**`
    *ROS (Oversampling) & RUS (Undersampling)*"]
    
    ClassTasks --> T4[Machine Learning Models]
    T4 --> D4["`**Decision Tree Classification**`
    *Tree pruning, evaluation & high-res plotting*"]
    T4 --> D5["`**Wine Quality Classification**`
    *Streamlit-based prediction dashboard*"]
    T4 --> D6["`**Car Price Prediction**`
    *Streamlit dashboard + XGBoost & LightGBM*"]
    T4 --> D7["`**Clustering & Customer Segmentation**`
    *K-Means & K-Modes profiling analysis*"]

    PrimaryProjects --> P1["`**Stock Price Prediction (GA + RF)**`
    *Evolusioner GA feature selection & Random Forest*"]
    PrimaryProjects --> P2["`**NusaCarbon Ecosystem**`
    *Aplikasi mobile & web penyeimbang karbon*"]

    P2 --> P2a["`**Nusa Carbon Mobile**`
    *Flutter mobile client + Spring Boot API*"]
    P2 --> P2b["`**NusaCarbonWEB**`
    *PHP Web portal, Buyer & Verifier dashboard*"]
```

---

## 📂 Portofolio Tugas Akademis (Coursework)

Berikut adalah daftar tugas akademik yang mencakup preprocessing data, pemodelan statistik, hingga pembuatan web dashboard sederhana:

| Rumpun Pembelajaran | Nama Folder | Topik & Metode | Deskripsi Singkat |
|---|---|---|---|
| **Data Preprocessing** | [`Data Normalization`](./Data%20Normalization) | Min-Max, Z-Score Standard, Robust Scaling | Melakukan normalisasi data pada dataset kanker paru dan belanja untuk menghilangkan bias skala pada fitur numerik. |
| **Statistical Analysis** | [`Feature Extraction & Selection`](./Feature%20Extraction%20%26%20Selection) | Principal Component Analysis (PCA), ANOVA | Mengurangi dimensi fitur menggunakan PCA (threshold 95% variance) dan melakukan seleksi fitur relevan menggunakan statistik ANOVA. |
| **Resampling** | [`Imbalanced Data Handling`](./Imbalanced%20Data%20Handling) | Random Oversampling (ROS), Random Undersampling (RUS) | Mengatasi ketimpangan distribusi kelas target (class imbalance) menggunakan library `imbalanced-learn`. |
| **Machine Learning** | [`Decision Tree Classification`](./Decision%20Tree%20Classification) | Gini & Entropy Decision Tree Classifier | Membangun pohon keputusan untuk klasifikasi kondisi pasien, lengkap dengan visualisasi detail 3 tingkat teratas. |
| **Interactive Dashboard** | [`Wine Quality Classification`](./Wine%20Quality%20Classification) | Streamlit Web App, Plotly charts | Menyediakan antarmuka web interaktif untuk menguji parameter kimia wine dan memprediksi kualitasnya secara real-time. |
| **Regression & Ensemble** | [`Car Price Prediction`](./Car%20Price%20Prediction) | XGBoost, LightGBM Regressor | Membandingkan performa model ensemble untuk melakukan estimasi harga mobil bekas berdasarkan detail spesifikasi. |
| **Unsupervised Learning** | [`Clustering & Customer Segmentation`](./Clustering%20%26%20Customer%20Segmentation) | K-Means & K-Modes Clustering | Segmentasi pasar berbasis data perilaku belanja dan riwayat kartu kredit menggunakan Elbow method & Silhouette score. |

---

## 🚀 Proyek Utama (Primary Projects Showcase)

Repositori ini juga memuat proyek akhir berskala besar yang mengintegrasikan berbagai domain teknologi:

### 1. NusaCarbon Ecosystem (Mobile & Web)
Sebuah ekosistem digital untuk perdagangan kredit karbon (*carbon credit trading*) dan sistem pemantauan kelayakan hijau (*MRV — Measurement, Reporting, and Verification*).
*   **[`Nusa Carbon Mobile`](./Nusa%20Carbon%20Mobile)**: Aplikasi mobile berbasis **Flutter** untuk sisi pembeli/pemilik proyek karbon. Dilengkapi dengan bagan pelacakan transaksi, integrasi API, dan simulasi transaksi blockchain.
*   **[`NusaCarbonWEB`](./Nusa%20Carbon%20WEB)**: Portal web berbasis **PHP** yang memisahkan akses pengguna (*role-based layout*) antara Buyer, Project Owner (untuk mengunggah proyek hijau), dan Verifier (untuk melakukan kurasi dan verifikasi dokumen kelayakan). Dockerized untuk kemudahan deploy lokal.

### 2. [`Stock Price Prediction (GA + RF)`](./Stock%20Price%20Prediction%20\(GA%20%2B%20RF\))
Sistem rekomendasi perdagangan saham dengan memprediksi arah pergerakan harga saham BBCA (Bank Central Asia) menggunakan metode kecerdasan buatan evolusioner.
*   **Genetic Algorithm (GA)**: Mengoptimalkan kombinasi indikator teknikal saham (RSI, MACD, Bollinger Bands, dll.) sebagai fitur masukan untuk mencegah overfitting.
*   **Random Forest (RF)**: Sebagai *classifier* utama untuk memprediksi arah naik/turun.
*   **Decision Threshold Tuning**: Mengoptimalkan batas keputusan (threshold probability) untuk memaksimalkan *Precision* (mengurangi transaksi rugi) dan meminimalkan *False Positives*.
*   **Hasil**: Dilengkapi visualisasi lengkap mencakup kurva ROC-AUC, riwayat fitness GA, studi ablasi, dan estimasi profitabilitas.

---

## 🛠️ Ringkasan Tech Stack

Daftar teknologi utama yang digunakan di seluruh proyek di repositori ini:

*   **Languages**: Python, Dart, PHP, JavaScript, SQL
*   **Machine Learning**: `scikit-learn`, `xgboost`, `lightgbm`, `imbalanced-learn`
*   **Data Analysis & Vis**: `pandas`, `numpy`, `matplotlib`, `seaborn`, `plotly`
*   **Mobile App Development**: `Flutter` (Dart)
*   **Web Frameworks**: `Streamlit`, Vanilla PHP (dengan Bootstrap/CSS modern)
*   **Infrastructure**: `Docker`, Local database server

---

## 👤 Author

**Muhammad Naufal Zaki**  
NIM: 187241115  
Program Studi Sistem Informasi  
Fakultas Teknologi Terpadu, Universitas Airlangga (UNAIR)
