### 🔴 Prioritas 1 — RF Hyperparameters (Dampak PALING BESAR)

Ini jantungnya performa model. Saat ini terlalu konservatif:

| Parameter | Sekarang | Rekomendasi | Alasan |
|---|---|---|---|
| max_depth | 6 | **10** | Depth 6 terlalu dangkal, model underfitting. Naik ke 10 biar model bisa tangkap pola lebih kompleks |
| n_estimators | 300 | **500** | Lebih banyak tree = voting lebih stabil, mengurangi varians antar skenario |
| min_samples_leaf | 5 | **3** | Membolehkan model belajar pola lebih detail dari leaf yang lebih kecil |

### 🟠 Prioritas 2 — GA Parameters (Dampak SEDANG-BESAR)

GA saat ini terlalu "cepat selesai", belum cukup eksplorasi:

| Parameter | Sekarang | Rekomendasi | Alasan |
|---|---|---|---|
| population_size | 30 | **50** | Populasi lebih besar = lebih banyak kandidat fitur dieksplorasi |
| generations | 25 | **40** | Lebih lama evolusi = konvergensi lebih baik |
| mutation_rate | 0.05 | **0.10** | Sedikit lebih agresif agar GA tidak terjebak di local optima |
| elite_size | 2 | **3** | Pertahankan lebih banyak solusi bagus antar generasi |

### 🟡 Prioritas 3 — GA Fitness RF (Pendukung)

RF yang dipakai GA untuk evaluasi fitness juga terlalu lemah:

| Parameter | Sekarang | Rekomendasi |
|---|---|---|
| n_estimators | 150 | **200** |
| max_depth | 5 | **8** |

Kalau fitness evaluator-nya lemah, GA memilih fitur berdasarkan sinyal yang kurang akurat.

### 🟢 Prioritas 4 — Full Pipeline untuk Semua Skenario

Yang bikin njomplang juga karena **75/25 dan 70/30 cuma pakai 1 seed** sementara 80/20 pakai 5 seeds + ablation + threshold tuning. Perlu disamakan.

---

## 📋 Ringkasan Perubahan yang Saya Rekomendasikan
RF_PARAMS:       max_depth 6→10, n_estimators 300→500, min_samples_leaf 5→3
GA_FITNESS_RF:   n_estimators 150→200, max_depth 5→8
GA_PARAMS:       population 30→50, generations 25→40, mutation 0.05→0.10, elite 2→3
Pipeline:        75/25 & 70/30 jalankan full pipeline seperti 80/20

**Ekspektasi:** AUROC dan F1 di 75/25 dan 70/30 akan naik mendekati 80/20, karena model lebih kuat (RF params) dan feature selection lebih optimal (GA params). Gap antar skenario harusnya menyusut signifikan.

> ⚠️ **Trade-off:** Runtime akan lebih lama (~2-3x dari sebelumnya) karena GA lebih besar dan n_estimators lebih banyak. Tapi worth it untuk hasil yang konsisten.



# Dokumentasi Progress Eksperimen: Optimasi Random Forest + Genetic Algorithm + Threshold Tuning

## Ringkasan

Tujuan utama dari rangkaian eksperimen ini adalah meningkatkan performa dan **stabilitas model prediksi arah harga saham** menggunakan kombinasi **Random Forest (RF)** dan **Genetic Algorithm (GA)**, sekaligus memastikan metodologi yang digunakan dapat dipertanggungjawabkan secara akademis.

Selain mengejar nilai metrik yang lebih baik, fokus penting lainnya adalah mengurangi perbedaan performa yang terlalu besar antar skenario pembagian data (80/20, 75/25, dan 70/30).

---

# Tahap 1 – Audit Konfigurasi Awal

Konfigurasi awal yang digunakan:

## Random Forest

* `n_estimators = 300`
* `max_depth = 6`
* `min_samples_leaf = 5`

## Genetic Algorithm

* Population = 30
* Generations = 25

Dari audit awal muncul hipotesis bahwa:

* Random Forest masih relatif konservatif (berpotensi underfitting).
* Genetic Algorithm mungkin belum mengeksplorasi ruang solusi secara optimal.

