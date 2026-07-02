import streamlit as st
import pandas as pd
import numpy as np
import joblib
import json
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(
    page_title="CarPrice AI",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .main-header {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        padding: 2.5rem 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 8px 32px rgba(15, 52, 96, 0.4);
    }

    .main-header h1 {
        color: #ffffff;
        font-size: 2.6rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: -0.5px;
    }

    .main-header p {
        color: #a8c4e0;
        font-size: 1.05rem;
        margin: 0.6rem 0 0;
    }

    .badge {
        display: inline-block;
        background: rgba(255,255,255,0.15);
        color: #e0eeff;
        padding: 4px 14px;
        border-radius: 20px;
        font-size: 0.8rem;
        margin-top: 0.8rem;
        font-weight: 500;
        letter-spacing: 0.5px;
    }

    .metric-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8faff 100%);
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 1.4rem 1.2rem;
        text-align: center;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }

    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.1);
    }

    .metric-label {
        font-size: 0.75rem;
        font-weight: 600;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 0.4rem;
    }

    .metric-value {
        font-size: 1.5rem;
        font-weight: 700;
        color: #1e293b;
    }

    .metric-sub {
        font-size: 0.75rem;
        color: #94a3b8;
        margin-top: 0.2rem;
    }

    .prediction-box {
        background: linear-gradient(135deg, #0f3460 0%, #533483 100%);
        border-radius: 20px;
        padding: 2.5rem 2rem;
        text-align: center;
        box-shadow: 0 8px 32px rgba(15, 52, 96, 0.3);
        margin: 1.5rem 0;
    }

    .prediction-box .price-label {
        color: #a8c4e0;
        font-size: 0.9rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 0.5rem;
    }

    .prediction-box .price-value {
        color: #ffffff;
        font-size: 3rem;
        font-weight: 700;
        margin: 0.3rem 0;
    }

    .prediction-box .price-usd {
        color: #a8c4e0;
        font-size: 1.1rem;
        margin-top: 0.3rem;
    }

    .model-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(255,255,255,0.15);
        color: #ffffff;
        padding: 6px 16px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-top: 1rem;
    }

    .section-header {
        font-size: 1.2rem;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid #0f3460;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .sidebar-section {
        background: #f8faff;
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 1rem;
        border: 1px solid #e2e8f0;
    }

    .comparison-winner {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        padding: 8px 16px;
        border-radius: 10px;
        font-weight: 600;
        font-size: 0.85rem;
        display: inline-block;
    }

    .stButton > button {
        background: linear-gradient(135deg, #0f3460 0%, #533483 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-size: 1.05rem;
        font-weight: 600;
        width: 100%;
        transition: all 0.2s ease;
        box-shadow: 0 4px 15px rgba(15, 52, 96, 0.3);
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(15, 52, 96, 0.4);
    }

    .info-row {
        display: flex;
        justify-content: space-between;
        padding: 0.5rem 0;
        border-bottom: 1px solid #f1f5f9;
        font-size: 0.9rem;
    }

    .info-row:last-child { border-bottom: none; }
    .info-key { color: #64748b; font-weight: 500; }
    .info-val { color: #1e293b; font-weight: 600; }

    div[data-testid="stExpander"] {
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        overflow: hidden;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_resources():
    try:
        model     = joblib.load('best_model.pkl')
        xgb_m     = joblib.load('xgb_model.pkl')
        lgbm_m    = joblib.load('lgbm_model.pkl')
        le_dict   = joblib.load('label_encoders.pkl')
        with open('model_metadata.json') as f:
            meta  = json.load(f)
        return model, xgb_m, lgbm_m, le_dict, meta
    except FileNotFoundError as e:
        st.error(f" File model tidak ditemukan: {e}\n\nJalankan notebook terlebih dahulu untuk menghasilkan file model.")
        st.stop()

model, xgb_model, lgbm_model, le_dict, meta = load_resources()

best_name = meta['best_model']
metrics   = meta['metrics']
features  = meta['features']
le_classes = meta['label_encoders_classes']


st.markdown("""
<div class="main-header">
    <h1> CarPrice AI</h1>
    <p>Prediksi Harga Mobil Bekas menggunakan Machine Learning</p>
    <span class="badge">XGBoost &nbsp;•&nbsp; LightGBM &nbsp;•&nbsp; Kelompok 9</span>
</div>
""", unsafe_allow_html=True)


with st.sidebar:
    st.markdown("##  Input Data Mobil")
    st.markdown("---")

    st.markdown("** Informasi Umum**")
    year = st.slider("Tahun Produksi", min_value=1990, max_value=2020, value=2015, step=1)
    km_driven = st.number_input("Kilometer Dikendarai (km)", min_value=0, max_value=500000, value=50000, step=1000)

    st.markdown("---")
    st.markdown("** Spesifikasi**")
    fuel = st.selectbox("Jenis Bahan Bakar", le_classes['fuel'])
    transmission = st.selectbox("Transmisi", le_classes['transmission'])
    seller_type = st.selectbox("Tipe Penjual", le_classes['seller_type'])
    owner = st.selectbox("Status Kepemilikan", le_classes['owner'])

    st.markdown("---")
    st.markdown("** Performa Mesin**")
    mileage   = st.slider("Konsumsi BBM (kmpl)", 5.0, 45.0, 18.0, 0.1)
    engine    = st.slider("Kapasitas Mesin (CC)", 600, 4000, 1200, 10)
    max_power = st.slider("Tenaga Maksimum (bhp)", 30.0, 400.0, 80.0, 0.5)
    seats     = st.selectbox("Jumlah Kursi", [2, 4, 5, 6, 7, 8, 9, 10], index=2)

    st.markdown("---")
    predict_btn = st.button(" Prediksi Harga", use_container_width=True)


tab1, tab2, tab3 = st.tabs([" Prediksi", " Evaluasi Model", " Visualisasi"])


with tab1:
    col_left, col_right = st.columns([1, 1], gap="large")

    with col_left:
        st.markdown('<div class="section-header"> Ringkasan Input</div>', unsafe_allow_html=True)

        input_summary = {
            "Tahun Produksi":       year,
            "KM Dikendarai":        f"{km_driven:,} km",
            "Bahan Bakar":          fuel,
            "Transmisi":            transmission,
            "Tipe Penjual":         seller_type,
            "Kepemilikan":          owner,
            "Konsumsi BBM":         f"{mileage} kmpl",
            "Kapasitas Mesin":      f"{engine} CC",
            "Tenaga Maksimum":      f"{max_power} bhp",
            "Jumlah Kursi":         seats,
        }

        for k, v in input_summary.items():
            st.markdown(f"""
            <div class="info-row">
                <span class="info-key">{k}</span>
                <span class="info-val">{v}</span>
            </div>""", unsafe_allow_html=True)

    with col_right:
        st.markdown('<div class="section-header"> Hasil Prediksi</div>', unsafe_allow_html=True)

        if predict_btn:
            fuel_enc    = le_dict['fuel'].transform([fuel])[0]
            trans_enc   = le_dict['transmission'].transform([transmission])[0]
            seller_enc  = le_dict['seller_type'].transform([seller_type])[0]
            owner_enc   = le_dict['owner'].transform([owner])[0]

            input_data = pd.DataFrame([[
                year, km_driven, fuel_enc, seller_enc,
                trans_enc, owner_enc, mileage, engine, max_power, seats
            ]], columns=features)

            pred_price = model.predict(input_data)[0]
            pred_price = max(0, pred_price)

            pred_idr = pred_price * 188

            st.markdown(f"""
            <div class="prediction-box">
                <div class="price-label">Estimasi Harga Jual</div>
                <div class="price-value">₹ {pred_price:,.0f}</div>
                <div class="price-usd">≈ Rp {pred_idr:,.0f}</div>
                <div class="model-badge"> {best_name} (Model Terbaik)</div>
            </div>
            """, unsafe_allow_html=True)

            mape_val = metrics[best_name]['MAPE (%)'] / 100
            low  = pred_price * (1 - mape_val)
            high = pred_price * (1 + mape_val)

            st.info(f" **Rentang Estimasi:** ₹ {low:,.0f} — ₹ {high:,.0f}")

            if pred_price < 200000:
                seg, seg_color = " Ekonomi", "#10b981"
            elif pred_price < 600000:
                seg, seg_color = " Menengah", "#f59e0b"
            elif pred_price < 1500000:
                seg, seg_color = " Premium", "#f97316"
            else:
                seg, seg_color = " Mewah", "#ef4444"

            st.markdown(f"""
            <div style='background:{seg_color}20; border-left:4px solid {seg_color};
                        border-radius:8px; padding:0.8rem 1rem; margin-top:0.5rem;'>
                <b>Segmen Harga:</b> {seg}
            </div>
            """, unsafe_allow_html=True)

        else:
            st.markdown("""
            <div style='background:#f8faff; border: 2px dashed #cbd5e1;
                        border-radius: 16px; padding: 3rem 2rem; text-align: center; margin-top:1rem;'>
                <div style='font-size:3rem;'></div>
                <div style='font-size:1.1rem; color:#64748b; margin-top:0.8rem; font-weight:500;'>
                    Isi form di sidebar, lalu<br>klik <b>Prediksi Harga</b>
                </div>
            </div>
            """, unsafe_allow_html=True)


with tab2:
    st.markdown('<div class="section-header"> Perbandingan Evaluasi Model</div>', unsafe_allow_html=True)

    metric_keys = ['MAE', 'MSE', 'RMSE', 'MAPE (%)', 'R²']

    for m_key in metric_keys:
        xgb_val  = metrics['XGBoost'][m_key]
        lgbm_val = metrics['LightGBM'][m_key]

        if m_key == 'R²':
            xgb_better  = xgb_val >= lgbm_val
        else:
            xgb_better  = xgb_val <= lgbm_val

        col1, col2 = st.columns(2)
        with col1:
            winner_badge = '<span style="background:#10b981;color:white;padding:2px 8px;border-radius:8px;font-size:0.7rem;margin-left:6px;"> TERBAIK</span>' if xgb_better else ''
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">XGBoost — {m_key} {winner_badge}</div>
                <div class="metric-value">{xgb_val:,.4f}</div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            winner_badge = '<span style="background:#10b981;color:white;padding:2px 8px;border-radius:8px;font-size:0.7rem;margin-left:6px;"> TERBAIK</span>' if not xgb_better else ''
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">LightGBM — {m_key} {winner_badge}</div>
                <div class="metric-value">{lgbm_val:,.4f}</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("---")

    st.markdown('<div class="section-header"> Tabel Perbandingan Lengkap</div>', unsafe_allow_html=True)

    df_eval = pd.DataFrame([metrics['XGBoost'], metrics['LightGBM']]).set_index('Model')

    def highlight_best(col):
        is_r2 = col.name == 'R²'
        if is_r2:
            best = col.max()
        else:
            best = col.min()
        return ['background-color: #d1fae5; font-weight: bold; color: #065f46'
                if v == best else '' for v in col]

    styled_df = df_eval.style.apply(highlight_best)
    st.dataframe(styled_df, use_container_width=True)

    st.markdown(f"""
    <div style='background:#eff6ff; border:1px solid #bfdbfe; border-radius:12px;
                padding:1.2rem 1.5rem; margin-top:1rem;'>
        <b> Kesimpulan:</b> <b>{best_name}</b> adalah model terbaik berdasarkan nilai 
        R² = {metrics[best_name]['R²']:.6f}, RMSE = {metrics[best_name]['RMSE']:,.2f} INR, 
        dan MAPE = {metrics[best_name]['MAPE (%)']:.4f}%.
        Model ini mampu menjelaskan <b>{metrics[best_name]['R²']*100:.2f}%</b> variansi data.
    </div>
    """, unsafe_allow_html=True)


with tab3:
    st.markdown('<div class="section-header"> Visualisasi Perbandingan Model</div>', unsafe_allow_html=True)

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    fig.patch.set_facecolor('#f8faff')

    metric_plot = [('MAE', 'lower'), ('RMSE', 'lower'), ('R²', 'higher')]
    colors_list = ['#4C72B0', '#DD8452']

    for ax, (m, direction) in zip(axes, metric_plot):
        vals = [metrics['XGBoost'][m], metrics['LightGBM'][m]]
        bars = ax.bar(['XGBoost', 'LightGBM'], vals, color=colors_list, alpha=0.9,
                      edgecolor='white', linewidth=1.5, width=0.5)
        ax.set_title(m, fontsize=13, fontweight='bold', pad=12)
        ax.set_facecolor('#f8faff')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        for bar, val in zip(bars, vals):
            ax.text(bar.get_x() + bar.get_width()/2., bar.get_height() * 1.01,
                    f'{val:,.4f}', ha='center', fontsize=10, fontweight='bold')

        if direction == 'lower':
            best_idx = vals.index(min(vals))
        else:
            best_idx = vals.index(max(vals))
        bars[best_idx].set_edgecolor('#10b981')
        bars[best_idx].set_linewidth(3)

    plt.tight_layout(pad=2)
    st.pyplot(fig, use_container_width=True)

    st.markdown("---")

    st.markdown('<div class="section-header"> Feature Importance</div>', unsafe_allow_html=True)

    fig2, axes2 = plt.subplots(1, 2, figsize=(14, 5))
    fig2.patch.set_facecolor('#f8faff')

    models_fi = [('XGBoost', xgb_model, '#4C72B0'), ('LightGBM', lgbm_model, '#DD8452')]

    for ax, (name, mdl, color) in zip(axes2, models_fi):
        imp = pd.Series(mdl.feature_importances_, index=features).sort_values()
        bars = ax.barh(imp.index, imp.values, color=color, alpha=0.85, edgecolor='white')
        ax.set_title(f'{name} — Feature Importance', fontsize=12, fontweight='bold')
        ax.set_xlabel('Importance Score')
        ax.set_facecolor('#f8faff')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        for bar, val in zip(bars, imp.values):
            ax.text(val + imp.max() * 0.01, bar.get_y() + bar.get_height()/2,
                    f'{val:.0f}', va='center', fontsize=9)

    plt.tight_layout(pad=2)
    st.pyplot(fig2, use_container_width=True)

    st.markdown("---")
    st.markdown('<div class="section-header"> MAPE Comparison</div>', unsafe_allow_html=True)

    fig3, ax3 = plt.subplots(figsize=(7, 4))
    fig3.patch.set_facecolor('#f8faff')
    ax3.set_facecolor('#f8faff')

    mape_vals = [metrics['XGBoost']['MAPE (%)'], metrics['LightGBM']['MAPE (%)']]
    bars3 = ax3.bar(['XGBoost', 'LightGBM'], mape_vals, color=colors_list, alpha=0.9,
                    edgecolor='white', width=0.4)
    ax3.set_ylabel('MAPE (%)', fontsize=11)
    ax3.set_title('Mean Absolute Percentage Error (MAPE) — semakin rendah semakin baik',
                  fontsize=11, fontweight='bold')
    ax3.spines['top'].set_visible(False)
    ax3.spines['right'].set_visible(False)

    for bar, val in zip(bars3, mape_vals):
        ax3.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.1,
                 f'{val:.4f}%', ha='center', fontsize=11, fontweight='bold')

    best_idx3 = mape_vals.index(min(mape_vals))
    bars3[best_idx3].set_edgecolor('#10b981')
    bars3[best_idx3].set_linewidth(3)

    plt.tight_layout()
    col_c, col_d = st.columns([1, 1])
    with col_c:
        st.pyplot(fig3, use_container_width=True)
    with col_d:
        st.markdown(f"""
        <div style='padding:1.5rem; background:#eff6ff; border-radius:14px;
                    border:1px solid #bfdbfe; margin-top:2rem;'>
            <h4 style='color:#1e40af; margin-top:0;'> Interpretasi MAPE</h4>
            <p style='color:#374151;'>MAPE mengukur rata-rata persentase kesalahan prediksi.</p>
            <ul style='color:#374151;'>
                <li><b>XGBoost:</b> {metrics['XGBoost']['MAPE (%)']:.4f}% error</li>
                <li><b>LightGBM:</b> {metrics['LightGBM']['MAPE (%)']:.4f}% error</li>
            </ul>
            <div style='background:#d1fae5; border-radius:8px; padding:8px 12px; margin-top:8px;'>
                 <b>{best_name}</b> unggul dengan MAPE lebih rendah,
                artinya prediksinya lebih akurat secara persentase.
            </div>
        </div>
        """, unsafe_allow_html=True)


st.markdown("---")
st.markdown("""
<div style='text-align:center; color:#94a3b8; padding:1rem; font-size:0.85rem;'>
     <b>CarPrice AI</b> — Prediksi Harga Mobil Bekas &nbsp;|&nbsp;
    Kelompok 9 &nbsp;|&nbsp;
    XGBoost • LightGBM &nbsp;|&nbsp;
    Dataset: Car Details v3
</div>
""", unsafe_allow_html=True)
