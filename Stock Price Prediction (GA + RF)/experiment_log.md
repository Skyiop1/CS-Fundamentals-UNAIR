# Ringkasan Hasil Eksperimen Random Forest Optimization dan Threshold Selection

## 1. Hasil Optimasi Threshold Random Forest

### Split Data 80:20

| Threshold Criterion       | Selected Threshold | Validation AUROC | Validation F1 | Test AUROC |  Test F1 |
| ------------------------- | -----------------: | ---------------: | ------------: | ---------: | -------: |
| Default (0.50)            |               0.50 |         0.528486 |      0.018692 |   0.601177 | 0.134146 |
| Maximum F1                |               0.12 |         0.528486 |      0.484988 |   0.601177 | 0.493601 |
| Maximum Balanced Accuracy |               0.36 |         0.528486 |      0.278146 |   0.601177 | 0.493225 |
| Maximum G-Mean            |               0.28 |         0.528486 |      0.409266 |   0.601177 | 0.490722 |

---

### Split Data 75:25

| Threshold Criterion       | Selected Threshold | Validation AUROC | Validation F1 | Test AUROC |  Test F1 |
| ------------------------- | -----------------: | ---------------: | ------------: | ---------: | -------: |
| Default (0.50)            |               0.50 |         0.533651 |      0.020202 |   0.577462 | 0.130653 |
| Maximum F1                |               0.20 |         0.533651 |      0.485714 |   0.577462 | 0.502229 |
| Maximum Balanced Accuracy |               0.20 |         0.533651 |      0.485714 |   0.577462 | 0.502229 |
| Maximum G-Mean            |               0.24 |         0.533651 |      0.452962 |   0.577462 | 0.496124 |

---

### Split Data 70:30

| Threshold Criterion       | Selected Threshold | Validation AUROC | Validation F1 | Test AUROC |  Test F1 |
| ------------------------- | -----------------: | ---------------: | ------------: | ---------: | -------: |
| Default (0.50)            |               0.50 |         0.564662 |      0.000000 |   0.611618 | 0.090498 |
| Maximum F1                |               0.20 |         0.564662 |      0.508571 |   0.611618 | 0.495641 |
| Maximum Balanced Accuracy |               0.26 |         0.564662 |      0.466926 |   0.611618 | 0.493544 |
| Maximum G-Mean            |               0.26 |         0.564662 |      0.466926 |   0.611618 | 0.493544 |

Chart hasil optimasi threshold disimpan pada file:

* `rf_optimization_comparison_chart.png`

---

# Ranking Model Berdasarkan AUROC

| Peringkat | Model                                    | Feature Set            | Threshold |    AUROC |
| --------- | ---------------------------------------- | ---------------------- | --------: | -------: |
| 1         | RF + GA (Best Test Seed 123 - Observasi) | GA Seed 123 Features   |      0.50 | 0.610723 |
| 2         | RF + GA (Seed 42)                        | GA Seed 42 Features    |      0.50 | 0.610108 |
| 3         | RF + GA (Seed 42, Tuned Threshold)       | GA Seed 42 Features    |      0.32 | 0.610108 |
| 4         | Baseline RF                              | All Features           |      0.50 | 0.598075 |
| 5         | Baseline RF (Tuned Threshold)            | All Features           |      0.31 | 0.598075 |
| 6         | SVM + GA (Seed 42)                       | GA Seed 42 Features    |      0.50 | 0.584436 |
| 7         | SVM + Frequent GA                        | Frequent GA ≥ 60%      |      0.50 | 0.576735 |
| 8         | Baseline SVM                             | All Features           |      0.50 | 0.538655 |
| 9         | Baseline SVM (Tuned Threshold)           | All Features           |      0.31 | 0.538655 |
| 10        | Dummy Majority                           | No Predictive Features |   Default | 0.500000 |

---

# Ranking Model Berdasarkan Balanced Accuracy

| Peringkat | Model                                    | Feature Set            | Threshold | Balanced Accuracy |
| --------- | ---------------------------------------- | ---------------------- | --------: | ----------------: |
| 1         | RF + GA (Seed 42, Tuned Threshold)       | GA Seed 42 Features    |      0.32 |          0.581936 |
| 2         | SVM + GA (Seed 42)                       | GA Seed 42 Features    |      0.50 |          0.559928 |
| 3         | Baseline RF (Tuned Threshold)            | All Features           |      0.31 |          0.555703 |
| 4         | SVM + Frequent GA                        | Frequent GA ≥ 60%      |      0.50 |          0.550715 |
| 5         | RF + GA (Seed 42)                        | GA Seed 42 Features    |      0.50 |          0.547466 |
| 6         | RF + GA (Best Test Seed 123 - Observasi) | GA Seed 123 Features   |      0.50 |          0.538067 |
| 7         | Baseline SVM                             | All Features           |      0.50 |          0.537331 |
| 8         | Baseline SVM (Tuned Threshold)           | All Features           |      0.31 |          0.533761 |
| 9         | Baseline RF                              | All Features           |      0.50 |          0.501217 |
| 10        | Dummy Majority                           | No Predictive Features |   Default |          0.500000 |

---

# Ranking Model Berdasarkan F1-Score

