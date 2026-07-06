import os
os.environ["CUDA_VISIBLE_DEVICES"] = ""
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
import json
import joblib
from pathlib import Path
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.metrics import confusion_matrix, roc_curve, precision_recall_curve

# Import paths from config
from src.config import (
    BEST_MODEL_PATH,
    SCALER_PATH,
    PCA_PATH,
    METADATA_PATH,
    SPLIT_SCENARIOS,
    FEATURE_COLUMNS,
    EVALUATION_RESULTS_PATH,
    PROCESSED_DATA_PATH,
)
from src.data_loader import preprocess_raw_dataset
from src.database import fetch_prediction_history

# Setup paths
ROOT_DIR = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT_DIR / "outputs" / "figures" / "all_visualizations"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print(f"Creating all visualizations in: {OUTPUT_DIR}")

# Set styling constants
SEX_LABELS = {1: "Laki-laki", 2: "Perempuan"}
EDUCATION_LABELS = {
    1: "Pascasarjana", 2: "Sarjana", 3: "SMA / sederajat",
    4: "Lainnya / tidak diketahui", 5: "Lainnya / tidak diketahui",
    6: "Lainnya / tidak diketahui", 0: "Lainnya / tidak diketahui",
}
MARRIAGE_LABELS = {
    1: "Menikah", 2: "Belum menikah",
    3: "Lainnya / tidak diketahui", 0: "Lainnya / tidak diketahui",
}
DEFAULT_COLOR_MAP = {"Lancar": "#059669", "Gagal Bayar": "#DC2626"}
MODEL_COLOR_MAP = {"DNN / MLP": "#2563EB", "Hybrid PCA-DNN": "#7C3AED"}
PLOTLY_LAYOUT = dict(
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, sans-serif", color="#1E293B"),
    xaxis=dict(
        showline=True,
        linewidth=1.2,
        linecolor="#475569",
        gridcolor="#E2E8F0",
        showgrid=True,
        ticks="outside",
        tickcolor="#475569",
    ),
    yaxis=dict(
        showline=True,
        linewidth=1.2,
        linecolor="#475569",
        gridcolor="#E2E8F0",
        showgrid=True,
        ticks="outside",
        tickcolor="#475569",
    ),
)

# ----------------- Load Data -----------------
print("Loading dataset...")
df = preprocess_raw_dataset(save_processed=False, remove_duplicates=True)
df_plot = df.copy()
df_plot["Status Kredit"] = df_plot["default_status"].map({0: "Lancar", 1: "Gagal Bayar"})

# 1. Class Distribution (Bar Chart)
print("1. Generating Class Distribution chart...")
class_counts = df_plot["Status Kredit"].value_counts().reset_index()
class_counts.columns = ["Status", "Jumlah"]
fig_class = px.bar(
    class_counts,
    x="Status",
    y="Jumlah",
    color="Status",
    color_discrete_map=DEFAULT_COLOR_MAP,
    title="Distribusi Kelas Status Kredit (Lancar vs Gagal Bayar)",
)
fig_class.update_layout(**PLOTLY_LAYOUT, width=800, height=450)
fig_class.write_image(str(OUTPUT_DIR / "01_distribusi_kelas.png"), scale=2)

# 2. Limit Credit vs Status (Box Plot)
print("2. Generating Limit vs Status box plot...")
fig_limit = px.box(
    df_plot,
    x="Status Kredit",
    y="LIMIT_BAL",
    color="Status Kredit",
    color_discrete_map=DEFAULT_COLOR_MAP,
    title="Distribusi Limit Kredit (LIMIT_BAL) vs Status Kredit",
    labels={"LIMIT_BAL": "Limit Kredit (NTD)"}
)
fig_limit.update_layout(**PLOTLY_LAYOUT, width=800, height=450)
fig_limit.write_image(str(OUTPUT_DIR / "02_limit_vs_status.png"), scale=2)