---

# Tahap 2 – Eksperimen Hyperparameter Random Forest

Dilakukan pengujian terhadap konfigurasi yang lebih agresif, antara lain:

* `n_estimators ≈ 500`
* `max_depth ≈ 10`
* `min_samples_leaf ≈ 3`

## Hasil

### Positif

* AUROC meningkat dibanding konfigurasi awal.

### Negatif

* Pada threshold default 0.50, F1-score justru turun.
* Model menjadi terlalu konservatif dalam memprediksi kelas positif.

Kesimpulan:

> Memperbesar kapasitas model meningkatkan kemampuan ranking (AUROC), tetapi keputusan klasifikasi akhir masih sangat dipengaruhi oleh threshold.

---

# Tahap 3 – Investigasi Threshold

Dilakukan eksperimen threshold tuning.

Awalnya digunakan threshold standar:

```
Threshold = 0.50
```

Kemudian dilakukan pencarian threshold berbasis validation.

## Temuan

Threshold optimal justru berada di kisaran:

* 0.12
* 0.18
* 0.24
* 0.26
* 0.38

bergantung pada skenario dan kriteria evaluasi.

## Dampak

F1-score meningkat secara signifikan tanpa mengubah AUROC.

Kesimpulan penting:

> Permasalahan utama bukan berada pada kualitas Random Forest, melainkan pada penggunaan threshold default 0.50 yang kurang sesuai dengan distribusi probabilitas model.

---

# Tahap 4 – Eksperimen Genetic Algorithm yang Lebih Besar

Dilakukan pengujian terhadap konfigurasi GA yang lebih besar.

Rencana parameter:

* Population: 30 → 50
* Generations: 25 → 40
* Mutation Rate: 0.05 → 0.10
* Elite Size: 2 → 3

Fitness evaluator RF juga diperkuat.

## Hasil

Setelah beberapa generasi berjalan:

* Validation score hanya meningkat sedikit.
* Tidak berhasil melampaui konfigurasi GA sebelumnya.
* Waktu komputasi meningkat drastis.

Kesimpulan:

> Memperbesar GA tidak memberikan peningkatan performa yang sebanding dengan biaya komputasi.

Keputusan:

* Tidak menjadikan GA expansion sebagai fokus utama.

---

# Tahap 5 – Systematic Random Forest Study

Dilakukan pendekatan yang lebih akademik:

## Hyperparameter tuning

Menggunakan:

* `RandomizedSearchCV`
* `TimeSeriesSplit`
* Validation internal

Grid yang dieksplorasi meliputi:

* n_estimators
* max_depth
* min_samples_leaf
* min_samples_split
* max_features
* class_weight

Tujuan:

* Memilih parameter berdasarkan validation, bukan test.

---

# Tahap 6 – Perbaikan Metodologi Threshold

Pipeline disusun sebagai berikut:

```
X_train
    │
    ├── X_sub_train
    │       │
    │       └── Hyperparameter tuning
    │
    ├── X_val
    │       │
    │       └── Threshold selection
    │
    └── X_test
            │
            └── Final evaluation
```

Dengan pendekatan ini:

* Test set tidak digunakan untuk memilih parameter.
* Test set hanya digunakan untuk evaluasi akhir.

Hal ini mengurangi risiko data leakage.

---

# Tahap 7 – Retraining Final

Setelah hyperparameter dan threshold dipilih:

1. Model dilatih ulang menggunakan seluruh `X_train`.
2. Threshold yang telah dipilih pada validation dipertahankan.
3. Model dievaluasi pada `X_test`.

Tujuannya adalah memanfaatkan seluruh data latih tanpa mengorbankan validitas evaluasi.

---

# Tahap 8 – Perluasan Grid Threshold

Grid threshold diperluas menjadi:

```
0.10
0.12
0.14
...
0.88
0.90
```

Pendekatan ini lebih fleksibel dibanding hanya menggunakan threshold sekitar 0.50.

---

# Tahap 9 – Hasil Eksperimen

