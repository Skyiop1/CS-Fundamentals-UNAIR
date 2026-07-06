from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_RAW_DIR = PROJECT_ROOT / "data" / "raw"
DATA_PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
MODELS_DIR = PROJECT_ROOT / "models"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"
FIGURES_DIR = OUTPUTS_DIR / "figures"
TABLES_DIR = OUTPUTS_DIR / "tables"
REPORTS_DIR = OUTPUTS_DIR / "reports"
DATABASE_DIR = PROJECT_ROOT / "database"

RAW_DATA_PATH = DATA_RAW_DIR / "default of credit card clients.csv"
PROCESSED_DATA_PATH = DATA_PROCESSED_DIR / "processed_credit_default.csv"
BEST_MODEL_PATH = MODELS_DIR / "best_model.keras"
SCALER_PATH = MODELS_DIR / "scaler.pkl"
PCA_PATH = MODELS_DIR / "pca.pkl"
METADATA_PATH = MODELS_DIR / "model_metadata.json"
FEATURE_COLUMNS_PATH = MODELS_DIR / "feature_columns.json"
EVALUATION_RESULTS_PATH = TABLES_DIR / "evaluation_results.csv"
DATABASE_PATH = DATABASE_DIR / "predictions.db"

RANDOM_STATE = 42
TARGET_COLUMN = "default_status"
SPLIT_SCENARIOS = {
    "80/20": 0.20,
    "75/25": 0.25,
    "70/30": 0.30,
}

FEATURE_COLUMNS = [
    "LIMIT_BAL",
    "SEX",
    "EDUCATION",
    "MARRIAGE",
    "AGE",
    "PAY_0",
    "PAY_2",
    "PAY_3",
    "PAY_4",
    "PAY_5",
    "PAY_6",
    "BILL_AMT1",
    "BILL_AMT2",
    "BILL_AMT3",
    "BILL_AMT4",
    "BILL_AMT5",
    "BILL_AMT6",
    "PAY_AMT1",
    "PAY_AMT2",
    "PAY_AMT3",
    "PAY_AMT4",
    "PAY_AMT5",
    "PAY_AMT6",
]


def ensure_directories() -> None:
    """Create required project directories if they do not exist."""
    for path in [
        DATA_RAW_DIR,
        DATA_PROCESSED_DIR,
        MODELS_DIR,
        FIGURES_DIR,
        TABLES_DIR,
        REPORTS_DIR,
        DATABASE_DIR,
    ]:
        path.mkdir(parents=True, exist_ok=True)
