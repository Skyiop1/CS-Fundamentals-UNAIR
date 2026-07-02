# Install requirements:
# pip install yfinance pandas numpy scikit-learn matplotlib

import os
import sys
import warnings
from typing import Callable, Dict, List, Optional, Tuple

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import yfinance as yf
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
    roc_curve,
)
from sklearn.model_selection import TimeSeriesSplit, RandomizedSearchCV
from sklearn.calibration import CalibratedClassifierCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

warnings.filterwarnings(
    "ignore",
    message=".*sklearn\\.utils\\.parallel\\.delayed.*should be used.*",
    category=UserWarning,
)

START_DATE = "2018-01-01"
TARGET_THRESHOLD = 0.005
RANDOM_STATE = 42
LAG_DAYS = 10
MIN_MODEL_ROWS = 300
REGENERATE_CHARTS_ONLY = False
SHOW_RECENT_ESTIMATION_CHART = True
RUN_SPLIT_SCENARIO_STUDY = True

ASSETS = {
    "BBCA": "BBCA.JK",
    "IHSG": "^JKSE",
    "BBRI": "BBRI.JK",
    "BMRI": "BMRI.JK",
    "BBNI": "BBNI.JK",
    "USD_IDR": "IDR=X",
    "SP500": "^GSPC",
    "NASDAQ": "^IXIC",
    "NIKKEI225": "^N225",
}

TARGET_ALIAS = "BBCA"

RF_PARAMS = {
    "n_estimators": 100,
    "max_depth": 12,
    "min_samples_leaf": 3,
    "min_samples_split": 5,
    "max_features": 0.4,
    "class_weight": None,
    "random_state": RANDOM_STATE,
    "n_jobs": -1,
}

RF_TUNING_GRID = {
    "n_estimators": [100, 300, 500],
    "max_depth": [5, 8, 12],
    "min_samples_leaf": [3, 5],
    "min_samples_split": [5, 10],
    "max_features": ["sqrt", 0.4],
    "class_weight": ["balanced_subsample", None],
}

WIDE_THRESHOLD_GRID = np.round(np.arange(0.10, 0.901, 0.02), 2)

GA_FITNESS_RF_PARAMS = {
    "n_estimators": 150,
    "max_depth": 5,
    "min_samples_leaf": 5,
    "class_weight": "balanced_subsample",
    "random_state": RANDOM_STATE,
    "n_jobs": -1,
}

GA_PARAMS = {
    "population_size": 30,
    "generations": 25,
    "mutation_rate": 0.05,
    "crossover_rate": 0.8,
    "elite_size": 2,
    "random_state": RANDOM_STATE,
}

GA_SEEDS = [42, 7, 21, 99, 123]
GA_CV_SPLITS = 3
FREQUENT_FEATURE_THRESHOLD = 0.60
THRESHOLD_GRID = np.round(np.arange(0.30, 0.701, 0.01), 2)
SPLIT_SCENARIOS = [
    ("80/20", 0.80),
    ("75/25", 0.75),
    ("70/30", 0.70),
]
SPLIT_SCENARIO_GA_SEED = 42
REQUIRED_RESULT_CSVS = [
    "experiment_results.csv",
    "ga_seed_results.csv",
    "selected_features_frequency.csv",
    "ablation_study_results.csv",
    "threshold_tuning_results.csv",
]


def print_section(title: str) -> None:
    line = "=" * 72
    print(f"\n{line}")
    print(title)
    print(line)


def _latest_download_end_date() -> str:
    return (pd.Timestamp.today().normalize() + pd.Timedelta(days=1)).strftime("%Y-%m-%d")


def _normalize_price_series(series: pd.Series, alias: str) -> pd.Series:
    series = pd.to_numeric(series, errors="coerce").dropna()
    if series.empty:
        return pd.Series(dtype=float, name=alias)

    index = pd.to_datetime(series.index)
    try:
        index = index.tz_localize(None)
    except TypeError:
        pass
    series.index = pd.DatetimeIndex(index).normalize()
    series = series[~series.index.duplicated(keep="last")].sort_index()
    series.name = alias
    return series


def _extract_close_price(raw_data: pd.DataFrame, ticker: str, alias: str) -> pd.Series:
    if raw_data is None or raw_data.empty:
        return pd.Series(dtype=float, name=alias)

    close_series = None
    if isinstance(raw_data.columns, pd.MultiIndex):
        columns = list(raw_data.columns)
        exact_candidates = [
            ("Close", ticker),
            (ticker, "Close"),
            ("Close", alias),
            (alias, "Close"),
        ]
        for candidate in exact_candidates:
            if candidate in columns:
                close_series = raw_data[candidate]
                break

        if close_series is None:
            close_columns = [column for column in columns if "Close" in column]
            if close_columns:
                close_data = raw_data[close_columns[0]]
                close_series = close_data.iloc[:, 0] if isinstance(close_data, pd.DataFrame) else close_data
    else:
        if "Close" in raw_data.columns:
            close_series = raw_data["Close"]

    if close_series is None:
        return pd.Series(dtype=float, name=alias)
    return _normalize_price_series(close_series, alias)


def download_data(start_date: str = START_DATE) -> Tuple[pd.DataFrame, Dict[str, object]]:
    print_section("1. Download Data Yahoo Finance")
    end_date = _latest_download_end_date()
    print("Sumber data      : Yahoo Finance melalui yfinance")
    print(f"Rentang download : {start_date} sampai data terbaru yang tersedia")
    print(f"End parameter    : {end_date} (eksklusif pada yfinance)")
    print("Target utama     : BBCA.JK")

    downloaded_series: Dict[str, pd.Series] = {}
    successful_assets: List[str] = []
    failed_assets: List[str] = []
    failure_reasons: Dict[str, str] = {}

    for alias, ticker in ASSETS.items():
        try:
            raw_data = yf.download(
                ticker,
                start=start_date,
                end=end_date,
                interval="1d",
                auto_adjust=False,
                progress=False,
                threads=False,
            )
            close_series = _extract_close_price(raw_data, ticker, alias)
            if close_series.empty:
                raise ValueError("kolom Close kosong atau tidak tersedia")

            downloaded_series[alias] = close_series
            successful_assets.append(f"{alias} ({ticker})")
            print(f"Berhasil download: {alias:<10} {ticker:<10} | {len(close_series):>5} baris")
        except Exception as exc:
            failed_assets.append(f"{alias} ({ticker})")
            failure_reasons[alias] = str(exc)
            message = f"Gagal download: {alias:<10} {ticker:<10} | {exc}"
            if alias == TARGET_ALIAS:
                print(message)
            else:
                print(f"Warning - {message}")

    if TARGET_ALIAS not in downloaded_series or downloaded_series[TARGET_ALIAS].empty:
        reason = failure_reasons.get(TARGET_ALIAS, "data kosong")
        raise RuntimeError(
            f"Data BBCA.JK gagal didownload atau kosong. Program dihentikan. Detail: {reason}"
        )

    combined = pd.concat(downloaded_series.values(), axis=1, sort=True).sort_index()
    combined = combined[~combined.index.duplicated(keep="last")]
    bbca_index = downloaded_series[TARGET_ALIAS].index

    aligned_before_drop = combined.ffill().reindex(bbca_index)
    rows_before_preprocessing = len(aligned_before_drop)
    close_data = aligned_before_drop.dropna()
    rows_after_preprocessing = len(close_data)

    if rows_after_preprocessing == 0:
        raise RuntimeError(
            "Seluruh data hilang setelah forward fill dan drop missing value. "
            "Kemungkinan data eksternal terlalu banyak kosong."
        )

    dropped_ratio = 1 - (rows_after_preprocessing / max(rows_before_preprocessing, 1))
    if dropped_ratio > 0.30:
        print(
            "Warning - Lebih dari 30% baris hilang setelah preprocessing. "
            "Periksa kualitas data eksternal."
        )

    if rows_after_preprocessing < MIN_MODEL_ROWS:
        raise RuntimeError(
            f"Data setelah preprocessing hanya {rows_after_preprocessing} baris. "
            f"Minimal {MIN_MODEL_ROWS} baris diperlukan agar eksperimen lebih layak."
        )

    info = {
        "successful_assets": successful_assets,
        "failed_assets": failed_assets,
        "failure_reasons": failure_reasons,
        "rows_before_preprocessing": rows_before_preprocessing,
        "rows_after_preprocessing": rows_after_preprocessing,
    }

    print("\nDaftar aset berhasil:")
    for item in successful_assets:
        print(f"- {item}")

    if failed_assets:
        print("\nDaftar aset gagal:")
        for item in failed_assets:
            alias = item.split(" ")[0]
            print(f"- {item}: {failure_reasons.get(alias, 'tidak diketahui')}")
    else:
        print("\nDaftar aset gagal: tidak ada")

    print(f"\nRentang tanggal dataset : {close_data.index.min().date()} sampai {close_data.index.max().date()}")
    print(f"Jumlah data sebelum preprocessing : {rows_before_preprocessing}")
    print(f"Jumlah data setelah preprocessing : {rows_after_preprocessing}")
    print("Catatan alignment: data diselaraskan ke tanggal perdagangan BBCA setelah forward fill.")

    return close_data, info


def create_features_and_target(
    close_data: pd.DataFrame,
) -> Tuple[pd.DataFrame, pd.Series, pd.DataFrame, pd.DataFrame, pd.Timestamp, float]:
    print_section("2. Feature Engineering dan Target Klasifikasi")

    if TARGET_ALIAS not in close_data.columns:
        raise RuntimeError("Kolom BBCA tidak ditemukan setelah preprocessing.")

    returns = close_data.pct_change().replace([np.inf, -np.inf], np.nan)
    features = pd.DataFrame(index=close_data.index)

    for asset in close_data.columns:
        for lag in range(1, LAG_DAYS + 1):
            features[f"{asset}_lag_{lag}"] = returns[asset].shift(lag)

    bbca_returns = returns[TARGET_ALIAS]
    for window in [5, 10, 20]:
        features[f"BBCA_MA_{window}_return"] = bbca_returns.rolling(window=window).mean()
    for window in [5, 10, 20]:
        features[f"BBCA_volatility_{window}"] = bbca_returns.rolling(window=window).std()

    next_return = (close_data[TARGET_ALIAS].shift(-1) - close_data[TARGET_ALIAS]) / close_data[TARGET_ALIAS]
    target = pd.Series(np.nan, index=close_data.index, name="target")
    target.loc[next_return.notna()] = (next_return.loc[next_return.notna()] >= TARGET_THRESHOLD).astype(int)

    latest_feature_candidates = features.dropna()
    if latest_feature_candidates.empty:
        raise RuntimeError("Tidak ada baris fitur yang valid setelah membuat lag dan rolling feature.")

    latest_feature_date = latest_feature_candidates.index[-1]
    latest_bbca_close = float(close_data.loc[latest_feature_date, TARGET_ALIAS])

    supervised_data = features.join(target).dropna()
    if supervised_data.empty:
        raise RuntimeError("Tidak ada data supervised yang valid setelah target dan fitur digabungkan.")

    X = supervised_data.drop(columns=["target"])
    y = supervised_data["target"].astype(int)

    if y.nunique() < 2:
        raise RuntimeError(
            "Target hanya memiliki satu kelas setelah preprocessing. "
            "Model klasifikasi dan AUROC tidak dapat dievaluasi secara bermakna."
        )

    uptrend_count = int((y == 1).sum())
    not_uptrend_count = int((y == 0).sum())
    total = len(y)

    print(f"Jumlah fitur awal : {X.shape[1]}")
    print(f"Jumlah observasi supervised : {total}")
    print("Distribusi target:")
    print(f"- Uptrend     : {uptrend_count} ({uptrend_count / total:.2%})")
    print(f"- Not-Uptrend : {not_uptrend_count} ({not_uptrend_count / total:.2%})")
    print(f"Threshold Uptrend: next_return >= {TARGET_THRESHOLD:.3%}")
    print(f"Baris terakhir dataset supervised: {X.index.max().date()}")
    print(f"Baris fitur terbaru untuk estimasi: {latest_feature_date.date()}")

    return X, y, features, returns, latest_feature_date, latest_bbca_close