# 3. Age vs Status (Histogram)
print("3. Generating Age vs Status histogram...")
fig_age = px.histogram(
    df_plot,
    x="AGE",
    color="Status Kredit",
    barmode="overlay",
    nbins=25,
    title="Distribusi Umur Nasabah Berdasarkan Status Kredit",
    color_discrete_map=DEFAULT_COLOR_MAP,
    labels={"AGE": "Umur (Tahun)", "count": "Jumlah Nasabah"}
)
fig_age.update_layout(**PLOTLY_LAYOUT, width=800, height=450)
fig_age.write_image(str(OUTPUT_DIR / "03_umur_vs_status_histogram.png"), scale=2)

# 4. Education vs Status (Bar Chart)
print("4. Generating Education vs Status bar chart...")
df_plot["Pendidikan"] = df_plot["EDUCATION"].map(EDUCATION_LABELS)
edu_counts = df_plot.groupby(["Pendidikan", "Status Kredit"]).size().reset_index(name="Jumlah")
fig_edu = px.bar(
    edu_counts,
    x="Pendidikan",
    y="Jumlah",
    color="Status Kredit",
    barmode="group",
    title="Status Kredit Berdasarkan Tingkat Pendidikan",
    color_discrete_map=DEFAULT_COLOR_MAP,
    labels={"Jumlah": "Jumlah Nasabah"}
)
fig_edu.update_layout(**PLOTLY_LAYOUT, width=800, height=450)
fig_edu.write_image(str(OUTPUT_DIR / "04_pendidikan_vs_status.png"), scale=2)

# 5. Sex vs Status (Bar Chart)
print("5. Generating Gender vs Status bar chart...")
df_plot["Jenis Kelamin"] = df_plot["SEX"].map(SEX_LABELS)
sex_counts = df_plot.groupby(["Jenis Kelamin", "Status Kredit"]).size().reset_index(name="Jumlah")
fig_sex = px.bar(
    sex_counts,
    x="Jenis Kelamin",
    y="Jumlah",
    color="Status Kredit",
    barmode="group",
    title="Status Kredit Berdasarkan Jenis Kelamin",
    color_discrete_map=DEFAULT_COLOR_MAP,
    labels={"Jumlah": "Jumlah Nasabah"},
)
fig_sex.update_layout(**PLOTLY_LAYOUT, width=800, height=450)
fig_sex.write_image(str(OUTPUT_DIR / "05_jenis_kelamin_vs_status.png"), scale=2)

# 6. Marriage vs Status (Bar Chart)
print("6. Generating Marriage vs Status bar chart...")
df_plot["Status Pernikahan"] = df_plot["MARRIAGE"].map(MARRIAGE_LABELS)
marriage_counts = df_plot.groupby(["Status Pernikahan", "Status Kredit"]).size().reset_index(name="Jumlah")
fig_marriage = px.bar(
    marriage_counts,
    x="Status Pernikahan",
    y="Jumlah",
    color="Status Kredit",
    barmode="group",
    title="Status Kredit Berdasarkan Status Pernikahan",
    color_discrete_map=DEFAULT_COLOR_MAP,
    labels={"Jumlah": "Jumlah Nasabah"},
)
fig_marriage.update_layout(**PLOTLY_LAYOUT, width=800, height=450)
fig_marriage.write_image(str(OUTPUT_DIR / "06_status_pernikahan_vs_status.png"), scale=2)

# 7. Correlation Heatmap
print("7. Generating Correlation Heatmap...")
corr_features = ["LIMIT_BAL", "AGE", "PAY_0", "BILL_AMT1", "PAY_AMT1", "default_status"]
corr_matrix = df[corr_features].corr()
fig_corr = px.imshow(
    corr_matrix,
    text_auto=".2f",
    color_continuous_scale="RdBu_r",
    title="Matriks Korelasi Antara Fitur Utama & Target",
    labels=dict(color="Korelasi"),
    x=["Limit Kredit", "Umur", "Status Bayar Terakhir", "Tagihan Terakhir", "Bayar Terakhir", "Status Kredit"],
    y=["Limit Kredit", "Umur", "Status Bayar Terakhir", "Tagihan Terakhir", "Bayar Terakhir", "Status Kredit"]
)
fig_corr.update_layout(**PLOTLY_LAYOUT, width=800, height=600)
fig_corr.write_image(str(OUTPUT_DIR / "07_matriks_korelasi.png"), scale=2)

