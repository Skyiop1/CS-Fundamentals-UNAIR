import os
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", "/tmp/akm_matplotlib")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)

from .config import EVALUATION_RESULTS_PATH, FIGURES_DIR, TARGET_COLUMN


def calculate_metrics(y_true, y_probability, threshold: float = 0.5) -> dict:
    y_pred = (np.asarray(y_probability).reshape(-1) >= threshold).astype(int)
    y_probability = np.asarray(y_probability).reshape(-1)

    try:
        auc_score = roc_auc_score(y_true, y_probability)
    except ValueError:
        auc_score = 0.0

    return {
        "accuracy": accuracy_score(y_true, y_pred),
        "precision": precision_score(y_true, y_pred, zero_division=0),
        "recall": recall_score(y_true, y_pred, zero_division=0),
        "f1_score": f1_score(y_true, y_pred, zero_division=0),
        "auc_score": auc_score,
    }


def plot_class_distribution(df: pd.DataFrame, output_path: Path | None = None) -> Path:
    output_path = output_path or FIGURES_DIR / "class_distribution.png"
    counts = df[TARGET_COLUMN].value_counts().sort_index()
    labels = ["Lancar", "Gagal Bayar"]

    plt.figure(figsize=(7, 4.5))
    ax = plt.gca()
    ax.set_axisbelow(True)
    plt.bar(labels, counts.values, color=["#059669", "#DC2626"], edgecolor="#0F172A", linewidth=1.2, zorder=3)
    plt.title("Distribusi Kelas Status Kredit (Lancar vs Gagal Bayar)")
    plt.ylabel("Jumlah Data")
    plt.grid(axis="y", color="#CBD5E1", linewidth=0.8, linestyle="--", alpha=0.7)
    
    # Clean dark border outline
    ax = plt.gca()
    for spine in ax.spines.values():
        spine.set_edgecolor('#0F172A')
        spine.set_linewidth(1.2)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=160)
    plt.close()
    return output_path


def plot_confusion_matrix(y_true, y_probability, output_path: Path | None = None) -> Path:
    output_path = output_path or FIGURES_DIR / "confusion_matrix_best_model.png"
    y_pred = (np.asarray(y_probability).reshape(-1) >= 0.5).astype(int)
    matrix = confusion_matrix(y_true, y_pred)

    plt.figure(figsize=(5.5, 4.5))
    plt.imshow(matrix, cmap="Blues")
    plt.title("Confusion Matrix Model Terbaik")
    plt.xticks([0, 1], ["Lancar", "Gagal Bayar"])
    plt.yticks([0, 1], ["Lancar", "Gagal Bayar"])
    plt.xlabel("Prediksi")
    plt.ylabel("Aktual")

    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            plt.text(j, i, matrix[i, j], ha="center", va="center", color="#020617", fontweight="bold")

    plt.grid(False)
    plt.colorbar()
    
    # Clean dark border outline
    ax = plt.gca()
    for spine in ax.spines.values():
        spine.set_edgecolor('#0F172A')
        spine.set_linewidth(1.2)
        
    plt.tight_layout()
    plt.savefig(output_path, dpi=160)
    plt.close()
    return output_path


def plot_training_history(history, prefix: str = "best_model") -> tuple[Path, Path]:
    accuracy_path = FIGURES_DIR / "training_accuracy.png"
    loss_path = FIGURES_DIR / "training_loss.png"
    history_dict = history.history if hasattr(history, "history") else history

    # Accuracy Plot
    plt.figure(figsize=(7, 4.5))
    ax = plt.gca()
    ax.set_axisbelow(True)
    plt.plot(history_dict.get("accuracy", []), label="Training Accuracy", color="#2563EB", linewidth=2, zorder=3)
    plt.plot(history_dict.get("val_accuracy", []), label="Validation Accuracy", color="#059669", linewidth=2, zorder=3)
    plt.title("Training dan Validation Accuracy")
    plt.xlabel("Epoch")
    plt.ylabel("Accuracy")
    plt.grid(color="#CBD5E1", linewidth=0.8, linestyle="--", alpha=0.7)
    plt.legend()
    
    ax = plt.gca()
    for spine in ax.spines.values():
        spine.set_edgecolor('#0F172A')
        spine.set_linewidth(1.2)
        
    plt.tight_layout()
    plt.savefig(accuracy_path, dpi=160)
    plt.close()

    # Loss Plot
    plt.figure(figsize=(7, 4.5))
    ax = plt.gca()
    ax.set_axisbelow(True)
    plt.plot(history_dict.get("loss", []), label="Training Loss", color="#DC2626", linewidth=2, zorder=3)
    plt.plot(history_dict.get("val_loss", []), label="Validation Loss", color="#D97706", linewidth=2, zorder=3)
    plt.title("Training dan Validation Loss")
    plt.xlabel("Epoch")
    plt.ylabel("Loss")
    plt.grid(color="#CBD5E1", linewidth=0.8, linestyle="--", alpha=0.7)
    plt.legend()
    
    ax = plt.gca()
    for spine in ax.spines.values():
        spine.set_edgecolor('#0F172A')
        spine.set_linewidth(1.2)
        
    plt.tight_layout()
    plt.savefig(loss_path, dpi=160)
    plt.close()

    return accuracy_path, loss_path


def plot_model_comparison(results: pd.DataFrame, output_path: Path | None = None) -> Path:
    output_path = output_path or FIGURES_DIR / "model_comparison.png"
    labels = results["scenario"] + " - " + results["model_name"]
    x = np.arange(len(labels))

    plt.figure(figsize=(12, 5.5))
    ax = plt.gca()
    ax.set_axisbelow(True)
    plt.bar(x - 0.2, results["accuracy"], width=0.4, label="Accuracy", color="#2563EB", edgecolor="#0F172A", linewidth=1.0, zorder=3)
    plt.bar(x + 0.2, results["f1_score"], width=0.4, label="F1-Score", color="#D97706", edgecolor="#0F172A", linewidth=1.0, zorder=3)
    plt.title("Perbandingan Accuracy dan F1-Score")
    plt.xticks(x, labels, rotation=35, ha="right")
    plt.ylim(0, 1)
    plt.grid(axis="y", color="#CBD5E1", linewidth=0.8, linestyle="--", alpha=0.7)
    plt.legend()
    
    ax = plt.gca()
    for spine in ax.spines.values():
        spine.set_edgecolor('#0F172A')
        spine.set_linewidth(1.2)
        
    plt.tight_layout()
    plt.savefig(output_path, dpi=160)
    plt.close()
    return output_path


def save_evaluation_results(results: list[dict]) -> pd.DataFrame:
    df = pd.DataFrame(results)
    df.to_csv(EVALUATION_RESULTS_PATH, index=False)
    return df
