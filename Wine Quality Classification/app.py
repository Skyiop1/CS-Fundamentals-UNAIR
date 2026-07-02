import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score, classification_report,
    confusion_matrix, ConfusionMatrixDisplay
)

# CONFIG & THEME
st.set_page_config(
    page_title="Wine Quality Prediction",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Premium Maroon UI
st.markdown("""
<style>
    /* Mengubah background utama menjadi maroon sangat gelap (Dark Maroon Theme) */
    .stApp {
        background-color: #1a0f12; 
    }
    
    /* Styling Header dan Teks secara umum agar terang di background gelap */
    h1, h2, h3, h4, h5, h6, p, span, div {
        color: #f8e8ea; /* Warna krem muda cerah */
        font-family: 'Inter', sans-serif;
    }
    
    /* Styling Navigasi Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        background-color: transparent;
    }
    .stTabs [data-baseweb="tab"] {
        height: 55px;
        white-space: pre-wrap;
        background-color: #2b1b1e; /* Warna abu-abu keunguan/maroon */
        border-radius: 10px 10px 0 0;
        gap: 1px;
        padding: 10px 25px;
        color: #b0a0a3 !important;
        border: 1px solid #4a252b;
        border-bottom: none;
        transition: background-color 0.3s;
    }
    .stTabs [aria-selected="true"] {
        background-color: #8B0000 !important; /* Maroon Solid yang tegas saat aktif */
        color: #ffffff !important;
        font-weight: bold;
        border: 1px solid #8B0000;
        border-bottom: none;
        box-shadow: 0 -3px 10px rgba(139, 0, 0, 0.4);
    }
    
    /* Metric Cards bergaya Premium Dark Mode */
    .metric-card {
        background-color: #2b1b1e;
        border-radius: 12px;
        padding: 25px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.5);
        text-align: center;
        border: 1px solid #4a252b;
        border-top: 5px solid #E32636; /* Aksen merah terang di atas kartu */
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 25px rgba(227, 38, 54, 0.2);
    }
    .metric-value {
        font-size: 2.8rem;
        font-weight: 900;
        color: #ffb3b3 !important; /* Pinkish Maroon cerah untuk angka */
        margin-top: 15px;
    }
    .metric-label {
        font-size: 1.1rem;
        color: #d1c1c3 !important;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1.5px;
    }
    
    /* Styling Garis Pemisah (Divider) */
    hr {
        border-color: #4a252b !important;
    }
    
    /* Memperbaiki warna blok Form Prediksi */
    div[data-testid="stForm"] {
        background-color: #221518;
        border: 1px solid #4a252b;
        border-radius: 15px;
        padding: 30px;
    }
    
    /* Styling Tombol Submit */
    button[kind="primaryFormSubmit"] {
        background-color: #8B0000 !important;
        color: white !important;
        border-radius: 8px;
        border: none;
        font-size: 1.2rem !important;
        padding: 10px 0;
        font-weight: bold;
        transition: 0.3s;
        box-shadow: 0 4px 10px rgba(139, 0, 0, 0.4);
    }
    button[kind="primaryFormSubmit"]:hover {
        background-color: #A52A2A !important;
        box-shadow: 0 6px 15px rgba(165, 42, 42, 0.6);
        transform: scale(1.02);
    }
</style>
""", unsafe_allow_html=True)

DATA_PATH = "WineQT.csv"


# LOAD & TRAIN (cached)
@st.cache_data
def load_and_train(path):
    df = pd.read_csv(path)
    
    if 'Id' in df.columns:
        df = df.drop(columns=['Id'])
        
    def map_quality(q):
        if q in [3, 4, 5]:
            return 0
        else:
            return 1
            
    df['quality_label'] = df['quality'].apply(map_quality)
        
    X = df.drop(columns=['quality', 'quality_label'])
    y = df['quality_label']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=0
    )

    model = DecisionTreeClassifier(random_state=0)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    return df, X, X_train, X_test, y_train, y_test, y_pred, model

df, X, X_train, X_test, y_train, y_test, y_pred, model = load_and_train(DATA_PATH)

# HEADER
col_logo, col_title = st.columns([1, 8])
with col_logo:
    st.markdown("<h1 style='text-align: center; font-size: 4rem;'>🍷</h1>", unsafe_allow_html=True)
with col_title:
    st.title("Wine Quality Classification")
    st.markdown(
        "Aplikasi cerdas berbasis **Decision Tree Classifier** untuk memprediksi "
        "kualitas wine berdasarkan komposisi bahan kimianya."
    )
st.divider()


# TABS
tab1, tab2, tab3 = st.tabs([
    "Eksplorasi Data",
    "Evaluasi Model",
    "Prediksi Kualitas Baru"
])