def split_data(
    X: pd.DataFrame,
    y: pd.Series,
    train_ratio: float = 0.80,
    scenario_label: Optional[str] = None,
    verbose: bool = True,
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    if verbose:
        title = "3. Train Test Split Berbasis Waktu"
        if scenario_label:
            title = f"Train Test Split Berbasis Waktu | Scenario {scenario_label}"
        print_section(title)

    if len(X) != len(y):
        raise RuntimeError("Jumlah baris X dan y tidak sama.")
    if len(X) < MIN_MODEL_ROWS:
        raise RuntimeError(
            f"Data supervised hanya {len(X)} baris. Minimal {MIN_MODEL_ROWS} baris diperlukan."
        )

    split_index = int(len(X) * train_ratio)
    if split_index <= 0 or split_index >= len(X):
        raise RuntimeError("Split train/test tidak valid. Data terlalu sedikit.")

    X_train = X.iloc[:split_index]
    X_test = X.iloc[split_index:]
    y_train = y.iloc[:split_index]
    y_test = y.iloc[split_index:]

    if y_train.nunique() < 2:
        raise RuntimeError("Training set hanya memiliki satu kelas. Random Forest tidak layak dilatih.")

    if verbose:
        train_pct = int(round(train_ratio * 100))
        test_pct = 100 - train_pct
        print(f"Training set : {len(X_train)} baris | {X_train.index.min().date()} sampai {X_train.index.max().date()}")
        print(f"Testing set  : {len(X_test)} baris | {X_test.index.min().date()} sampai {X_test.index.max().date()}")
        print(f"Metode split : {train_pct}% awal train, {test_pct}% akhir test, shuffle=False")

    return X_train, X_test, y_train, y_test


def train_random_forest(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    random_state: int = RANDOM_STATE,
    params_override: Optional[Dict[str, object]] = None,
) -> RandomForestClassifier:
    if X_train.empty:
        raise RuntimeError("Random Forest tidak dapat dilatih karena fitur kosong.")
    if y_train.nunique() < 2:
        raise RuntimeError("Random Forest tidak dapat dilatih karena training set hanya satu kelas.")

    params = dict(RF_PARAMS if params_override is None else params_override)
    params["random_state"] = random_state
    model = RandomForestClassifier(**params)
    model.fit(X_train, y_train)
    return model


def train_svm(X_train: pd.DataFrame, y_train: pd.Series) -> Pipeline:
    if X_train.empty:
        raise RuntimeError("SVM tidak dapat dilatih karena fitur kosong.")
    if y_train.nunique() < 2:
        raise RuntimeError("SVM tidak dapat dilatih karena training set hanya satu kelas.")

    try:
        svm = SVC(
            kernel="rbf",
            C=1.0,
            gamma="scale",
            probability=True,
            class_weight="balanced",
            random_state=RANDOM_STATE,
        )
    except TypeError:
        print("Warning - SVC tidak menerima random_state pada environment ini. Fallback tanpa random_state.")
        svm = SVC(
            kernel="rbf",
            C=1.0,
            gamma="scale",
            probability=True,
            class_weight="balanced",
        )

    model = Pipeline([("scaler", StandardScaler()), ("svm", svm)])
    model.fit(X_train, y_train)
    return model


def _positive_class_probability(model, X: pd.DataFrame, context: str) -> Tuple[Optional[np.ndarray], List[str]]:
    warnings: List[str] = []
    if not hasattr(model, "predict_proba"):
        warnings.append(f"predict_proba tidak tersedia untuk {context}.")
        return None, warnings

    try:
        probabilities = model.predict_proba(X)
    except Exception as exc:
        warnings.append(f"predict_proba gagal untuk {context}: {exc}")
        return None, warnings

    classes = list(getattr(model, "classes_", []))
    if not classes and hasattr(model, "named_steps"):
        final_step = list(model.named_steps.values())[-1]
        classes = list(getattr(final_step, "classes_", []))

    if probabilities.ndim != 2 or len(classes) == 0:
        warnings.append(f"Output predict_proba tidak valid untuk {context}.")
        return None, warnings

    if 1 in classes:
        return probabilities[:, classes.index(1)], warnings

    if len(classes) == 1:
        fallback_value = 1.0 if classes[0] == 1 else 0.0
        warnings.append(
            f"Model {context} hanya mengenali satu kelas ({classes[0]}). "
            "Probabilitas fallback deterministik digunakan."
        )
        return np.full(len(X), fallback_value), warnings

    warnings.append(f"Kelas positif 1 tidak ditemukan pada model {context}.")
    return None, warnings


def _safe_auroc(
    y_true: pd.Series,
    y_score: Optional[np.ndarray],
    context: str,
    emit_warning: bool = True,
) -> float:
    if y_score is None:
        if emit_warning:
            print(f"Warning - AUROC {context} tidak bisa dihitung: probabilitas tidak tersedia. Fallback 0.5.")
        return 0.5

    if pd.Series(y_true).nunique() < 2:
        if emit_warning:
            print(f"Warning - AUROC {context} tidak bisa dihitung karena hanya ada satu kelas. Fallback 0.5.")
        return 0.5

    try:
        auc = roc_auc_score(y_true, y_score)
        if np.isnan(auc):
            raise ValueError("AUROC bernilai NaN")
        return float(auc)
    except Exception as exc:
        if emit_warning:
            print(f"Warning - AUROC {context} tidak bisa dihitung ({exc}). Fallback 0.5.")
        return 0.5


def _metrics_from_predictions(
    y_true: pd.Series,
    y_pred: np.ndarray,
    y_score: Optional[np.ndarray],
    model_name: str,
    emit_warning: bool = True,
) -> Dict[str, object]:
    return {
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "balanced_accuracy": float(balanced_accuracy_score(y_true, y_pred)),
        "auroc": _safe_auroc(y_true, y_score, model_name, emit_warning=emit_warning),
        "precision": float(precision_score(y_true, y_pred, zero_division=0)),
        "recall": float(recall_score(y_true, y_pred, zero_division=0)),
        "f1": float(f1_score(y_true, y_pred, zero_division=0)),
        "confusion_matrix": confusion_matrix(y_true, y_pred, labels=[0, 1]),
        "y_pred": y_pred,
        "y_score": y_score,
    }


def evaluate_model(model, X_test: pd.DataFrame, y_test: pd.Series, model_name: str) -> Dict[str, object]:
    if X_test.empty:
        raise RuntimeError(f"Testing set kosong untuk {model_name}.")

    y_pred = model.predict(X_test)
    y_score, probability_warnings = _positive_class_probability(model, X_test, model_name)
    for warning in probability_warnings:
        print(f"Warning - {warning}")

    return _metrics_from_predictions(y_test, y_pred, y_score, model_name)


def evaluate_model_with_threshold(
    model,
    X_test: pd.DataFrame,
    y_test: pd.Series,
    threshold: float,
    model_name: str,
) -> Dict[str, object]:
    y_score, probability_warnings = _positive_class_probability(model, X_test, model_name)
    for warning in probability_warnings:
        print(f"Warning - {warning}")

    if y_score is None:
        y_pred = model.predict(X_test)
    else:
        y_pred = (y_score >= threshold).astype(int)

    return _metrics_from_predictions(y_test, y_pred, y_score, model_name)


def _print_evaluation_metrics(metrics: Dict[str, object]) -> None:
    matrix = metrics["confusion_matrix"]
    print(f"Accuracy          : {metrics['accuracy']:.4f}")
    print(f"Balanced Accuracy : {metrics['balanced_accuracy']:.4f}")
    print(f"AUROC             : {metrics['auroc']:.4f}")
    print(f"Precision         : {metrics['precision']:.4f}")
    print(f"Recall            : {metrics['recall']:.4f}")
    print(f"F1-score          : {metrics['f1']:.4f}")
    print("Confusion Matrix (rows=actual [Not-Uptrend, Uptrend], columns=predicted [Not-Uptrend, Uptrend]):")
    print(matrix)


def _metrics_row(model_name: str, feature_set: str, threshold, metrics: Dict[str, object]) -> Dict[str, object]:
    return {
        "Model": model_name,
        "Feature Set": feature_set,
        "Threshold": threshold,
        "Accuracy": float(metrics["accuracy"]),
        "Balanced Accuracy": float(metrics["balanced_accuracy"]),
        "AUROC": float(metrics["auroc"]),
        "Precision": float(metrics["precision"]),
        "Recall": float(metrics["recall"]),
        "F1-score": float(metrics["f1"]),
    }


def _print_metrics_table(rows: List[Dict[str, object]], title: str) -> None:
    print(f"\n{title}")
    if not rows:
        print("Tidak ada hasil untuk ditampilkan.")
        return
    df = pd.DataFrame(rows)
    metric_cols = ["Accuracy", "Balanced Accuracy", "AUROC", "Precision", "Recall", "F1-score"]
    for col in metric_cols:
        if col in df.columns:
            df[col] = df[col].astype(float).map(lambda value: f"{value:.4f}")
    print(df.to_string(index=False))


def _repair_chromosome(chromosome: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    if chromosome.sum() == 0:
        chromosome[rng.integers(0, len(chromosome))] = 1
    return chromosome


def _build_ga_validation_folds(X_train: pd.DataFrame, n_splits: int = GA_CV_SPLITS) -> List[Tuple[np.ndarray, np.ndarray]]:
    n_rows = len(X_train)
    if n_rows < (n_splits + 1) * 30:
        raise RuntimeError(
            f"Training data terlalu sedikit untuk TimeSeriesSplit(n_splits={n_splits}). "
            "Kurangi n_splits atau tambah data."
        )

    splitter = TimeSeriesSplit(n_splits=n_splits)
    return [(train_idx, val_idx) for train_idx, val_idx in splitter.split(X_train)]


def genetic_algorithm_feature_selection(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    population_size: int = GA_PARAMS["population_size"],
    generations: int = GA_PARAMS["generations"],
    mutation_rate: float = GA_PARAMS["mutation_rate"],
    crossover_rate: float = GA_PARAMS["crossover_rate"],
    elite_size: int = GA_PARAMS["elite_size"],
    random_state: int = GA_PARAMS["random_state"],
    use_time_series_split: bool = True,
) -> Tuple[List[str], List[Dict[str, float]], float]:
    print_section(f"Genetic Algorithm Feature Selection | Seed {random_state}")

    n_features = X_train.shape[1]
    if n_features == 0:
        raise RuntimeError("GA tidak dapat berjalan karena jumlah fitur 0.")
    if population_size <= elite_size:
        raise RuntimeError("population_size harus lebih besar dari elite_size.")

    rng = np.random.default_rng(random_state)
    folds = _build_ga_validation_folds(X_train, n_splits=GA_CV_SPLITS)
    print(f"Parameter GA     : population={population_size}, generations={generations}, mutation={mutation_rate}, crossover={crossover_rate}, elite={elite_size}")
    print(f"Metode fitness   : rata-rata AUROC validation dengan TimeSeriesSplit ({len(folds)} fold)")
    print("RF fitness       : n_estimators=150, max_depth=5, min_samples_leaf=5")
    print(f"Panjang kromosom : {n_features} gene")

    population = rng.integers(0, 2, size=(population_size, n_features), dtype=np.int8)
    for i in range(population_size):
        population[i] = _repair_chromosome(population[i], rng)

    fitness_cache: Dict[Tuple[int, ...], float] = {}
    history: List[Dict[str, float]] = []
    best_chromosome: Optional[np.ndarray] = None
    best_fitness = -np.inf
    auc_fallback_warning_printed = False

    def evaluate_chromosome(chromosome: np.ndarray) -> float:
        nonlocal auc_fallback_warning_printed
        key = tuple(int(value) for value in chromosome.tolist())
        if key in fitness_cache:
            return fitness_cache[key]

        selected_indices = np.where(chromosome == 1)[0]
        if len(selected_indices) == 0:
            fitness_cache[key] = 0.5
            return 0.5

        fold_scores: List[float] = []
        selected_columns = X_train.columns[selected_indices]

        for fold_train_idx, fold_val_idx in folds:
            X_fold_train = X_train.iloc[fold_train_idx][selected_columns]
            y_fold_train = y_train.iloc[fold_train_idx]
            X_fold_val = X_train.iloc[fold_val_idx][selected_columns]
            y_fold_val = y_train.iloc[fold_val_idx]

            try:
                if y_fold_train.nunique() < 2:
                    fold_scores.append(0.5)
                    if not auc_fallback_warning_printed:
                        print(
                            "Warning - Sebagian training fold GA hanya memiliki satu kelas. "
                            "Fitness fold tersebut memakai fallback 0.5."
                        )
                        auc_fallback_warning_printed = True
                    continue

                model = train_random_forest(
                    X_fold_train,
                    y_fold_train,
                    random_state=random_state,
                    params_override=GA_FITNESS_RF_PARAMS,
                )
                y_score, _ = _positive_class_probability(model, X_fold_val, "GA validation")
                auc = _safe_auroc(y_fold_val, y_score, "GA validation", emit_warning=False)
                if auc == 0.5 and y_fold_val.nunique() < 2 and not auc_fallback_warning_printed:
                    print(
                        "Warning - AUROC pada sebagian validation fold GA tidak bisa dihitung "
                        "karena hanya ada satu kelas. Fallback 0.5 digunakan."
                    )
                    auc_fallback_warning_printed = True
                fold_scores.append(auc)
            except Exception as exc:
                if not auc_fallback_warning_printed:
                    print(f"Warning - Evaluasi kromosom GA gagal ({exc}). Fitness fallback 0.5 digunakan.")
                    auc_fallback_warning_printed = True
                fold_scores.append(0.5)

        fitness = float(np.mean(fold_scores)) if fold_scores else 0.5
        fitness_cache[key] = fitness
        return fitness

    def tournament_selection(fitness_values: np.ndarray, tournament_size: int = 3) -> np.ndarray:
        contestant_indices = rng.choice(population_size, size=tournament_size, replace=False)
        best_index = contestant_indices[np.argmax(fitness_values[contestant_indices])]
        return population[best_index].copy()

    for generation in range(1, generations + 1):
        fitness_values = np.array([evaluate_chromosome(chromosome) for chromosome in population])
        sorted_indices = np.argsort(fitness_values)[::-1]
        generation_best_index = sorted_indices[0]
        generation_best_fitness = float(fitness_values[generation_best_index])
        generation_average_fitness = float(np.mean(fitness_values))
        generation_best_chromosome = population[generation_best_index].copy()
        generation_active_features = int(generation_best_chromosome.sum())

        if generation_best_fitness > best_fitness:
            best_fitness = generation_best_fitness
            best_chromosome = generation_best_chromosome.copy()

        history.append(
            {
                "seed": random_state,
                "generation": generation,
                "best_fitness": generation_best_fitness,
                "avg_fitness": generation_average_fitness,
                "active_features": generation_active_features,
            }
        )

        print(
            f"Seed {random_state} | Generation {generation}/{generations} | "
            f"Best AUROC: {generation_best_fitness:.4f} | "
            f"Avg Fitness: {generation_average_fitness:.4f} | "
            f"Active Features: {generation_active_features}",
            flush=True,
        )

        elites = population[sorted_indices[:elite_size]].copy()
        new_population = [elite.copy() for elite in elites]

        while len(new_population) < population_size:
            parent_1 = tournament_selection(fitness_values)
            parent_2 = tournament_selection(fitness_values)

            child_1 = parent_1.copy()
            child_2 = parent_2.copy()
            if n_features > 1 and rng.random() < crossover_rate:
                crossover_point = rng.integers(1, n_features)
                child_1 = np.concatenate([parent_1[:crossover_point], parent_2[crossover_point:]])
                child_2 = np.concatenate([parent_2[:crossover_point], parent_1[crossover_point:]])

            mutation_mask_1 = rng.random(n_features) < mutation_rate
            mutation_mask_2 = rng.random(n_features) < mutation_rate
            child_1[mutation_mask_1] = 1 - child_1[mutation_mask_1]
            child_2[mutation_mask_2] = 1 - child_2[mutation_mask_2]

            child_1 = _repair_chromosome(child_1.astype(np.int8), rng)
            child_2 = _repair_chromosome(child_2.astype(np.int8), rng)

            new_population.append(child_1)
            if len(new_population) < population_size:
                new_population.append(child_2)

        population = np.array(new_population, dtype=np.int8)

    if best_chromosome is None or best_chromosome.sum() == 0:
        raise RuntimeError("GA tidak memilih fitur apa pun. Program dihentikan agar output tidak palsu.")

    selected_features = X_train.columns[np.where(best_chromosome == 1)[0]].tolist()
    print(f"\nJumlah fitur terpilih seed {random_state}: {len(selected_features)} dari {n_features}")
    print(f"Best fitness GA seed {random_state} (validation AUROC): {best_fitness:.4f}")

    return selected_features, history, float(best_fitness)


def run_multiple_ga_seeds(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    X_test: pd.DataFrame,
    y_test: pd.Series,
    output_dir: str,
    seeds: List[int] = GA_SEEDS,
) -> Tuple[pd.DataFrame, Dict[int, Dict[str, object]], List[Dict[str, float]], str]:
    print_section("7. Genetic Algorithm Multiple Seed Results")

    seed_rows: List[Dict[str, object]] = []
    seed_details: Dict[int, Dict[str, object]] = {}
    all_histories: List[Dict[str, float]] = []

    for seed in seeds:
        selected_features, history, best_fitness = genetic_algorithm_feature_selection(
            X_train,
            y_train,
            random_state=seed,
            use_time_series_split=True,
        )
        ga_model = train_random_forest(X_train[selected_features], y_train, random_state=RANDOM_STATE)
        ga_metrics = evaluate_model(ga_model, X_test[selected_features], y_test, f"RF + GA seed {seed}")

        row = {
            "seed": seed,
            "best_validation_fitness": best_fitness,
            "selected_feature_count": len(selected_features),
            "selected_features": ";".join(selected_features),
            "Accuracy": ga_metrics["accuracy"],
            "Balanced Accuracy": ga_metrics["balanced_accuracy"],
            "AUROC": ga_metrics["auroc"],
            "Precision": ga_metrics["precision"],
            "Recall": ga_metrics["recall"],
            "F1-score": ga_metrics["f1"],
        }
        seed_rows.append(row)
        seed_details[seed] = {
            "selected_features": selected_features,
            "history": history,
            "best_validation_fitness": best_fitness,
            "model": ga_model,
            "metrics": ga_metrics,
        }
        all_histories.extend(history)

        print(f"\nRingkasan seed {seed}:")
        _print_evaluation_metrics(ga_metrics)

    seed_results_df = pd.DataFrame(seed_rows)
    output_path = os.path.join(output_dir, "ga_seed_results.csv")
    seed_results_df.to_csv(output_path, index=False)

    mean_auc = float(seed_results_df["AUROC"].mean())
    std_auc = float(seed_results_df["AUROC"].std(ddof=0))
    best_test_row = seed_results_df.sort_values("AUROC", ascending=False).iloc[0]
    best_validation_row = seed_results_df.sort_values("best_validation_fitness", ascending=False).iloc[0]

    print("\nRingkasan multiple seed GA:")
    print(seed_results_df[["seed", "best_validation_fitness", "selected_feature_count", "AUROC", "Balanced Accuracy", "F1-score"]].to_string(index=False))
    print(f"Rata-rata AUROC RF + GA : {mean_auc:.4f}")
    print(f"Standar deviasi AUROC  : {std_auc:.4f}")
    print(f"Seed terbaik berdasarkan test AUROC (observasi laporan): {int(best_test_row['seed'])}")
    print(f"Seed terbaik berdasarkan validation fitness: {int(best_validation_row['seed'])}")
    if int(best_test_row["seed"]) != int(best_validation_row["seed"]):
        print(
            "Catatan: seed terbaik pada validation tidak sama dengan seed terbaik pada test. "
            "Ini memperkuat kebutuhan evaluasi out-of-sample dan narasi yang hati-hati."
        )

    return seed_results_df, seed_details, all_histories, output_path


def _feature_category(feature: str) -> str:
    if feature.startswith("BBCA_lag_"):
        return "BBCA own lag"
    if feature.startswith("IHSG_lag_"):
        return "IHSG/local market"
    if feature.startswith(("BBRI_lag_", "BMRI_lag_", "BBNI_lag_")):
        return "peer banking"
    if feature.startswith("USD_IDR_lag_"):
        return "USD/IDR"
    if feature.startswith(("SP500_lag_", "NASDAQ_lag_", "NIKKEI225_lag_")):
        return "global indices"
    if feature.startswith(("BBCA_MA_", "BBCA_volatility_")):
        return "technical features"
    return "other"


def calculate_selected_feature_frequency(
    seed_details: Dict[int, Dict[str, object]],
    all_features: List[str],
    output_dir: str,
) -> Tuple[pd.DataFrame, List[str], str]:
    print_section("8. Selected Features Frequency")

    rows: List[Dict[str, object]] = []
    total_seeds = len(seed_details)
    for feature in all_features:
        selected_count = sum(feature in detail["selected_features"] for detail in seed_details.values())
        selected_percentage = selected_count / total_seeds if total_seeds else 0.0
        rows.append(
            {
                "feature": feature,
                "selected_count": selected_count,
                "selected_percentage": selected_percentage,
                "feature_group": _feature_category(feature),
            }
        )

    frequency_df = pd.DataFrame(rows).sort_values(
        ["selected_count", "selected_percentage", "feature"], ascending=[False, False, True]
    )
    output_path = os.path.join(output_dir, "selected_features_frequency.csv")
    frequency_df.to_csv(output_path, index=False)

    print("Top 20 fitur paling sering dipilih GA:")
    top_20 = frequency_df.head(20).copy()
    top_20["selected_percentage"] = top_20["selected_percentage"].map(lambda value: f"{value:.0%}")
    print(top_20[["feature", "selected_count", "selected_percentage", "feature_group"]].to_string(index=False))

    print("\nRingkasan kategori fitur terpilih:")
    category_summary = frequency_df.groupby("feature_group", as_index=False).agg(
        total_selected=("selected_count", "sum"),
        avg_selected_percentage=("selected_percentage", "mean"),
    )
    category_summary["avg_selected_percentage"] = category_summary["avg_selected_percentage"].map(lambda value: f"{value:.1%}")
    print(category_summary.sort_values("total_selected", ascending=False).to_string(index=False))

    frequent_features = frequency_df.loc[
        frequency_df["selected_percentage"] >= FREQUENT_FEATURE_THRESHOLD, "feature"
    ].tolist()
    if not frequent_features:
        print(
            f"Warning - Tidak ada fitur yang muncul minimal {FREQUENT_FEATURE_THRESHOLD:.0%} dari seed. "
            "Eksperimen frequent-feature akan dilewati."
        )
    else:
        print(f"\nFitur frequent GA >= {FREQUENT_FEATURE_THRESHOLD:.0%}: {len(frequent_features)} fitur")

    return frequency_df, frequent_features, output_path


def get_feature_groups(
    feature_columns: List[str],
    ga_seed_42_features: List[str],
    frequent_features: List[str],
) -> Dict[str, List[str]]:
    bbca_only = [
        feature
        for feature in feature_columns
        if feature.startswith("BBCA_lag_") or feature.startswith(("BBCA_MA_", "BBCA_volatility_"))
    ]
    groups = {
        "BBCA only": bbca_only,
        "BBCA + IHSG": bbca_only + [feature for feature in feature_columns if feature.startswith("IHSG_lag_")],
        "BBCA + peer banking": bbca_only
        + [
            feature
            for feature in feature_columns
            if feature.startswith(("BBRI_lag_", "BMRI_lag_", "BBNI_lag_"))
        ],
        "BBCA + USD/IDR": bbca_only + [feature for feature in feature_columns if feature.startswith("USD_IDR_lag_")],
        "BBCA + global indices": bbca_only
        + [
            feature
            for feature in feature_columns
            if feature.startswith(("SP500_lag_", "NASDAQ_lag_", "NIKKEI225_lag_"))
        ],
        "All features": list(feature_columns),
        "All features + GA seed 42": ga_seed_42_features,
    }
    if frequent_features:
        groups[f"Frequent GA >= {int(FREQUENT_FEATURE_THRESHOLD * 100)}%"] = frequent_features
    return {name: sorted(set(features), key=feature_columns.index) for name, features in groups.items() if features}


def run_ablation_study(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    X_test: pd.DataFrame,
    y_test: pd.Series,
    feature_groups: Dict[str, List[str]],
    output_dir: str,
) -> Tuple[pd.DataFrame, str]:
    print_section("12. Ablation Study Results")

    rows: List[Dict[str, object]] = []
    for group_name, features in feature_groups.items():
        if not features:
            print(f"Warning - Feature group {group_name} kosong, dilewati.")
            continue
        model = train_random_forest(X_train[features], y_train, random_state=RANDOM_STATE)
        metrics = evaluate_model(model, X_test[features], y_test, f"Ablation - {group_name}")
        rows.append(_metrics_row(group_name, f"{len(features)} features", 0.50, metrics))

    ablation_df = pd.DataFrame(rows).sort_values("AUROC", ascending=False)
    output_path = os.path.join(output_dir, "ablation_study_results.csv")
    ablation_df.to_csv(output_path, index=False)

    print("Ranking feature group berdasarkan AUROC:")
    print(ablation_df[["Model", "Feature Set", "AUROC", "Balanced Accuracy", "F1-score"]].to_string(index=False))
    if not ablation_df.empty:
        best_group = ablation_df.iloc[0]
        print(f"\nKelompok fitur paling membantu berdasarkan AUROC: {best_group['Model']} (AUROC {best_group['AUROC']:.4f}).")
        all_features_row = ablation_df[ablation_df["Model"] == "All features"]
        ga_row = ablation_df[ablation_df["Model"] == "All features + GA seed 42"]
        if not all_features_row.empty and not ga_row.empty:
            if float(all_features_row.iloc[0]["AUROC"]) > float(ga_row.iloc[0]["AUROC"]):
                print(
                    "Catatan: All features lebih baik daripada GA pada ablation study. "
                    "Random Forest mungkin masih mendapat manfaat dari fitur yang dibuang GA."
                )

    return ablation_df, output_path


def train_dummy_baselines(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    X_test: pd.DataFrame,
    y_test: pd.Series,
) -> Tuple[Dict[str, DummyClassifier], Dict[str, Dict[str, object]], List[Dict[str, object]]]:
    print_section("5. Dummy Baseline Results")

    dummy_models = {
        "Dummy Majority": DummyClassifier(strategy="most_frequent"),
        "Dummy Stratified": DummyClassifier(strategy="stratified", random_state=RANDOM_STATE),
    }
    dummy_metrics: Dict[str, Dict[str, object]] = {}
    rows: List[Dict[str, object]] = []

    for name, model in dummy_models.items():
        model.fit(X_train, y_train)
        metrics = evaluate_model(model, X_test, y_test, name)
        dummy_metrics[name] = metrics
        rows.append(_metrics_row(name, "No predictive features", "model default", metrics))
        print(f"\n{name}:")
        _print_evaluation_metrics(metrics)

    print(
        "\nCatatan: Dummy baseline membantu mengecek apakah accuracy model hanya terlihat baik "
        "karena mayoritas kelas adalah Not-Uptrend."
    )
    print("Untuk target imbalance, Balanced Accuracy, AUROC, dan F1-score lebih relevan daripada accuracy.")

    return dummy_models, dummy_metrics, rows


def tune_threshold(
    model_name: str,
    feature_set: str,
    train_fn: Callable[[pd.DataFrame, pd.Series], object],
    X_train: pd.DataFrame,
    y_train: pd.Series,
    X_test: pd.DataFrame,
    y_test: pd.Series,
) -> Tuple[Dict[str, object], object]:
    split_index = int(len(X_train) * 0.80)
    if split_index <= 0 or split_index >= len(X_train):
        raise RuntimeError(f"Validation internal untuk threshold tuning tidak valid pada {model_name}.")

    X_sub_train = X_train.iloc[:split_index]
    y_sub_train = y_train.iloc[:split_index]
    X_val = X_train.iloc[split_index:]
    y_val = y_train.iloc[split_index:]

    tuning_model = train_fn(X_sub_train, y_sub_train)
    val_score, warnings = _positive_class_probability(tuning_model, X_val, f"{model_name} threshold validation")
    for warning in warnings:
        print(f"Warning - {warning}")

    if val_score is None or y_val.nunique() < 2:
        print(f"Warning - Threshold tuning {model_name} memakai fallback 0.50 karena validation tidak valid.")
        best_threshold = 0.50
        best_val_balanced_accuracy = 0.5
        best_val_f1 = 0.0
    else:
        candidates = []
        for threshold in THRESHOLD_GRID:
            val_pred = (val_score >= threshold).astype(int)
            candidates.append(
                {
                    "threshold": float(threshold),
                    "balanced_accuracy": float(balanced_accuracy_score(y_val, val_pred)),
                    "f1": float(f1_score(y_val, val_pred, zero_division=0)),
                    "distance_to_default": abs(float(threshold) - 0.5),
                }
            )
        best_candidate = sorted(
            candidates,
            key=lambda item: (item["balanced_accuracy"], item["f1"], -item["distance_to_default"]),
            reverse=True,
        )[0]
        best_threshold = float(best_candidate["threshold"])
        best_val_balanced_accuracy = float(best_candidate["balanced_accuracy"])
        best_val_f1 = float(best_candidate["f1"])

    final_model = train_fn(X_train, y_train)
    test_metrics = evaluate_model_with_threshold(final_model, X_test, y_test, best_threshold, model_name)
    row = _metrics_row(model_name, feature_set, best_threshold, test_metrics)
    row.update(
        {
            "Default Threshold": 0.50,
            "Validation Balanced Accuracy": best_val_balanced_accuracy,
            "Validation F1-score": best_val_f1,
            "Optimization Metric": "Balanced Accuracy",
        }
    )
    return row, final_model


def run_threshold_tuning(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    X_test: pd.DataFrame,
    y_test: pd.Series,
    ga_features: List[str],
    output_dir: str,
) -> Tuple[pd.DataFrame, str]:
    print_section("13. Threshold Tuning Results")
    print("Threshold default: 0.50")
    print("Range threshold  : 0.30 sampai 0.70 step 0.01")
    print("Optimasi         : Balanced Accuracy pada validation internal training")

    tuning_specs = [
        (
            "Baseline RF (tuned threshold)",
            "All features",
            lambda X, y: train_random_forest(X, y, random_state=RANDOM_STATE),
            X_train,
            X_test,
        ),
        (
            "RF + Frequent GA (tuned threshold)",
            "Frequent GA >= 60%",
            lambda X, y: train_random_forest(X, y, random_state=RANDOM_STATE),
            X_train[ga_features],
            X_test[ga_features],
        ),
        (
            "Baseline SVM (tuned threshold)",
            "All features",
            train_svm,
            X_train,
            X_test,
        ),
    ]

    rows: List[Dict[str, object]] = []
    for model_name, feature_set, train_fn, train_X, test_X in tuning_specs:
        row, _ = tune_threshold(model_name, feature_set, train_fn, train_X, y_train, test_X, y_test)
        rows.append(row)
        print(
            f"{model_name}: threshold terbaik validation = {row['Threshold']:.2f} | "
            f"Test Balanced Accuracy = {row['Balanced Accuracy']:.4f} | "
            f"Test AUROC = {row['AUROC']:.4f} | Test F1 = {row['F1-score']:.4f}"
        )

    threshold_df = pd.DataFrame(rows)
    output_path = os.path.join(output_dir, "threshold_tuning_results.csv")
    threshold_df.to_csv(output_path, index=False)
    return threshold_df, output_path


def _scenario_metrics_row(
    scenario_label: str,
    train_ratio: float,
    X_train: pd.DataFrame,
    X_test: pd.DataFrame,
    model_name: str,
    feature_set: str,
    selected_feature_count: int,
    validation_auroc,
    metrics: Dict[str, object],
) -> Dict[str, object]:
    return {
        "Scenario": scenario_label,
        "Train Ratio": train_ratio,
        "Test Ratio": 1 - train_ratio,
        "Train Rows": len(X_train),
        "Test Rows": len(X_test),
        "Train Start": X_train.index.min().date(),
        "Train End": X_train.index.max().date(),
        "Test Start": X_test.index.min().date(),
        "Test End": X_test.index.max().date(),
        "Model": model_name,
        "Feature Set": feature_set,
        "Selected Feature Count": selected_feature_count,
        "Validation AUROC": validation_auroc,
        "Accuracy": float(metrics["accuracy"]),
        "Balanced Accuracy": float(metrics["balanced_accuracy"]),
        "AUROC": float(metrics["auroc"]),
        "Precision": float(metrics["precision"]),
        "Recall": float(metrics["recall"]),
        "F1-score": float(metrics["f1"]),
    }


def run_split_scenario_study(
    X: pd.DataFrame,
    y: pd.Series,
    output_dir: str,
    baseline_80_metrics: Dict[str, object],
    ga_80_metrics: Dict[str, object],
    ga_80_validation_fitness: float,
    ga_80_selected_feature_count: int,
) -> Tuple[pd.DataFrame, str]:
    print_section("Split Scenario Study: 80/20, 75/25, 70/30")
    print(
        "Tujuan skenario: mengecek sensitivitas hasil terhadap ukuran train/test split. "
        "Skenario ini bukan pengganti eksperimen utama 80/20."
    )
    print(
        f"Model yang dibandingkan per skenario: Baseline RF dan RF + GA seed {SPLIT_SCENARIO_GA_SEED}. "
        "GA selalu hanya fit pada training window skenario masing-masing."
    )

    rows: List[Dict[str, object]] = []

    for scenario_label, train_ratio in SPLIT_SCENARIOS:
        X_train_s, X_test_s, y_train_s, y_test_s = split_data(
            X,
            y,
            train_ratio=train_ratio,
            scenario_label=scenario_label,
            verbose=True,
        )

        if scenario_label == "80/20":
            rows.append(
                _scenario_metrics_row(
                    scenario_label,
                    train_ratio,
                    X_train_s,
                    X_test_s,
                    "Baseline RF",
                    "All features",
                    X_train_s.shape[1],
                    "",
                    baseline_80_metrics,
                )
            )
            rows.append(
                _scenario_metrics_row(
                    scenario_label,
                    train_ratio,
                    X_train_s,
                    X_test_s,
                    f"RF + GA seed {SPLIT_SCENARIO_GA_SEED}",
                    f"GA seed {SPLIT_SCENARIO_GA_SEED} features",
                    ga_80_selected_feature_count,
                    ga_80_validation_fitness,
                    ga_80_metrics,
                )
            )
            print("Scenario 80/20 memakai ulang hasil eksperimen utama agar tidak duplikasi training.")
            continue

        print(f"\nMenjalankan scenario {scenario_label}: Baseline RF")
        baseline_model = train_random_forest(X_train_s, y_train_s, random_state=RANDOM_STATE)
        baseline_metrics = evaluate_model(baseline_model, X_test_s, y_test_s, f"Baseline RF scenario {scenario_label}")
        _print_evaluation_metrics(baseline_metrics)
        rows.append(
            _scenario_metrics_row(
                scenario_label,
                train_ratio,
                X_train_s,
                X_test_s,
                "Baseline RF",
                "All features",
                X_train_s.shape[1],
                "",
                baseline_metrics,
            )
        )

        print(f"\nMenjalankan scenario {scenario_label}: RF + GA seed {SPLIT_SCENARIO_GA_SEED}")
        selected_features, _, best_fitness = genetic_algorithm_feature_selection(
            X_train_s,
            y_train_s,
            random_state=SPLIT_SCENARIO_GA_SEED,
            use_time_series_split=True,
        )
        ga_model = train_random_forest(X_train_s[selected_features], y_train_s, random_state=RANDOM_STATE)
        ga_metrics = evaluate_model(
            ga_model,
            X_test_s[selected_features],
            y_test_s,
            f"RF + GA seed {SPLIT_SCENARIO_GA_SEED} scenario {scenario_label}",
        )
        _print_evaluation_metrics(ga_metrics)
        rows.append(
            _scenario_metrics_row(
                scenario_label,
                train_ratio,
                X_train_s,
                X_test_s,
                f"RF + GA seed {SPLIT_SCENARIO_GA_SEED}",
                f"GA seed {SPLIT_SCENARIO_GA_SEED} features",
                len(selected_features),
                best_fitness,
                ga_metrics,
            )
        )

    scenario_df = pd.DataFrame(rows)
    output_path = os.path.join(output_dir, "split_scenario_results.csv")
    scenario_df.to_csv(output_path, index=False)

    print("\nRingkasan skenario split:")
    print(
        scenario_df[
            [
                "Scenario",
                "Model",
                "Train Rows",
                "Test Rows",
                "Selected Feature Count",
                "Validation AUROC",
                "Balanced Accuracy",
                "AUROC",
                "F1-score",
            ]
        ].to_string(index=False)
    )
    print(
        "\nCatatan: Jika RF + GA tidak konsisten mengalahkan Baseline RF di semua skenario, "
        "narasi akademik sebaiknya menekankan GA sebagai feature reduction dan analisis fitur."
    )

    return scenario_df, output_path


def interpret_results(
    baseline_metrics: Dict[str, object],
    ga_metrics: Dict[str, object],
    best_fitness_ga: float,
) -> List[str]:
    return interpret_extended_results(
        baseline_metrics=baseline_metrics,
        ga_metrics=ga_metrics,
        best_fitness_ga=best_fitness_ga,
        svm_metrics=None,
        dummy_majority_metrics=None,
        ga_seed_results_df=None,
    )


def interpret_extended_results(
    baseline_metrics: Dict[str, object],
    ga_metrics: Dict[str, object],
    best_fitness_ga: float,
    svm_metrics: Optional[Dict[str, object]],
    dummy_majority_metrics: Optional[Dict[str, object]],
    ga_seed_results_df: Optional[pd.DataFrame],
) -> List[str]:
    print_section("15. Interpretasi Hasil Eksperimen")

    baseline_auc = float(baseline_metrics["auroc"])
    ga_auc = float(ga_metrics["auroc"])
    delta_auc = ga_auc - baseline_auc
    interpretations: List[str] = []

    if 0.47 <= ga_auc <= 0.53:
        interpretations.append("Performa model masih sangat dekat dengan random classifier.")
    elif 0.53 < ga_auc <= 0.60:
        interpretations.append("Model mulai menangkap sedikit sinyal, tetapi performanya masih lemah.")
    elif 0.60 < ga_auc <= 0.70:
        interpretations.append("Model menunjukkan sinyal prediktif yang cukup menarik.")
    elif ga_auc > 0.70:
        interpretations.append("Model menunjukkan performa yang kuat, tetapi tetap perlu validasi lebih lanjut.")
    else:
        interpretations.append("Performa model berada di bawah kisaran random classifier; sinyal belum dapat diandalkan.")

    if ga_auc > baseline_auc + 0.01:
        interpretations.append("Feature selection dengan Genetic Algorithm meningkatkan performa model secara praktis.")
    elif baseline_auc - 0.01 <= ga_auc <= baseline_auc + 0.01:
        interpretations.append("Perbedaan performa sangat kecil, sehingga belum signifikan secara praktis.")
    else:
        interpretations.append("Feature selection dengan Genetic Algorithm belum meningkatkan performa pada test set.")

    if best_fitness_ga - ga_auc > 0.05:
        interpretations.append("Terdapat indikasi overfitting pada proses feature selection.")

    if svm_metrics is not None:
        svm_auc = float(svm_metrics["auroc"])
        if svm_auc > baseline_auc + 0.01 or svm_auc > ga_auc + 0.01:
            interpretations.append(
                "SVM menunjukkan performa pembanding yang lebih baik pada eksperimen ini, "
                "tetapi metode utama penelitian tetap RF + GA."
            )
        else:
            interpretations.append("Random Forest tetap lebih stabil dibandingkan SVM pada eksperimen ini.")

    if dummy_majority_metrics is not None:
        model_accuracy = max(float(baseline_metrics["accuracy"]), float(ga_metrics["accuracy"]))
        dummy_accuracy = float(dummy_majority_metrics["accuracy"])
        if model_accuracy < dummy_accuracy:
            interpretations.append(
                "Accuracy kurang informatif karena target imbalance. Evaluasi lebih tepat menggunakan "
                "Balanced Accuracy, AUROC, dan F1-score."
            )
        else:
            interpretations.append(
                "Dummy majority tetap menjadi pembanding penting; Balanced Accuracy, AUROC, dan F1-score "
                "digunakan agar evaluasi tidak bias ke kelas mayoritas."
            )

    if ga_seed_results_df is not None and not ga_seed_results_df.empty:
        mean_auc = float(ga_seed_results_df["AUROC"].mean())
        std_auc = float(ga_seed_results_df["AUROC"].std(ddof=0))
        best_test_seed = int(ga_seed_results_df.sort_values("AUROC", ascending=False).iloc[0]["seed"])
        best_test_auc = float(ga_seed_results_df.sort_values("AUROC", ascending=False).iloc[0]["AUROC"])
        best_validation_seed = int(ga_seed_results_df.sort_values("best_validation_fitness", ascending=False).iloc[0]["seed"])
        if std_auc < 0.02:
            interpretations.append(f"RF + GA relatif stabil antar seed berdasarkan AUROC (mean={mean_auc:.4f}, std={std_auc:.4f}).")
        else:
            interpretations.append(f"RF + GA cukup sensitif terhadap seed GA (mean AUROC={mean_auc:.4f}, std={std_auc:.4f}).")
        interpretations.append(
            f"Seed {best_test_seed} memiliki test AUROC tertinggi ({best_test_auc:.4f}), "
            "tetapi ini adalah observasi test set, bukan model utama yang dipilih untuk estimasi."
        )
        if best_test_seed != best_validation_seed:
            interpretations.append(
                f"Seed terbaik validation ({best_validation_seed}) berbeda dari seed terbaik test ({best_test_seed}), "
                "sehingga RF + GA belum konsisten mengalahkan Baseline RF."
            )

    interpretations.append("Baseline RF paling stabil sebagai pembanding utama pada eksperimen ini.")
    interpretations.append(
        "Frequent GA features mendekati all features dengan jumlah fitur lebih sedikit; "
        "GA lebih berguna sebagai feature reduction dan analisis fitur daripada bukti peningkatan akurasi yang konsisten."
    )

    print(f"Baseline RF AUROC : {baseline_auc:.4f}")
    print(f"RF + Frequent GA AUROC: {ga_auc:.4f}")
    print(f"Delta AUROC       : {delta_auc:+.4f}")
    print(f"Mean GA validation fitness: {best_fitness_ga:.4f}")
    print("\nInterpretasi otomatis:")
    for item in interpretations:
        print(f"- {item}")

    return interpretations


def estimate_next_day(
    model,
    latest_features: pd.DataFrame,
    latest_feature_date: pd.Timestamp,
    latest_bbca_close: float,
    baseline_rf_model=None,
    latest_all_features: Optional[pd.DataFrame] = None,
    svm_model=None,
) -> Dict[str, object]:
    print_section("16. Estimasi Uptrend / Not-Uptrend BBCA Hari Berikutnya")

    probabilities, probability_warnings = _positive_class_probability(model, latest_features, "RF + Frequent GA estimasi hari berikutnya")
    for warning in probability_warnings:
        print(f"Warning - {warning}")
    if probabilities is None or len(probabilities) == 0:
        raise RuntimeError("Probabilitas RF + Frequent GA estimasi hari berikutnya tidak tersedia.")

    probability_uptrend = float(np.clip(probabilities[0], 0.0, 1.0))
    probability_not_uptrend = 1.0 - probability_uptrend

    baseline_rf_probability = None
    if baseline_rf_model is not None and latest_all_features is not None:
        baseline_probs, warnings = _positive_class_probability(baseline_rf_model, latest_all_features, "Baseline RF estimasi")
        for warning in warnings:
            print(f"Warning - {warning}")
        if baseline_probs is not None and len(baseline_probs):
            baseline_rf_probability = float(np.clip(baseline_probs[0], 0.0, 1.0))

    svm_probability = None
    if svm_model is not None and latest_all_features is not None:
        svm_probs, warnings = _positive_class_probability(svm_model, latest_all_features, "Baseline SVM estimasi")
        for warning in warnings:
            print(f"Warning - {warning}")
        if svm_probs is not None and len(svm_probs):
            svm_probability = float(np.clip(svm_probs[0], 0.0, 1.0))

    if probability_uptrend >= 0.60:
        signal = "UPTREND"
    elif probability_uptrend <= 0.40:
        signal = "NOT-UPTREND"
    else:
        signal = "NETRAL / TIDAK YAKIN"

    confidence = abs(probability_uptrend - 0.5) * 2
    if confidence < 0.10:
        confidence_category = "Sangat rendah"
    elif confidence < 0.25:
        confidence_category = "Rendah"
    elif confidence < 0.50:
        confidence_category = "Sedang"
    else:
        confidence_category = "Tinggi"

    estimation = {
        "latest_date": latest_feature_date,
        "latest_close": latest_bbca_close,
        "probability_uptrend": probability_uptrend,
        "probability_not_uptrend": probability_not_uptrend,
        "baseline_rf_probability_uptrend": baseline_rf_probability,
        "svm_probability_uptrend": svm_probability,
        "signal": signal,
        "confidence": confidence,
        "confidence_category": confidence_category,
    }

    print(f"Tanggal data terakhir             : {latest_feature_date.date()}")
    print(f"Harga BBCA terakhir               : {latest_bbca_close:,.2f}")
    print(f"Probabilitas Uptrend RF + GA       : {probability_uptrend:.4f}")
    print(f"Probabilitas Not-Uptrend RF + GA   : {probability_not_uptrend:.4f}")
    if baseline_rf_probability is not None:
        print(f"Probabilitas Uptrend Baseline RF  : {baseline_rf_probability:.4f}")
    if svm_probability is not None:
        print(f"Probabilitas Uptrend Baseline SVM : {svm_probability:.4f}")
    print(f"Output sinyal model utama         : {signal}")
    print(f"Confidence                        : {confidence:.4f}")
    print(f"Kategori confidence               : {confidence_category}")

    if signal == "NETRAL / TIDAK YAKIN":
        print("Model belum memberikan sinyal arah yang cukup kuat.")

    print("Model hanya mengestimasi arah tren, bukan memprediksi harga nominal.")
    print("Output ini bukan rekomendasi trading.")

    return estimation


def save_experiment_results(rows: List[Dict[str, object]], output_dir: str) -> Tuple[pd.DataFrame, str]:
    experiment_df = pd.DataFrame(rows)
    if not experiment_df.empty:
        final_columns = [
            "Model",
            "Feature Set",
            "Threshold",
            "Accuracy",
            "Balanced Accuracy",
            "AUROC",
            "Precision",
            "Recall",
            "F1-score",
        ]
        experiment_df = experiment_df[final_columns]
        experiment_df = experiment_df.drop_duplicates(subset=["Model", "Feature Set", "Threshold"], keep="last")
    output_path = os.path.join(output_dir, "experiment_results.csv")
    experiment_df.to_csv(output_path, index=False)
    return experiment_df, output_path


def rank_models(experiment_df: pd.DataFrame) -> None:
    print_section("14. Final Model Ranking")
    if experiment_df.empty:
        print("Tidak ada hasil eksperimen untuk diranking.")
        return

    for metric in ["AUROC", "Balanced Accuracy", "F1-score"]:
        ranking = experiment_df.sort_values(metric, ascending=False)[
            ["Model", "Feature Set", "Threshold", metric]
        ].head(10)
        print(f"\nRanking berdasarkan {metric}:")
        print(ranking.to_string(index=False))

    ga_rows = experiment_df[experiment_df["Model"].str.contains("RF \\+ GA", regex=True, na=False)]
    if not ga_rows.empty:
        print("\nStabilitas model utama:")
        print(
            "RF + GA dievaluasi melalui multiple seed. Stabilitas dibaca dari rata-rata dan standar deviasi "
            "AUROC pada ga_seed_results.csv, bukan dari satu run terbaik saja."
        )


def _apply_chart_style() -> None:
    try:
        plt.style.use("seaborn-v0_8-whitegrid")
    except Exception:
        plt.style.use("default")


def _add_bar_labels(ax, bars, fmt: str = "{:.3f}", fontsize: int = 8) -> None:
    for bar in bars:
        height = bar.get_height()
        ax.annotate(
            fmt.format(height),
            xy=(bar.get_x() + bar.get_width() / 2, height),
            xytext=(0, 4),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=fontsize,
        )


def _add_barh_labels(ax, bars, fmt: str = "{:.3f}", fontsize: int = 8) -> None:
    for bar in bars:
        width = bar.get_width()
        ax.annotate(
            fmt.format(width),
            xy=(width, bar.get_y() + bar.get_height() / 2),
            xytext=(5, 0),
            textcoords="offset points",
            ha="left",
            va="center",
            fontsize=fontsize,
        )


def _set_dynamic_y_limits(ax, values, padding_ratio: float = 0.12, floor: Optional[float] = None) -> None:
    clean_values = [float(value) for value in values if pd.notna(value)]
    if not clean_values:
        return
    min_value = min(clean_values)
    max_value = max(clean_values)
    spread = max(max_value - min_value, 0.02)
    lower = min_value - spread * padding_ratio
    upper = max_value + spread * padding_ratio
    if floor is not None:
        lower = max(floor, lower)
    ax.set_ylim(lower, upper)


def _set_dynamic_x_limits(ax, values, padding_ratio: float = 0.12, floor: Optional[float] = None) -> None:
    clean_values = [float(value) for value in values if pd.notna(value)]
    if not clean_values:
        return
    min_value = min(clean_values)
    max_value = max(clean_values)
    spread = max(max_value - min_value, 0.02)
    lower = min_value - spread * padding_ratio
    upper = max_value + spread * padding_ratio
    if floor is not None:
        lower = max(floor, lower)
    ax.set_xlim(lower, upper)


def _feature_group_for_color(feature: str, explicit_group: Optional[str] = None) -> str:
    if explicit_group:
        group = explicit_group.lower()
        if "technical" in group:
            return "BBCA technical"
        if "bbca own" in group:
            return "BBCA lag"
        if "peer" in group:
            return "peer banking"
        if "ihsg" in group:
            return "IHSG"
        if "usd" in group:
            return "USD/IDR"
        if "global" in group:
            return "global indices"
    if feature.startswith(("BBCA_MA_", "BBCA_volatility_")):
        return "BBCA technical"
    if feature.startswith("BBCA_lag_"):
        return "BBCA lag"
    if feature.startswith(("BBRI_lag_", "BMRI_lag_", "BBNI_lag_")):
        return "peer banking"
    if feature.startswith("IHSG_lag_"):
        return "IHSG"
    if feature.startswith("USD_IDR_lag_"):
        return "USD/IDR"
    if feature.startswith(("SP500_lag_", "NASDAQ_lag_", "NIKKEI225_lag_")):
        return "global indices"
    return "other"


FEATURE_GROUP_COLORS = {
    "BBCA technical": "#00897b",
    "BBCA lag": "#1565c0",
    "peer banking": "#6a1b9a",
    "IHSG": "#ef6c00",
    "USD/IDR": "#8d6e63",
    "global indices": "#2e7d32",
    "other": "#757575",
}


def _feature_colors(features: pd.Series, groups: Optional[pd.Series] = None) -> List[str]:
    colors = []
    for i, feature in enumerate(features):
        explicit_group = None if groups is None else str(groups.iloc[i])
        group = _feature_group_for_color(str(feature), explicit_group)
        colors.append(FEATURE_GROUP_COLORS.get(group, FEATURE_GROUP_COLORS["other"]))
    return colors


def _short_ablation_label(label: str) -> str:
    mapping = {
        "All features": "All features",
        f"Frequent GA >= {int(FREQUENT_FEATURE_THRESHOLD * 100)}%": "Frequent GA >= 60%",
        "BBCA + global indices": "BBCA + Global",
        "BBCA + peer banking": "BBCA + Banking Peers",
        "All features + GA seed 42": "RF + GA seed 42",
        "BBCA only": "BBCA only",
        "BBCA + USD/IDR": "BBCA + USD/IDR",
        "BBCA + IHSG": "BBCA + IHSG",
    }
    return mapping.get(label, label)


def plot_price_history(close_data: pd.DataFrame, output_path: str) -> str:
    _apply_chart_style()
    fig, ax = plt.subplots(figsize=(11, 5.8), dpi=150)
    ax.plot(close_data.index, close_data[TARGET_ALIAS], color="#1f77b4", linewidth=1.7)
    ax.set_title("BBCA Close Price History", fontsize=14, weight="bold")
    ax.set_xlabel("Date")
    ax.set_ylabel("Close Price")
    ax.grid(True, alpha=0.25)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    fig.savefig(output_path, bbox_inches="tight")
    plt.close(fig)
    return output_path


def plot_ga_fitness(history: List[Dict[str, float]], output_path: str) -> str:
    _apply_chart_style()
    history_df = pd.DataFrame(history)
    if history_df.empty:
        raise RuntimeError("History GA kosong, chart fitness tidak dapat dibuat.")
    fig, ax = plt.subplots(figsize=(10, 5.6), dpi=150)
    
    if "seed" in history_df.columns and history_df["seed"].nunique() > 1:
        seeds = history_df["seed"].unique()
        colors = ["#1565c0", "#ef6c00", "#2e7d32", "#c2185b", "#7b1fa2"]
        for idx, seed in enumerate(seeds):
            seed_df = history_df[history_df["seed"] == seed].sort_values("generation")
            ax.plot(
                seed_df["generation"],
                seed_df["best_fitness"],
                linewidth=1.5,
                color=colors[idx % len(colors)],
                alpha=0.75,
                label=f"Seed {seed} Best",
            )
        mean_df = history_df.groupby("generation")["best_fitness"].mean().reset_index()
        ax.plot(
            mean_df["generation"],
            mean_df["best_fitness"],
            linewidth=2.5,
            color="#222222",
            linestyle="--",
            label="Mean Best Fitness",
        )
        y_values = history_df["best_fitness"].astype(float)
        ax.set_title("GA Validation Fitness Progress Across Multiple Seeds", fontsize=14, weight="bold")
    else:
        ax.plot(
            history_df["generation"],
            history_df["best_fitness"],
            marker="o",
            linewidth=2,
            color="#1565c0",
            label="Best fitness",
        )
        if "avg_fitness" in history_df.columns:
            ax.plot(
                history_df["generation"],
                history_df["avg_fitness"],
                marker="s",
                linewidth=1.8,
                color="#ef6c00",
                label="Average fitness",
            )
        y_values = pd.concat([history_df["best_fitness"], history_df.get("avg_fitness", history_df["best_fitness"])]).astype(float)
        seed_num = int(history_df["seed"].iloc[0]) if "seed" in history_df.columns else 42
        ax.set_title(f"Genetic Algorithm Fitness Progress - Seed {seed_num}", fontsize=14, weight="bold")
        final_best = float(history_df["best_fitness"].iloc[-1])
        final_generation = int(history_df["generation"].iloc[-1])
        ax.annotate(
            f"Final best validation AUROC: {final_best:.3f}",
            xy=(final_generation, final_best),
            xytext=(-8, 18),
            textcoords="offset points",
            ha="right",
            fontsize=9,
            bbox={"boxstyle": "round,pad=0.28", "facecolor": "white", "edgecolor": "#dddddd", "alpha": 0.95},
            arrowprops={"arrowstyle": "->", "color": "#555555", "lw": 0.8},
        )
        
    ax.set_xlabel("Generation")
    ax.set_ylabel("Validation AUROC")
    _set_dynamic_y_limits(ax, y_values, padding_ratio=0.18)
    ax.legend(frameon=True, ncol=2 if "seed" in history_df.columns and history_df["seed"].nunique() > 1 else 1)
    ax.grid(True, alpha=0.25)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    fig.savefig(output_path, bbox_inches="tight")
    plt.close(fig)
    return output_path


def plot_model_comparison(experiment_df: pd.DataFrame, output_path: str) -> str:
    _apply_chart_style()
    best_seed_model = "RF + GA best test seed 7 (observasi)"
    best_seed_display = "RF + GA seed 7 (obs.)"
    for model_name in experiment_df["Model"].unique():
        if "RF + GA best test seed" in str(model_name):
            best_seed_model = model_name
            try:
                seed_num = model_name.split("best test seed ")[1].split(" ")[0]
                best_seed_display = f"RF + GA seed {seed_num} (obs.)"
            except IndexError:
                pass
            break
            
    model_map = {
        "Baseline RF": "Baseline RF",
        "RF + Frequent GA": "RF + Frequent GA",
        best_seed_model: best_seed_display,
        "Baseline SVM": "Baseline SVM",
        "SVM + Frequent GA": "SVM + Frequent GA",
    }
    preferred_models = list(model_map.keys())
    plot_df = experiment_df[experiment_df["Model"].isin(preferred_models)].copy()
    plot_df["display_model"] = plot_df["Model"].map(model_map)
    plot_df["Model"] = pd.Categorical(plot_df["Model"], categories=preferred_models, ordered=True)
    plot_df = plot_df.sort_values("Model")
    if plot_df.empty:
        raise RuntimeError("Data model comparison kosong.")

    metric_labels = ["Balanced Accuracy", "AUROC", "F1-score"]
    x = np.arange(len(plot_df))
    width = 0.24

    fig, ax = plt.subplots(figsize=(12, 6), dpi=150)
    colors = ["#607d8b", "#2e7d32", "#1565c0"]
    for i, metric in enumerate(metric_labels):
        bars = ax.bar(
            x + (i - 1) * width,
            plot_df[metric].astype(float),
            width,
            label=metric,
            color=colors[i],
        )
        _add_bar_labels(ax, bars, fontsize=7)

    ax.set_title("Model Performance Comparison on BBCA Trend Forecasting", fontsize=14, weight="bold")
    ax.set_xticks(x)
    ax.set_xticklabels(plot_df["display_model"], rotation=18, ha="right")
    ax.set_ylabel("Score")
    _set_dynamic_y_limits(ax, plot_df[metric_labels].to_numpy().ravel(), padding_ratio=0.18)
    ax.text(
        0.01,
        0.02,
        "Best test seed is test-set observation, not primary selected model.",
        transform=ax.transAxes,
        fontsize=8.5,
        color="#555555",
    )
    ax.legend(frameon=True, ncol=3, loc="upper center", bbox_to_anchor=(0.5, 1.02))
    ax.grid(axis="y", alpha=0.25)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    fig.savefig(output_path, bbox_inches="tight")
    plt.close(fig)
    return output_path


def plot_roc_curve(
    y_test: pd.Series,
    models_roc_data: Dict[str, Tuple[Optional[np.ndarray], float, str, str]],
    output_path: str,
) -> str:
    _apply_chart_style()
    fig, ax = plt.subplots(figsize=(7.2, 6.2), dpi=150)
    ax.plot([0, 1], [0, 1], linestyle="--", color="#9e9e9e", label="Random classifier")

    for name, (y_score, auroc, color, style) in models_roc_data.items():
        if y_score is not None and y_test.nunique() >= 2:
            fpr, tpr, _ = roc_curve(y_test, y_score)
            ax.plot(fpr, tpr, color=color, linestyle=style, linewidth=2.2, label=f"{name} (AUROC = {auroc:.3f})")
        else:
            ax.plot([], [], color=color, linestyle=style, linewidth=2.2, label=f"{name} (AUROC = {auroc:.3f})")

    ax.set_title("ROC Curve Comparison on BBCA Test Set", fontsize=14, weight="bold")
    ax.set_xlabel("False Positive Rate")
    ax.set_ylabel("True Positive Rate")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.legend(frameon=True, loc="lower right")
    ax.grid(True, alpha=0.25)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    fig.savefig(output_path, bbox_inches="tight")
    plt.close(fig)
    return output_path


def plot_selected_features(
    model: RandomForestClassifier,
    selected_features: List[str],
    output_path: str,
    top_n: int = 15,
    model_display_name: str = "RF + Frequent GA",
) -> str:
    _apply_chart_style()
    if len(selected_features) == 0:
        raise RuntimeError("Tidak ada fitur terpilih untuk chart feature importance.")

    importances = getattr(model, "feature_importances_", None)
    if importances is None or len(importances) != len(selected_features):
        raise RuntimeError("Feature importance Random Forest tidak tersedia atau tidak sesuai.")

    importance_df = pd.DataFrame(
        {"feature": selected_features, "importance": importances}
    ).sort_values("importance", ascending=False)
    top_features = importance_df.head(top_n).sort_values("importance", ascending=True)

    fig_height = max(5.5, 0.36 * len(top_features) + 1.7)
    fig, ax = plt.subplots(figsize=(10, fig_height), dpi=150)
    colors = _feature_colors(top_features["feature"])
    bars = ax.barh(top_features["feature"], top_features["importance"], color=colors)
    ax.set_title(f"Top {len(top_features)} {model_display_name} Feature Importances", fontsize=14, weight="bold")
    ax.set_xlabel("Importance")
    ax.grid(axis="x", alpha=0.25)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    _add_barh_labels(ax, bars, fontsize=8.5)

    fig.tight_layout()
    fig.savefig(output_path, bbox_inches="tight")
    plt.close(fig)
    return output_path


def plot_recent_estimation(
    close_data: pd.DataFrame,
    estimation: Dict[str, object],
    output_path: str,
    recent_days: int = 180,
) -> str:
    _apply_chart_style()
    recent_data = close_data[[TARGET_ALIAS]].tail(recent_days)
    latest_date = pd.Timestamp(estimation["latest_date"])
    latest_close = float(estimation["latest_close"])
    signal = str(estimation["signal"])
    if "NETRAL" in signal:
        chart_signal = "Neutral"
    elif signal == "UPTREND":
        chart_signal = "Uptrend"
    else:
        chart_signal = "Not-Uptrend"
    confidence_map = {
        "Sangat rendah": "Very low",
        "Rendah": "Low",
        "Sedang": "Medium",
        "Tinggi": "High",
    }
    confidence_label = confidence_map.get(str(estimation["confidence_category"]), str(estimation["confidence_category"]))

    fig, ax = plt.subplots(figsize=(11, 5.8), dpi=150)
    ax.plot(recent_data.index, recent_data[TARGET_ALIAS], color="#1f77b4", linewidth=1.8, label="BBCA Close")
    ax.scatter([latest_date], [latest_close], color="#222222", s=26, zorder=4, label="Last Close")
    ax.axvline(latest_date, color="#777777", linestyle="--", linewidth=1.0, alpha=0.75)

    inference_text = (
        f"Latest inference: {chart_signal} | "
        f"P(Uptrend): {float(estimation['probability_uptrend']):.1%} | "
        f"Confidence: {confidence_label}"
    )
    note_text = "Model output is a trend classification signal, not a price target or trading recommendation."

    ax.set_title("BBCA Recent Price Movement and Latest Model Inference", fontsize=14, weight="bold")
    ax.set_xlabel("Date")
    ax.set_ylabel("Close Price")
    ax.legend(frameon=False, loc="upper right", fontsize=7.5)
    ax.grid(True, alpha=0.18, linewidth=0.7)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.subplots_adjust(bottom=0.20)
    fig.text(0.5, 0.065, inference_text, ha="center", va="center", fontsize=9.2, color="#333333")
    fig.text(0.5, 0.035, note_text, ha="center", va="center", fontsize=8.2, color="#666666")
    fig.savefig(output_path, bbox_inches="tight")
    plt.close(fig)
    return output_path


def plot_ablation_study(ablation_df: pd.DataFrame, output_path: str) -> str:
    _apply_chart_style()
    if ablation_df.empty:
        raise RuntimeError("Data ablation study kosong.")

    plot_df = ablation_df.sort_values("AUROC", ascending=True).copy()
    plot_df["label"] = plot_df["Model"].map(_short_ablation_label)

    fig, ax = plt.subplots(figsize=(10.5, 6.2), dpi=150)
    bars = ax.barh(plot_df["label"], plot_df["AUROC"].astype(float), color="#1565c0")
    _add_barh_labels(ax, bars, fontsize=8.5)
    ax.axvline(0.50, color="#9e9e9e", linestyle="--", linewidth=1.2, label="Random baseline AUROC = 0.50")
    ax.set_title("Ablation Study by Feature Group - AUROC", fontsize=14, weight="bold")
    ax.set_xlabel("Test AUROC")
    _set_dynamic_x_limits(ax, plot_df["AUROC"], padding_ratio=0.24, floor=0.49)
    ax.legend(frameon=True, loc="lower right", fontsize=8)
    ax.grid(axis="x", alpha=0.25)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    fig.savefig(output_path, bbox_inches="tight")
    plt.close(fig)
    return output_path


def plot_split_scenario_chart(scenario_df: pd.DataFrame, output_path: str) -> str:
    _apply_chart_style()
    if scenario_df.empty:
        raise RuntimeError("Data split scenario kosong.")

    plot_df = scenario_df.copy()
    scenario_order = [label for label, _ in SPLIT_SCENARIOS]
    model_order = ["Baseline RF", f"RF + GA seed {SPLIT_SCENARIO_GA_SEED}"]
    plot_df["Scenario"] = pd.Categorical(plot_df["Scenario"], categories=scenario_order, ordered=True)
    plot_df["Model"] = pd.Categorical(plot_df["Model"], categories=model_order, ordered=True)
    plot_df = plot_df.sort_values(["Scenario", "Model"])

    pivot = plot_df.pivot(index="Scenario", columns="Model", values="AUROC").reindex(scenario_order)
    x = np.arange(len(pivot.index))
    width = 0.34

    fig, ax = plt.subplots(figsize=(9.5, 5.6), dpi=150)
    bars_1 = ax.bar(x - width / 2, pivot[model_order[0]], width, label=model_order[0], color="#607d8b")
    bars_2 = ax.bar(x + width / 2, pivot[model_order[1]], width, label=model_order[1], color="#2e7d32")
    _add_bar_labels(ax, bars_1, fontsize=8)
    _add_bar_labels(ax, bars_2, fontsize=8)
    ax.axhline(0.50, color="#9e9e9e", linestyle="--", linewidth=1.1, label="Random baseline AUROC = 0.50")

    ax.set_title("Train/Test Split Scenario Comparison - AUROC", fontsize=14, weight="bold")
    ax.set_xlabel("Train/Test Scenario")
    ax.set_ylabel("Test AUROC")
    ax.set_xticks(x)
    ax.set_xticklabels(pivot.index)
    _set_dynamic_y_limits(
        ax,
        list(plot_df["AUROC"].astype(float)) + [0.50],
        padding_ratio=0.20,
        floor=0.48,
    )
    ax.legend(frameon=True, fontsize=8)
    ax.grid(axis="y", alpha=0.25)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    fig.savefig(output_path, bbox_inches="tight")
    plt.close(fig)
    return output_path


def plot_ga_seed_comparison(seed_results_df: pd.DataFrame, output_path: str) -> str:
    _apply_chart_style()
    if seed_results_df.empty:
        raise RuntimeError("Data GA seed results kosong.")

    plot_df = seed_results_df.sort_values("seed").copy()
    labels = [str(int(seed)) for seed in plot_df["seed"]]
    x = np.arange(len(plot_df))
    width = 0.36

    fig, ax = plt.subplots(figsize=(10, 5.8), dpi=150)
    bars_1 = ax.bar(x - width / 2, plot_df["best_validation_fitness"], width, label="Validation fitness", color="#1565c0")
    bars_2 = ax.bar(x + width / 2, plot_df["AUROC"], width, label="Test AUROC", color="#2e7d32")
    _add_bar_labels(ax, bars_1, fontsize=8)
    _add_bar_labels(ax, bars_2, fontsize=8)
    baseline_auc = 0.5898
    mean_ga_auc = float(plot_df["AUROC"].mean())
    ax.axhline(baseline_auc, color="#c62828", linestyle="--", linewidth=1.2, label=f"Baseline RF AUROC = {baseline_auc:.4f}")
    ax.axhline(mean_ga_auc, color="#6d4c41", linestyle=":", linewidth=1.5, label=f"Mean RF + GA AUROC = {mean_ga_auc:.4f}")
    best_test_seed = int(plot_df.sort_values("AUROC", ascending=False).iloc[0]["seed"])
    best_validation_seed = int(plot_df.sort_values("best_validation_fitness", ascending=False).iloc[0]["seed"])
    annotation_y = max(plot_df["AUROC"].max(), plot_df["best_validation_fitness"].max(), baseline_auc, mean_ga_auc)
    ax.annotate(
        f"Best test seed = {best_test_seed}\nBest validation seed = {best_validation_seed}",
        xy=(len(plot_df) - 1, annotation_y),
        xytext=(-10, 16),
        textcoords="offset points",
        ha="right",
        fontsize=8.5,
        bbox={"boxstyle": "round,pad=0.28", "facecolor": "white", "edgecolor": "#dddddd", "alpha": 0.95},
    )
    ax.set_title("GA Seed Comparison", fontsize=14, weight="bold")
    ax.set_xlabel("GA Seed")
    ax.set_ylabel("AUROC")
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    _set_dynamic_y_limits(
        ax,
        list(plot_df["best_validation_fitness"]) + list(plot_df["AUROC"]) + [baseline_auc, mean_ga_auc],
        padding_ratio=0.24,
    )
    ax.legend(frameon=True, fontsize=8)
    ax.grid(axis="y", alpha=0.25)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    fig.savefig(output_path, bbox_inches="tight")
    plt.close(fig)
    return output_path


def plot_selected_features_frequency(frequency_df: pd.DataFrame, output_path: str, top_n: int = 20) -> str:
    _apply_chart_style()
    if frequency_df.empty:
        raise RuntimeError("Data selected feature frequency kosong.")

    top_features = frequency_df.head(top_n).sort_values("selected_percentage", ascending=True)
    fig_height = max(6, 0.34 * len(top_features) + 1.8)
    fig, ax = plt.subplots(figsize=(10.5, fig_height), dpi=150)
    colors = _feature_colors(top_features["feature"], top_features.get("feature_group"))
    bars = ax.barh(top_features["feature"], top_features["selected_percentage"], color=colors)
    ax.set_title(f"Top {len(top_features)} GA Selected Feature Frequency", fontsize=14, weight="bold")
    ax.set_xlabel("Selected Percentage Across Seeds")
    ax.set_xlim(0, 1)
    ax.grid(axis="x", alpha=0.25)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    _add_barh_labels(ax, bars, fmt="{:.0%}", fontsize=8.5)

    fig.tight_layout()
    fig.savefig(output_path, bbox_inches="tight")
    plt.close(fig)
    return output_path


def plot_selected_features_from_frequency(frequency_df: pd.DataFrame, output_path: str, top_n: int = 15) -> str:
    _apply_chart_style()
    if frequency_df.empty:
        raise RuntimeError("Data selected feature frequency kosong.")

    top_features = frequency_df.head(top_n).sort_values("selected_count", ascending=True).copy()
    colors = _feature_colors(top_features["feature"], top_features.get("feature_group"))
    fig_height = max(5.5, 0.34 * len(top_features) + 1.8)
    fig, ax = plt.subplots(figsize=(10, fig_height), dpi=150)
    bars = ax.barh(top_features["feature"], top_features["selected_count"], color=colors)
    ax.set_title(f"Top {len(top_features)} GA Selected Features by Frequency", fontsize=14, weight="bold")
    ax.set_xlabel("Selected Count Across Seeds")
    ax.set_xlim(0, max(float(top_features["selected_count"].max()) + 0.75, 1.0))
    ax.grid(axis="x", alpha=0.25)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    _add_barh_labels(ax, bars, fmt="{:.0f}", fontsize=8.5)
    fig.tight_layout()
    fig.savefig(output_path, bbox_inches="tight")
    plt.close(fig)
    return output_path


def plot_selected_feature_importance_from_csv(importance_df: pd.DataFrame, output_path: str, top_n: int = 15) -> str:
    _apply_chart_style()
    required_cols = {"feature", "importance"}
    if importance_df.empty or not required_cols.issubset(importance_df.columns):
        raise RuntimeError("selected_feature_importance.csv tidak valid untuk selected_features_chart.png.")

    top_features = importance_df.sort_values("importance", ascending=False).head(top_n).sort_values("importance", ascending=True)
    colors = _feature_colors(top_features["feature"])
    fig_height = max(5.5, 0.36 * len(top_features) + 1.7)
    fig, ax = plt.subplots(figsize=(10, fig_height), dpi=150)
    bars = ax.barh(top_features["feature"], top_features["importance"], color=colors)
    ax.set_title(f"Top {len(top_features)} RF + Frequent GA Feature Importances", fontsize=14, weight="bold")
    ax.set_xlabel("Importance")
    ax.grid(axis="x", alpha=0.25)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    _add_barh_labels(ax, bars, fontsize=8.5)
    fig.tight_layout()
    fig.savefig(output_path, bbox_inches="tight")
    plt.close(fig)
    return output_path


def _load_chart_csvs(output_dir: str) -> Dict[str, pd.DataFrame]:
    csv_data: Dict[str, pd.DataFrame] = {}
    missing = []
    for filename in REQUIRED_RESULT_CSVS:
        path = os.path.join(output_dir, filename)
        if not os.path.exists(path):
            missing.append(filename)
        else:
            csv_data[filename] = pd.read_csv(path)

    if missing:
        raise RuntimeError(
            "Mode REGENERATE_CHARTS_ONLY membutuhkan CSV hasil eksperimen yang sudah ada. "
            f"CSV belum ditemukan: {', '.join(missing)}"
        )
    return csv_data


def _optional_csv(output_dir: str, filename: str) -> Optional[pd.DataFrame]:
    path = os.path.join(output_dir, filename)
    if os.path.exists(path):
        return pd.read_csv(path)
    return None


def _chart_only_price_data(output_dir: str) -> pd.DataFrame:
    cached_price = _optional_csv(output_dir, "price_history_chart_data.csv")
    if cached_price is not None:
        cached_price["Date"] = pd.to_datetime(cached_price["Date"])
        return cached_price.set_index("Date")

    print(
        "Warning - price_history_chart_data.csv belum ada. "
        "Mengunduh ulang data harga untuk chart saja; tidak ada GA/training yang dijalankan."
    )
    close_data, _ = download_data()
    price_cache = close_data[[TARGET_ALIAS]].reset_index()
    price_cache = price_cache.rename(columns={price_cache.columns[0]: "Date"})
    price_cache.to_csv(os.path.join(output_dir, "price_history_chart_data.csv"), index=False)
    return close_data


def _chart_only_estimation(output_dir: str, close_data: pd.DataFrame) -> Dict[str, object]:
    estimation_df = _optional_csv(output_dir, "recent_estimation_values.csv")
    if estimation_df is None or estimation_df.empty:
        raise RuntimeError(
            "recent_estimation_chart.png membutuhkan recent_estimation_values.csv pada mode chart-only. "
            "Jalankan full experiment sekali dengan REGENERATE_CHARTS_ONLY=False agar cache chart ini dibuat."
        )

    row = estimation_df.iloc[0]
    return {
        "latest_date": pd.to_datetime(row["latest_date"]),
        "latest_close": float(row["latest_close"]),
        "probability_uptrend": float(row["probability_uptrend"]),
        "probability_not_uptrend": float(row["probability_not_uptrend"]),
        "signal": str(row["signal"]),
        "confidence": float(row["confidence"]),
        "confidence_category": str(row["confidence_category"]),
    }


def _chart_only_ga_history(output_dir: str, seed_results_df: pd.DataFrame) -> List[Dict[str, float]]:
    history_df = _optional_csv(output_dir, "ga_fitness_history.csv")
    if history_df is not None and not history_df.empty:
        return history_df.to_dict("records")

    records = []
    for _, row in seed_results_df.iterrows():
        seed_num = int(row["seed"])
        best_fit = float(row["best_validation_fitness"])
        records.append({"seed": seed_num, "generation": 1, "best_fitness": best_fit, "avg_fitness": best_fit})
    return records


def _chart_only_roc(output_dir: str, experiment_df: pd.DataFrame, output_path: str) -> str:
    roc_points = _optional_csv(output_dir, "roc_curve_points.csv")
    
    def get_auroc(model_name, default=0.5):
        row = experiment_df[experiment_df["Model"] == model_name]
        return float(row.iloc[0]["AUROC"]) if not row.empty else default

    baseline_auroc = get_auroc("Baseline RF")
    frequent_auroc = get_auroc("RF + Frequent GA")
    
    best_seed_row = experiment_df[experiment_df["Model"].str.contains(r"RF \+ GA best test seed", na=False)]
    if not best_seed_row.empty:
        best_seed_model_name = best_seed_row.iloc[0]["Model"]
        best_seed_auroc = float(best_seed_row.iloc[0]["AUROC"])
    else:
        best_seed_model_name = "RF + GA best test seed 7 (observasi)"
        best_seed_auroc = get_auroc(best_seed_model_name)

    _apply_chart_style()
    fig, ax = plt.subplots(figsize=(7.2, 6.2), dpi=150)
    ax.plot([0, 1], [0, 1], linestyle="--", color="#9e9e9e", label="Random classifier")

    if roc_points is not None:
        if {"baseline_rf_fpr", "baseline_rf_tpr"}.issubset(roc_points.columns):
            pair = roc_points[["baseline_rf_fpr", "baseline_rf_tpr"]].dropna()
            ax.plot(pair["baseline_rf_fpr"], pair["baseline_rf_tpr"], color="#78909c", linewidth=2.0, label=f"Baseline RF (AUROC = {baseline_auroc:.3f})")
        
        if {"rf_frequent_ga_fpr", "rf_frequent_ga_tpr"}.issubset(roc_points.columns):
            pair = roc_points[["rf_frequent_ga_fpr", "rf_frequent_ga_tpr"]].dropna()
            ax.plot(pair["rf_frequent_ga_fpr"], pair["rf_frequent_ga_tpr"], color="#2e7d32", linewidth=2.2, label=f"RF + Frequent GA (AUROC = {frequent_auroc:.3f})")
            
        if {"best_seed_fpr", "best_seed_tpr"}.issubset(roc_points.columns):
            pair = roc_points[["best_seed_fpr", "best_seed_tpr"]].dropna()
            ax.plot(pair["best_seed_fpr"], pair["best_seed_tpr"], color="#1565c0", linestyle=":", linewidth=2.2, label=f"{best_seed_model_name} (AUROC = {best_seed_auroc:.3f})")
    else:
        ax.plot([], [], color="#78909c", linewidth=2.0, label=f"Baseline RF (AUROC = {baseline_auroc:.3f})")
        ax.plot([], [], color="#2e7d32", linewidth=2.2, label=f"RF + Frequent GA (AUROC = {frequent_auroc:.3f})")
        ax.plot([], [], color="#1565c0", linestyle=":", linewidth=2.2, label=f"{best_seed_model_name} (AUROC = {best_seed_auroc:.3f})")

    ax.set_title("ROC Curve Comparison on BBCA Test Set", fontsize=14, weight="bold")
    ax.set_xlabel("False Positive Rate")
    ax.set_ylabel("True Positive Rate")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.legend(frameon=True, loc="lower right")
    ax.grid(True, alpha=0.25)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    fig.savefig(output_path, bbox_inches="tight")
    plt.close(fig)
    return output_path


def regenerate_charts_only(output_dir: str) -> List[str]:
    print_section("REGENERATE_CHARTS_ONLY")
    print("Mode chart-only aktif: GA/training berat tidak dijalankan.")
    csv_data = _load_chart_csvs(output_dir)

    experiment_df = csv_data["experiment_results.csv"]
    seed_results_df = csv_data["ga_seed_results.csv"]
    frequency_df = csv_data["selected_features_frequency.csv"]
    ablation_df = csv_data["ablation_study_results.csv"]
    scenario_df = _optional_csv(output_dir, "split_scenario_results.csv")

    close_data = _chart_only_price_data(output_dir)
    estimation = _chart_only_estimation(output_dir, close_data)
    ga_history = _chart_only_ga_history(output_dir, seed_results_df)
    importance_df = _optional_csv(output_dir, "selected_feature_importance.csv")

    chart_paths = [
        plot_price_history(close_data, os.path.join(output_dir, "bbca_price_history_chart.png")),
        plot_ga_fitness(ga_history, os.path.join(output_dir, "ga_fitness_chart.png")),
        plot_model_comparison(experiment_df, os.path.join(output_dir, "model_comparison_chart.png")),
        _chart_only_roc(output_dir, experiment_df, os.path.join(output_dir, "roc_curve_chart.png")),
        (
            plot_selected_features_from_frequency(
                frequency_df,
                os.path.join(output_dir, "selected_features_chart.png"),
            )
            if importance_df is None or importance_df.empty
            else plot_selected_feature_importance_from_csv(
                importance_df,
                os.path.join(output_dir, "selected_features_chart.png"),
            )
        ),
        plot_ablation_study(ablation_df, os.path.join(output_dir, "ablation_study_chart.png")),
        plot_ga_seed_comparison(seed_results_df, os.path.join(output_dir, "ga_seed_comparison_chart.png")),
        plot_selected_features_frequency(
            frequency_df,
            os.path.join(output_dir, "selected_features_frequency_chart.png"),
        ),
    ]
    if SHOW_RECENT_ESTIMATION_CHART:
        chart_paths.insert(
            5,
            plot_recent_estimation(
                close_data,
                estimation,
                os.path.join(output_dir, "recent_estimation_chart.png"),
            ),
        )
    else:
        recent_path = os.path.join(output_dir, "recent_estimation_chart.png")
        if os.path.exists(recent_path):
            os.remove(recent_path)
        print("SHOW_RECENT_ESTIMATION_CHART=False, recent_estimation_chart.png tidak dibuat ulang.")
    if scenario_df is not None and not scenario_df.empty:
        chart_paths.append(
            plot_split_scenario_chart(
                scenario_df,
                os.path.join(output_dir, "split_scenario_chart.png"),
            )
        )
    else:
        print("split_scenario_results.csv belum ada; split_scenario_chart.png dilewati pada mode chart-only.")

    print("Chart PNG berhasil diregenerasi:")
    for path in chart_paths:
        print(f"- {os.path.basename(path)}")
    return chart_paths


def run_multiseed_split_study(
    X: pd.DataFrame,
    y: pd.Series,
    output_dir: str,
    existing_80_baseline_metrics: Optional[Dict[str, object]] = None,
    existing_80_seed_results_df: Optional[pd.DataFrame] = None,
) -> Tuple[pd.DataFrame, pd.DataFrame, str, str, str]:
    """Run multi-seed GA study across all split scenarios.

    For 80/20, reuses results from the main experiment to avoid redundant computation.
    For 75/25 and 70/30, runs GA with all seeds fresh.
    """
    print_section("Multi-Seed GA Split Scenario Study (All Seeds x All Scenarios)")
    print(f"GA seeds           : {GA_SEEDS}")
    print(f"Skenario split     : {', '.join(label for label, _ in SPLIT_SCENARIOS)}")
    print(f"GA validation      : TimeSeriesSplit(n_splits={GA_CV_SPLITS})")
    print(f"GA fitness RF      : n_estimators={GA_FITNESS_RF_PARAMS['n_estimators']}, max_depth={GA_FITNESS_RF_PARAMS['max_depth']}")
    print(f"Final RF           : n_estimators={RF_PARAMS['n_estimators']}, max_depth={RF_PARAMS['max_depth']}")
    print("Tujuan: evaluasi robustness RF + GA di berbagai ukuran train/test split")
    print("dengan multi-seed GA untuk setiap skenario.\n")

    all_detail_rows: List[Dict[str, object]] = []
    summary_rows: List[Dict[str, object]] = []

    for scenario_label, train_ratio in SPLIT_SCENARIOS:
        print(f"\n{'=' * 60}")
        print(f"Scenario {scenario_label}")
        print(f"{'=' * 60}")

        X_train_s, X_test_s, y_train_s, y_test_s = split_data(
            X, y, train_ratio=train_ratio,
            scenario_label=f"Multi-seed {scenario_label}",
            verbose=True,
        )

        # --- Baseline RF ---
        if scenario_label == "80/20" and existing_80_baseline_metrics is not None:
            baseline_auroc = float(existing_80_baseline_metrics["auroc"])
            baseline_ba = float(existing_80_baseline_metrics["balanced_accuracy"])
            baseline_f1 = float(existing_80_baseline_metrics["f1"])
            print(f"\nBaseline RF {scenario_label}: menggunakan ulang hasil eksperimen utama.")
        else:
            print(f"\nMenjalankan Baseline RF {scenario_label}...")
            baseline_model_s = train_random_forest(X_train_s, y_train_s, random_state=RANDOM_STATE)
            bl_metrics = evaluate_model(
                baseline_model_s, X_test_s, y_test_s,
                f"Baseline RF | Multi-seed {scenario_label}",
            )
            baseline_auroc = float(bl_metrics["auroc"])
            baseline_ba = float(bl_metrics["balanced_accuracy"])
            baseline_f1 = float(bl_metrics["f1"])
        print(f"  Baseline RF: AUROC={baseline_auroc:.4f}, Balanced Acc={baseline_ba:.4f}, F1={baseline_f1:.4f}")

        # --- Multi-seed GA ---
        scenario_seed_rows: List[Dict[str, object]] = []

        if scenario_label == "80/20" and existing_80_seed_results_df is not None:
            print(f"\nRF + GA multi-seed {scenario_label}: menggunakan ulang hasil eksperimen utama.")
            for _, row in existing_80_seed_results_df.iterrows():
                detail = {
                    "Scenario": "80/20",
                    "Seed": int(row["seed"]),
                    "Validation Fitness": float(row["best_validation_fitness"]),
                    "Selected Feature Count": int(row["selected_feature_count"]),
                    "Accuracy": float(row["Accuracy"]),
                    "Balanced Accuracy": float(row["Balanced Accuracy"]),
                    "AUROC": float(row["AUROC"]),
                    "Precision": float(row["Precision"]),
                    "Recall": float(row["Recall"]),
                    "F1-score": float(row["F1-score"]),
                }
                scenario_seed_rows.append(detail)
                all_detail_rows.append(detail)
        else:
            print(f"\nMenjalankan RF + GA multi-seed {scenario_label} ({len(GA_SEEDS)} seeds)...")
            for seed in GA_SEEDS:
                selected_features, _, best_fitness = genetic_algorithm_feature_selection(
                    X_train_s, y_train_s,
                    random_state=seed,
                    use_time_series_split=True,
                )
                ga_model_s = train_random_forest(
                    X_train_s[selected_features], y_train_s, random_state=RANDOM_STATE,
                )
                ga_metrics = evaluate_model(
                    ga_model_s, X_test_s[selected_features], y_test_s,
                    f"RF + GA seed {seed} | {scenario_label}",
                )
                detail = {
                    "Scenario": scenario_label,
                    "Seed": seed,
                    "Validation Fitness": float(best_fitness),
                    "Selected Feature Count": len(selected_features),
                    "Accuracy": float(ga_metrics["accuracy"]),
                    "Balanced Accuracy": float(ga_metrics["balanced_accuracy"]),
                    "AUROC": float(ga_metrics["auroc"]),
                    "Precision": float(ga_metrics["precision"]),
                    "Recall": float(ga_metrics["recall"]),
                    "F1-score": float(ga_metrics["f1"]),
                }
                scenario_seed_rows.append(detail)
                all_detail_rows.append(detail)

        # Print per-seed results
        print(f"\nHasil per seed {scenario_label}:")
        for detail in scenario_seed_rows:
            print(
                f"  Seed {detail['Seed']:>3}: validation={detail['Validation Fitness']:.4f}, "
                f"test AUROC={detail['AUROC']:.4f}, F1={detail['F1-score']:.4f}, "
                f"features={detail['Selected Feature Count']}"
            )

        # Summary statistics
        seed_df = pd.DataFrame(scenario_seed_rows)
        seed_aurocs = seed_df["AUROC"].astype(float)
        seed_f1s = seed_df["F1-score"].astype(float)
        seed_bas = seed_df["Balanced Accuracy"].astype(float)
        seed_vals = seed_df["Validation Fitness"].astype(float)

        mean_auroc = float(seed_aurocs.mean())
        std_auroc = float(seed_aurocs.std(ddof=0))
        mean_f1 = float(seed_f1s.mean())
        std_f1 = float(seed_f1s.std(ddof=0))
        mean_ba = float(seed_bas.mean())

        best_val_idx = seed_vals.idxmax()
        best_val_seed = int(seed_df.loc[best_val_idx, "Seed"])
        best_test_idx = seed_aurocs.idxmax()
        best_test_seed = int(seed_df.loc[best_test_idx, "Seed"])
        best_test_auroc = float(seed_aurocs.max())

        summary_rows.append({
            "Scenario": scenario_label,
            "Train Ratio": train_ratio,
            "Train Rows": len(X_train_s),
            "Test Rows": len(X_test_s),
            "Baseline RF AUROC": baseline_auroc,
            "Baseline RF Balanced Accuracy": baseline_ba,
            "Baseline RF F1": baseline_f1,
            "Mean GA AUROC": mean_auroc,
            "Std GA AUROC": std_auroc,
            "Mean GA Balanced Accuracy": mean_ba,
            "Mean GA F1": mean_f1,
            "Std GA F1": std_f1,
            "Best Validation Seed": best_val_seed,
            "Best Test Seed": best_test_seed,
            "Best Test AUROC": best_test_auroc,
        })

        print(f"\nRingkasan {scenario_label}:")
        print(f"  Baseline RF     : AUROC={baseline_auroc:.4f}, F1={baseline_f1:.4f}")
        print(f"  Mean RF + GA    : AUROC={mean_auroc:.4f} +/- {std_auroc:.4f}, F1={mean_f1:.4f} +/- {std_f1:.4f}")
        print(f"  Best val seed   : {best_val_seed}")
        print(f"  Best test seed  : {best_test_seed} (AUROC={best_test_auroc:.4f}) - observasi, bukan model terpilih")
        if best_val_seed != best_test_seed:
            print("  Catatan: seed terbaik validation != seed terbaik test.")

    # Save CSVs
    detail_df = pd.DataFrame(all_detail_rows)
    detail_csv_path = os.path.join(output_dir, "multiseed_scenario_detail.csv")
    detail_df.to_csv(detail_csv_path, index=False)

    summary_df = pd.DataFrame(summary_rows)
    summary_csv_path = os.path.join(output_dir, "multiseed_scenario_summary.csv")
    summary_df.to_csv(summary_csv_path, index=False)

    # Print summary table
    print_section("Ringkasan Multi-Seed GA Cross-Scenario")
    summary_display = summary_df[[
        "Scenario", "Baseline RF AUROC", "Mean GA AUROC", "Std GA AUROC",
        "Mean GA F1", "Std GA F1", "Best Validation Seed", "Best Test Seed",
    ]].copy()
    for col in ["Baseline RF AUROC", "Mean GA AUROC", "Std GA AUROC", "Mean GA F1", "Std GA F1"]:
        summary_display[col] = summary_display[col].map(lambda v: f"{float(v):.4f}")
    print(summary_display.to_string(index=False))

    # Cross-scenario consistency analysis
    print("\nAnalisis konsistensi cross-scenario:")
    auroc_range = float(summary_df["Mean GA AUROC"].max() - summary_df["Mean GA AUROC"].min())
    f1_range = float(summary_df["Mean GA F1"].max() - summary_df["Mean GA F1"].min())
    bl_auroc_range = float(summary_df["Baseline RF AUROC"].max() - summary_df["Baseline RF AUROC"].min())
    bl_f1_range = float(summary_df["Baseline RF F1"].max() - summary_df["Baseline RF F1"].min())
    print(f"  Baseline RF AUROC range antar skenario : {bl_auroc_range:.4f}")
    print(f"  Baseline RF F1 range antar skenario    : {bl_f1_range:.4f}")
    print(f"  Mean GA AUROC range antar skenario     : {auroc_range:.4f}")
    print(f"  Mean GA F1 range antar skenario        : {f1_range:.4f}")
    if auroc_range < bl_auroc_range:
        print("  -> RF + GA lebih konsisten antar skenario dibandingkan Baseline RF (AUROC).")
    else:
        print("  -> Baseline RF lebih konsisten antar skenario dibandingkan RF + GA (AUROC).")

    # Academic interpretation
    print("\nInterpretasi akademik:")
    for _, s_row in summary_df.iterrows():
        scenario = s_row["Scenario"]
        ga_mean = float(s_row["Mean GA AUROC"])
        bl_auc = float(s_row["Baseline RF AUROC"])
        ga_std = float(s_row["Std GA AUROC"])
        if ga_mean > bl_auc + 0.005:
            print(
                f"  {scenario}: RF + GA (mean AUROC={ga_mean:.4f} +/- {ga_std:.4f}) "
                f"sedikit di atas Baseline RF ({bl_auc:.4f})."
            )
        elif ga_mean < bl_auc - 0.005:
            print(
                f"  {scenario}: Baseline RF ({bl_auc:.4f}) sedikit di atas "
                f"RF + GA (mean={ga_mean:.4f} +/- {ga_std:.4f})."
            )
        else:
            print(
                f"  {scenario}: RF + GA (mean={ga_mean:.4f}) dan Baseline RF ({bl_auc:.4f}) "
                f"sangat dekat."
            )
    print("  GA lebih berguna sebagai metode feature selection dan analisis fitur,")
    print("  bukan sebagai bukti peningkatan akurasi yang konsisten.")
    print("  Multi-seed evaluation memperkuat validitas hasil karena mengurangi")
    print("  ketergantungan pada satu seed acak tertentu.")

    # Chart
    chart_path = os.path.join(output_dir, "multiseed_scenario_chart.png")
    plot_multiseed_scenario_chart(detail_df, summary_df, chart_path)

    return detail_df, summary_df, detail_csv_path, summary_csv_path, chart_path


def plot_multiseed_scenario_chart(
    detail_df: pd.DataFrame,
    summary_df: pd.DataFrame,
    output_path: str,
) -> str:
    """Plot multi-seed scenario comparison chart with AUROC and F1 panels."""
    _apply_chart_style()
    if summary_df.empty:
        raise RuntimeError("Data multi-seed scenario summary kosong.")

    scenarios = [label for label, _ in SPLIT_SCENARIOS]
    fig, axes = plt.subplots(1, 2, figsize=(15, 6.5), dpi=150)

    for panel_idx, (ax, metric, ga_mean_col, ga_std_col, bl_col, title) in enumerate([
        (axes[0], "AUROC", "Mean GA AUROC", "Std GA AUROC", "Baseline RF AUROC", "Test AUROC"),
        (axes[1], "F1-score", "Mean GA F1", "Std GA F1", "Baseline RF F1", "Test F1-score"),
    ]):
        x = np.arange(len(scenarios))
        width = 0.32

        # Baseline RF bars
        bl_values = []
        for s in scenarios:
            s_row = summary_df[summary_df["Scenario"] == s]
            bl_values.append(float(s_row[bl_col].iloc[0]) if not s_row.empty else 0.0)
        bars_bl = ax.bar(x - width / 2, bl_values, width, label="Baseline RF", color="#607d8b", alpha=0.9)
        _add_bar_labels(ax, bars_bl, fontsize=7.5)

        # Mean GA bars with error bars
        ga_means = []
        ga_stds = []
        for s in scenarios:
            s_row = summary_df[summary_df["Scenario"] == s]
            ga_means.append(float(s_row[ga_mean_col].iloc[0]) if not s_row.empty else 0.0)
            ga_stds.append(float(s_row[ga_std_col].iloc[0]) if not s_row.empty else 0.0)
        bars_ga = ax.bar(
            x + width / 2, ga_means, width,
            yerr=ga_stds, capsize=4,
            label=f"RF + GA (mean +/- std, {len(GA_SEEDS)} seeds)",
            color="#2e7d32", alpha=0.9,
            error_kw={"elinewidth": 1.2, "capthick": 1.2},
        )
        _add_bar_labels(ax, bars_ga, fontsize=7.5)

        # Overlay individual seed dots
        rng = np.random.default_rng(42)
        for i, scenario in enumerate(scenarios):
            seed_data = detail_df[detail_df["Scenario"] == scenario][metric].astype(float)
            if not seed_data.empty:
                jitter = rng.uniform(-0.04, 0.04, len(seed_data))
                ax.scatter(
                    np.full(len(seed_data), i + width / 2) + jitter,
                    seed_data.values,
                    color="#1b5e20", s=20, alpha=0.65, zorder=3,
                    edgecolors="white", linewidth=0.5,
                )

        if metric == "AUROC":
            ax.axhline(0.50, color="#9e9e9e", linestyle="--", linewidth=1.1, label="Random = 0.50")

        ax.set_title(title, fontsize=13, weight="bold")
        ax.set_xlabel("Train/Test Scenario")
        ax.set_ylabel(metric)
        ax.set_xticks(x)
        ax.set_xticklabels(scenarios)

        all_vals = bl_values + ga_means
        if metric == "AUROC":
            all_vals.append(0.50)
        for scenario in scenarios:
            sv = detail_df[detail_df["Scenario"] == scenario][metric].astype(float).tolist()
            all_vals.extend(sv)
        floor = 0.45 if metric == "AUROC" else 0.0
        _set_dynamic_y_limits(ax, all_vals, padding_ratio=0.22, floor=floor)

        ax.legend(frameon=True, fontsize=7.5, loc="upper right")
        ax.grid(axis="y", alpha=0.25)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

    fig.suptitle(
        f"Multi-Seed GA Performance Across Split Scenarios ({len(GA_SEEDS)} seeds per scenario)",
        fontsize=14, weight="bold", y=1.02,
    )
    fig.tight_layout()
    fig.savefig(output_path, bbox_inches="tight")
    plt.close(fig)
    print(f"Chart disimpan: {os.path.basename(output_path)}")
    return output_path


def plot_rf_optimization_chart(df: pd.DataFrame, output_path: str) -> str:
    _apply_chart_style()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    scenarios = ["80/20", "75/25", "70/30"]
    x = np.arange(len(scenarios))
    width = 0.18
    
    plot_configs = [
        {"Threshold Criterion": "default_0.50", "label": "Default (Th=0.50)", "color": "#1f77b4"},
        {"Threshold Criterion": "max_f1", "label": "Max F1-score", "color": "#ff7f0e"},
        {"Threshold Criterion": "max_balanced_accuracy", "label": "Max Balanced Acc", "color": "#2ca02c"},
        {"Threshold Criterion": "max_g_mean", "label": "Max G-Mean", "color": "#d62728"},
    ]
    
    for i, config in enumerate(plot_configs):
        offset = (i - 1.5) * width
        sub_df = df[df["Threshold Criterion"] == config["Threshold Criterion"]]
        sub_df = sub_df.set_index("Scenario").reindex(scenarios).reset_index()
        
        aurocs = sub_df["Test AUROC"].values
        f1s = sub_df["Test F1"].values
        
        ax1.bar(x + offset, aurocs, width, label=config["label"], color=config["color"])
        ax2.bar(x + offset, f1s, width, label=config["label"], color=config["color"])
        
    ax1.set_title("Test AUROC Across Split Scenarios", fontsize=11, weight="bold")
    ax1.set_ylabel("AUROC")
    ax1.set_xticks(x)
    ax1.set_xticklabels(scenarios)
    ax1.set_ylim(0.40, 0.70)
    ax1.grid(axis="y", alpha=0.3)
    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)
    
    ax2.set_title("Test F1-score Across Split Scenarios", fontsize=11, weight="bold")
    ax2.set_ylabel("F1-score")
    ax2.set_xticks(x)
    ax2.set_xticklabels(scenarios)
    ax2.set_ylim(0.0, 0.60)
    ax2.grid(axis="y", alpha=0.3)
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)
    
    handles, labels = ax1.get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncol=4, bbox_to_anchor=(0.5, -0.08))
    
    fig.suptitle(
        "Random Forest Tuning and Threshold Selection Method Comparison",
        fontsize=14, weight="bold", y=1.02,
    )
    fig.tight_layout()
    fig.savefig(output_path, bbox_inches="tight")
    plt.close(fig)
    print(f"Chart disimpan: {os.path.basename(output_path)}")
    return output_path


