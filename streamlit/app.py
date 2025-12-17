import streamlit as st
import pandas as pd
import joblib
import os
import json
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from sklearn.tree import plot_tree

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="Prediksi Kesejahteraan Jawa Barat",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# PATH
# =========================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "../modelling/rf_model_kesejahteraan.pkl")
DATASET_PATH = os.path.join(BASE_DIR, "../preprocessing/dataset_preprocessed.csv")
METRICS_PATH = os.path.join(BASE_DIR, "../modelling/metrics.json")
IMG_DIR = os.path.join(BASE_DIR, "../modelling")

# =========================================================
# CUSTOM CSS
# =========================================================
st.markdown("""
<style>
.main-header {
    padding: 3rem;
    background: linear-gradient(135deg, #283048, #859398);
    border-radius: 18px;
    color: white;
    margin-bottom: 2rem;
}
.card {
    background: white;
    padding: 1.8rem;
    border-radius: 18px;
    box-shadow: 0 12px 30px rgba(0,0,0,0.08);
    margin-bottom: 1.5rem;
}
.card-title {
    font-size: 20px;
    font-weight: 600;
    margin-bottom: 1rem;
}
.result-box {
    padding: 30px;
    border-radius: 18px;
    font-size: 26px;
    font-weight: bold;
    text-align: center;
    color: white;
}
.success { background: linear-gradient(135deg,#11998e,#38ef7d); }
.warning { background: linear-gradient(135deg,#f7971e,#ffd200); color:#333; }
.danger { background: linear-gradient(135deg,#cb2d3e,#ef473a); }
</style>
""", unsafe_allow_html=True)

# =========================================================
# LOAD RESOURCE
# =========================================================
@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)

@st.cache_data
def load_dataset():
    return pd.read_csv(DATASET_PATH)

@st.cache_data
def load_metrics():
    with open(METRICS_PATH) as f:
        return json.load(f)

artifacts = load_model()
df = load_dataset()
metrics = load_metrics()

# =========================================================
# FUNGSI SKOR
# =========================================================
def hitung_skor_kesejahteraan(P, M, U, Y, S):
    return ((Y / 1e10) * 4) + (S * 10) - ((M / P) * 50) - ((U / P) * 50)

def tentukan_kategori(skor):
    if skor < 20:
        return "Sangat Tidak Sejahtera"
    elif skor < 40:
        return "Tidak Sejahtera"
    elif skor < 60:
        return "Cukup"
    elif skor < 120:
        return "Sejahtera"
    else:
        return "Sangat Sejahtera"

def get_css_class(kategori):
    if kategori in ["Sejahtera", "Sangat Sejahtera"]:
        return "success"
    elif kategori == "Cukup":
        return "warning"
    else:
        return "danger"

# =========================================================
# SIDEBAR
# =========================================================
with st.sidebar:
    st.markdown("## 📊 Welfare Dashboard")
    menu = st.radio(
        "Navigasi",
        ["🏠 Home", "🔮 Prediksi", "📊 Dataset", "📈 Evaluasi Model", "🌳 Pohon Keputusan", "ℹ️ About"]
    )
    st.divider()
    st.metric("Akurasi Model", f"{metrics['accuracy']*100:.2f}%")

# =========================================================
# HEADER
# =========================================================
st.markdown("""
<div class="main-header">
    <h1>📊 Prediksi Kesejahteraan Masyarakat Jawa Barat</h1>
    <p>Perhitungan Skor Manual & Validasi Random Forest</p>
</div>
""", unsafe_allow_html=True)

# =========================================================
# HOME
# =========================================================
if menu == "🏠 Home":
    st.markdown("""
    Aplikasi ini memprediksi tingkat kesejahteraan masyarakat Jawa Barat
    menggunakan **skor manual sebagai metode utama** dan
    **Random Forest sebagai validasi Machine Learning**.
    """)

# =========================================================
# PREDIKSI
# =========================================================
elif menu == "🔮 Prediksi":

    model = artifacts["model"]
    scaler = artifacts["scaler"]
    mapping = artifacts["mapping"]
    features = artifacts["features"]

    col1, col2 = st.columns([1.2, 1])

    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">📝 Input Data</div>', unsafe_allow_html=True)

        with st.form("form"):
            P = st.number_input("Jumlah Penduduk", 1, 10_000_000, 1_000_000)
            M = st.number_input("Penduduk Miskin", 0, 1_000_000, 80_000)
            U = st.number_input("Pengangguran", 0, 1_000_000, 50_000)
            Y = st.number_input("PDRB ADHK", 0.0, 1e15, 120_000_000_000.0)
            S = st.selectbox("Skor Pendidikan", [1,2,3,4])
            submit = st.form_submit_button("🔍 Analisis")

        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">📌 Hasil</div>', unsafe_allow_html=True)

        if submit:
            skor = hitung_skor_kesejahteraan(P, M, U, Y, S)
            kategori = tentukan_kategori(skor)
            css = get_css_class(kategori)

            input_df = pd.DataFrame([[M, U, Y, S]], columns=features)
            pred = model.predict(scaler.transform(input_df))[0]
            kategori_ml = mapping[pred]

            st.markdown(f'<div class="result-box {css}">{kategori}</div>', unsafe_allow_html=True)
            st.metric("Skor Kesejahteraan", f"{skor:.2f}")

            # ===== RINCIAN & GRAFIK =====
            pdrb = (Y / 1e10) * 4
            sekolah = S * 10
            miskin = (M / P) * 50
            pengangguran = (U / P) * 50

            komponen_df = pd.DataFrame({
                "Komponen": ["PDRB", "Pendidikan", "Kemiskinan", "Pengangguran"],
                "Nilai": [pdrb, sekolah, -miskin, -pengangguran]
            })

            fig = px.bar(
                komponen_df,
                x="Komponen",
                y="Nilai",
                text_auto=".2f",
                title="Kontribusi Komponen Skor"
            )
            fig.update_layout(template="plotly_white", height=350)
            st.plotly_chart(fig, use_container_width=True)

        st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# DATASET
# =========================================================
elif menu == "📊 Dataset":
    st.dataframe(df, use_container_width=True)

# =========================================================
# EVALUASI MODEL
# =========================================================
elif menu == "📈 Evaluasi Model":
    st.metric("Akurasi", f"{metrics['accuracy']*100:.2f}%")
    st.image(os.path.join(IMG_DIR, "confusion_matrix.png"))
    st.image(os.path.join(IMG_DIR, "feature_importance.png"))

# =========================================================
# POHON KEPUTUSAN
# =========================================================
elif menu == "🌳 Pohon Keputusan":
    st.subheader("🌳 Pohon Random Forest")

    model = artifacts["model"]
    idx = st.slider("Pilih indeks pohon", 0, len(model.estimators_)-1, 0)

    fig, ax = plt.subplots(figsize=(22,10))
    plot_tree(
        model.estimators_[idx],
        feature_names=features,
        class_names=list(mapping.values()),
        filled=True,
        rounded=True,
        ax=ax
    )
    st.pyplot(fig)

# =========================================================
# ABOUT
# =========================================================
elif menu == "ℹ️ About":
    st.markdown("""
    **Sistem Prediksi Kesejahteraan Jawa Barat**  
    Metode utama: Skor Manual  
    Validasi: Random Forest Classifier  
    """)