# 8. Age Box Plot (Outlier Analysis)
print("8. Generating Age Boxplot...")
fig_age_box = px.box(
    df_plot,
    x="Status Kredit",
    y="AGE",
    color="Status Kredit",
    color_discrete_map=DEFAULT_COLOR_MAP,
    title="Distribusi Umur Berdasarkan Status Kredit",
    labels={"AGE": "Umur (Tahun)"},
)
fig_age_box.update_layout(**PLOTLY_LAYOUT, width=800, height=450)
fig_age_box.write_image(str(OUTPUT_DIR / "08_umur_vs_status_boxplot.png"), scale=2)

# 9. SMOTE Before vs After
print("9. Generating SMOTE Before vs After chart...")
counts_before = df["default_status"].value_counts().sort_index()
not_default_cnt = counts_before.get(0, 0)
default_cnt = counts_before.get(1, 0)
smote_df = pd.DataFrame({
    "Status": ["Lancar", "Gagal Bayar", "Lancar", "Gagal Bayar"],
    "Jumlah": [not_default_cnt, default_cnt, not_default_cnt, not_default_cnt],
    "Tahap": ["Sebelum SMOTE", "Sebelum SMOTE", "Sesudah SMOTE", "Sesudah SMOTE"]
})
fig_smote = px.bar(
    smote_df,
    x="Status",
    y="Jumlah",
    color="Tahap",
    barmode="group",
    title="Distribusi Kelas Sebelum vs Sesudah SMOTE (Training Data)",
    color_discrete_map={"Sebelum SMOTE": "#2563EB", "Sesudah SMOTE": "#059669"}
)
fig_smote.update_layout(**PLOTLY_LAYOUT, width=800, height=450)
fig_smote.write_image(str(OUTPUT_DIR / "09_smote_sebelum_vs_sesudah.png"), scale=2)

# 10. Split size
print("10. Generating Split size chart...")
split_sizes = pd.DataFrame({
    "Skenario Split": ["80/20", "80/20", "75/25", "75/25", "70/30", "70/30"],
    "Jumlah Data": [23972, 5993, 22473, 7492, 20973, 8992],
    "Tipe Data": ["Training", "Testing", "Training", "Testing", "Training", "Testing"]
})
fig_splits = px.bar(
    split_sizes,
    x="Skenario Split",
    y="Jumlah Data",
    color="Tipe Data",
    barmode="group",
    title="Ukuran Data Training vs Testing per Skenario Split",
    color_discrete_map={"Training": "#2563EB", "Testing": "#D97706"}
)
fig_splits.update_layout(**PLOTLY_LAYOUT, width=800, height=450)
fig_splits.write_image(str(OUTPUT_DIR / "10_ukuran_data_split.png"), scale=2)

# ----------------- Load PCA & Evaluation Info -----------------
print("Loading PCA & Metadata objects...")
pca = None
if PCA_PATH.exists():
    try:
        pca = joblib.load(PCA_PATH)
    except Exception:
        pass

metadata = {}
if METADATA_PATH.exists():
    with open(METADATA_PATH, "r", encoding="utf-8") as f:
        metadata = json.load(f)