# TAB 1: EKSPLORASI DATA
with tab1:
    st.markdown("### Dataset Overview")
    
    # Premium Metrics
    c1, c2, c3, c4 = st.columns(4)
    c1.markdown(f'<div class="metric-card"><div class="metric-label">Total Data</div><div class="metric-value">{len(df):,}</div></div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="metric-card"><div class="metric-label">Total Fitur</div><div class="metric-value">{X.shape[1]}</div></div>', unsafe_allow_html=True)
    c3.markdown(f'<div class="metric-card"><div class="metric-label">Kategori "Bad" (3,4,5)</div><div class="metric-value">{(df["quality_label"]==0).sum()}</div></div>', unsafe_allow_html=True)
    c4.markdown(f'<div class="metric-card"><div class="metric-label">Kategori "Good" (6,7,8)</div><div class="metric-value">{(df["quality_label"]==1).sum()}</div></div>', unsafe_allow_html=True)
    
    st.write("")
    st.markdown("#### Sampel Data Awal")
    st.dataframe(df.head(10), width='stretch')

    st.markdown("#### Visualisasi Distribusi Kualitas (Interaktif)")
    col_a, col_b = st.columns([1, 1])

    with col_a:
        quality_counts = df['quality_label'].value_counts().reset_index()
        quality_counts.columns = ['Quality', 'Count']
        quality_counts['Kategori'] = quality_counts['Quality'].map({0: 'Bad (3,4,5)', 1: 'Good (6,7,8)'})
        
        # Plotly Bar Chart - Disesuaikan untuk dark mode
        fig1 = px.bar(quality_counts, x='Kategori', y='Count', color='Kategori',
                      color_discrete_map={'Bad (3,4,5)': '#E32636', 'Good (6,7,8)': '#4CAF50'},
                      title='Distribusi Kelas Quality')
        fig1.update_layout(
            showlegend=False, 
            paper_bgcolor='rgba(0,0,0,0)', 
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#f8e8ea')
        )
        st.plotly_chart(fig1, use_container_width=True)

    with col_b:
        st.markdown("#### Matriks Korelasi (Fitur vs Kualitas)")
        # Plotly Heatmap - Disesuaikan untuk dark mode maroon
        corr = df.drop(columns=['quality']).corr()
        fig2 = px.imshow(corr, text_auto=".2f", aspect="auto", color_continuous_scale='RdBu_r',
                         title='Correlation Heatmap')
        fig2.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', 
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#f8e8ea')
        )
        st.plotly_chart(fig2, use_container_width=True)


# TAB 2: EVALUASI MODEL
with tab2:
    st.markdown("### Evaluasi Model (Decision Tree)")

    accuracy = round(accuracy_score(y_test, y_pred) * 100, 2)
    
    c1, c2, c3 = st.columns(3)
    c1.markdown(f'<div class="metric-card"><div class="metric-label">Akurasi Model</div><div class="metric-value">{accuracy}%</div></div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="metric-card"><div class="metric-label">Data Training</div><div class="metric-value">{len(X_train):,} (80%)</div></div>', unsafe_allow_html=True)
    c3.markdown(f'<div class="metric-card"><div class="metric-label">Data Testing</div><div class="metric-value">{len(X_test):,} (20%)</div></div>', unsafe_allow_html=True)
    
    st.write("")
    col_cm, col_cr = st.columns([1, 1])

    with col_cm:
        st.markdown("#### Confusion Matrix")
        cm = confusion_matrix(y_test, y_pred)
        fig3, ax3 = plt.subplots(figsize=(6, 5))
        
        # Penyesuaian tema grafik agar serasi dengan background dark maroon
        fig3.patch.set_facecolor('#1a0f12')
        ax3.set_facecolor('#1a0f12')
        
        sns.heatmap(cm, annot=True, fmt='d', cmap='Reds', ax=ax3, 
                    xticklabels=['Bad (0)', 'Good (1)'], 
                    yticklabels=['Bad (0)', 'Good (1)'],
                    annot_kws={"color": "black", "size": 14})
        ax3.set_xlabel("Prediksi Kualitas", fontsize=12, color='#f8e8ea')
        ax3.set_ylabel("Kualitas Aktual", fontsize=12, color='#f8e8ea')
        ax3.tick_params(colors='#f8e8ea')
        st.pyplot(fig3)

    with col_cr:
        st.markdown("#### Classification Report")
        report = classification_report(y_test, y_pred, output_dict=True)
        report_df = pd.DataFrame(report).transpose().round(2)
        st.dataframe(
            report_df.style.background_gradient(cmap='Reds', subset=['f1-score']),
            width='stretch', height=350
        )
        
    st.markdown("#### Visualisasi Decision Tree (3 Level Teratas)")
    fig4, ax4 = plt.subplots(figsize=(25, 12))
    
    fig4.patch.set_facecolor('#1a0f12')
    
    plot_tree(
        model,
        feature_names=X.columns.tolist(),
        class_names=['Bad', 'Good'],
        filled=True,
        rounded=True,
        max_depth=3,
        fontsize=10,
        ax=ax4
    )
    ax4.set_title("Visualisasi Decision Tree", fontsize=16, color='#f8e8ea')
    st.pyplot(fig4)


