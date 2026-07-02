import pandas as pd
from scipy.stats import pearsonr, spearmanr
from sklearn.preprocessing import LabelEncoder


# SELEKSI FITUR - DATASET STUDENT PERFORMANCE
# Label: Numerik (Performance Index)
# Metode: Pearson & Spearman Correlation

# Memuat dataset
df = pd.read_csv("performance.csv", sep=";")

# Fix kolom Performance Index yang bermasalah
df['Performance Index'] = df['Performance Index'].astype(str).str.replace(r'\.00$', '', regex=True).astype(float)

# Encode kolom kategorikal
le = LabelEncoder()
df['Extracurricular Activities'] = le.fit_transform(df['Extracurricular Activities'])

# Pisahkan fitur dan target
target_col = "Performance Index"
feature_cols = [col for col in df.columns if col != target_col]

print("SELEKSI FITUR - STUDENT PERFORMANCE DATASET (PEARSON & SPEARMAN)")
print(f"{'Fitur':<35} {'Pearson r':>10} {'P-Pearson':>12} {'Spearman r':>12} {'P-Spearman':>12} {'Signifikan'}")

results = []
alpha = 0.05

for col in feature_cols:
    pearson_r, pearson_p = pearsonr(df[col], df[target_col])
    spearman_r, spearman_p = spearmanr(df[col], df[target_col])
    signifikan = "Ya" if pearson_p < alpha or spearman_p < alpha else "Tidak"
    print(f"{col:<35} {pearson_r:>10.4f} {pearson_p:>12.4e} {spearman_r:>12.4f} {spearman_p:>12.4e}   {signifikan}")
    results.append({
        "Fitur": col,
        "Pearson_r": round(pearson_r, 6),
        "P_Value_Pearson": round(pearson_p, 10),
        "Spearman_r": round(spearman_r, 6),
        "P_Value_Spearman": round(spearman_p, 10),
        "Signifikan": signifikan
    })

df_result = pd.DataFrame(results)
df_result.to_csv("hasil_seleksi_fitur_performance.csv", index=False)

print("\nFitur SIGNIFIKAN (p < 0.05):")
significant = df_result[df_result['Signifikan'] == 'Ya']
for _, row in significant.iterrows():
    print(f"  - {row['Fitur']} (Pearson r={row['Pearson_r']}, Spearman r={row['Spearman_r']})")

print(f"\nTotal: {len(significant)} dari {len(feature_cols)} fitur signifikan")
print("Hasil disimpan ke: hasil_seleksi_fitur_performance.csv")