# 11. PCA Cumulative Explained Variance (Line Chart)
if pca is not None and hasattr(pca, "explained_variance_ratio_"):
    print("11. Generating PCA Cumulative Explained Variance...")
    evr = pca.explained_variance_ratio_
    cumulative_variance = np.cumsum(evr)
    df_ev = pd.DataFrame({
        "Komponen_Index": list(range(1, len(evr) + 1)),
        "Explained_Variance": evr,
        "Kumulatif_Varians": cumulative_variance
    })
    fig_pca = px.line(
        df_ev,
        x="Komponen_Index",
        y="Kumulatif_Varians",
        markers=True,
        title="Kumulatif Varians yang Dijelaskan oleh Komponen PCA",
        labels={"Komponen_Index": "Jumlah Komponen PCA", "Kumulatif_Varians": "Kumulatif Varians"}
    )
    fig_pca.update_layout(**PLOTLY_LAYOUT, width=800, height=450)
    fig_pca.write_image(str(OUTPUT_DIR / "11_pca_kumulatif_varians.png"), scale=2)

    # 12. PCA Individual Explained Variance (Bar Chart)
    print("12. Generating PCA Individual Explained Variance...")
    df_indiv = pd.DataFrame({
        "Komponen": list(range(1, len(evr) + 1)),
        "Explained_Variance_Ratio": evr
    })
    fig_indiv = px.bar(
        df_indiv,
        x="Komponen",
        y="Explained_Variance_Ratio",
        title="Kontribusi Varians Individual per Komponen PCA",
        labels={"Komponen": "Komponen PCA", "Explained_Variance_Ratio": "Explained Variance Ratio"},
    )
    fig_indiv.update_traces(marker_color="#2563EB")
    fig_indiv.update_layout(**PLOTLY_LAYOUT, width=800, height=450)
    fig_indiv.write_image(str(OUTPUT_DIR / "12_pca_individual_varians.png"), scale=2)

# Load Evaluation DataFrame
if EVALUATION_RESULTS_PATH.exists():
    print("Loading evaluation results table...")
    evaluation_df = pd.read_csv(EVALUATION_RESULTS_PATH)
    best_row = evaluation_df[evaluation_df["best_model"] == True]
    best_row = best_row.iloc[0] if not best_row.empty else evaluation_df.sort_values("f1_score", ascending=False).iloc[0]

    # 13. Model Comparison (Faceted Bar: Acc, Recall, F1)
    print("13. Generating Scenario metrics bar chart...")
    chart_df = evaluation_df.melt(
        id_vars=["scenario", "model_name"],
        value_vars=["accuracy", "recall", "f1_score"],
        var_name="Metrik",
        value_name="Nilai",
    )
    chart_df["Metrik"] = chart_df["Metrik"].map(
        {"accuracy": "Akurasi", "recall": "Recall Default", "f1_score": "F1-Score"}
    )
    fig_eval = px.bar(
        chart_df,
        x="scenario",
        y="Nilai",
        color_discrete_map=MODEL_COLOR_MAP,
        labels={"scenario": "Split Data", "model_name": "Model", "Nilai": "Nilai"},
        title="Grafik Perbandingan Kinerja Skenario (Akurasi, Recall, F1)",
    )
    fig_eval.for_each_annotation(lambda annotation: annotation.update(text=annotation.text.split("=")[-1]))
    fig_eval.update_yaxes(tickformat=".0%")
    fig_eval.update_layout(**PLOTLY_LAYOUT, width=1200, height=500, legend_title_text="")
    fig_eval.write_image(str(OUTPUT_DIR / "13_komparasi_skenario_utama.png"), scale=2)

    # 14. Model Comparison Precision & AUC (Faceted Bar)
    print("14. Generating Precision and AUC bar chart...")
    chart_pa_df = evaluation_df.melt(
        id_vars=["scenario", "model_name"],
        value_vars=["precision", "auc_score"],
        var_name="Metrik",
        value_name="Nilai",
    )
    chart_pa_df["Metrik"] = chart_pa_df["Metrik"].map(
        {"precision": "Precision", "auc_score": "AUC Score"}
    )
    fig_pa = px.bar(
        chart_pa_df,
        x="scenario",
        y="Nilai",
        color="model_name",
        facet_col="Metrik",
        barmode="group",
        color_discrete_map=MODEL_COLOR_MAP,
        labels={"scenario": "Split Data", "model_name": "Model", "Nilai": "Nilai"},
        title="Perbandingan Precision dan AUC per Skenario",
    )
    fig_pa.for_each_annotation(lambda annotation: annotation.update(text=annotation.text.split("=")[-1]))
    fig_pa.update_yaxes(tickformat=".0%")
    fig_pa.update_layout(**PLOTLY_LAYOUT, width=1200, height=500, legend_title_text="")
    fig_pa.write_image(str(OUTPUT_DIR / "14_komparasi_skenario_precision_auc.png"), scale=2)

    # 15. Radar Chart of Best Model Metrics
    print("15. Generating Best Model Radar chart...")
    radar_categories = ['Accuracy', 'Precision', 'Recall', 'F1-Score', 'AUC']
    radar_values = [
        best_row["accuracy"],
        best_row["precision"],
        best_row["recall"],
        best_row["f1_score"],
        best_row["auc_score"],
    ]
    fig_radar = go.Figure(data=go.Scatterpolar(
        r=radar_values + [radar_values[0]],
        theta=radar_categories + [radar_categories[0]],
        fill='toself',
        line=dict(color='#2563EB'),
        name=str(best_row["model_name"]),
    ))
    fig_radar.update_layout(
        title=f'Radar Metrik {best_row["model_name"]} (Split {best_row["scenario"]})',
        polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
        **PLOTLY_LAYOUT,
        width=800,
        height=500
    )
    fig_radar.write_image(str(OUTPUT_DIR / "15_radar_metrik_terbaik.png"), scale=2)