# TAB 3: PREDIKSI KUALITAS BARU
with tab3:
    st.markdown("### Form Prediksi Kualitas Wine")
    st.markdown("Geser slider di bawah ini sesuai dengan hasil uji lab wine untuk melihat prediksi kualitasnya.")

    with st.form("form_prediksi"):
        st.markdown("#### Parameter Kimiawi")
        col1, col2, col3 = st.columns(3)

        with col1:
            fixed_acidity = st.slider("Fixed Acidity", float(X['fixed acidity'].min()), float(X['fixed acidity'].max()), float(X['fixed acidity'].mean()))
            volatile_acidity = st.slider("Volatile Acidity", float(X['volatile acidity'].min()), float(X['volatile acidity'].max()), float(X['volatile acidity'].mean()))
            citric_acid = st.slider("Citric Acid", float(X['citric acid'].min()), float(X['citric acid'].max()), float(X['citric acid'].mean()))
            residual_sugar = st.slider("Residual Sugar", float(X['residual sugar'].min()), float(X['residual sugar'].max()), float(X['residual sugar'].mean()))

        with col2:
            chlorides = st.slider("Chlorides", float(X['chlorides'].min()), float(X['chlorides'].max()), float(X['chlorides'].mean()), format="%.3f")
            free_sulfur_dioxide = st.slider("Free Sulfur Dioxide", float(X['free sulfur dioxide'].min()), float(X['free sulfur dioxide'].max()), float(X['free sulfur dioxide'].mean()))
            total_sulfur_dioxide = st.slider("Total Sulfur Dioxide", float(X['total sulfur dioxide'].min()), float(X['total sulfur dioxide'].max()), float(X['total sulfur dioxide'].mean()))
            density = st.slider("Density", float(X['density'].min()), float(X['density'].max()), float(X['density'].mean()), step=0.001, format="%.4f")

        with col3:
            pH = st.slider("pH", float(X['pH'].min()), float(X['pH'].max()), float(X['pH'].mean()))
            sulphates = st.slider("Sulphates", float(X['sulphates'].min()), float(X['sulphates'].max()), float(X['sulphates'].mean()))
            alcohol = st.slider("Alcohol", float(X['alcohol'].min()), float(X['alcohol'].max()), float(X['alcohol'].mean()))

        st.write("")
        submitted = st.form_submit_button("Prediksi Kualitas Wine", use_container_width=True)

    if submitted:
        features = [[
            fixed_acidity, volatile_acidity, citric_acid, residual_sugar, 
            chlorides, free_sulfur_dioxide, total_sulfur_dioxide, density, 
            pH, sulphates, alcohol
        ]]

        input_df = pd.DataFrame(features, columns=X.columns)
        
        result = model.predict(input_df)[0]

        st.divider()
        st.markdown("### Hasil Prediksi")

        col_res1, col_res2 = st.columns([1, 2])

        with col_res1:
            if result == 1:
                kategori_str = "GOOD"
                warna = "#00CC96" # Hijau untuk Good
                bg_warna = "rgba(0, 204, 150, 0.2)"
            else:
                kategori_str = "BAD"
                warna = "#E32636" # Merah Alizarin untuk Bad
                bg_warna = "rgba(227, 38, 54, 0.2)"
                
            st.markdown(
                f"""
                <div style="background-color: {bg_warna}; padding: 30px; border-radius: 15px; border: 2px solid {warna}; text-align: center; color: white; box-shadow: 0 4px 15px {bg_warna};">
                    <h3 style="color: #f8e8ea; margin-bottom: 5px;">Quality Prediction</h3>
                    <h1 style="color: {warna} !important; font-size: 5rem; font-weight: 900; margin: 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.5);">{kategori_str}</h1>
                </div>
                """, 
                unsafe_allow_html=True
            )

        with col_res2:
            st.markdown("#### Detail Input:")
            st.dataframe(input_df, width='stretch')
            
            if result == 1:
                st.success("**Wine Berkualitas Baik (Good)** - Ciri khas komposisi sudah seimbang.")
            else:
                st.error("**Wine Berkualitas Kurang (Bad)** - Terdapat komposisi kimia yang belum optimal.")
