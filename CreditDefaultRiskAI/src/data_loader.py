import re
from pathlib import Path

import pandas as pd

from .config import PROCESSED_DATA_PATH, RAW_DATA_PATH, TARGET_COLUMN, ensure_directories


ORIGINAL_TARGET = "default payment next month"


def clean_column_name(name: str) -> str:
    """Convert a raw column name to a clear snake_case name when needed."""
    cleaned = str(name).strip()
    if cleaned == ORIGINAL_TARGET:
        return TARGET_COLUMN
    cleaned = re.sub(r"[^0-9a-zA-Z]+", "_", cleaned).strip("_").lower()
    return cleaned


def _looks_like_embedded_header(first_row: pd.Series) -> bool:
    values = {str(value).strip() for value in first_row.tolist()}
    return {"ID", "LIMIT_BAL", "default payment next month"}.issubset(values)


def load_raw_dataset(path: str | Path = RAW_DATA_PATH) -> pd.DataFrame:
    """Load the CSV dataset and normalize the converted Excel header layout."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Dataset tidak ditemukan: {path}")

    df = pd.read_csv(path)

    if _looks_like_embedded_header(df.iloc[0]):
        header = [str(value).strip() for value in df.iloc[0].tolist()]
        df = df.iloc[1:].reset_index(drop=True)
        df.columns = header

    if "ID" in df.columns:
        df = df.drop(columns=["ID"])
    if "Unnamed: 0" in df.columns:
        df = df.drop(columns=["Unnamed: 0"])

    rename_map = {ORIGINAL_TARGET: TARGET_COLUMN, "Y": TARGET_COLUMN}
    df = df.rename(columns=rename_map)

    if TARGET_COLUMN not in df.columns:
        raise ValueError(f"Kolom target `{TARGET_COLUMN}` tidak ditemukan.")

    for column in df.columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    return df


def preprocess_raw_dataset(
    path: str | Path = RAW_DATA_PATH,
    save_processed: bool = True,
    remove_duplicates: bool = True,
) -> pd.DataFrame:
    """Load, clean, validate, and optionally save processed credit default data."""
    ensure_directories()
    df = load_raw_dataset(path)
    df = df.dropna().reset_index(drop=True)

    if remove_duplicates:
        df = df.drop_duplicates().reset_index(drop=True)

    df[TARGET_COLUMN] = df[TARGET_COLUMN].astype(int)
    feature_columns = [column for column in df.columns if column != TARGET_COLUMN]
    df[feature_columns] = df[feature_columns].astype(float)

    if save_processed:
        df.to_csv(PROCESSED_DATA_PATH, index=False)

    return df


def get_dataset_summary(df: pd.DataFrame) -> dict:
    """Return compact dataset summary for reports and the Streamlit app."""
    class_counts = df[TARGET_COLUMN].value_counts().sort_index()
    class_percentages = (class_counts / len(df) * 100).round(2)
    return {
        "rows": int(df.shape[0]),
        "columns": int(df.shape[1]),
        "feature_count": int(df.shape[1] - 1),
        "missing_values": int(df.isna().sum().sum()),
        "duplicate_rows": int(df.duplicated().sum()),
        "class_counts": {int(k): int(v) for k, v in class_counts.items()},
        "class_percentages": {int(k): float(v) for k, v in class_percentages.items()},
    }