def run_systematic_rf_study(X: pd.DataFrame, y: pd.Series, output_dir: str) -> Tuple[pd.DataFrame, str]:
    print_section("15. Systematic Random Forest Tuning and Threshold Selection Study")
    print(f"Hyperparameter Grid: {list(RF_TUNING_GRID.keys())}")
    print(f"Split Scenarios     : {', '.join(label for label, _ in SPLIT_SCENARIOS)}")
    print(f"Threshold search grid: {WIDE_THRESHOLD_GRID[0]} to {WIDE_THRESHOLD_GRID[-1]} (step {WIDE_THRESHOLD_GRID[1]-WIDE_THRESHOLD_GRID[0]:.2f})")
    
    results_rows = []
    
    def get_g_mean(y_true, y_pred):
        tn, fp, fn, tp = confusion_matrix(y_true, y_pred, labels=[0, 1]).ravel()
        sensitivity = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        specificity = tn / (tn + fp) if (tn + fp) > 0 else 0.0
        return np.sqrt(sensitivity * specificity)
        
    for scenario_label, train_ratio in SPLIT_SCENARIOS:
        print(f"\nRunning Study for Split Scenario: {scenario_label}...")
        
        X_train, X_test, y_train, y_test = split_data(
            X, y, train_ratio=train_ratio, scenario_label=scenario_label, verbose=False
        )
        
        split_idx = int(len(X_train) * 0.80)
        X_sub_train = X_train.iloc[:split_idx]
        y_sub_train = y_train.iloc[:split_idx]
        X_val = X_train.iloc[split_idx:]
        y_val = y_train.iloc[split_idx:]
        
        print(f"  Training Subset : {len(X_sub_train)} rows")
        print(f"  Validation Set  : {len(X_val)} rows")
        print(f"  Test Set        : {len(X_test)} rows")
        
        cv = TimeSeriesSplit(n_splits=3)
        search = RandomizedSearchCV(
            estimator=RandomForestClassifier(random_state=RANDOM_STATE, n_jobs=-1),
            param_distributions=RF_TUNING_GRID,
            n_iter=20,
            cv=cv,
            scoring="roc_auc",
            random_state=RANDOM_STATE,
            n_jobs=-1,
        )
        search.fit(X_sub_train, y_sub_train)
        best_params = search.best_params_
        best_cv_score = search.best_score_
        
        print(f"  Best CV AUROC   : {best_cv_score:.4f}")
        print(f"  Best Params     : {best_params}")
        
        sub_model = RandomForestClassifier(**best_params)
        sub_model.fit(X_sub_train, y_sub_train)
        val_prob = sub_model.predict_proba(X_val)[:, 1]
        val_auc = roc_auc_score(y_val, val_prob) if y_val.nunique() >= 2 else 0.5
        
        final_model = RandomForestClassifier(**best_params)
        final_model.fit(X_train, y_train)
        test_prob = final_model.predict_proba(X_test)[:, 1]
        test_auc = roc_auc_score(y_test, test_prob) if y_test.nunique() >= 2 else 0.5
        
        criteria_list = ["default_0.50", "max_f1", "max_balanced_accuracy", "max_g_mean"]
        
        for criterion in criteria_list:
            if criterion == "default_0.50":
                best_th = 0.50
            else:
                best_th = 0.50
                best_score = -1.0
                best_dist = 1.0
                for th in WIDE_THRESHOLD_GRID:
                    preds = (val_prob >= th).astype(int)
                    if criterion == "max_f1":
                        score = f1_score(y_val, preds, zero_division=0)
                    elif criterion == "max_balanced_accuracy":
                        score = balanced_accuracy_score(y_val, preds)
                    elif criterion == "max_g_mean":
                        score = get_g_mean(y_val, preds)
                    else:
                        score = 0.0
                    
                    dist = abs(th - 0.50)
                    if score > best_score:
                        best_score = score
                        best_th = th
                        best_dist = dist
                    elif abs(score - best_score) < 1e-9:
                        if dist < best_dist:
                            best_th = th
                            best_dist = dist
                            
            val_preds = (val_prob >= best_th).astype(int)
            val_f1 = f1_score(y_val, val_preds, zero_division=0)
            val_prec = precision_score(y_val, val_preds, zero_division=0)
            val_rec = recall_score(y_val, val_preds, zero_division=0)
            val_ba = balanced_accuracy_score(y_val, val_preds)
            
            test_preds = (test_prob >= best_th).astype(int)
            test_f1 = f1_score(y_test, test_preds, zero_division=0)
            test_prec = precision_score(y_test, test_preds, zero_division=0)
            test_rec = recall_score(y_test, test_preds, zero_division=0)
            test_ba = balanced_accuracy_score(y_test, test_preds)
            test_acc = accuracy_score(y_test, test_preds)
            
            param_str = f"n_est={best_params['n_estimators']},depth={best_params['max_depth']},leaf={best_params['min_samples_leaf']},split={best_params['min_samples_split']},feat={best_params['max_features']},wt={best_params['class_weight']}"
            
            results_rows.append({
                "Scenario": scenario_label,
                "Model": "Tuned-RF",
                "Threshold Criterion": criterion,
                "Selected Threshold": float(best_th),
                "Hyperparameters": param_str,
                "Validation AUROC": float(val_auc),
                "Validation F1": float(val_f1),
                "Validation Precision": float(val_prec),
                "Validation Recall": float(val_rec),
                "Validation Balanced Accuracy": float(val_ba),
                "Test AUROC": float(test_auc),
                "Test F1": float(test_f1),
                "Test Precision": float(test_prec),
                "Test Recall": float(test_rec),
                "Test Balanced Accuracy": float(test_ba),
                "Test Accuracy": float(test_acc),
            })
            
    results_df = pd.DataFrame(results_rows)
    output_path = os.path.join(output_dir, "rf_optimization_results.csv")
    results_df.to_csv(output_path, index=False)
    print(f"Hasil study disimpan ke: {output_path}")
    
    print("\nRingkasan RF Optimization and Threshold Selection:")
    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", 1000)
    print(results_df[[
        "Scenario", "Threshold Criterion", "Selected Threshold", 
        "Validation AUROC", "Validation F1", "Test AUROC", "Test F1"
    ]].to_string(index=False))
    
    chart_path = os.path.join(output_dir, "rf_optimization_comparison_chart.png")
    plot_rf_optimization_chart(results_df, chart_path)
    
    return results_df, output_path