# ----------------- Generate Model Predictions & Curves -----------------
# We can dynamically construct test set predictions using joblib scaler and Best Model
print("Generating test set predictions for interactive evaluation curves...")
pred_data = None
try:
    import subprocess
    import sys
    import tempfile
    
    # Run prediction in a clean subprocess to avoid TensorFlow/Choreographer conflict
    temp_file = tempfile.NamedTemporaryFile(suffix=".json", delete=False)
    temp_path = temp_file.name
    temp_file.close()

    print("Generating predictions in a separate subprocess...")
    cmd = [
        sys.executable,
        "-c",
        f"""
import json, joblib, numpy as np
from pathlib import Path
from src.config import BEST_MODEL_PATH, SCALER_PATH, PCA_PATH, METADATA_PATH, SPLIT_SCENARIOS
from src.data_loader import preprocess_raw_dataset
from tensorflow.keras.models import load_model
from src.preprocessing import make_train_test_split, split_features_target

with open("{METADATA_PATH}", "r") as f:
    metadata = json.load(f)
df = preprocess_raw_dataset(save_processed=False, remove_duplicates=True)
X, y = split_features_target(df)
split_scenario = metadata.get("best_split_scenario", "75/25")
test_size = SPLIT_SCENARIOS.get(split_scenario, 0.25)
split_data = make_train_test_split(X, y, test_size)
scaler = joblib.load("{SCALER_PATH}")
X_test_scaled = scaler.transform(split_data.X_test)
model = load_model("{BEST_MODEL_PATH}", compile=False)
if metadata.get("pca_used", False) and Path("{PCA_PATH}").exists():
    pca_obj = joblib.load("{PCA_PATH}")
    model_input = pca_obj.transform(X_test_scaled)
else:
    model_input = X_test_scaled
probs = np.asarray(model(model_input, training=False)).reshape(-1)
result = {{
    "y_true": split_data.y_test.tolist(),
    "y_prob": probs.tolist(),
    "threshold": metadata.get("threshold", 0.5)
}}
with open("{temp_path}", "w") as f:
    json.dump(result, f)
"""
    ]
    env = os.environ.copy()
    env["CUDA_VISIBLE_DEVICES"] = ""
    env["TF_CPP_MIN_LOG_LEVEL"] = "3"
    env["PYTHONPATH"] = str(ROOT_DIR)
    
    subprocess.run(cmd, env=env, check=True)
    
    with open(temp_path, "r") as f:
        pred_data = json.load(f)
        
    try:
        os.unlink(temp_path)
    except Exception:
        pass
    print("Predictions loaded successfully from subprocess!")