## Threshold default (0.50)

F1-score sangat rendah:

* sekitar 0.11–0.18

Model gagal menangkap banyak kelas positif.

---

## Threshold hasil optimasi

Threshold optimal berada di kisaran:

* 0.12
* 0.18
* 0.24
* 0.26
* 0.38

Hasil:

* Test F1 meningkat menjadi sekitar 0.48–0.51.
* AUROC tetap berada di kisaran ±0.58–0.63.

---

# Tahap 10 – Stabilitas Antar Split

Dilakukan evaluasi pada:

* 80/20
* 75/25
* 70/30

Hasil menunjukkan F1 yang sangat konsisten.

Contoh:

| Split | Test F1 (max_f1) |
| ----- | ---------------: |
| 80/20 |           0.4972 |
| 75/25 |           0.4971 |
| 70/30 |           0.4836 |

Gap maksimum hanya sekitar 0.014.

Kesimpulan:

> Model menjadi jauh lebih stabil dan tidak lagi menunjukkan perbedaan performa yang ekstrem antar skenario split.

---

# Tahap 11 – Hyperparameter Final

Melalui systematic tuning diperoleh konfigurasi Random Forest yang sederhana namun efektif:

```
n_estimators = 100
max_depth = 12
min_samples_leaf = 3
min_samples_split = 5
max_features = 0.4
class_weight = None
```

Menariknya, konfigurasi ini mengungguli atau menyamai konfigurasi yang lebih kompleks (misalnya 500 pohon) sambil memberikan efisiensi komputasi yang lebih baik.

---

# Insight Penting

1. Memperbesar Random Forest tidak selalu meningkatkan performa akhir.
2. Genetic Algorithm yang lebih besar tidak memberikan keuntungan signifikan.
3. Threshold default 0.50 bukan pilihan terbaik untuk dataset ini.
4. Optimasi threshold berbasis validation memberikan peningkatan F1 paling besar.
5. Evaluasi menggunakan TimeSeriesSplit membuat pemilihan hyperparameter lebih robust.
6. Retraining pada seluruh data training setelah threshold dipilih merupakan pendekatan yang tepat.
7. Model final menunjukkan stabilitas yang baik pada berbagai skenario split.

---

# Catatan Tambahan

Selama proses eksperimen muncul warning seperti:

```
UserWarning:
sklearn.utils.parallel.delayed should be used with
sklearn.utils.parallel.Parallel
```

Warning tersebut berasal dari mekanisme paralelisasi internal `scikit-learn` dan tidak memengaruhi hasil prediksi maupun validitas eksperimen selama proses berjalan hingga selesai.

---

# Kesimpulan Akhir

Eksperimen menunjukkan bahwa peningkatan performa terbesar **bukan berasal dari memperbesar kompleksitas model**, melainkan dari **pemilihan threshold klasifikasi yang tepat dan prosedur validasi yang benar**.

Pendekatan akhir berhasil menghasilkan model yang:

* memiliki performa yang konsisten pada berbagai skenario split,
* menghindari data leakage,
* menggunakan proses tuning yang sistematis,
* serta lebih efisien dibanding konfigurasi yang lebih kompleks.

Secara keseluruhan, pipeline akhir telah memenuhi praktik yang baik untuk penelitian akademik dan layak dijadikan versi final untuk pelaporan atau skripsi.


Berdasarkan hasil eksperimen pengujian skenario pembagian data (Train/Test Split) yang tercatat di 
multiseed_scenario_summary.csv
 dan 
split_scenario_results.csv
, berikut adalah rangkuman performa dan analisis mendalam mengenai skenario 80/20, 75/25, dan 70/30:

Rangkuman Hasil Skenario Split
Skenario	Data Train	Data Test	Baseline RF AUROC	Mean GA AUROC (± Std)	Baseline RF F1	Mean GA F1 (± Std)	Best Test AUROC (Seed)
80/20	1.644 baris	412 baris	0.5981	0.6038 (± 0.005)	0.1494	0.2396 (± 0.021)	0.6107 (Seed 123)
75/25	1.542 baris	514 baris	0.5748	0.5974 (± 0.007)	0.1182	0.1566 (± 0.032)	0.6100 (Seed 99)
70/30	1.439 baris	617 baris	0.5880	0.5810 (± 0.014)	0.1304	0.1570 (± 0.021)	0.6067 (Seed 123)