| Peringkat | Model                                    | Feature Set            | Threshold | F1-Score |
| --------- | ---------------------------------------- | ---------------------- | --------: | -------: |
| 1         | RF + GA (Seed 42, Tuned Threshold)       | GA Seed 42 Features    |      0.32 | 0.511057 |
| 2         | Baseline RF (Tuned Threshold)            | All Features           |      0.31 | 0.503341 |
| 3         | Baseline SVM (Tuned Threshold)           | All Features           |      0.31 | 0.486726 |
| 4         | SVM + GA (Seed 42)                       | GA Seed 42 Features    |      0.50 | 0.464183 |
| 5         | SVM + Frequent GA                        | Frequent GA ≥ 60%      |      0.50 | 0.454023 |
| 6         | Baseline SVM                             | All Features           |      0.50 | 0.429003 |
| 7         | Dummy Stratified                         | No Predictive Features |   Default | 0.300752 |
| 8         | RF + GA (Seed 42)                        | GA Seed 42 Features    |      0.50 | 0.270270 |
| 9         | RF + GA (Best Test Seed 123 - Observasi) | GA Seed 123 Features   |      0.50 | 0.235955 |
| 10        | Baseline RF                              | All Features           |      0.50 | 0.149425 |

---

# Evaluasi Stabilitas Model

Evaluasi stabilitas dilakukan menggunakan beberapa nilai random seed. Stabilitas model Random Forest dengan Genetic Algorithm dinilai berdasarkan rata-rata (mean) dan standar deviasi AUROC pada file `ga_seed_results.csv`, bukan berdasarkan satu hasil terbaik saja.

| Komponen          |   Nilai |
| ----------------- | ------: |
| Baseline RF AUROC |  0.5981 |
| RF + GA AUROC     |  0.6101 |
| Delta AUROC       | +0.0120 |
| Best GA Fitness   |  0.5845 |

---

# Interpretasi Hasil

* Model menunjukkan kemampuan prediktif yang cukup baik berdasarkan hasil evaluasi.
* Genetic Algorithm memberikan peningkatan performa secara praktis melalui proses seleksi fitur.
* Random Forest menunjukkan kestabilan yang lebih baik dibandingkan SVM pada eksperimen ini.
* Penggunaan Dummy Classifier sebagai baseline membantu memastikan bahwa model memiliki kemampuan prediksi di atas tebakan acak. Evaluasi dilakukan menggunakan AUROC, Balanced Accuracy, dan F1-score untuk mengurangi bias akibat ketidakseimbangan kelas.
* RF + GA menunjukkan performa yang relatif stabil antar-seed dengan nilai rata-rata AUROC sebesar **0.6038** dan standar deviasi sebesar **0.0056**.
* Seed **123** menghasilkan AUROC test tertinggi (**0.6107**), namun hanya digunakan sebagai hasil observasi pada data uji dan bukan sebagai model utama.
* Seed terbaik berdasarkan validation adalah **21**, sedangkan seed terbaik berdasarkan test adalah **123**, sehingga peningkatan performa RF + GA terhadap Baseline RF belum sepenuhnya konsisten.
* Baseline Random Forest tetap menjadi model pembanding yang paling stabil sepanjang eksperimen.
* Frequent GA Features menghasilkan performa yang mendekati penggunaan seluruh fitur dengan jumlah fitur yang lebih sedikit, sehingga Genetic Algorithm lebih bermanfaat sebagai metode reduksi fitur dan analisis pentingnya fitur dibandingkan sebagai bukti peningkatan akurasi yang konsisten.

---

# Estimasi Prediksi Terbaru

| Informasi                           | Nilai        |
| ----------------------------------- | ------------ |
| Tanggal Data Terakhir               | 26 Juni 2026 |
| Harga Penutupan BBCA                | 6,175.00     |
| Probabilitas Uptrend (RF + GA)      | 0.2965       |
| Probabilitas Not-Uptrend (RF + GA)  | 0.7035       |
| Probabilitas Uptrend (Baseline RF)  | 0.3487       |
| Probabilitas Uptrend (Baseline SVM) | 0.3133       |
| Output Sinyal Model                 | NOT-UPTREND  |
| Confidence                          | 0.4071       |
| Kategori Confidence                 | Sedang       |

Catatan:

* Model hanya mengestimasi arah pergerakan tren saham.
* Model tidak memprediksi harga saham secara nominal.
* Hasil prediksi tidak dimaksudkan sebagai rekomendasi investasi maupun trading.

---

# File Output Eksperimen

### Data

* experiment_results.csv
* ga_seed_results.csv
* selected_features_frequency.csv
* ablation_study_results.csv
* threshold_tuning_results.csv
* split_scenario_results.csv
* multiseed_scenario_detail.csv
* multiseed_scenario_summary.csv
* rf_optimization_results.csv

### Visualisasi

* bbca_price_history_chart.png
* ga_fitness_chart.png
* model_comparison_chart.png
* roc_curve_chart.png
* selected_features_chart.png
* recent_estimation_chart.png
* ablation_study_chart.png
* ga_seed_comparison_chart.png
* selected_features_frequency_chart.png
* split_scenario_chart.png
* multiseed_scenario_chart.png
* rf_optimization_comparison_chart.png

---

**Eksperimen telah selesai. Seluruh hasil diperoleh berdasarkan data historis saham BBCA yang bersumber dari Yahoo Finance. Model hanya digunakan untuk mengestimasi arah tren harga saham dan tidak dirancang untuk memprediksi harga saham secara nominal maupun memberikan rekomendasi investasi atau trading.**
