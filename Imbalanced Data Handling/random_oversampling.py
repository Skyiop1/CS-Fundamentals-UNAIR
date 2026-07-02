    import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from imblearn.over_sampling import RandomOverSampler

# Load & Preview Dataset
df = pd.read_csv("WineQT.csv")
df.columns = df.columns.str.strip()

print("Sample Data:")
print(df.head())



# Preprocessing
df["target"] = (df["quality"] >= 7).astype(int)

print("\nMissing Values:")
print(df.isna().sum())

X = df.drop(columns=["quality", "target", "Id"])
y = df["target"]



# Random Over Sampling
ros = RandomOverSampler(random_state=42)
X_resampled, y_resampled = ros.fit_resample(X, y)
y_resampled = pd.Series(y_resampled)



# Visualisasi Distribusi
labels = ["Bad Wine", "Good Wine"]
before_counts = y.value_counts().sort_index()
after_counts = y_resampled.value_counts().sort_index()

fig, axes = plt.subplots(1, 2, figsize=(12, 4))

sns.barplot(x=labels, y=before_counts.values, color="skyblue", ax=axes[0])
axes[0].set_title("Distribusi Sebelum ROS")
axes[0].set_xlabel("Kualitas Wine")
axes[0].set_ylabel("Jumlah")

sns.barplot(x=labels, y=after_counts.values, palette="coolwarm", ax=axes[1])
axes[1].set_title("Distribusi Sesudah ROS")
axes[1].set_xlabel("Kualitas Wine")
axes[1].set_ylabel("Jumlah")

plt.tight_layout()
plt.show()



# Ringkasan Hasil
print("\nDistribusi Sebelum ROS:")
print(before_counts.rename({0: "Bad Wine", 1: "Good Wine"}))

print("\nDistribusi Sesudah ROS:")
print(after_counts.rename({0: "Bad Wine", 1: "Good Wine"}))

print(f"\nTotal data setelah ROS: {len(X_resampled)}")