import json
import os
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", "/tmp/akm_matplotlib")
os.environ.setdefault("XDG_CACHE_HOME", "/tmp/akm_cache")

import joblib
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau

if __package__ is None or __package__ == "":
    import sys

    sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.config import (  # noqa: E402
    BEST_MODEL_PATH,
    FEATURE_COLUMNS_PATH,
    FIGURES_DIR,
    METADATA_PATH,
    MODELS_DIR,
    PCA_PATH,
    REPORTS_DIR,
    SCALER_PATH,
    SPLIT_SCENARIOS,
    ensure_directories,
)
from src.data_loader import get_dataset_summary, preprocess_raw_dataset  # noqa: E402
from src.evaluate import (  # noqa: E402
    calculate_metrics,
    plot_class_distribution,
    plot_confusion_matrix,
    plot_model_comparison,
    plot_training_history,
    save_evaluation_results,
)
from src.model_dnn import build_dnn_model  # noqa: E402
from src.model_pca_dnn import build_pca_dnn_model  # noqa: E402
from src.preprocessing import (  # noqa: E402
    apply_smote_to_training,
    fit_pca_data,
    fit_scale_data,
    make_train_test_split,
    split_features_target,
)


def train_single_model(model, X_train, y_train, epochs: int, batch_size: int):
    callbacks = [
        EarlyStopping(monitor="val_loss", patience=10, restore_best_weights=True),
        ReduceLROnPlateau(monitor="val_loss", patience=5, factor=0.5, min_lr=1e-5),
    ]
    return model.fit(
        X_train,
        y_train,
        epochs=epochs,
        batch_size=batch_size,
        validation_split=0.2,
        callbacks=callbacks,
        verbose=1,
    )


def select_best_result(results: list[dict]) -> dict:
    return sorted(
        results,
        key=lambda item: (
            item["f1_score"],
            item["recall"],
            item["precision"],
            item["accuracy"],
            -item["loss"],
        ),
        reverse=True,
    )[0]


def write_experiment_summary(summary: dict, best_result: dict) -> None:
    path = REPORTS_DIR / "experiment_summary.md"
    content = f"""# Experiment Summary - Credit Default Risk AI

## Dataset
- Total data: {summary["rows"]}
- Feature count: {summary["feature_count"]}
- Missing value: {summary["missing_values"]}
- Non-default distribution: {summary["class_counts"].get(0, 0)} ({summary["class_percentages"].get(0, 0)}%)
- Default distribution: {summary["class_counts"].get(1, 0)} ({summary["class_percentages"].get(1, 0)}%)

## Best Model
- Best model: {best_result["model_name"]}
- Split scenario: {best_result["scenario"]}
- Accuracy: {best_result["accuracy"]:.4f}
- Precision: {best_result["precision"]:.4f}
- Recall: {best_result["recall"]:.4f}
- F1-score: {best_result["f1_score"]:.4f}
- ROC-AUC: {best_result["auc_score"]:.4f}

## Methodology Notes
SMOTE is applied only to the training data after train-test splitting and scaling.
PCA is used as a feature extraction stage for the Hybrid PCA-DNN pipeline, not as the primary deep learning model.
"""
    path.write_text(content, encoding="utf-8")