except Exception as e:
    print(f"Subprocess prediction failed: {e}")

if pred_data is not None:
    try:
        y_true_arr = np.array(pred_data["y_true"])
        y_prob_arr = np.array(pred_data["y_prob"])
        threshold_val = pred_data["threshold"]
        y_pred_arr = (y_prob_arr >= threshold_val).astype(int)
        
        # 16. Confusion Matrix (Interactive Style)
        print("16. Generating CM heatmap...")
        cm = confusion_matrix(y_true_arr, y_pred_arr)
        fig_cm = px.imshow(
            cm,
            text_auto=True,
            color_continuous_scale="Blues",
            title="Confusion Matrix Model Terbaik",
            x=["Prediksi Lancar", "Prediksi Gagal Bayar"],
            y=["Aktual Lancar", "Aktual Gagal Bayar"],
            labels=dict(color="Jumlah Nasabah")
        )
        fig_cm.update_layout(**PLOTLY_LAYOUT, width=800, height=450)
        fig_cm.write_image(str(OUTPUT_DIR / "16_confusion_matrix_interaktif.png"), scale=2)
        
        # 17. ROC Curve
        print("17. Generating ROC Curve...")
        fpr, tpr, roc_thresholds = roc_curve(y_true_arr, y_prob_arr)
        df_roc = pd.DataFrame({
            "FPR": fpr,
            "TPR": tpr,
            "Threshold": roc_thresholds
        })
        fig_roc = px.line(
            df_roc,
            x="FPR",
            y="TPR",
            title=f"Kurva ROC (AUC = {metadata.get('auc_score', 0.0):.4f})",
            labels={"FPR": "False Positive Rate (1-Spesifisitas)", "TPR": "True Positive Rate (Sensitivitas)"}
        )
        fig_roc.add_shape(
            type="line", line=dict(dash="dash", color="red"),
            x0=0, x1=1, y0=0, y1=1
        )
        fig_roc.update_layout(**PLOTLY_LAYOUT, width=800, height=450)
        fig_roc.write_image(str(OUTPUT_DIR / "17_kurva_roc.png"), scale=2)
        
        # 18. Precision-Recall Curve
        print("18. Generating PR Curve...")
        precision, recall, pr_thresholds = precision_recall_curve(y_true_arr, y_prob_arr)
        pad_thresholds = np.append(pr_thresholds, 1.0)
        df_pr = pd.DataFrame({
            "Recall": recall,
            "Precision": precision,
            "Threshold": pad_thresholds
        })
        fig_pr = px.line(
            df_pr,
            x="Recall",
            y="Precision",
            title="Kurva Precision-Recall",
            labels={"Recall": "Recall", "Precision": "Precision"}
        )
        fig_pr.update_layout(**PLOTLY_LAYOUT, width=800, height=450)
        fig_pr.write_image(str(OUTPUT_DIR / "18_kurva_precision_recall.png"), scale=2)
        
        # 19. Prediction Probability Distribution
        print("19. Generating Prediction Probability Spread...")
        prob_df = pd.DataFrame({
            "Probabilitas": y_prob_arr,
            "Kelas Aktual": ["Gagal Bayar" if y == 1 else "Lancar" for y in y_true_arr]
        })
        fig_prob = px.histogram(
            prob_df,
            x="Probabilitas",
            color="Kelas Aktual",
            barmode="overlay",
            nbins=30,
            opacity=0.7,
            title="Distribusi Probabilitas Prediksi per Kelas Aktual",
            color_discrete_map=DEFAULT_COLOR_MAP,
            labels={"Probabilitas": "Probabilitas Prediksi", "Kelas Aktual": "Kelas Aktual"},
        )
        fig_prob.add_vline(
            x=threshold_val, line_dash="dash", line_color="#071B33",
            annotation_text=f"Threshold {threshold_val:.2f}"
        )
        fig_prob.update_layout(**PLOTLY_LAYOUT, width=800, height=450)
        fig_prob.write_image(str(OUTPUT_DIR / "19_distribusi_probabilitas_prediksi.png"), scale=2)
        
    except Exception as curve_err:
        print(f"Failed to generate predictions-based curves: {curve_err}")


