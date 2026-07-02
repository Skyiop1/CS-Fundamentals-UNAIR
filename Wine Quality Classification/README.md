# Wine Quality Classification

An interactive web application built with Streamlit for wine quality prediction using a Decision Tree Classifier.

## 📋 Description

The application features:
- **Data Exploration** — dataset overview, class distribution plots, and interactive Plotly correlation heatmaps.
- **Model Evaluation** — performance metrics (accuracy, confusion matrix, classification reports) and decision tree splits visualization.
- **Real-Time Prediction** — interactive sliders to input chemical components and evaluate wine quality tags on the fly.

Wine quality is classified into:
- **Bad** (quality score of 3, 4, or 5).
- **Good** (quality score of 6, 7, or 8).

## 📁 Datasets

| Dataset | File | Description |
|---------|------|-----------|
| Wine Quality | `WineQT.csv` | Red wine chemical composition and labels (1,143 samples, 11 features). |

## 🚀 Getting Started

```bash
pip install streamlit pandas numpy matplotlib seaborn plotly scikit-learn
streamlit run app.py
```

## 📂 Directory Structure

```
Wine Quality Classification/
├── app.py                          # Streamlit main app script
├── WineQT.csv                      # Wine quality dataset
└── report-wine-quality.pdf         # Coursework report
```

## 🖥️ Screen Mockup

The app utilizes a premium dark maroon theme with:
- Hover-animated metric cards.
- Interactive Plotly visualizations.
- A custom-styled user inputs form.
