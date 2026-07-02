import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler


# EKSTRAKSI FITUR - DATASET DIABETES
# Metode: PCA dengan n_components optimal

# Memuat dataset
df = pd.read_csv("Diabetes.csv", sep=";")

# Fix kolom bermasalah
df['BMI'] = df['BMI'].astype(str).str.replace(r'\.00$', '', regex=True).astype(float)
df['DiabetesPedigreeFunction'] = df['DiabetesPedigreeFunction'].astype(str).str.replace(',', '.').astype(float)

# Pisahkan fitur dan target
X = df.drop(columns=["Outcome"])
y = df["Outcome"]

# Standarisasi
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Cari n_components optimal (threshold: 95% explained variance)
pca_full = PCA()
pca_full.fit(X_scaled)
cumulative_variance = np.cumsum(pca_full.explained_variance_ratio_)

optimal_n = np.argmax(cumulative_variance >= 0.95) + 1
print(f"Cumulative Variance per Komponen:")
for i, v in enumerate(cumulative_variance):
    print(f"  PC{i+1}: {v*100:.2f}%")
print(f"\nN komponen optimal (>= 95% variance): {optimal_n}")

# PCA dengan n_components optimal
pca = PCA(n_components=optimal_n)
X_pca = pca.fit_transform(X_scaled)

print("\nExplained Variance Ratio per Komponen:")
for i, v in enumerate(pca.explained_variance_ratio_):
    print(f"  PC{i+1}: {v*100:.4f}%")
print(f"Total Variance Explained: {sum(pca.explained_variance_ratio_)*100:.4f}%")

# Buat DataFrame hasil PCA
col_names = [f"PC{i+1}" for i in range(optimal_n)]
df_pca = pd.DataFrame(X_pca, columns=col_names)
df_pca["Outcome"] = y.values

# Simpan ke CSV
df_pca.to_csv("hasil_pca_diabetes.csv", index=False)
print(df_pca.head())

# Plot Scree Plot
plt.figure(figsize=(8, 5))
plt.plot(range(1, len(pca_full.explained_variance_ratio_) + 1),
         cumulative_variance, marker='o', color='steelblue')
plt.axhline(y=0.95, color='red', linestyle='--', label='95% threshold')
plt.axvline(x=optimal_n, color='green', linestyle='--', label=f'Optimal = {optimal_n}')
plt.xlabel("Jumlah Komponen")
plt.ylabel("Cumulative Explained Variance")
plt.title("Scree Plot PCA - Diabetes Dataset")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("scree_plot_diabetes.png", dpi=150)
plt.show()

#Plot PCA 2D (PC1 vs PC2) untuk visualisasi
plt.figure(figsize=(8, 6))
plt.scatter(df_pca["PC1"], df_pca["PC2"], c=df_pca["Outcome"],
            cmap="coolwarm", alpha=0.7)
plt.xlabel("Principal Component 1")
plt.ylabel("Principal Component 2")
plt.title("PCA: Diabetes Dataset")
plt.colorbar(label="Outcome")
plt.tight_layout()
plt.savefig("pca_plot_diabetes.png", dpi=150)
plt.show()
