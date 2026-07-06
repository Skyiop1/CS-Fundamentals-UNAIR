from dataclasses import dataclass

import joblib
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from .config import PCA_PATH, RANDOM_STATE, SCALER_PATH, TARGET_COLUMN


@dataclass
class SplitData:
    X_train: pd.DataFrame
    X_test: pd.DataFrame
    y_train: pd.Series
    y_test: pd.Series


def split_features_target(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    X = df.drop(columns=[TARGET_COLUMN])
    y = df[TARGET_COLUMN].astype(int)
    return X, y


def make_train_test_split(
    X: pd.DataFrame,
    y: pd.Series,
    test_size: float,
    random_state: int = RANDOM_STATE,
) -> SplitData:
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=test_size,
        random_state=random_state,
        stratify=y,
    )
    return SplitData(X_train, X_test, y_train, y_test)


def fit_scale_data(
    X_train: pd.DataFrame,
    X_test: pd.DataFrame,
    save_scaler: bool = False,
) -> tuple[pd.DataFrame, pd.DataFrame, StandardScaler]:
    scaler = StandardScaler()
    X_train_scaled = pd.DataFrame(
        scaler.fit_transform(X_train),
        columns=X_train.columns,
        index=X_train.index,
    )
    X_test_scaled = pd.DataFrame(
        scaler.transform(X_test),
        columns=X_test.columns,
        index=X_test.index,
    )
    if save_scaler:
        joblib.dump(scaler, SCALER_PATH)
    return X_train_scaled, X_test_scaled, scaler


def apply_smote_to_training(X_train, y_train, random_state: int = RANDOM_STATE):
    """Apply SMOTE only to training data to prevent data leakage."""
    from imblearn.over_sampling import SMOTE

    smote = SMOTE(random_state=random_state)
    return smote.fit_resample(X_train, y_train)


def fit_pca_data(
    X_train,
    X_test,
    n_components: float = 0.95,
    save_pca: bool = False,
):
    pca = PCA(n_components=n_components, random_state=RANDOM_STATE)
    X_train_pca = pca.fit_transform(X_train)
    X_test_pca = pca.transform(X_test)
    if save_pca:
        joblib.dump(pca, PCA_PATH)
    return X_train_pca, X_test_pca, pca