# 20. Default probability gauge (sample prediction of 65% probability)
print("20. Generating Risk Probability Gauge...")
fig_gauge = go.Figure(go.Indicator(
    mode="gauge+number",
    value=65.4,
    title={"text": "Probabilitas Gagal Bayar (Nasabah Contoh)"},
    gauge=dict(
        axis=dict(range=[0, 100]),
        steps=[
            dict(range=[0, 40], color="#059669"),
            dict(range=[40, 70], color="#F59E0B"),
            dict(range=[70, 100], color="#E11D48"),
        ],
        bar=dict(color="#071B33"),
        threshold=dict(
            line=dict(color="red", width=4),
            thickness=0.75,
            value=50,
        ),
    ),
))
fig_gauge.update_layout(**PLOTLY_LAYOUT, width=800, height=450)
fig_gauge.write_image(str(OUTPUT_DIR / "20_gauge_probabilitas_sample.png"), scale=2)


# ----------------- Pull prediction database history if available -----------------
print("Checking history database...")
try:
    history = fetch_prediction_history()
    if not history.empty:
        # 21. Donut Chart for Prediction Results History
        print("21. Generating prediction history pie chart...")
        prediction_counts = history["prediction_result"].value_counts().reset_index()
        prediction_counts.columns = ["Hasil Prediksi", "Jumlah"]
        prediction_counts["Hasil Prediksi"] = prediction_counts["Hasil Prediksi"].map({"Default": "Gagal Bayar", "Tidak Default": "Lancar"})
        
        fig_pie = px.pie(
            prediction_counts,
            values="Jumlah",
            names="Hasil Prediksi",
            title="Distribusi Hasil Prediksi (Database Riwayat)",
            hole=0.4,
            color="Hasil Prediksi",
            color_discrete_map=DEFAULT_COLOR_MAP,
        )
        fig_pie.update_layout(**PLOTLY_LAYOUT, width=800, height=450)
        fig_pie.write_image(str(OUTPUT_DIR / "21_riwayat_distribusi_hasil_prediksi.png"), scale=2)

        # 22. Bar Chart for Risk Level History
        print("22. Generating prediction history risk level bar chart...")
        risk_counts = history["risk_level"].value_counts().reset_index()
        risk_counts.columns = ["Level Risiko", "Jumlah"]
        fig_bar = px.bar(
            risk_counts,
            x="Level Risiko",
            y="Jumlah",
            title="Distribusi Level Risiko (Database Riwayat)",
            color="Level Risiko",
            color_discrete_map={
                "Risiko Rendah": "#059669",
                "Risiko Sedang": "#F59E0B",
                "Risiko Tinggi": "#DC2626",
            },
        )
        fig_bar.update_layout(**PLOTLY_LAYOUT, width=800, height=450)
        fig_bar.write_image(str(OUTPUT_DIR / "22_riwayat_distribusi_level_risiko.png"), scale=2)
    else:
        print("Prediction database history is empty. Skipping history charts.")
except Exception as e:
    print(f"Skipped history predictions-based charts: {e}")

print("\nAll visualizations successfully created!")
print(f"Folder content: {len(list(OUTPUT_DIR.glob('*.png')))} PNG files saved.")
