import pandas as pd
from scipy.stats import f_oneway

# SELEKSI FITUR - DATASET DIABETES
# Label: Kategorikal (Outcome: 0 atau 1)
# Metode: ANOVA (fitur numerik dengan target kategori)

# Memuat dataset
df = pd.read_csv("Diabetes.csv", sep=";")

# Fix kolom yang bermasalah akibat format Excel
df['BMI'] = df['BMI'].astype(str).str.replace(r'\.00$', '', regex=True).astype(float)
df['DiabetesPedigreeFunction'] = df['DiabetesPedigreeFunction'].astype(str).str.replace(',', '.').astype(float)

# Pisahkan fitur dan target
target_col = "Outcome"
feature_cols = [col for col in df.columns if col != target_col]

# Kelompokkan berdasarkan label
group_0 = df[df[target_col] == 0]
group_1 = df[df[target_col] == 1]

# ANOVA untuk setiap fitur
print("=" * 60)
print("SELEKSI FITUR - DIABETES DATASET (ANOVA)")
print("=" * 60)
print(f"{'Fitur':<32} {'F-Value':>10} {'P-Value':>15} {'Signifikan'}")
print("-" * 60)

results = []
alpha = 0.05

for col in feature_cols:
    f_val, p_val = f_oneway(group_0[col], group_1[col])
    signifikan = "Ya" if p_val < alpha else "Tidak"
    print(f"{col:<32} {f_val:>10.4f} {p_val:>15.6e}   {signifikan}")
    results.append({
        "Fitur": col,
        "F_Value": round(f_val, 6),
        "P_Value": round(p_val, 10),
        "Signifikan": signifikan
    })

df_result = pd.DataFrame(results)
df_result.to_csv("hasil_seleksi_fitur_diabetes.csv", index=False)

print("\nFitur SIGNIFIKAN (p < 0.05):")
significant = df_result[df_result['Signifikan'] == 'Ya']
for _, row in significant.iterrows():
    print(f"  - {row['Fitur']}")

print(f"\nTotal: {len(significant)} dari {len(feature_cols)} fitur signifikan")
print("Hasil disimpan ke: hasil_seleksi_fitur_diabetes.csv")
