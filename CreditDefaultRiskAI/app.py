import json
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from src.config import (
    BEST_MODEL_PATH,
    DATABASE_PATH,
    EVALUATION_RESULTS_PATH,
    FEATURE_COLUMNS,
    FIGURES_DIR,
    METADATA_PATH,
    PROCESSED_DATA_PATH,
    SCALER_PATH,
    PCA_PATH,
)
from src.data_loader import get_dataset_summary, preprocess_raw_dataset
from src.database import clear_prediction_history, fetch_prediction_history, insert_prediction
from src.predict import get_recommendation, predict_default


st.set_page_config(
    page_title="Credit Default Risk AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)


BRAND_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

.stApp {
    background: radial-gradient(circle at 50% 0%, #FFFFFF 0%, #F5F7FB 100%) !important;
    color: #0F172A !important;
}

/* Sidebar Styling */
section[data-testid="stSidebar"] {
    background-color: #071B33 !important;
    border-right: 1px solid #E5E7EB !important;
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span {
    color: #FFFFFF !important;
}

section[data-testid="stSidebar"] label {
    color: #64748B !important;
}

/* Redesign sidebar navigation items (st.radio) to look like menu list buttons */
section[data-testid="stSidebar"] div[data-testid="stRadio"] [role="radiogroup"] {
    padding: 0 !important;
}

section[data-testid="stSidebar"] div[data-testid="stRadio"] [role="radiogroup"] label {
    display: flex !important;
    align-items: center !important;
    background-color: transparent !important;
    border: 1px solid transparent !important;
    border-radius: 12px !important;
    padding: 12px 18px !important;
    color: #94A3B8 !important; /* light gray for unselected text in dark sidebar */
    margin-bottom: 8px !important;
    cursor: pointer !important;
    transition: all 0.2s ease-in-out !important;
    width: 100% !important;
}

section[data-testid="stSidebar"] div[data-testid="stRadio"] [role="radiogroup"] label:hover {
    background-color: rgba(255, 255, 255, 0.08) !important;
    color: #FFFFFF !important;
    transform: translateX(4px) !important;
}

/* Active navigation item has gradient pill background */
section[data-testid="stSidebar"] div[data-testid="stRadio"] [role="radiogroup"] label[data-checked="true"],
section[data-testid="stSidebar"] div[data-testid="stRadio"] [role="radiogroup"] label:has(input:checked) {
    background: linear-gradient(135deg, #2563EB 0%, #E11D48 100%) !important;
    color: #FFFFFF !important;
    font-weight: 700 !important;
    box-shadow: 0 4px 15px rgba(37, 99, 235, 0.3) !important;
}

/* Hide standard radio dot indicator and empty containers */
section[data-testid="stSidebar"] div[data-testid="stRadio"] [role="radiogroup"] label div[data-testid="stMarker"],
section[data-testid="stSidebar"] div[data-testid="stRadio"] [role="radiogroup"] label > div:first-child:not([data-testid="stMarkdownContainer"]),
section[data-testid="stSidebar"] div[data-testid="stRadio"] [role="radiogroup"] label input[type="radio"] {
    display: none !important;
    width: 0 !important;
    height: 0 !important;
    opacity: 0 !important;
    margin: 0 !important;
    padding: 0 !important;
}

/* Align text to the left in the radio button layout */
section[data-testid="stSidebar"] div[data-testid="stRadio"] [role="radiogroup"] label [data-testid="stMarkdownContainer"] {
    width: 100% !important;
    text-align: left !important;
}

/* Styling main content horizontal radio buttons as elegant Segmented controls */
div[data-testid="stRadio"] [role="radiogroup"] {
    display: flex !important;
    flex-direction: row !important;
    gap: 8px !important;
    background-color: rgba(15, 23, 42, 0.04) !important;
    padding: 6px !important;
    border-radius: 14px !important;
    border: 1px solid rgba(15, 23, 42, 0.06) !important;
    width: fit-content !important;
}

div[data-testid="stRadio"] [role="radiogroup"] label {
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    padding: 10px 20px !important;
    border-radius: 10px !important;
    background-color: transparent !important;
    border: 1px solid transparent !important;
    color: #64748B !important;
    font-weight: 600 !important;
    font-size: 13.5px !important;
    cursor: pointer !important;
    margin: 0 !important;
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
    box-shadow: none !important;
}

/* Force all inner wrappers of options to be transparent and borderless by default */
div[data-testid="stRadio"] [role="radiogroup"] label div,
div[data-testid="stRadio"] [role="radiogroup"] label span {
    background-color: transparent !important;
    border: none !important;
    box-shadow: none !important;
}

div[data-testid="stRadio"] [role="radiogroup"] label:hover {
    color: #0F172A !important;
}

div[data-testid="stRadio"] [role="radiogroup"] label[data-checked="true"],
div[data-testid="stRadio"] [role="radiogroup"] label:has(input:checked) {
    background-color: #FFFFFF !important;
    color: #2563EB !important;
    font-weight: 700 !important;
    border: 1px solid rgba(15, 23, 42, 0.05) !important;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06) !important;
}

/* Force color change on the text container inside the active label */
div[data-testid="stRadio"] [role="radiogroup"] label[data-checked="true"] [data-testid="stMarkdownContainer"] *,
div[data-testid="stRadio"] [role="radiogroup"] label:has(input:checked) [data-testid="stMarkdownContainer"] * {
    color: #2563EB !important;
    font-weight: 700 !important;
}

/* Hide standard dot indicators for segmented controls */
div[data-testid="stRadio"] [role="radiogroup"] label div[data-testid="stMarker"],
div[data-testid="stRadio"] [role="radiogroup"] label > div:first-child:not([data-testid="stMarkdownContainer"]),
div[data-testid="stRadio"] [role="radiogroup"] label input[type="radio"] {
    display: none !important;
    width: 0 !important;
    height: 0 !important;
    margin: 0 !important;
    padding: 0 !important;
    opacity: 0 !important;
}

/* Brand header design */
.brand-container {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 24px;
    padding: 8px 4px;
}

.brand-title {
    margin: 0;
    color: #FFFFFF;
    font-weight: 800;
    font-size: 18px;
    letter-spacing: 0.5px;
    line-height: 1.2;
}

.brand-subtitle {
    color: #64748B;
    font-size: 11px;
}

/* Hero Section */
.hero-card {
    position: relative;
    background: linear-gradient(135deg, #071B33 0%, #2563EB 55%, #E11D48 100%);
    border-radius: 24px;
    padding: 40px;
    color: #FFFFFF;
    overflow: hidden;
    box-shadow: 0 20px 40px rgba(7, 27, 51, 0.15);
    margin-bottom: 24px;
}

.hero-glow {
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, rgba(255, 255, 255, 0.08) 0%, transparent 60%);
    pointer-events: none;
}

.hero-badge {
    display: inline-block;
    background: rgba(255, 255, 255, 0.15);
    color: #FFFFFF;
    backdrop-filter: blur(8px);
    padding: 6px 14px;
    border-radius: 99px;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 0.5px;
    margin-bottom: 18px;
    border: 1px solid rgba(255, 255, 255, 0.2);
}

.hero-title {
    font-size: 38px;
    font-weight: 800;
    margin: 0 0 12px 0;
    line-height: 1.2;
    letter-spacing: -0.5px;
    color: #FFFFFF;
}

.hero-subtitle {
    font-size: 16px;
    line-height: 1.6;
    color: rgba(255, 255, 255, 0.85);
    max-width: 800px;
    margin: 0;
}

/* Content Container Cards (st.container(border=True)) */
div[data-testid="stContainer"] {
    background-color: #FFFFFF !important;
    border: 1px solid #E5E7EB !important;
    border-radius: 20px !important;
    padding: 24px !important;
    box-shadow: 0 10px 30px rgba(15, 23, 42, 0.04) !important;
    margin-bottom: 24px !important;
}

/* Step Preprocessing card layout */
.step-card {
    background: #FFFFFF;
    border: 1px solid #E5E7EB;
    border-radius: 18px;
    padding: 20px;
    box-shadow: 0 8px 24px rgba(15, 23, 42, 0.03);
    margin-bottom: 16px;
    transition: all 0.2s ease;
    min-height: 160px;
}

.step-card:hover {
    transform: translateY(-2px);
    border-color: #3B82F6;
    box-shadow: 0 10px 30px rgba(59, 130, 246, 0.08);
}

.step-card h4 {
    margin: 0 0 10px 0;
    color: #0F172A;
    font-weight: 700;
    font-size: 16px;
}

.step-card p {
    margin: 0;
    color: #64748B;
    font-size: 13.5px;
    line-height: 1.5;
}

/* Metric Cards */
.metric-card {
    background: #FFFFFF;
    border: 1px solid #E5E7EB;
    border-radius: 18px;
    padding: 20px;
    position: relative;
    overflow: hidden;
    box-shadow: 0 4px 12px rgba(15, 23, 42, 0.03);
    transition: all 0.25s ease-in-out;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    min-height: 120px;
    margin-bottom: 16px;
}

.metric-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 12px 24px rgba(15, 23, 42, 0.08);
    border-color: #3B82F6;
}

.metric-accent {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: linear-gradient(90deg, #2563EB 0%, #E11D48 100%);
}

.metric-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 10px;
}

.metric-label {
    color: #64748B;
    font-size: 12.5px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.metric-icon-wrapper {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 32px;
    height: 32px;
    border-radius: 8px;
    background: #F0F4FF;
    color: #2563EB;
}

.metric-value {
    color: #0F172A;
    font-size: 24px;
    font-weight: 800;
    margin-bottom: 6px;
}

.metric-caption {
    color: #64748B;
    font-size: 12px;
}

/* Button Customizations */
div.stButton > button, 
div.stFormSubmitButton > button {
    border-radius: 12px !important;
    padding: 10px 24px !important;
    font-weight: 700 !important;
    transition: all 0.2s ease-in-out !important;
}

button[data-testid="stBaseButton-primary"],
div.stFormSubmitButton > button {
    background: linear-gradient(135deg, #2563EB 0%, #E11D48 100%) !important;
    color: #FFFFFF !important;
    border: none !important;
    box-shadow: 0 4px 14px rgba(37, 99, 235, 0.3) !important;
}

button[data-testid="stBaseButton-primary"]:hover,
div.stFormSubmitButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(37, 99, 235, 0.4) !important;
    filter: brightness(1.08) !important;
}

button[data-testid="stBaseButton-secondary"] {
    background: transparent !important;
    color: #2563EB !important;
    border: 2px solid #2563EB !important;
    box-shadow: 0 2px 6px rgba(37, 99, 235, 0.05) !important;
}

button[data-testid="stBaseButton-secondary"]:hover {
    transform: translateY(-2px) !important;
    background-color: rgba(37, 99, 235, 0.06) !important;
    box-shadow: 0 4px 12px rgba(37, 99, 235, 0.15) !important;
}

/* Custom Workflow Pipeline layout */
.pipeline-container {
    background: #FFFFFF;
    border: 1px solid #E5E7EB;
    border-radius: 20px;
    padding: 24px;
    box-shadow: 0 10px 30px rgba(15, 23, 42, 0.04);
    margin-top: 12px;
    margin-bottom: 24px;
}

.pipeline-title {
    font-size: 18px;
    font-weight: 800;
    color: #0F172A;
    margin-bottom: 20px;
    letter-spacing: -0.3px;
}

.pipeline-steps {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 8px;
}

.pipeline-step {
    flex: 1;
    min-width: 130px;
    background: #F8FAFC;
    border: 1px solid #E5E7EB;
    border-radius: 12px;
    padding: 16px 12px;
    text-align: center;
    transition: all 0.2s ease;
}

.pipeline-step:hover {
    border-color: #2563EB;
    background: #F0F4FF;
    transform: translateY(-2px);
}

.step-num {
    font-size: 20px;
    font-weight: 850;
    color: #2563EB;
    margin-bottom: 4px;
}

.step-label {
    font-size: 12px;
    font-weight: 700;
    color: #0F172A;
    margin-bottom: 4px;
}

.step-desc {
    font-size: 11px;
    color: #64748B;
}

.pipeline-arrow {
    color: #94A3B8;
    font-size: 20px;
    font-weight: 800;
}

/* Risk Prediction Results Cards */
.risk-card-low, .risk-card-medium, .risk-card-high {
    border-radius: 20px;
    color: #FFFFFF;
    padding: 28px;
    box-shadow: 0 15px 35px rgba(15, 23, 42, 0.12);
    margin-bottom: 24px;
}

.risk-card-low { background: linear-gradient(135deg, #064E3B 0%, #10B981 100%); }
.risk-card-medium { background: linear-gradient(135deg, #92400E 0%, #F59E0B 100%); }
.risk-card-high { background: linear-gradient(135deg, #991B1B 0%, #E11D48 100%); }

.risk-card-low h2, .risk-card-medium h2, .risk-card-high h2 {
    color: #FFFFFF !important;
    font-size: 28px;
    font-weight: 800;
    margin: 0 0 10px 0;
}

.risk-card-low p, .risk-card-medium p, .risk-card-high p {
    color: rgba(255, 255, 255, 0.9) !important;
    margin: 4px 0;
    line-height: 1.5;
}

.prediction-summary {
    background: #FFFFFF;
    border: 1px solid #E5E7EB;
    border-radius: 20px;
    padding: 24px;
    box-shadow: 0 10px 30px rgba(15, 23, 42, 0.04);
}

.prediction-summary h3 {
    margin: 0 0 12px 0;
    color: #0F172A;
    font-weight: 800;
}

.prediction-summary p {
    margin: 0;
    color: #475569;
    line-height: 1.6;
}

/* Form layouts */
div[data-testid="stForm"] {
    background: #FFFFFF !important;
    border: 1px solid #E5E7EB !important;
    border-radius: 20px !important;
    padding: 28px !important;
    box-shadow: 0 10px 30px rgba(15, 23, 42, 0.04) !important;
}

/* Input boxes overrides */
div[data-testid="stNumberInput"] input,
div[data-testid="stTextInput"] input,
div[data-baseweb="input"] {
    background-color: #FFFFFF !important;
    color: #0F172A !important;
    border-color: #E5E7EB !important;
    border-radius: 10px !important;
}

/* Info Box / Status badges */
.info-box {
    background: #F0F4FF;
    border-left: 5px solid #2563EB;
    border-radius: 12px;
    color: #071B33;
    padding: 16px 20px;
    font-size: 14.5px;
    margin-bottom: 20px;
    font-weight: 500;
}

.status-badge {
    display: inline-block;
    background: #E0F2FE;
    color: #2563EB;
    border-radius: 99px;
    padding: 6px 14px;
    font-size: 11.5px;
    font-weight: 700;
}

/* Sidebar best model card */
.sidebar-best-card {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 16px;
    padding: 16px;
    margin-top: 12px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.sidebar-best-card .badge {
    display: inline-block;
    background: linear-gradient(135deg, #10B981 0%, #059669 100%);
    color: #FFFFFF !important;
    border-radius: 99px;
    padding: 4px 10px;
    font-size: 11px;
    font-weight: 800;
    margin-bottom: 8px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.sidebar-best-card .model {
    color: #FFFFFF;
    font-size: 15px;
    font-weight: 700;
    margin-bottom: 4px;
}

.sidebar-best-card .split {
    color: #94A3B8;
    font-size: 11.5px;
}

/* Expanders */
div[data-testid="stExpander"] {
    background: #FFFFFF !important;
    border: 1px solid #E5E7EB !important;
    border-radius: 12px !important;
    margin-bottom: 12px !important;
}

div[data-testid="stExpander"] summary,
div[data-testid="stExpander"] p {
    color: #0F172A !important;
}
</style>
"""

st.markdown(BRAND_CSS, unsafe_allow_html=True)


@st.cache_data(show_spinner=False)
def load_dataset() -> pd.DataFrame:
    return preprocess_raw_dataset(save_processed=True, remove_duplicates=True)


@st.cache_data(show_spinner=False)
def load_metadata() -> dict:
    if METADATA_PATH.exists():
        with open(METADATA_PATH, "r", encoding="utf-8") as file:
            return json.load(file)
    return {}


@st.cache_data(show_spinner=False)
def load_evaluation_results() -> pd.DataFrame:
    if EVALUATION_RESULTS_PATH.exists():
        return pd.read_csv(EVALUATION_RESULTS_PATH)
    return pd.DataFrame()


def add_chart_downloads(fig, df_data: pd.DataFrame, filename_prefix: str) -> None:
    col_csv, col_png = st.columns([1, 1])
    
    csv = df_data.to_csv(index=False).encode('utf-8')
    col_csv.download_button(
        label="📥 Unduh Data (CSV)",
        data=csv,
        file_name=f"{filename_prefix}_data.csv",
        mime="text/csv",
        key=f"dl_csv_{filename_prefix}",
        use_container_width=True
    )
    
    try:
        png_bytes = fig.to_image(format="png", width=1200, height=600, scale=2)
        col_png.download_button(
            label="📊 Unduh Grafik (PNG)",
            data=png_bytes,
            file_name=f"{filename_prefix}_chart.png",
            mime="image/png",
            key=f"dl_png_{filename_prefix}",
            use_container_width=True
        )
    except Exception:
        import io
        buf = io.StringIO()
        fig.write_html(buf, include_plotlyjs="cdn")
        col_png.download_button(
            label="📊 Unduh Grafik (HTML)",
            data=buf.getvalue().encode('utf-8'),
            file_name=f"{filename_prefix}_chart.html",
            mime="text/html",
            key=f"dl_png_{filename_prefix}",
            use_container_width=True
        )


@st.cache_data(show_spinner=False)
def get_best_model_predictions():
    from src.config import BEST_MODEL_PATH, SCALER_PATH, PCA_PATH, METADATA_PATH, SPLIT_SCENARIOS
    if not BEST_MODEL_PATH.exists() or not SCALER_PATH.exists() or not METADATA_PATH.exists():
        return None
    try:
        from src.preprocessing import make_train_test_split, split_features_target
        import joblib
        import numpy as np
        from tensorflow.keras.models import load_model
        
        # Load metadata
        with open(METADATA_PATH, "r", encoding="utf-8") as file:
            metadata = json.load(file)
            
        # Load dataset
        df = preprocess_raw_dataset(save_processed=False, remove_duplicates=True)
        X, y = split_features_target(df)
        
        # Get test size from metadata
        split_scenario = metadata.get("best_split_scenario", "75/25")
        test_size = SPLIT_SCENARIOS.get(split_scenario, 0.25)
        
        # Split and Scale
        split_data = make_train_test_split(X, y, test_size)
        scaler = joblib.load(SCALER_PATH)
        
        X_test_scaled = scaler.transform(split_data.X_test)
        
        # Load model
        model = load_model(BEST_MODEL_PATH, compile=False)
        
        # PCA if needed
        if metadata.get("pca_used", False):
            if PCA_PATH.exists():
                pca = joblib.load(PCA_PATH)
                model_input = pca.transform(X_test_scaled)
            else:
                return None
        else:
            model_input = X_test_scaled
            
        # Predict
        probs = np.asarray(model.predict(model_input, verbose=0)).reshape(-1)
        
        return {
            "y_true": split_data.y_test.tolist(),
            "y_prob": probs.tolist(),
            "threshold": metadata.get("threshold", 0.5)
        }
    except Exception:
        return None


@st.cache_resource(show_spinner=False)
def load_pca_object():
    from src.config import PCA_PATH
    if PCA_PATH.exists():
        try:
            import joblib
            return joblib.load(PCA_PATH)
        except Exception:
            return None
    return None


def format_percent(value) -> str:
    if pd.isna(value):
        return "-"
    return f"{float(value) * 100:.2f}%"


def format_probability_text(probability: float) -> str:
    return f"{probability * 100:.2f}%"


# ──────────── Label Constants (used across all render functions) ────────────
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


SVG_ICONS = {
    "database": '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22c5.523 0 10-2.239 10-5V5c0-2.761-4.477-5-10-5S2 2.239 2 5v12c0 2.761 4.477 5 10 5z"/><path d="M2 12c0 2.761 4.477 5 10 5s10-2.239 10-5"/><path d="M2 5c0 2.761 4.477 5 10 5s10-2.239 10-5"/></svg>',
    "cpu": '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="4" width="16" height="16" rx="2" ry="2"/><rect x="9" y="9" width="6" height="6"/><path d="M9 1v3M15 1v3M9 20v3M15 20v3M20 9h3M20 15h3M1 9h3M1 15h3"/></svg>',
    "percent": '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="19" y1="5" x2="5" y2="19"/><circle cx="6.5" cy="6.5" r="2.5"/><circle cx="17.5" cy="17.5" r="2.5"/></svg>',
    "trophy": '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 9H4.5a2.5 2.5 0 0 1 0-5H6M18 9h1.5a2.5 2.5 0 0 0 0-5H18M4 22h16M10 14.66V17c0 .55-.45 1-1 1H4v2h16v-2h-5c-.55 0-1-.45-1-1v-2.34M12 2a4 4 0 0 0-4 4v5c0 1.5 1.5 3 4 3s4-1.5 4-3V6a4 4 0 0 0-4-4z"/></svg>',
    "shield": '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>',
    "clock": '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>',
    "history": '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><polyline points="3 3 3 8 8 8"/><line x1="12" y1="7" x2="12" y2="12"/><line x1="12" y1="12" x2="16" y2="14"/></svg>'
}

def get_icon_for_label(label: str) -> str:
    lbl = label.lower()
    if "total data" in lbl or "jumlah baris" in lbl or "jumlah kolom" in lbl:
        return SVG_ICONS["database"]
    elif "fitur" in lbl or "komponen" in lbl:
        return SVG_ICONS["cpu"]
    elif "rasio" in lbl or "f1-score" in lbl or "recall" in lbl or "accuracy" in lbl or "akurasi" in lbl or "persen" in lbl or "peluang" in lbl:
        return SVG_ICONS["percent"]
    elif "terbaik" in lbl or "model" in lbl:
        return SVG_ICONS["trophy"]
    elif "waktu" in lbl or "terbaru" in lbl or "timestamp" in lbl:
        return SVG_ICONS["clock"]
    elif "riwayat" in lbl or "total prediksi" in lbl:
        return SVG_ICONS["history"]
    else:
        return SVG_ICONS["shield"]

def metric_card(label: str, value: str, caption: str = "") -> None:
    icon_svg = get_icon_for_label(label)
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-accent"></div>
            <div class="metric-header">
                <span class="metric-label">{label}</span>
                <span class="metric-icon-wrapper">{icon_svg}</span>
            </div>
            <div class="metric-value">{value}</div>
            <div class="metric-caption">{caption}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def metric_row(items: list[tuple[str, str, str]], columns: int | None = None) -> None:
    cols = st.columns(columns or len(items))
    for col, (label, value, caption) in zip(cols, items):
        with col:
            metric_card(label, value, caption)


def section_title(title: str, description: str) -> None:
    st.subheader(title)
    st.caption(description)


def queue_navigation(page: str) -> None:
    st.session_state.pending_page = page


def sidebar_navigation() -> str:
    metadata = load_metadata()
    pages = [
        "Beranda",
        "Dataset",
        "Preprocessing",
        "Ekstraksi Fitur",
        "Evaluasi Model",
        "Prediksi Risiko",
        "Riwayat Prediksi",
    ]
    if "active_page" not in st.session_state:
        st.session_state.active_page = "Beranda"
    if "pending_page" in st.session_state:
        st.session_state.active_page = st.session_state.pending_page
        del st.session_state.pending_page
    if st.session_state.active_page not in pages:
        st.session_state.active_page = "Beranda"

    with st.sidebar:
        st.markdown(
            """
            <div style="display: flex; align-items: center; gap: 12px; padding: 14px 16px; background: rgba(255, 255, 255, 0.04); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 16px; margin-bottom: 24px; margin-top: 10px;">
                <svg width="34" height="34" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="flex-shrink: 0;">
                    <path d="M12 2L3 7v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V7l-9-5z" fill="url(#shieldGrad)" />
                    <path d="M9 11l2 2 4-4" stroke="#FFFFFF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    <defs>
                        <linearGradient id="shieldGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                            <stop offset="0%" stop-color="#2563EB" />
                            <stop offset="100%" stop-color="#E11D48" />
                        </linearGradient>
                    </defs>
                </svg>
                <div style="display: flex; flex-direction: column;">
                    <span style="font-family: 'Inter', sans-serif; font-size: 15px; font-weight: 800; color: #FFFFFF; line-height: 1.2; letter-spacing: 0.3px; display: block;">Credit Default Risk AI</span>
                    <span style="font-family: 'Inter', sans-serif; font-size: 9.5px; font-weight: 600; color: #94A3B8; margin-top: 3px; letter-spacing: 0.5px; text-transform: uppercase;">Machine Learning Project</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        page = st.radio(
            "Navigasi",
            pages,
            index=pages.index(st.session_state.active_page),
        )
        st.session_state.active_page = page
        st.divider()
        if metadata:
            st.markdown(
                f"""
                <div class="sidebar-best-card">
                    <div class="badge">Model Terbaik</div>
                    <div class="model">{metadata.get("best_model_name", "-")}</div>
                    <div class="split">Split {metadata.get("best_split_scenario", "-")}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.info("Model belum dilatih.")
    return page


def render_home(df: pd.DataFrame, metadata: dict, evaluation_df: pd.DataFrame) -> None:
    summary = get_dataset_summary(df)
    st.markdown(
        """
        <div class="hero-card">
            <div class="hero-glow"></div>
            <span class="hero-badge">Machine Learning Project 2026</span>
            <h1 class="hero-title">Credit Default Risk AI</h1>
            <p class="hero-subtitle">A deep learning dashboard for credit card default risk analysis using DNN and Hybrid PCA-DNN pipelines.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.write("")
    cta_col_1, cta_col_2, _ = st.columns([0.18, 0.18, 0.64])
    if cta_col_1.button("Mulai Prediksi", type="primary", use_container_width=True):
        queue_navigation("Prediksi Risiko")
        st.rerun()
    if cta_col_2.button("Lihat Evaluasi", use_container_width=True):
        queue_navigation("Evaluasi Model")
        st.rerun()
    st.write("")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        metric_card("Total Data", f"{summary['rows']:,}", "Setelah pembersihan data")
    with col2:
        metric_card("Jumlah Fitur", str(summary["feature_count"]), "Input model prediksi")
    with col3:
        ratio = summary["class_percentages"].get(1, 0)
        metric_card("Rasio Default", f"{ratio:.2f}%", "Kelas gagal bayar")
    with col4:
        best_model = metadata.get("best_model_name", "Belum dilatih")
        metric_card("Model Terbaik", best_model, metadata.get("best_split_scenario", "Jalankan training"))

    st.write("")
    col_a, col_b = st.columns([1.2, 0.8])
    with col_a:
        with st.container(border=True):
            section_title("Ringkasan Studi Kasus", "Klasifikasi risiko gagal bayar kartu kredit.")
            st.write(
                "Dataset berisi profil nasabah, limit kredit, riwayat pembayaran, jumlah tagihan, "
                "jumlah pembayaran, dan status gagal bayar bulan berikutnya. Sistem membandingkan "
                "DNN/MLP dengan Hybrid PCA-DNN untuk memilih model terbaik berbasis metrik evaluasi."
            )
    with col_b:
        with st.container(border=True):
            section_title("Status Artefak", "Kesiapan model dan output eksperimen.")
            st.write(f"Processed dataset: {'tersedia' if PROCESSED_DATA_PATH.exists() else 'belum tersedia'}")
            st.write(f"Evaluation table: {'tersedia' if not evaluation_df.empty else 'belum tersedia'}")
            st.write(f"Model metadata: {'tersedia' if metadata else 'belum tersedia'}")

    st.write("")
    st.markdown(
        """
        <div class="pipeline-container">
            <div class="pipeline-title">Credit Default Risk AI Pipeline</div>
            <div class="pipeline-steps">
                <div class="pipeline-step">
                    <div class="step-num">01</div>
                    <div class="step-label">Data Raw</div>
                    <div class="step-desc">Tabular credit card clients</div>
                </div>
                <div class="pipeline-arrow">&rarr;</div>
                <div class="pipeline-step">
                    <div class="step-num">02</div>
                    <div class="step-label">Preprocessing</div>
                    <div class="step-desc">Cleaning, scaling, & splitting</div>
                </div>
                <div class="pipeline-arrow">&rarr;</div>
                <div class="pipeline-step">
                    <div class="step-num">03</div>
                    <div class="step-label">SMOTE</div>
                    <div class="step-desc">Imbalance handling (train only)</div>
                </div>
                <div class="pipeline-arrow">&rarr;</div>
                <div class="pipeline-step">
                    <div class="step-num">04</div>
                    <div class="step-label">PCA</div>
                    <div class="step-desc">Feature extraction (Hybrid)</div>
                </div>
                <div class="pipeline-arrow">&rarr;</div>
                <div class="pipeline-step">
                    <div class="step-num">05</div>
                    <div class="step-label">DNN Training</div>
                    <div class="step-desc">Optimization with Adam</div>
                </div>
                <div class="pipeline-arrow">&rarr;</div>
                <div class="pipeline-step">
                    <div class="step-num">06</div>
                    <div class="step-label">Evaluasi</div>
                    <div class="step-desc">Automatic best model selection</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_dataset(df: pd.DataFrame) -> None:
    summary = get_dataset_summary(df)
    section_title("Dataset", "Dataset ini berisi informasi profil nasabah, limit kredit, riwayat pembayaran, tagihan, pembayaran, dan status gagal bayar.")

    metric_row(
        [
            ("Jumlah Baris", f"{summary['rows']:,}", "Data setelah preprocessing"),
            ("Jumlah Kolom", f"{summary['columns']:,}", "Termasuk target"),
            ("Jumlah Fitur", str(summary["feature_count"]), "Input model"),
            ("Missing Value", str(summary["missing_values"]), "Nilai kosong"),
        ]
    )
    st.write("")

    st.subheader("Visualisasi & Analisis Eksplorasi Data (EDA)")
    
    # Tab layout for different visualizations to keep it clean and premium
    tab_dist, tab_demo, tab_corr, tab_stats = st.tabs([
        "📊 Distribusi Kelas & Limit", 
        "👤 Analisis Demografi", 
        "🔥 Analisis Korelasi",
        "📋 Statistik Deskriptif"
    ])
    
    with tab_dist:
        col_c1, col_c2 = st.columns(2)
        
        with col_c1:
            counts = pd.DataFrame(
                {
                    "Status": ["Lancar", "Gagal Bayar"],
                    "Jumlah": [
                        summary["class_counts"].get(0, 0),
                        summary["class_counts"].get(1, 0),
                    ],
                }
            )
            fig_class = px.bar(
                counts,
                x="Status",
                y="Jumlah",
                color="Status",
                color_discrete_map=DEFAULT_COLOR_MAP,
                title="Distribusi Kelas Status Kredit (Lancar vs Gagal Bayar)",
            )
            fig_class.update_layout(
                **PLOTLY_LAYOUT,
                margin=dict(l=10, r=10, t=40, b=10),
                height=350,
            )
            with st.container(border=True):
                st.plotly_chart(fig_class, use_container_width=True)
                add_chart_downloads(fig_class, counts, "distribusi_kelas")
                
        with col_c2:
            df_plot = df.copy()
            df_plot["Status Kredit"] = df_plot["default_status"].map({0: "Lancar", 1: "Gagal Bayar"})
            fig_limit = px.box(
                df_plot,
                x="Status Kredit",
                y="LIMIT_BAL",
                color="Status Kredit",
                color_discrete_map=DEFAULT_COLOR_MAP,
                title="Distribusi Limit Kredit (LIMIT_BAL) vs Status Kredit",
                labels={"LIMIT_BAL": "Limit Kredit (NTD)"}
            )
            fig_limit.update_layout(
                **PLOTLY_LAYOUT,
                margin=dict(l=10, r=10, t=40, b=10),
                height=350,
            )
            with st.container(border=True):
                st.plotly_chart(fig_limit, use_container_width=True)
                # prepare limit statistics for download
                limit_stats = df_plot.groupby("Status Kredit")["LIMIT_BAL"].describe().reset_index()
                add_chart_downloads(fig_limit, limit_stats, "limit_kredit_stats")

    with tab_demo:
        col_d1, col_d2 = st.columns(2)
        
        with col_d1:
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
            fig_age.update_layout(
                **PLOTLY_LAYOUT,
                margin=dict(l=10, r=10, t=40, b=10),
                height=350,
            )
            with st.container(border=True):
                st.plotly_chart(fig_age, use_container_width=True)
                age_counts = df_plot.groupby(["AGE", "Status Kredit"]).size().reset_index(name="Jumlah")
                add_chart_downloads(fig_age, age_counts, "distribusi_umur")
                
        with col_d2:
            # Map education codes to text labels
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
            fig_edu.update_layout(
                **PLOTLY_LAYOUT,
                margin=dict(l=10, r=10, t=40, b=10),
                height=350,
            )
            with st.container(border=True):
                st.plotly_chart(fig_edu, use_container_width=True)
                add_chart_downloads(fig_edu, edu_counts, "pendidikan_vs_default")

        # --- Gender chart ---
        col_d3, col_d4 = st.columns(2)

        with col_d3:
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
            fig_sex.update_layout(**PLOTLY_LAYOUT, height=350, margin=dict(l=10, r=10, t=40, b=10))
            with st.container(border=True):
                st.plotly_chart(fig_sex, use_container_width=True)
                add_chart_downloads(fig_sex, sex_counts, "jenis_kelamin_vs_default")

        # --- Marriage chart ---
        with col_d4:
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
            fig_marriage.update_layout(**PLOTLY_LAYOUT, height=350, margin=dict(l=10, r=10, t=40, b=10))
            with st.container(border=True):
                st.plotly_chart(fig_marriage, use_container_width=True)
                add_chart_downloads(fig_marriage, marriage_counts, "pernikahan_vs_default")

    with tab_corr:
        # Correlation heatmap of numeric features
        corr_features = ["LIMIT_BAL", "AGE", "PAY_0", "BILL_AMT1", "PAY_AMT1", "default_status"]
        corr_matrix = df[corr_features].corr()
        fig_corr = px.imshow(
            corr_matrix,
            text_auto=".2f",
            color_continuous_scale="RdBu_r",
            title="Matriks Korelasi Antara Fitur Utama & Target",
            labels=dict(color="Korelasi"),
            x=["Limit Kredit", "Umur", "Status Bayar Terakhir", "Tagihan Terakhir", "Bayar Terakhir", "Status Default"],
            y=["Limit Kredit", "Umur", "Status Bayar Terakhir", "Tagihan Terakhir", "Bayar Terakhir", "Status Default"]
        )
        fig_corr.update_layout(
            **PLOTLY_LAYOUT,
            margin=dict(l=10, r=10, t=40, b=10),
            height=400,
        )
        with st.container(border=True):
            st.plotly_chart(fig_corr, use_container_width=True)
            # convert correlation matrix to clean df for download
            corr_df = corr_matrix.reset_index().rename(columns={"index": "Fitur"})
            add_chart_downloads(fig_corr, corr_df, "matriks_korelasi")

    with tab_stats:
        # Descriptive statistics table
        with st.container(border=True):
            st.markdown("<h4 style='margin: 0 0 14px 0; font-weight: 750;'>Statistik Deskriptif</h4>", unsafe_allow_html=True)
            desc_df = df.describe().T
            st.dataframe(desc_df.style.format("{:.2f}"), use_container_width=True)

        st.write("")

        # Box plot of AGE by default status
        df_plot_stats = df.copy()
        df_plot_stats["Status Kredit"] = df_plot_stats["default_status"].map({0: "Lancar", 1: "Gagal Bayar"})
        fig_age_box = px.box(
            df_plot_stats,
            x="Status Kredit",
            y="AGE",
            color="Status Kredit",
            color_discrete_map=DEFAULT_COLOR_MAP,
            title="Distribusi Umur Berdasarkan Status Kredit",
            labels={"AGE": "Umur (Tahun)"},
        )
        fig_age_box.update_layout(**PLOTLY_LAYOUT, height=350, margin=dict(l=10, r=10, t=40, b=10))
        with st.container(border=True):
            st.plotly_chart(fig_age_box, use_container_width=True)
            age_box_data = df_plot_stats.groupby("Status Kredit")["AGE"].describe().reset_index()
            add_chart_downloads(fig_age_box, age_box_data, "umur_boxplot")

    st.write("")
    
    with st.container(border=True):
        st.markdown("<h4 style='margin: 0 0 14px 0; font-weight: 750;'>Pratinjau Dataset</h4>", unsafe_allow_html=True)
        st.dataframe(df.head(10), use_container_width=True)

    st.write("")

    feature_description = pd.DataFrame(
        {
            "Kelompok": [
                "Profil Nasabah",
                "Profil Nasabah",
                "Profil Nasabah",
                "Profil Nasabah",
                "Profil Nasabah",
                "Riwayat Pembayaran",
                "Jumlah Tagihan",
                "Jumlah Pembayaran",
                "Target",
            ],
            "Kolom": [
                "LIMIT_BAL",
                "SEX",
                "EDUCATION",
                "MARRIAGE",
                "AGE",
                "PAY_0 sampai PAY_6",
                "BILL_AMT1 sampai BILL_AMT6",
                "PAY_AMT1 sampai PAY_AMT6",
                "default_status",
            ],
            "Keterangan": [
                "Limit kredit nasabah.",
                "Jenis kelamin dalam kode numerik dataset.",
                "Tingkat pendidikan dalam kode numerik dataset.",
                "Status pernikahan dalam kode numerik dataset.",
                "Umur nasabah.",
                "Status keterlambatan pembayaran historis.",
                "Jumlah tagihan pada beberapa periode.",
                "Jumlah pembayaran pada beberapa periode.",
                "0 = Lancar (Aman), 1 = Gagal Bayar (Macet).",
            ],
        }
    )
    with st.container(border=True):
        st.markdown("<h4 style='margin: 0 0 14px 0; font-weight: 750;'>Deskripsi Fitur</h4>", unsafe_allow_html=True)
        st.dataframe(feature_description, use_container_width=True, hide_index=True)


def render_preprocessing(df: pd.DataFrame) -> None:
    section_title("Preprocessing", "Tahap pembersihan dan persiapan data sebelum model dilatih.")
    st.markdown(
        '<div class="info-box">SMOTE hanya diterapkan pada data training agar tidak terjadi data leakage.</div>',
        unsafe_allow_html=True,
    )
    st.write("")

    steps = [
        ("Data Cleaning", "Mendeteksi baris header hasil konversi CSV, membuang kolom ID, menghapus missing value, dan menghapus duplikasi."),
        ("Feature & Target Separation", "Memisahkan 23 fitur input dari target default_status."),
        ("Scaling", "Menggunakan StandardScaler agar fitur numerik berada pada skala yang stabil untuk DNN."),
        ("Train-Test Split", "Menjalankan skenario 80/20, 75/25, dan 70/30 dengan stratified split."),
        ("SMOTE on Training Data", "Menyeimbangkan kelas hanya pada data training setelah split dan scaling."),
    ]
    columns = st.columns(3)
    for index, (title, body) in enumerate(steps):
        with columns[index % 3]:
            st.markdown(f'<div class="step-card"><h4>{title}</h4><p>{body}</p></div>', unsafe_allow_html=True)

    st.write("")
    with st.container(border=True):
        st.markdown("<h4 style='margin: 0 0 14px 0; font-weight: 750;'>Ringkasan Kualitas Data</h4>", unsafe_allow_html=True)
        st.dataframe(
            pd.DataFrame(
                {
                    "Pemeriksaan": ["Missing value", "Duplikasi setelah preprocessing", "Target", "Scaler"],
                    "Hasil": [int(df.isna().sum().sum()), int(df.duplicated().sum()), "default_status", "StandardScaler"],
                }
            ).astype(str),
            use_container_width=True,
            hide_index=True,
        )

    st.write("")
    st.subheader("Visualisasi Penyeimbangan Kelas & Pembagian Skenario Data")
    
    col_pre1, col_pre2 = st.columns(2)
    
    with col_pre1:
        # Before SMOTE: count class 0 and class 1 from df
        counts_before = df["default_status"].value_counts().sort_index()
        not_default_cnt = counts_before.get(0, 0)
        default_cnt = counts_before.get(1, 0)
        
        # After SMOTE (on training set, classes are balanced to the majority size)
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
            color_discrete_map={"Sebelum SMOTE": "#2563EB", "Sesudah SMOTE": "#E11D48"}
        )
        fig_smote.update_layout(**PLOTLY_LAYOUT, height=320, margin=dict(l=10, r=10, t=40, b=10))
        with st.container(border=True):
            st.plotly_chart(fig_smote, use_container_width=True)
            add_chart_downloads(fig_smote, smote_df, "distribusi_smote")

    with col_pre2:
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
            color_discrete_map={"Training": "#2563EB", "Testing": "#E11D48"}
        )
        fig_splits.update_layout(**PLOTLY_LAYOUT, height=320, margin=dict(l=10, r=10, t=40, b=10))
        with st.container(border=True):
            st.plotly_chart(fig_splits, use_container_width=True)
            add_chart_downloads(fig_splits, split_sizes, "ukuran_data_split")


def render_feature_extraction(metadata: dict) -> None:
    section_title("Ekstraksi Fitur", "PCA digunakan untuk mereduksi dimensi fitur tanpa menghilangkan informasi utama dari dataset.")
    metric_row(
        [
            ("Fitur Sebelum PCA", str(len(FEATURE_COLUMNS)), "Fitur asli dataset"),
            ("Komponen PCA", str(metadata.get("pca_components", "-")), "Model terbaik"),
            ("PCA Digunakan", "Ya" if metadata.get("pca_used") else "Tidak", "Hybrid PCA-DNN"),
        ]
    )
    st.write("")

    pca = load_pca_object()
    if pca is not None and hasattr(pca, "explained_variance_ratio_"):
        import numpy as np
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
        fig_pca.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=10, r=10, t=40, b=10),
            height=350,
            font=dict(family="Inter, sans-serif")
        )
        with st.container(border=True):
            st.markdown("<h4 style='margin: 0 0 14px 0; font-weight: 750;'>Analisis Varians PCA</h4>", unsafe_allow_html=True)
            st.plotly_chart(fig_pca, use_container_width=True)
            add_chart_downloads(fig_pca, df_ev, "pca_explained_variance")

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
        fig_indiv.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=10, r=10, t=40, b=10),
            height=350,
            font=dict(family="Inter, sans-serif")
        )
        with st.container(border=True):
            st.markdown("<h4 style='margin: 0 0 14px 0; font-weight: 750;'>Kontribusi Varians Individual per Komponen PCA</h4>", unsafe_allow_html=True)
            st.plotly_chart(fig_indiv, use_container_width=True)
            add_chart_downloads(fig_indiv, df_indiv, "pca_individual_variance")

    st.write("")

    with st.container(border=True):
        st.markdown(
            """
            <div style="padding: 4px 0;">
                <h4 style="margin: 0 0 16px 0; color: #0F172A; font-weight: 800; font-size: 18px;">Pipeline Hybrid PCA-DNN</h4>
                <div style="background: #F8FAFC; border: 1px solid #E5E7EB; border-radius: 12px; padding: 18px; font-family: monospace; font-size: 14px; margin-bottom: 16px; color: #071B33; font-weight: bold;">
                    Preprocessed Features &rarr; PCA Feature Extraction &rarr; DNN Classifier &rarr; Prediction
                </div>
                <p style="color: #64748B; font-size: 13.5px; margin: 0; line-height: 1.5;">PCA bukan model deep learning utama. PCA adalah tahap ekstraksi fitur untuk pipeline Hybrid PCA-DNN.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )


def add_file_download_button(file_path: Path, label: str, filename: str):
    if file_path.exists():
        with open(file_path, "rb") as f:
            data_bytes = f.read()
        st.download_button(
            label=label,
            data=data_bytes,
            file_name=filename,
            mime="image/png",
            key=f"dl_file_{filename}",
            use_container_width=True
        )


def render_evaluation(evaluation_df: pd.DataFrame, metadata: dict) -> None:
    section_title("Evaluasi Model", "Perbandingan DNN/MLP dan Hybrid PCA-DNN pada tiga skenario split.")
    if evaluation_df.empty:
        st.warning("Hasil evaluasi belum tersedia. Jalankan `python src/train.py` terlebih dahulu.")
        return

    best_row = evaluation_df[evaluation_df["best_model"] == True]
    best_row = best_row.iloc[0] if not best_row.empty else evaluation_df.sort_values("f1_score", ascending=False).iloc[0]

    metric_row(
        [
            ("Model Terbaik", str(best_row["model_name"]), str(best_row["scenario"])),
            ("F1-Score Terbaik", format_percent(best_row["f1_score"]), "Prioritas utama"),
            ("Recall Default", format_percent(best_row["recall"]), "Kelas gagal bayar"),
            ("Accuracy Terbaik", format_percent(best_row["accuracy"]), "Akurasi test set"),
        ]
    )

    st.markdown(
        '<div class="info-box">Pada kasus kredit macet, F1-score dan recall kelas default lebih penting dibanding akurasi saja karena dataset dapat mengalami imbalance.</div>',
        unsafe_allow_html=True,
    )
    st.write("")

    display_df = evaluation_df[
        ["scenario", "model_name", "accuracy", "precision", "recall", "f1_score", "auc_score", "best_model"]
    ].copy()
    for column in ["accuracy", "precision", "recall", "f1_score", "auc_score"]:
        display_df[column] = display_df[column].map(format_percent)
    display_df["best_model"] = display_df["best_model"].map(lambda value: "Ya" if value else "-")
    display_df = display_df.rename(
        columns={
            "scenario": "Split",
            "model_name": "Model",
            "accuracy": "Accuracy",
            "precision": "Precision",
            "recall": "Recall",
            "f1_score": "F1-Score",
            "auc_score": "AUC",
            "best_model": "Terbaik",
        }
    )
    
    with st.container(border=True):
        st.markdown("<h4 style='margin: 0 0 14px 0; font-weight: 750;'>Tabel Ringkas Evaluasi</h4>", unsafe_allow_html=True)
        st.dataframe(display_df, use_container_width=True, hide_index=True)
        # Download button for scenario metrics
        csv_eval = evaluation_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Unduh Hasil Evaluasi Skenario (CSV)",
            data=csv_eval,
            file_name="hasil_evaluasi_skenario.csv",
            mime="text/csv",
            key="dl_eval_scenarios",
            use_container_width=True
        )

    chart_df = evaluation_df.melt(
        id_vars=["scenario", "model_name"],
        value_vars=["accuracy", "recall", "f1_score"],
        var_name="Metrik",
        value_name="Nilai",
    )
    chart_df["Metrik"] = chart_df["Metrik"].map(
        {"accuracy": "Akurasi", "recall": "Recall Default", "f1_score": "F1-Score"}
    )
    fig = px.bar(
        chart_df,
        x="scenario",
        y="Nilai",
        color="model_name",
        facet_col="Metrik",
        barmode="group",
        color_discrete_map={"DNN / MLP": "#2563EB", "Hybrid PCA-DNN": "#E11D48"},
        labels={"scenario": "Split Data", "model_name": "Model", "Nilai": "Nilai"},
        title="Grafik Ringkas Evaluasi",
    )
    fig.for_each_annotation(lambda annotation: annotation.update(text=annotation.text.split("=")[-1]))
    fig.update_yaxes(tickformat=".0%")
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        height=320,
        margin=dict(l=18, r=18, t=48, b=18),
        legend_title_text="",
        font=dict(family="Inter, sans-serif")
    )
    
    with st.container(border=True):
        st.markdown("<h4 style='margin: 0 0 14px 0; font-weight: 750;'>Visualisasi Perbandingan</h4>", unsafe_allow_html=True)
        st.plotly_chart(fig, use_container_width=True)
        add_chart_downloads(fig, chart_df, "perbandingan_skenario")

    # Precision & AUC Comparison Chart
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
    fig_pa.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        height=320,
        margin=dict(l=18, r=18, t=48, b=18),
        legend_title_text="",
        font=dict(family="Inter, sans-serif")
    )
    with st.container(border=True):
        st.markdown("<h4 style='margin: 0 0 14px 0; font-weight: 750;'>Perbandingan Precision dan AUC</h4>", unsafe_allow_html=True)
        st.plotly_chart(fig_pa, use_container_width=True)
        add_chart_downloads(fig_pa, chart_pa_df, "perbandingan_precision_auc")

    # Radar Chart for Best Model
    import plotly.graph_objects as go
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
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        height=400,
        font=dict(family="Inter, sans-serif")
    )
    radar_df = pd.DataFrame({"Metrik": radar_categories, "Nilai": radar_values})
    with st.container(border=True):
        st.markdown("<h4 style='margin: 0 0 14px 0; font-weight: 750;'>Radar Metrik Model Terbaik</h4>", unsafe_allow_html=True)
        st.plotly_chart(fig_radar, use_container_width=True)
        add_chart_downloads(fig_radar, radar_df, "radar_metrik_terbaik")

    # Dynamic ML Evaluation Visualizations
    pred_data = get_best_model_predictions()
    if pred_data is not None:
        import numpy as np
        st.subheader("Visualisasi Kinerja Model Terbaik (Interaktif)")
        
        tab_cm, tab_roc, tab_pr = st.tabs([
            "🎯 Confusion Matrix", 
            "📈 Kurva ROC", 
            "📏 Kurva Precision-Recall"
        ])
        
        with tab_cm:
            from sklearn.metrics import confusion_matrix
            y_true_arr = np.array(pred_data["y_true"])
            y_prob_arr = np.array(pred_data["y_prob"])
            threshold_val = pred_data["threshold"]
            y_pred_arr = (y_prob_arr >= threshold_val).astype(int)
            
            cm = confusion_matrix(y_true_arr, y_pred_arr)
            cm_df = pd.DataFrame(
                cm, 
                index=["Aktual Lancar", "Aktual Gagal Bayar"],
                columns=["Prediksi Lancar", "Prediksi Gagal Bayar"]
            )
            fig_cm = px.imshow(
                cm,
                text_auto=True,
                color_continuous_scale="Blues",
                title="Confusion Matrix Model Terbaik",
                x=["Prediksi Lancar", "Prediksi Gagal Bayar"],
                y=["Aktual Lancar", "Aktual Gagal Bayar"],
                labels=dict(color="Jumlah Nasabah")
            )
            fig_cm.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                height=350,
                font=dict(family="Inter, sans-serif")
            )
            with st.container(border=True):
                st.plotly_chart(fig_cm, use_container_width=True)
                cm_dl_df = cm_df.reset_index().rename(columns={"index": "Kategori"})
                add_chart_downloads(fig_cm, cm_dl_df, "confusion_matrix_terbaik")
                
        with tab_roc:
            from sklearn.metrics import roc_curve
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
            fig_roc.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                height=350,
                font=dict(family="Inter, sans-serif")
            )
            with st.container(border=True):
                st.plotly_chart(fig_roc, use_container_width=True)
                add_chart_downloads(fig_roc, df_roc, "roc_curve_terbaik")
                
        with tab_pr:
            from sklearn.metrics import precision_recall_curve
            precision, recall, pr_thresholds = precision_recall_curve(y_true_arr, y_prob_arr)
            # thresholds length is 1 less than precision/recall, pad it
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
            fig_pr.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                height=350,
                font=dict(family="Inter, sans-serif")
            )
            with st.container(border=True):
                st.plotly_chart(fig_pr, use_container_width=True)
                add_chart_downloads(fig_pr, df_pr, "pr_curve_terbaik")

    # Prediction Probability Distribution
    if pred_data is not None:
        prob_df = pd.DataFrame({
            "Probabilitas": np.array(pred_data["y_prob"]),
            "Kelas Aktual": ["Gagal Bayar" if y == 1 else "Lancar" for y in pred_data["y_true"]]
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
            x=0.5, line_dash="dash", line_color="#071B33",
            annotation_text="Threshold 0.5"
        )
        fig_prob.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            height=350,
            font=dict(family="Inter, sans-serif")
        )
        with st.container(border=True):
            st.markdown("<h4 style='margin: 0 0 14px 0; font-weight: 750;'>Distribusi Probabilitas Prediksi</h4>", unsafe_allow_html=True)
            st.plotly_chart(fig_prob, use_container_width=True)
            add_chart_downloads(fig_prob, prob_df, "distribusi_probabilitas_prediksi")

    with st.expander("Grafik pendukung training (Unduh Aset Laporan & Poster)", expanded=False):
        col_a, col_b = st.columns(2)
        
        with col_a:
            path_cm = FIGURES_DIR / "confusion_matrix_best_model.png"
            if path_cm.exists():
                st.image(str(path_cm), use_container_width=True, caption="Confusion Matrix Model Terbaik")
                add_file_download_button(path_cm, "📥 Unduh Confusion Matrix (PNG)", "confusion_matrix.png")
                
        with col_b:
            path_acc = FIGURES_DIR / "training_accuracy.png"
            if path_acc.exists():
                st.image(str(path_acc), use_container_width=True, caption="Training & Validation Accuracy")
                add_file_download_button(path_acc, "📥 Unduh Kurva Akurasi (PNG)", "training_accuracy.png")
                
        st.write("")
        col_c, col_d = st.columns(2)
        
        with col_c:
            path_loss = FIGURES_DIR / "training_loss.png"
            if path_loss.exists():
                st.image(str(path_loss), use_container_width=True, caption="Training & Validation Loss")
                add_file_download_button(path_loss, "📥 Unduh Kurva Loss (PNG)", "training_loss.png")
                
        with col_d:
            path_comp = FIGURES_DIR / "model_comparison.png"
            if path_comp.exists():
                st.image(str(path_comp), use_container_width=True, caption="Perbandingan Model Eksperimen")
                add_file_download_button(path_comp, "📥 Unduh Perbandingan Model (PNG)", "model_comparison.png")


def number_input(label: str, value: float, step: float = 1.0, help_text: str | None = None):
    return st.number_input(label, value=value, step=step, help=help_text)


PAYMENT_PERIOD_LABELS = {
    "PAY_0": "Status pembayaran bulan terakhir",
    "PAY_2": "Status pembayaran 2 bulan lalu",
    "PAY_3": "Status pembayaran 3 bulan lalu",
    "PAY_4": "Status pembayaran 4 bulan lalu",
    "PAY_5": "Status pembayaran 5 bulan lalu",
    "PAY_6": "Status pembayaran 6 bulan lalu",
}

BILL_PERIOD_LABELS = {
    "BILL_AMT1": "Tagihan bulan terakhir",
    "BILL_AMT2": "Tagihan 2 bulan lalu",
    "BILL_AMT3": "Tagihan 3 bulan lalu",
    "BILL_AMT4": "Tagihan 4 bulan lalu",
    "BILL_AMT5": "Tagihan 5 bulan lalu",
    "BILL_AMT6": "Tagihan 6 bulan lalu",
}

PAYMENT_AMOUNT_LABELS = {
    "PAY_AMT1": "Pembayaran bulan terakhir",
    "PAY_AMT2": "Pembayaran 2 bulan lalu",
    "PAY_AMT3": "Pembayaran 3 bulan lalu",
    "PAY_AMT4": "Pembayaran 4 bulan lalu",
    "PAY_AMT5": "Pembayaran 5 bulan lalu",
    "PAY_AMT6": "Pembayaran 6 bulan lalu",
}


def payment_status_text(value: int) -> str:
    if value <= -2:
        return "Tidak ada tagihan / tidak aktif"
    if value == -1:
        return "Lunas lebih awal"
    if value == 0:
        return "Tepat waktu"
    return f"Terlambat {value} bulan"


SEX_LABELS = {
    1: "Laki-laki",
    2: "Perempuan",
}

EDUCATION_LABELS = {
    1: "Pascasarjana",
    2: "Sarjana",
    3: "SMA / sederajat",
    4: "Lainnya / tidak diketahui",
    5: "Lainnya / tidak diketahui",
    6: "Lainnya / tidak diketahui",
    0: "Lainnya / tidak diketahui",
}

MARRIAGE_LABELS = {
    1: "Menikah",
    2: "Belum menikah",
    3: "Lainnya / tidak diketahui",
    0: "Lainnya / tidak diketahui",
}

EDUCATION_OPTIONS = [2, 3, 1, 4]
MARRIAGE_OPTIONS = [2, 1, 3]


def prediction_sentence(result: dict) -> str:
    if result["prediction_result"] == "Default":
        return "Nasabah diprediksi berisiko gagal bayar pada periode berikutnya."
    return "Nasabah diprediksi tidak gagal bayar pada periode berikutnya."


def risk_explanation(result: dict) -> str:
    probability = format_probability_text(result["default_probability"])
    if result["risk_level"] == "Risiko Rendah":
        return f"Peluang gagal bayar berada di {probability}, sehingga risikonya relatif rendah."
    if result["risk_level"] == "Risiko Sedang":
        return f"Peluang gagal bayar berada di {probability}, jadi data nasabah perlu dicek lebih teliti."
    return f"Peluang gagal bayar berada di {probability}, sehingga pengajuan sebaiknya tidak langsung disetujui."


def build_quick_demo_input(data: dict) -> dict:
    input_data = {column: 0 for column in FEATURE_COLUMNS}
    input_data.update(
        {
            "LIMIT_BAL": data["LIMIT_BAL"],
            "SEX": data["SEX"],
            "EDUCATION": data["EDUCATION"],
            "MARRIAGE": data["MARRIAGE"],
            "AGE": data["AGE"],
        }
    )
    for column in ["PAY_0", "PAY_2", "PAY_3", "PAY_4", "PAY_5", "PAY_6"]:
        input_data[column] = data["PAY_STATUS"]
    for column in ["BILL_AMT1", "BILL_AMT2", "BILL_AMT3", "BILL_AMT4", "BILL_AMT5", "BILL_AMT6"]:
        input_data[column] = data["BILL_AMOUNT"]
    for column in ["PAY_AMT1", "PAY_AMT2", "PAY_AMT3", "PAY_AMT4", "PAY_AMT5", "PAY_AMT6"]:
        input_data[column] = data["PAY_AMOUNT"]
    return input_data


def render_quick_demo_form() -> tuple[dict, bool]:
    st.markdown(
        """
        <div class="mode-panel">
            <h4>Mode Demo Cepat</h4>
            <p>Untuk presentasi atau simulasi cepat. Cukup isi data utama; riwayat bulan lain otomatis disamakan agar model tetap menerima 23 fitur lengkap.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.form("quick_prediction_form"):
        st.subheader("Data Utama")
        col1, col2, col3 = st.columns(3)
        quick_data = {
            "LIMIT_BAL": col1.number_input("Limit kredit", min_value=0.0, value=120000.0, step=10000.0),
            "AGE": col2.number_input("Umur", min_value=18, max_value=100, value=35, step=1),
            "SEX": col3.selectbox("Jenis kelamin", [1, 2], format_func=lambda x: SEX_LABELS[x]),
        }
        col4, col5 = st.columns(2)
        quick_data["EDUCATION"] = col4.selectbox(
            "Pendidikan",
            EDUCATION_OPTIONS,
            format_func=lambda x: EDUCATION_LABELS[x],
        )
        quick_data["MARRIAGE"] = col5.selectbox(
            "Status pernikahan",
            MARRIAGE_OPTIONS,
            format_func=lambda x: MARRIAGE_LABELS[x],
        )

        st.subheader("Kondisi Keuangan Singkat")
        col6, col7, col8 = st.columns(3)
        quick_data["PAY_STATUS"] = col6.selectbox(
            "Kondisi pembayaran",
            [-2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8],
            index=2,
            format_func=payment_status_text,
            help="Untuk demo cepat, status ini dipakai sebagai gambaran riwayat pembayaran 6 bulan.",
        )
        quick_data["BILL_AMOUNT"] = col7.number_input(
            "Perkiraan tagihan bulanan",
            min_value=0.0,
            value=0.0,
            step=1000.0,
            help="Nilai ini otomatis dipakai untuk tagihan historis.",
        )
        quick_data["PAY_AMOUNT"] = col8.number_input(
            "Perkiraan pembayaran bulanan",
            min_value=0.0,
            value=0.0,
            step=1000.0,
            help="Nilai ini otomatis dipakai untuk pembayaran historis.",
        )
        st.markdown(
            '<div class="quick-note">Mode ini tetap mengirim 23 fitur ke model. Bedanya, fitur historis diisi otomatis agar demo lebih cepat dan tidak membingungkan.</div>',
            unsafe_allow_html=True,
        )
        submitted = st.form_submit_button("Hitung Risiko Sekarang")

    return build_quick_demo_input(quick_data), submitted


def render_complete_form() -> tuple[dict, bool]:
    st.markdown(
        """
        <div class="mode-panel">
            <h4>Mode Lengkap</h4>
            <p>Untuk simulasi detail. Semua fitur dataset tetap bisa diisi, tetapi dikelompokkan agar lebih mudah dibaca.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.form("complete_prediction_form"):
        st.subheader("Data Utama Nasabah")
        col1, col2, col3 = st.columns(3)
        input_data = {
            "LIMIT_BAL": col1.number_input("Limit kredit nasabah", min_value=0.0, value=120000.0, step=10000.0),
            "AGE": col2.number_input("Umur", min_value=18, max_value=100, value=35, step=1),
            "SEX": col3.selectbox("Jenis Kelamin", [1, 2], format_func=lambda x: SEX_LABELS[x]),
        }
        col4, col5 = st.columns(2)
        input_data["EDUCATION"] = col4.selectbox(
            "Pendidikan",
            EDUCATION_OPTIONS,
            format_func=lambda x: EDUCATION_LABELS[x],
        )
        input_data["MARRIAGE"] = col5.selectbox(
            "Status Pernikahan",
            MARRIAGE_OPTIONS,
            format_func=lambda x: MARRIAGE_LABELS[x],
        )

        with st.expander("Riwayat pembayaran 6 bulan", expanded=False):
            st.caption("Isi status pembayaran tiap bulan. Default-nya tepat waktu.")
            pay_cols = st.columns(3)
            for index, column in enumerate(["PAY_0", "PAY_2", "PAY_3", "PAY_4", "PAY_5", "PAY_6"]):
                input_data[column] = pay_cols[index % 3].selectbox(
                    PAYMENT_PERIOD_LABELS[column],
                    [-2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8],
                    index=2,
                    format_func=payment_status_text,
                )

        with st.expander("Detail tagihan dan pembayaran", expanded=False):
            st.caption("Nominal boleh dibiarkan 0 untuk demo cepat. Isi jika ingin simulasi yang lebih mendekati data nasabah.")
            st.markdown("##### Jumlah Tagihan")
            bill_cols = st.columns(3)
            for index, column in enumerate(["BILL_AMT1", "BILL_AMT2", "BILL_AMT3", "BILL_AMT4", "BILL_AMT5", "BILL_AMT6"]):
                input_data[column] = bill_cols[index % 3].number_input(
                    BILL_PERIOD_LABELS[column],
                    value=0.0,
                    step=1000.0,
                )

            st.markdown("##### Jumlah Pembayaran")
            amount_cols = st.columns(3)
            for index, column in enumerate(["PAY_AMT1", "PAY_AMT2", "PAY_AMT3", "PAY_AMT4", "PAY_AMT5", "PAY_AMT6"]):
                input_data[column] = amount_cols[index % 3].number_input(
                    PAYMENT_AMOUNT_LABELS[column],
                    value=0.0,
                    step=1000.0,
                )

        submitted = st.form_submit_button("Hitung Risiko Gagal Bayar")

    return input_data, submitted


def render_prediction_result(input_data: dict) -> None:
    try:
        with st.spinner("Model sedang menghitung risiko gagal bayar..."):
            result = predict_default(input_data)
            insert_prediction({**input_data, **result, "waktu_prediksi": result["timestamp"]})

        risk_class = {
            "Risiko Rendah": "risk-card-low",
            "Risiko Sedang": "risk-card-medium",
            "Risiko Tinggi": "risk-card-high",
        }[result["risk_level"]]
        
        st.success("Hasil prediksi tersimpan ke database.")
        
        st.markdown(
            f"""
            <div class="{risk_class}">
                <h2>{result["risk_level"]}</h2>
                <p style="font-size: 16px; font-weight: 700; margin-bottom: 8px;">{prediction_sentence(result)}</p>
                <p style="font-size: 14px; opacity: 0.9;">{risk_explanation(result)}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
        with st.container(border=True):
            st.markdown("<h4 style='margin: 0 0 14px 0; font-weight: 750;'>Analisis Probabilitas & Model</h4>", unsafe_allow_html=True)
            st.progress(min(max(result["default_probability"], 0.0), 1.0))
            st.write("")
            metric_row(
                [
                    ("Model", result["model_used"], "Model terbaik"),
                    ("Peluang Gagal Bayar", format_probability_text(result["default_probability"]), "Semakin besar, semakin berisiko"),
                    ("Waktu", result["timestamp"], "Riwayat tersimpan"),
                ],
                columns=3,
            )
            
        with st.container(border=True):
            st.markdown("<h4 style='margin: 0 0 14px 0; font-weight: 750;'>Gauge Probabilitas Gagal Bayar</h4>", unsafe_allow_html=True)
            probability = result["default_probability"]
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=probability * 100,
                title={"text": "Probabilitas Gagal Bayar"},
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
            fig_gauge.update_layout(**PLOTLY_LAYOUT, height=280)
            st.plotly_chart(fig_gauge, use_container_width=True)

        st.markdown(
            f"""
            <div class="prediction-summary">
                <h3>Rekomendasi Keputusan</h3>
                <p>{result["recommendation"]}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    except Exception as exc:
        st.error(f"Prediksi belum dapat diproses: {exc}")


def render_prediction_form() -> None:
    section_title("Prediksi Risiko", "Pilih mode sesuai kebutuhan demo, lalu sistem menghitung peluang gagal bayar.")
    if not METADATA_PATH.exists():
        st.warning("Model belum tersedia. Jalankan `python src/train.py` sebelum melakukan prediksi.")

    mode = st.radio(
        "Mode prediksi",
        ["Mode Demo Cepat", "Mode Lengkap"],
        horizontal=True,
        help="Mode Demo Cepat cocok untuk presentasi. Mode Lengkap cocok untuk simulasi data nasabah yang lebih detail.",
    )
    st.write("")

    if mode == "Mode Demo Cepat":
        input_data, submitted = render_quick_demo_form()
    else:
        input_data, submitted = render_complete_form()

    if submitted:
        render_prediction_result(input_data)


def render_history() -> None:
    section_title("Riwayat Prediksi", "Database riwayat prediksi dari GUI.")
    history = fetch_prediction_history()

    metric_row(
        [
            ("Total Prediksi", str(len(history)), "Semua riwayat"),
            ("Gagal Bayar", str(int((history["prediction_result"] == "Default").sum()) if not history.empty else 0), "Risiko terdeteksi"),
            ("Lancar", str(int((history["prediction_result"] == "Tidak Default").sum()) if not history.empty else 0), "Risiko rendah"),
            ("Prediksi Terbaru", history["waktu_prediksi"].iloc[0] if not history.empty else "-", "Timestamp"),
        ]
    )

    if not history.empty:
        display_history = history[
            [
                "waktu_prediksi",
                "limit_balance",
                "age",
                "sex",
                "education",
                "marriage",
                "pay_0",
                "prediction_result",
                "default_probability",
                "risk_level",
                "model_used",
            ]
        ].copy()
        display_history["sex"] = display_history["sex"].map(SEX_LABELS)
        display_history["education"] = display_history["education"].map(EDUCATION_LABELS)
        display_history["marriage"] = display_history["marriage"].map(MARRIAGE_LABELS)
        display_history["pay_0"] = display_history["pay_0"].map(payment_status_text)
        display_history["default_probability"] = display_history["default_probability"].map(format_probability_text)
        display_history["prediction_result"] = display_history["prediction_result"].map({"Default": "Gagal Bayar", "Tidak Default": "Lancar"})
        display_history = display_history.rename(
            columns={
                "waktu_prediksi": "Waktu Prediksi",
                "limit_balance": "Limit Kredit",
                "age": "Umur",
                "sex": "Jenis Kelamin",
                "education": "Pendidikan",
                "marriage": "Status Pernikahan",
                "pay_0": "Pembayaran Terakhir",
                "prediction_result": "Hasil Prediksi",
                "default_probability": "Peluang Gagal Bayar",
                "risk_level": "Level Risiko",
                "model_used": "Model",
            }
        )
        
        with st.container(border=True):
            st.markdown("<h4 style='margin: 0 0 14px 0; font-weight: 750;'>Tabel Riwayat Prediksi</h4>", unsafe_allow_html=True)
            st.dataframe(display_history, use_container_width=True, height=280)

        if not history.empty:
            col1, col2 = st.columns(2)

            with col1:
                with st.container(border=True):
                    prediction_counts = history["prediction_result"].value_counts().reset_index()
                    prediction_counts.columns = ["Hasil Prediksi", "Jumlah"]
                    prediction_counts["Hasil Prediksi"] = prediction_counts["Hasil Prediksi"].map({"Default": "Gagal Bayar", "Tidak Default": "Lancar"})
                    fig_pie = px.pie(
                        prediction_counts,
                        values="Jumlah",
                        names="Hasil Prediksi",
                        title="Distribusi Hasil Prediksi",
                        hole=0.4,
                        color="Hasil Prediksi",
                        color_discrete_map={"Gagal Bayar": "#E11D48", "Lancar": "#2563EB"},
                    )
                    fig_pie.update_layout(**PLOTLY_LAYOUT, height=280)
                    st.plotly_chart(fig_pie, use_container_width=True)
                    add_chart_downloads(fig_pie, prediction_counts, "distribusi_hasil_prediksi")

            with col2:
                with st.container(border=True):
                    risk_counts = history["risk_level"].value_counts().reset_index()
                    risk_counts.columns = ["Level Risiko", "Jumlah"]
                    fig_bar = px.bar(
                        risk_counts,
                        x="Level Risiko",
                        y="Jumlah",
                        title="Distribusi Level Risiko",
                        color="Level Risiko",
                        color_discrete_map={
                            "Risiko Rendah": "#059669",
                            "Risiko Sedang": "#F59E0B",
                            "Risiko Tinggi": "#E11D48",
                        },
                    )
                    fig_bar.update_layout(**PLOTLY_LAYOUT, height=280)
                    st.plotly_chart(fig_bar, use_container_width=True)
                    add_chart_downloads(fig_bar, risk_counts, "distribusi_level_risiko")

        if st.button("Bersihkan Riwayat", type="secondary"):
            clear_prediction_history()
            st.success("Riwayat prediksi berhasil dibersihkan.")
            st.rerun()
    else:
        st.info("Belum ada prediksi yang tersimpan.")


def main() -> None:
    page = sidebar_navigation()
    df = load_dataset()
    metadata = load_metadata()
    evaluation_df = load_evaluation_results()

    if page == "Beranda":
        render_home(df, metadata, evaluation_df)
    elif page == "Dataset":
        render_dataset(df)
    elif page == "Preprocessing":
        render_preprocessing(df)
    elif page == "Ekstraksi Fitur":
        render_feature_extraction(metadata)
    elif page == "Evaluasi Model":
        render_evaluation(evaluation_df, metadata)
    elif page == "Prediksi Risiko":
        render_prediction_form()
    elif page == "Riwayat Prediksi":
        render_history()


if __name__ == "__main__":
    main()