Analisis & Temuan Kunci
1. Skenario 80/20 Adalah Skenario Terbaik secara Konsisten
Skenario 80/20 menghasilkan performa paling optimal di hampir semua metrik:

AUROC Tertinggi: Rata-rata AUROC setelah seleksi fitur GA mencapai 0.6038, dan performa terbaik perorangan mencapai 0.6107 (menggunakan Seed 123).
F1-score & Balanced Accuracy Tertinggi: F1-score rata-rata melonjak ke 0.2396 (dibandingkan ~0.15 pada skenario lainnya), dan Balanced Accuracy rata-rata naik ke 0.5335.

Alasan Fundamental:
Volume Data Training: Skenario 80/20 melatih model menggunakan data terbanyak (1.644 baris) hingga September 2024. Data yang lebih melimpah membantu model Random Forest mempelajari pola musiman (seasonal patterns) dan tren pasar secara lebih matang.
Kedekatan Temporal Test Set: Periode uji (test set) pada 80/20 lebih pendek dan lebih baru (September 2024 – Juni 2026). Dinamika pasar pada periode ini lebih dekat ke kondisi data training terakhir dibandingkan dengan skenario 70/30 yang data ujinya ditarik terlalu jauh ke belakang (sejak November 2023).

2. GA Efektif pada Skenario 80/20 & 75/25, Namun Gagal pada Skenario 70/30
Pada 80/20 dan 75/25, seleksi fitur menggunakan GA berhasil menaikkan performa model dibandingkan baseline (misal pada 75/25, AUROC naik dari 0.5748 menjadi 0.5974).

Namun pada 70/30, GA justru menurunkan performa rata-rata dari 0.5880 menjadi 0.5810.
Alasan Teknis (Overfitting GA): GA membutuhkan data training/validation yang cukup representatif untuk mengevaluasi kecocokan (fitness) kromosom fitur. Ketika data training dikurangi menjadi 70% (1.439 baris), GA mengalami overfitting pada subset data training tersebut. Akibatnya, fitur-fitur yang dipilih GA menjadi terlalu spesifik untuk periode 2018–2023, dan gagal bergeneralisasi pada periode uji 2023–2026 yang sangat panjang (30% dari total data).

3. Stabilitas Model Meningkat Seiring Bertambahnya Data Training
Perhatikan nilai standar deviasi (Std) AUROC GA:
Skenario 80/20: ± 0.005 (sangat stabil antar seed)
Skenario 75/25: ± 0.007
Skenario 70/30: ± 0.014 (fluktuatif antar seed)
Ini menunjukkan bahwa data training yang lebih besar (seperti pada 80/20) membuat proses pencarian fitur GA jauh lebih stabil dan tidak sensitif terhadap inisialisasi awal (seed dependency). Pada data yang lebih sedikit (70/30), variasi performa antar seed GA menjadi dua kali lipat lebih tinggi.
Kesimpulan Praktis untuk Langkah Pengembangan
Berdasarkan analisis split ini, rekomendasi terbaik untuk konfigurasi model Anda adalah:

Gunakan Skenario 80/20 sebagai basis pengembangan utama. Model mendapatkan keuntungan terbesar dari ketersediaan data latih yang lebih baru hingga kuartal akhir 2024.
Hindari skenario pengujian 70/30 jika menggunakan GA. Data latih yang terlalu sempit membuat algoritma pencari fitur GA tersesat ke arah overfitting (over-selection terhadap noise masa lalu).
Optimasi Berkelanjutan: Mengingat performa AUROC terbaik mentok di angka ~0.61, langkah berikutnya yang paling menjanjikan adalah mencoba menambahkan data volume perdagangan saham (market volume) atau mencoba algoritma gradient boosting (seperti XGBoost) pada skenario split 80/20 ini.


