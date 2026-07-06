import json
import os
from datetime import datetime

os.environ.setdefault("MPLCONFIGDIR", "/tmp/akm_matplotlib")
os.environ.setdefault("XDG_CACHE_HOME", "/tmp/akm_cache")
os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "2")

import joblib
import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model

from .config import (
    BEST_MODEL_PATH,
    FEATURE_COLUMNS,
    FEATURE_COLUMNS_PATH,
    METADATA_PATH,
    PCA_PATH,
    SCALER_PATH,
)


def load_metadata() -> dict:
    if not METADATA_PATH.exists():
        raise FileNotFoundError("Metadata model belum tersedia. Jalankan `python src/train.py` terlebih dahulu.")
    with open(METADATA_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def load_feature_columns() -> list[str]:
    if FEATURE_COLUMNS_PATH.exists():
        with open(FEATURE_COLUMNS_PATH, "r", encoding="utf-8") as file:
            return json.load(file)
    return FEATURE_COLUMNS


def get_risk_level(probability: float) -> str:
    if probability < 0.40:
        return "Risiko Rendah"
    if probability < 0.70:
        return "Risiko Sedang"
    return "Risiko Tinggi"


def get_recommendation(risk_level: str) -> str:
    recommendations = {
        "Risiko Rendah": "Pengajuan dapat diproses dengan pemeriksaan dokumen standar.",
        "Risiko Sedang": "Perlu verifikasi tambahan, terutama riwayat pembayaran dan kemampuan bayar nasabah.",
        "Risiko Tinggi": "Sebaiknya pengajuan tidak langsung disetujui sebelum ada analisis dan dokumen pendukung tambahan.",
    }
    return recommendations[risk_level]


def predict_default(input_data: dict) -> dict:
    if not BEST_MODEL_PATH.exists() or not SCALER_PATH.exists():
        raise FileNotFoundError("Model belum tersedia. Jalankan training terlebih dahulu.")

    metadata = load_metadata()
    feature_columns = load_feature_columns()
    scaler = joblib.load(SCALER_PATH)
    model = load_model(BEST_MODEL_PATH, compile=False)

    row = pd.DataFrame([{column: input_data[column] for column in feature_columns}])
    scaled = pd.DataFrame(scaler.transform(row), columns=feature_columns)

    if metadata.get("pca_used", False):
        if not PCA_PATH.exists():
            raise FileNotFoundError("Model terbaik membutuhkan PCA, tetapi file pca.pkl tidak ditemukan.")
        pca = joblib.load(PCA_PATH)
        model_input = pca.transform(scaled)
    else:
        model_input = scaled.to_numpy()

    probability = float(np.asarray(model(model_input, training=False)).reshape(-1)[0])
    prediction_result = "Default" if probability >= metadata.get("threshold", 0.5) else "Tidak Default"
    risk_level = get_risk_level(probability)

    return {
        "prediction_result": prediction_result,
        "default_probability": probability,
        "risk_level": risk_level,
        "model_used": metadata.get("best_model_name", "Model Terbaik"),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "recommendation": get_recommendation(risk_level),
    }
