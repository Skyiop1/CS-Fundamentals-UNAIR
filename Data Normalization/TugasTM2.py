import pandas as pd
from sklearn.preprocessing import MinMaxScaler, StandardScaler, RobustScaler

# ============================================================
# DATASET 1 - LUNG CANCER PREDICTION
# ============================================================

df = pd.read_csv("Lung Cancer Prediction.csv", sep=';')
df.columns = df.columns.str.strip()

print(df.shape)
print(df.columns)
print(df.dtypes)
print(df.isna().sum())

print(df['LUNG_CANCER'].value_counts())

df_features = df.drop(columns=['LUNG_CANCER', 'GENDER'])
numerical_cols = df_features.select_dtypes(include=['float64', 'int64']).columns

df_minmax = df_features.copy()
df_minmax[numerical_cols] = MinMaxScaler().fit_transform(df_features[numerical_cols])

df_standard = df_features.copy()
df_standard[numerical_cols] = StandardScaler().fit_transform(df_features[numerical_cols])

df_robust = df_features.copy()
df_robust[numerical_cols] = RobustScaler().fit_transform(df_features[numerical_cols])

print("=== Min-Max (Lung Cancer) ===")
print(df_minmax.head())
print("\n=== Standard (Lung Cancer) ===")
print(df_standard.head())
print("\n=== Robust (Lung Cancer) ===")
print(df_robust.head())


# ============================================================
# DATASET 2 - SHOPPING MALL CUSTOMERS
# ============================================================

df2 = pd.read_csv("Shopping.csv", sep=';')
df2.columns = df2.columns.str.strip()

print(df2.shape)
print(df2.columns)
print(df2.dtypes)
print(df2.isna().sum())

# Handling missing values dengan mean
df2['Age'] = df2['Age'].fillna(df2['Age'].mean())
df2['Annual Income (k$)'] = df2['Annual Income (k$)'].fillna(df2['Annual Income (k$)'].mean())
df2['Spending Score (1-100)'] = df2['Spending Score (1-100)'].fillna(df2['Spending Score (1-100)'].mean())

df2_features = df2.drop(columns=['CustomerID', 'Genre'])
numerical_cols2 = df2_features.select_dtypes(include=['float64', 'int64']).columns

df2_minmax = df2_features.copy()
df2_minmax[numerical_cols2] = MinMaxScaler().fit_transform(df2_features[numerical_cols2])

df2_standard = df2_features.copy()
df2_standard[numerical_cols2] = StandardScaler().fit_transform(df2_features[numerical_cols2])

df2_robust = df2_features.copy()
df2_robust[numerical_cols2] = RobustScaler().fit_transform(df2_features[numerical_cols2])

print("\n=== Min-Max (Shopping) ===")
print(df2_minmax.head())
print("\n=== Standard (Shopping) ===")
print(df2_standard.head())
print("\n=== Robust (Shopping) ===")
print(df2_robust.head())