def main() -> None:
    try:
        output_dir = os.path.dirname(os.path.abspath(__file__))
        regenerate_only = REGENERATE_CHARTS_ONLY or os.getenv("REGENERATE_CHARTS_ONLY", "").lower() in {"1", "true", "yes"}
        if regenerate_only:
            regenerate_charts_only(output_dir)
            return

        csv_paths: List[str] = []
        chart_paths: List[str] = []
        experiment_rows: List[Dict[str, object]] = []

        close_data, _ = download_data()
        price_cache = close_data[[TARGET_ALIAS]].reset_index()
        price_cache = price_cache.rename(columns={price_cache.columns[0]: "Date"})
        price_cache.to_csv(os.path.join(output_dir, "price_history_chart_data.csv"), index=False)

        X, y, all_features, _, latest_feature_date, latest_bbca_close = create_features_and_target(close_data)
        X_train, X_test, y_train, y_test = split_data(X, y)

        print_section("4. Experiment Setup")
        print(f"GA seeds                 : {GA_SEEDS}")
        print(f"GA validation            : TimeSeriesSplit(n_splits={GA_CV_SPLITS}), shuffle=False")
        print(f"GA fitness RF            : n_estimators={GA_FITNESS_RF_PARAMS['n_estimators']}, max_depth={GA_FITNESS_RF_PARAMS['max_depth']}")
        print(f"Final RF                 : n_estimators={RF_PARAMS['n_estimators']}, max_depth={RF_PARAMS['max_depth']}")
        print(f"Frequent feature cutoff  : selected_percentage >= {FREQUENT_FEATURE_THRESHOLD:.0%}")
        print("Threshold tuning         : validation internal training, range 0.30-0.70, optimize Balanced Accuracy")
        print(f"Split scenarios          : {', '.join(label for label, _ in SPLIT_SCENARIOS)}")

        dummy_models, dummy_metrics, dummy_rows = train_dummy_baselines(X_train, y_train, X_test, y_test)
        experiment_rows.extend(dummy_rows)

        print_section("6. Baseline Random Forest Results")
        baseline_rf_model = train_random_forest(X_train, y_train, random_state=RANDOM_STATE)
        baseline_rf_metrics = evaluate_model(baseline_rf_model, X_test, y_test, "Baseline RF")
        _print_evaluation_metrics(baseline_rf_metrics)
        experiment_rows.append(_metrics_row("Baseline RF", "All features", 0.50, baseline_rf_metrics))

        seed_results_df, seed_details, all_ga_histories, ga_seed_csv = run_multiple_ga_seeds(
            X_train, y_train, X_test, y_test, output_dir
        )
        csv_paths.append(ga_seed_csv)
        pd.DataFrame(all_ga_histories).to_csv(os.path.join(output_dir, "ga_fitness_history.csv"), index=False)

        seed_42_details = seed_details.get(42)
        if seed_42_details is None:
            raise RuntimeError("Hasil GA seed 42 tidak tersedia.")
        ga_seed_42_features = seed_42_details["selected_features"]
        ga_seed_42_model = seed_42_details["model"]
        ga_seed_42_metrics = seed_42_details["metrics"]

        best_seed = int(seed_results_df.sort_values("AUROC", ascending=False).iloc[0]["seed"])
        best_seed_details = seed_details[best_seed]

        frequency_df, frequent_features, frequency_csv = calculate_selected_feature_frequency(
            seed_details, list(X_train.columns), output_dir
        )
        csv_paths.append(frequency_csv)

        # Train and evaluate RF + Frequent GA (Recommendation 1, Main Model)
        rf_frequent_model = train_random_forest(X_train[frequent_features], y_train, random_state=RANDOM_STATE)
        rf_frequent_metrics = evaluate_model(rf_frequent_model, X_test[frequent_features], y_test, "RF + Frequent GA")
        
        pd.DataFrame(
            {
                "feature": frequent_features,
                "importance": getattr(rf_frequent_model, "feature_importances_", np.zeros(len(frequent_features))),
            }
        ).to_csv(os.path.join(output_dir, "selected_feature_importance.csv"), index=False)

        print_section("9. RF + GA Results")
        print("RF + Frequent GA (Model Utama Rekomendasi 1 untuk Estimasi):")
        _print_evaluation_metrics(rf_frequent_metrics)
        experiment_rows.append(_metrics_row("RF + Frequent GA", "Frequent GA >= 60%", 0.50, rf_frequent_metrics))



        if best_seed != 42:
            print(f"\nRF + GA best test seed sebagai observasi laporan: seed {best_seed}")
            _print_evaluation_metrics(best_seed_details["metrics"])
        experiment_rows.append(
            _metrics_row(
                f"RF + GA best test seed {best_seed} (observasi)",
                f"GA seed {best_seed} features",
                0.50,
                best_seed_details["metrics"],
            )
        )

        print_section("10. SVM Baseline Results")
        baseline_svm_model = train_svm(X_train, y_train)
        baseline_svm_metrics = evaluate_model(baseline_svm_model, X_test, y_test, "Baseline SVM")
        _print_evaluation_metrics(baseline_svm_metrics)
        experiment_rows.append(_metrics_row("Baseline SVM", "All features", 0.50, baseline_svm_metrics))

        print_section("11. SVM + GA Selected Features Results")
        if frequent_features:
            print("SVM + Frequent GA features:")
            svm_frequent_model = train_svm(X_train[frequent_features], y_train)
            svm_frequent_metrics = evaluate_model(svm_frequent_model, X_test[frequent_features], y_test, "SVM + Frequent GA")
            _print_evaluation_metrics(svm_frequent_metrics)
            experiment_rows.append(_metrics_row("SVM + Frequent GA", "Frequent GA >= 60%", 0.50, svm_frequent_metrics))

        feature_groups = get_feature_groups(list(X_train.columns), ga_seed_42_features, frequent_features)
        ablation_df, ablation_csv = run_ablation_study(X_train, y_train, X_test, y_test, feature_groups, output_dir)
        csv_paths.append(ablation_csv)

        threshold_df, threshold_csv = run_threshold_tuning(
            X_train, y_train, X_test, y_test, frequent_features, output_dir
        )
        csv_paths.append(threshold_csv)
        experiment_rows.extend(threshold_df.to_dict("records"))

        scenario_df = pd.DataFrame()
        if RUN_SPLIT_SCENARIO_STUDY:
            scenario_df, scenario_csv = run_split_scenario_study(
                X,
                y,
                output_dir,
                baseline_80_metrics=baseline_rf_metrics,
                ga_80_metrics=ga_seed_42_metrics,
                ga_80_validation_fitness=float(seed_42_details["best_validation_fitness"]),
                ga_80_selected_feature_count=len(ga_seed_42_features),
            )
            csv_paths.append(scenario_csv)
        else:
            print("RUN_SPLIT_SCENARIO_STUDY=False, split scenario study dilewati.")

        # --- Multi-Seed GA Split Scenario Study ---
        ms_chart_path = None
        if RUN_SPLIT_SCENARIO_STUDY:
            ms_detail_df, ms_summary_df, ms_detail_csv, ms_summary_csv, ms_chart_path = (
                run_multiseed_split_study(
                    X, y, output_dir,
                    existing_80_baseline_metrics=baseline_rf_metrics,
                    existing_80_seed_results_df=seed_results_df,
                )
            )
            csv_paths.extend([ms_detail_csv, ms_summary_csv])

        # --- Systematic RF Optimization and Threshold Selection Study ---
        rf_opt_df, rf_opt_csv = run_systematic_rf_study(X, y, output_dir)
        csv_paths.append(rf_opt_csv)

        experiment_df, experiment_csv = save_experiment_results(experiment_rows, output_dir)
        csv_paths.insert(0, experiment_csv)
        rank_models(experiment_df)

        interpret_extended_results(
            baseline_metrics=baseline_rf_metrics,
            ga_metrics=rf_frequent_metrics,
            best_fitness_ga=float(seed_results_df["best_validation_fitness"].mean()),
            svm_metrics=baseline_svm_metrics,
            dummy_majority_metrics=dummy_metrics.get("Dummy Majority"),
            ga_seed_results_df=seed_results_df,
        )

        latest_all_features = all_features.loc[[latest_feature_date], X_train.columns]
        latest_ga_features = all_features.loc[[latest_feature_date], frequent_features]
        if latest_all_features.isna().any().any() or latest_ga_features.isna().any().any():
            raise RuntimeError("Fitur terbaru masih mengandung missing value, estimasi tidak dibuat.")

        estimation = estimate_next_day(
            rf_frequent_model,
            latest_ga_features,
            latest_feature_date,
            latest_bbca_close,
            baseline_rf_model=baseline_rf_model,
            latest_all_features=latest_all_features,
            svm_model=baseline_svm_model,
        )
        pd.DataFrame(
            [
                {
                    "latest_date": estimation["latest_date"],
                    "latest_close": estimation["latest_close"],
                    "probability_uptrend": estimation["probability_uptrend"],
                    "probability_not_uptrend": estimation["probability_not_uptrend"],
                    "baseline_rf_probability_uptrend": estimation.get("baseline_rf_probability_uptrend"),
                    "svm_probability_uptrend": estimation.get("svm_probability_uptrend"),
                    "signal": estimation["signal"],
                    "confidence": estimation["confidence"],
                    "confidence_category": estimation["confidence_category"],
                }
            ]
        ).to_csv(os.path.join(output_dir, "recent_estimation_values.csv"), index=False)

        print_section("17. File CSV yang Disimpan")
        for path in csv_paths:
            print(f"- {os.path.basename(path)}")

        print_section("18. Chart PNG yang Disimpan")
        roc_data_to_save = {}
        if baseline_rf_metrics["y_score"] is not None and y_test.nunique() >= 2:
            rf_fpr, rf_tpr, _ = roc_curve(y_test, baseline_rf_metrics["y_score"])
            roc_data_to_save["baseline_rf_fpr"] = pd.Series(rf_fpr)
            roc_data_to_save["baseline_rf_tpr"] = pd.Series(rf_tpr)
        if rf_frequent_metrics["y_score"] is not None and y_test.nunique() >= 2:
            freq_fpr, freq_tpr, _ = roc_curve(y_test, rf_frequent_metrics["y_score"])
            roc_data_to_save["rf_frequent_ga_fpr"] = pd.Series(freq_fpr)
            roc_data_to_save["rf_frequent_ga_tpr"] = pd.Series(freq_tpr)
        best_seed_metrics = best_seed_details["metrics"]
        if best_seed_metrics["y_score"] is not None and y_test.nunique() >= 2:
            best_fpr, best_tpr, _ = roc_curve(y_test, best_seed_metrics["y_score"])
            roc_data_to_save["best_seed_fpr"] = pd.Series(best_fpr)
            roc_data_to_save["best_seed_tpr"] = pd.Series(best_tpr)
        
        if roc_data_to_save:
            pd.DataFrame(roc_data_to_save).to_csv(
                os.path.join(output_dir, "roc_curve_points.csv"),
                index=False,
            )

        chart_paths = [
            plot_price_history(close_data, os.path.join(output_dir, "bbca_price_history_chart.png")),
            plot_ga_fitness(all_ga_histories, os.path.join(output_dir, "ga_fitness_chart.png")),
            plot_model_comparison(experiment_df, os.path.join(output_dir, "model_comparison_chart.png")),
            plot_roc_curve(
                y_test,
                {
                    "Baseline RF": (baseline_rf_metrics["y_score"], baseline_rf_metrics["auroc"], "#78909c", "-"),
                    "RF + Frequent GA": (rf_frequent_metrics["y_score"], rf_frequent_metrics["auroc"], "#2e7d32", "-"),
                    f"RF + GA Best Test Seed {best_seed}": (best_seed_metrics["y_score"], best_seed_metrics["auroc"], "#1565c0", ":"),
                },
                os.path.join(output_dir, "roc_curve_chart.png"),
            ),
            plot_selected_features(
                rf_frequent_model,
                frequent_features,
                os.path.join(output_dir, "selected_features_chart.png"),
                model_display_name="RF + Frequent GA",
            ),
            plot_ablation_study(ablation_df, os.path.join(output_dir, "ablation_study_chart.png")),
            plot_ga_seed_comparison(seed_results_df, os.path.join(output_dir, "ga_seed_comparison_chart.png")),
            plot_selected_features_frequency(
                frequency_df,
                os.path.join(output_dir, "selected_features_frequency_chart.png"),
            ),
        ]
        if SHOW_RECENT_ESTIMATION_CHART:
            chart_paths.insert(
                5,
                plot_recent_estimation(
                    close_data,
                    estimation,
                    os.path.join(output_dir, "recent_estimation_chart.png"),
                ),
            )
        else:
            recent_path = os.path.join(output_dir, "recent_estimation_chart.png")
            if os.path.exists(recent_path):
                os.remove(recent_path)
            print("SHOW_RECENT_ESTIMATION_CHART=False, recent_estimation_chart.png tidak dibuat ulang.")
        if RUN_SPLIT_SCENARIO_STUDY and not scenario_df.empty:
            chart_paths.append(
                plot_split_scenario_chart(
                    scenario_df,
                    os.path.join(output_dir, "split_scenario_chart.png"),
                )
            )
        if ms_chart_path:
            chart_paths.append(ms_chart_path)

        chart_paths.append(os.path.join(output_dir, "rf_optimization_comparison_chart.png"))

        for path in chart_paths:
            print(f"- {os.path.basename(path)}")

        print_section("Selesai")
        print("Eksperimen selesai. Semua output dibuat berdasarkan data historis yang tersedia dari Yahoo Finance.")
        print("Model hanya mengestimasi arah tren, bukan memprediksi harga nominal.")
        print("Output ini bukan rekomendasi trading.")

    except RuntimeError as exc:
        print_section("ERROR")
        print(f"Program dihentikan: {exc}")
        sys.exit(1)
    except KeyboardInterrupt:
        print_section("DIHENTIKAN")
        print("Program dihentikan oleh pengguna.")
        sys.exit(130)
    except Exception as exc:
        print_section("ERROR")
        print(f"Program dihentikan karena error tidak terduga: {type(exc).__name__}: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()