def run_training(epochs: int = 50, batch_size: int = 64) -> None:
    ensure_directories()
    df = preprocess_raw_dataset()
    dataset_summary = get_dataset_summary(df)
    plot_class_distribution(df)

    X, y = split_features_target(df)
    feature_columns = list(X.columns)
    results = []
    best_bundle = None

    for scenario, test_size in SPLIT_SCENARIOS.items():
        split_data = make_train_test_split(X, y, test_size)
        X_train_scaled, X_test_scaled, scaler = fit_scale_data(split_data.X_train, split_data.X_test)
        X_train_smote, y_train_smote = apply_smote_to_training(X_train_scaled, split_data.y_train)

        dnn_model = build_dnn_model(input_dim=X_train_smote.shape[1])
        dnn_history = train_single_model(dnn_model, X_train_smote, y_train_smote, epochs, batch_size)
        dnn_probability = dnn_model.predict(X_test_scaled, verbose=0).reshape(-1)
        dnn_metrics = calculate_metrics(split_data.y_test, dnn_probability)
        dnn_loss = float(dnn_model.evaluate(X_test_scaled, split_data.y_test, verbose=0)[0])
        results.append(
            {
                "scenario": scenario,
                "model_name": "DNN / MLP",
                **dnn_metrics,
                "loss": dnn_loss,
                "train_size": int(len(split_data.X_train)),
                "test_size": int(len(split_data.X_test)),
                "smote_used": True,
                "pca_used": False,
                "pca_components": 0,
                "best_model": False,
                "_model": dnn_model,
                "_history": dnn_history.history,
                "_scaler": scaler,
                "_pca": None,
                "_y_test": split_data.y_test,
                "_probability": dnn_probability,
            }
        )

        X_train_pca, X_test_pca, pca = fit_pca_data(X_train_smote, X_test_scaled)
        pca_model = build_pca_dnn_model(input_dim=X_train_pca.shape[1])
        pca_history = train_single_model(pca_model, X_train_pca, y_train_smote, epochs, batch_size)
        pca_probability = pca_model.predict(X_test_pca, verbose=0).reshape(-1)
        pca_metrics = calculate_metrics(split_data.y_test, pca_probability)
        pca_loss = float(pca_model.evaluate(X_test_pca, split_data.y_test, verbose=0)[0])
        results.append(
            {
                "scenario": scenario,
                "model_name": "Hybrid PCA-DNN",
                **pca_metrics,
                "loss": pca_loss,
                "train_size": int(len(split_data.X_train)),
                "test_size": int(len(split_data.X_test)),
                "smote_used": True,
                "pca_used": True,
                "pca_components": int(getattr(pca, "n_components_", X_train_pca.shape[1])),
                "best_model": False,
                "_model": pca_model,
                "_history": pca_history.history,
                "_scaler": scaler,
                "_pca": pca,
                "_y_test": split_data.y_test,
                "_probability": pca_probability,
            }
        )

    best_result = select_best_result(results)
    for result in results:
        result["best_model"] = result is best_result

    best_result["_model"].save(BEST_MODEL_PATH)
    joblib.dump(best_result["_scaler"], SCALER_PATH)
    if best_result["_pca"] is not None:
        joblib.dump(best_result["_pca"], PCA_PATH)
    elif PCA_PATH.exists():
        PCA_PATH.unlink()

    with open(FEATURE_COLUMNS_PATH, "w", encoding="utf-8") as file:
        json.dump(feature_columns, file, indent=2)

    metadata = {
        "best_model_name": best_result["model_name"],
        "best_split_scenario": best_result["scenario"],
        "accuracy": float(best_result["accuracy"]),
        "precision": float(best_result["precision"]),
        "recall": float(best_result["recall"]),
        "f1_score": float(best_result["f1_score"]),
        "auc_score": float(best_result["auc_score"]),
        "loss": float(best_result["loss"]),
        "threshold": 0.5,
        "pca_used": bool(best_result["pca_used"]),
        "smote_used": bool(best_result["smote_used"]),
        "pca_components": int(best_result["pca_components"]),
    }
    with open(METADATA_PATH, "w", encoding="utf-8") as file:
        json.dump(metadata, file, indent=2)

    clean_results = [
        {key: value for key, value in result.items() if not key.startswith("_")}
        for result in results
    ]
    evaluation_df = save_evaluation_results(clean_results)
    plot_model_comparison(evaluation_df)
    plot_training_history(best_result["_history"])
    plot_confusion_matrix(best_result["_y_test"], best_result["_probability"])
    write_experiment_summary(dataset_summary, best_result)

    temp_model_paths = list(MODELS_DIR.glob("*.tmp.keras"))
    for path in temp_model_paths:
        path.unlink(missing_ok=True)

    print("Training completed.")
    print(f"Best model: {best_result['model_name']} ({best_result['scenario']})")
    print(f"F1-score: {best_result['f1_score']:.4f}")


if __name__ == "__main__":
    run_training()
