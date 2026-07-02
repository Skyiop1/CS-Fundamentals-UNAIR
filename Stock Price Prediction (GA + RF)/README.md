# BBCA Stock Price Direction Prediction — GA + Random Forest Pipeline

📊 **Advanced Machine Learning Pipeline** for predicting the daily price movement direction of BBCA (Bank Central Asia) stock, using a custom **Genetic Algorithm (GA)** for evolutionary feature selection, **Random Forest (RF)** for classification, and **Decision Threshold Tuning**.

> **Objective:** Maximize trading prediction precision and system stability while controlling risk (False Positives) across multiple data split scenarios.

---

## 🧬 Architectural Overview

The project implements a complete, end-to-end quantitative machine learning pipeline:

```
                           [ Technical Indicators Extraction ]
                             (RSI, MACD, Bollinger Bands)
                                          |
                                          v
                           [ Evolutionary Feature Selection ]
                             (Custom Genetic Algorithm)
                                          |
                                          v
                            [ Hyperparameter Tuning ]
                           (Time-Series Cross Validation)
                                          |
                                          v
                            [ Random Forest Classifier ]
                                          |
                                          v
                            [ Decision Threshold Tuning ]
                          (Optimizing Precision vs Recall)
```

1.  **Technical Indicator Extraction**: Generates lagged indicators from Yahoo Finance price history (`yfinance`).
2.  **Genetic Algorithm (GA)**: Evolves binary feature-selection vectors over multiple generations to find the most predictive subset of technical indicators, minimizing overfitting.
3.  **Random Forest Classifier**: The core predictive model, tuned via randomized search.
4.  **Threshold Tuning**: Shifts the default classification boundary (0.5 probability) to optimize precision, ensuring that "buy" signals are highly reliable.

---

## 📈 Visualizations & Outputs Guide

The directory contains comprehensive graphical analysis located in the [`output/charts/`](./output/charts/) directory:

*   **`bbca_price_history_chart.png`**: Visualizes BBCA's historical stock price movement alongside overlayed technical indicator baselines.
*   **`ga_fitness_chart.png`**: Displays the GA fitness score evolution (best and average) across generations, proving convergence.
*   **`ga_seed_comparison_chart.png`**: Compares the results of genetic algorithm optimization across multiple random seeds to validate the search stability.
*   **`selected_features_frequency_chart.png`**: Analyzes which technical indicators (e.g., RSI, MACD) were most frequently selected by the GA across runs, establishing feature importance.
*   **`rf_optimization_comparison_chart.png`**: Compares the out-of-sample performance of the baseline Random Forest model versus the GA-selected, hyperparameter-tuned model.
*   **`roc_curve_chart.png`**: Displays the Receiver Operating Characteristic (ROC) curve and Area Under the Curve (AUC) for all scenarios.
*   **`confusion_matrix_comparison.png`**: Compares True Positives, False Positives, True Negatives, and False Negatives across different split scenarios (80/20, 75/25, 70/30) and decision thresholds.
*   **`ablation_study_chart.png`**: Illustrates model performance variations when specific groups of features are programmatically removed (Ablation Study).
*   **`recent_estimation_chart.png`**: Shows the latest model prediction direction against the actual price action for the most recent trading periods.

---

## 📊 Performance Scenarios & Data Directory

All numerical metrics and experimental records are structured as CSV logs in the [`output/data/`](./output/data/) directory:

-   `experiment_results.csv`: General performance metrics (Accuracy, Balanced Accuracy, F1-Score, ROC-AUC) for all runs.
-   `ga_fitness_history.csv`: Numerical log of fitness scores per generation.
-   `split_scenario_results.csv`: Comparative metrics across different data splits (80/20, 75/25, 70/30).
-   `threshold_tuning_results.csv`: Precision, Recall, and F1 trade-offs evaluated at thresholds from 0.0 to 1.0.

---

## 🛠️ Installation & Execution

### Prerequisites
- Python 3.9 or higher
- Internet connection (to download stock data automatically via Yahoo Finance API)

### Dependencies
Install the required packages using pip:
```bash
pip install yfinance pandas numpy scikit-learn matplotlib
```

### Run the Pipeline
Execute the main script to run the feature extraction, GA optimization, model training, and chart rendering:
```bash
python main.py
```

---

## 📂 Directory Structure

```
Stock Price Prediction (GA + RF)/
├── README.md              # This guide
├── main.py                # Main execution script
├── DOCUMENTATION.md       # Detailed research progress log
├── experiment_log.md      # CLI execution log output
└── output/
    ├── charts/            # Renders of all evaluation plots (PNG)
    └── data/              # CSV logs of fitness history and tuning metrics
```
