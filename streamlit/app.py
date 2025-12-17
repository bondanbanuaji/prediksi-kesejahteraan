import streamlit as st
import pandas as pd
import joblib
import os
import time
import json
import matplotlib.pyplot as plt
import seaborn as sns

# --- Konfigurasi Page ---
st.set_page_config(
    page_title="Prediksi Kesejahteraan",
    page_icon="🌟",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Path Configuration ---
# Menggunakan relative path agar portable
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, '../modelling/rf_model_kesejahteraan.pkl')
DATASET_PATH = os.path.join(BASE_DIR, '../preprocessing/dataset_preprocessed.csv')
METRICS_PATH = os.path.join(BASE_DIR, '../modelling/metrics.json')
IMG_DIR = os.path.join(BASE_DIR, '../modelling')

# --- Custom CSS (Rich Aesthetics) ---
def load_css():
    st.markdown("""
        <style>
        /* Main Container */
        .main {
            background-color: #f8f9fa;
        }
        
        /* Headers */
        h1, h2, h3 {
            color: #2c3e50;
            font-family: 'Segoe UI', sans-serif;
            font-weight: 600;
        }
        
        .main-header {
            text-align: center;
            padding: 2rem 0;
            background: linear-gradient(90deg, #4b6cb7 0%, #182848 100%);
            color: white;
            border-radius: 10px;
            margin-bottom: 2rem;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        
        /* Cards & Containers */
        .stCard {
            background-color: white;
            padding: 1.5rem;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            transition: transform 0.2s;
        }
        .stCard:hover {
            transform: translateY(-5px);
        }
        
        /* Metric Cards */
        div[data-testid="stMetric"] {
            background-color: #ffffff;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
            border-left: 5px solid #4b6cb7;
        }
        
        /* Sidebar */
        .css-1d391kg {
            background-color: #ffffff;
        }
        
        /* Buttons */
        .stButton>button {
            width: 100%;
            border-radius: 20px;
            font-weight: bold;
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        
        /* Custom Classes */
        .prediction-result {
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            font-size: 24px;
            font-weight: bold;
            margin-top: 20px;
            color: white;
        }
        .success-bg { background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); }
        .warning-bg { background: linear-gradient(135deg, #fceabb 0%, #f8b500 100%); color: #333;}
        .danger-bg { background: linear-gradient(135deg, #cb2d3e 0%, #ef473a 100%); }
        
        </style>
    """, unsafe_allow_html=True)

load_css()

# --- Load Resources (Cached) ---
@st.cache_resource
def load_resources():
    try:
        artifacts = joblib.load(MODEL_PATH)
        return artifacts
    except FileNotFoundError:
        return None
    except Exception as e:
        st.error(f"Error loading resources: {e}")
        return None

@st.cache_data
def load_dataset():
    try:
        return pd.read_csv(DATASET_PATH)
    except:
        return None

@st.cache_data
def load_metrics():
    try:
        with open(METRICS_PATH, 'r') as f:
            return json.load(f)
    except:
        return None

# --- Main App Logic ---
artifacts = load_resources()
df = load_dataset()
metrics = load_metrics()

# --- Sidebar ---
with st.sidebar:
    st.image("https://img.icons8.com/clouds/200/000000/futures.png", output_format='PNG')
    st.markdown("### 🧭 Navigasi")
    
    # Custom Navigation menu using radio instead of default for better control look
    # (Optional: can use st.sidebar.title/header)
    
    st.info("Aplikasi Prediksi Kesejahteraan Daerah berbasis Machine Learning.")
    st.markdown("---")
    st.markdown("**Model:** Random Forest Classifier")
    if metrics:
        st.metric("Akurasi Model", f"{metrics['accuracy']*100:.2f}%")
    st.markdown("---")
    st.caption("© 2025 Magang PSI STT Wastukancana")


# --- Tabs ---
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🏠 Home",
    "📊 Dataset",
    "📈 Performa",
    "🌳 Trees",
    "🔮 Prediksi",
    "ℹ️ About"
])

# --- TAB 1: HOME ---
with tab1:
    st.markdown('<div class="main-header"><h1>🌟 Dashboard Prediksi Kesejahteraan</h1></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### Selamat Datang! 👋
        
        Aplikasi ini dirancang untuk membantu pemerintah dan pemangku kepentingan dalam **memprediksi tingkat kesejahteraan** suatu daerah berdasarkan indikator sosial-ekonomi utama.
        
        **Fitur Utama:**
        - **Akurasi Tinggi:** Menggunakan algoritma Random Forest yang terbukti handal.
        - **Analisis Mendalam:** Visualisasi data dan feature importance.
        - **Real-time Prediction:** Masukkan data dan dapatkan hasil seketika.
        
        Silahkan jelajahi menu di atas untuk memulai analisis Anda.
        """)
        
    with col2:
        st.markdown("### 💡 Quick Stats")
        if df is not None:
            st.write(f"**Total Data:** {len(df)} Records")
            st.write(f"**Fitur:** {len(df.columns)-1} Variabel")
        else:
            st.warning("Data belum dimuat.")

# --- TAB 2: DATASET ---
with tab2:
    st.header("📂 Eksplorasi Dataset")
    if df is not None:
        st.caption("Data yang digunakan untuk pelatihan model.")
        
        col_desc, col_table = st.columns([1, 2])
        
        with col_desc:
            st.markdown("#### Statistik Deskriptif")
            st.dataframe(df.describe(), height=400)
            
        with col_table:
            st.markdown("#### Raw Data")
            st.dataframe(df, use_container_width=True, height=400)
            
            # Download Button
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                "📥 Download CSV",
                csv,
                "dataset_welfare.csv",
                "text/csv",
                key='download-csv'
            )
    else:
        st.error("Dataset tidak ditemukan. Jalankan script preprocessing terlebih dahulu.")

# --- TAB 3: PERFORMA ---
with tab3:
    st.header("📈 Evaluasi Model")

    if os.path.exists(IMG_DIR):
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Confusion Matrix")
            cm_path = os.path.join(IMG_DIR, 'confusion_matrix.png')
            if os.path.exists(cm_path):
                st.image(cm_path, caption="Confusion Matrix Model", use_container_width=True)
            else:
                st.info("Gambar Confusion Matrix belum tersedia.")

        with col2:
            st.subheader("Feature Importance")
            fi_path = os.path.join(IMG_DIR, 'feature_importance.png')
            if os.path.exists(fi_path):
                st.image(fi_path, caption="Tingkat Kepentingan Fitur", use_container_width=True)
            else:
                st.info("Gambar Feature Importance belum tersedia.")

        if metrics:
            st.markdown("### 📋 Classification Report")
            report_df = pd.DataFrame(metrics['classification_report']).transpose()
            st.dataframe(report_df.style.highlight_max(axis=0), use_container_width=True)
    else:
        st.error("Directory modelling tidak ditemukan.")

# --- TAB 4: DECISION TREES ---
with tab4:
    st.header("🌳 Visualisasi Pohon Keputusan")

    if os.path.exists(IMG_DIR):
        st.markdown("""
        ### 📊 Struktur Pohon Keputusan
        Visualisasi berikut menunjukkan struktur dari salah satu pohon keputusan dalam Random Forest.
        Setiap node menyajikan keputusan berdasarkan fitur-fitur yang digunakan dalam model.
        """)

        # Decision Tree Visualization
        tree_path = os.path.join(IMG_DIR, 'decision_tree_viz.png')
        if os.path.exists(tree_path):
            st.image(tree_path, caption="Visualisasi Pohon Keputusan (Pohon Pertama)", use_container_width=True)
        else:
            st.info("Visualisasi pohon keputusan belum tersedia.")

        # Performance Metrics Visualization
        perf_path = os.path.join(IMG_DIR, 'performance_metrics.png')
        if os.path.exists(perf_path):
            st.markdown("### 📈 Metrik Kinerja Berdasarkan Kelas")
            st.image(perf_path, caption="Perbandingan Precision, Recall, dan F1-Score per Kelas", use_container_width=True)
        else:
            st.info("Visualisasi metrik kinerja kelas belum tersedia.")

        # Explanation of tree visualization
        with st.expander("🔍 Penjelasan Visualisasi Pohon Keputusan"):
            st.markdown("""
            **Pohon Keputusan** menunjukkan jalur keputusan yang dibuat oleh model:

            - **Node dalam**: Kondisi keputusan berdasarkan fitur
            - **Node daun**: Prediksi akhir dari model
            - **Warna**: Mewakili kelas target (semakin gelap, semakin kontras ke kelas tertentu)
            - **Nilai**: Jumlah sampel yang mencapai node tersebut

            Visualisasi ini membantu memahami bagaimana model membuat keputusan klasifikasi.
            """)
    else:
        st.error("Directory modelling tidak ditemukan.")

# --- TAB 5: PREDIKSI ---
with tab5:
    st.header("🔮 Prediksi Kesejahteraan")
    
    if artifacts:
        model = artifacts['model']
        scaler = artifacts['scaler']
        mapping = artifacts['mapping']
        features = artifacts['features']
        
        col_input, col_result = st.columns([1, 1], gap="large")
        
        with col_input:
            st.markdown("### 📝 Masukkan Data")
            with st.form("prediction_form"):
                # Input fields sesuai features
                # ['jumlah_penduduk_miskin', 'jumlah_pengangguran_terbuka', 'pdrb_total_adhk', 'harapan_lama_sekolah']
                
                v1 = st.number_input("Jumlah Penduduk Miskin", min_value=0, value=10000, step=100)
                v2 = st.number_input("Jumlah Pengangguran Terbuka", min_value=0, value=5000, step=100)
                v3 = st.number_input("PDRB Total ADHK (Rp)", min_value=0.0, value=1000000000.0, step=1000000.0, format="%.0f")
                v4 = st.number_input("Harapan Lama Sekolah (Tahun)", min_value=0.0, max_value=25.0, value=12.0, step=0.1)
                
                submitted = st.form_submit_button("🔍 Analisis Sekarang")
        
        with col_result:
            if submitted:
                # Prepare input
                input_data = pd.DataFrame([[v1, v2, v3, v4]], columns=features)
                
                # Preprocessing input (Scaling)
                input_scaled = scaler.transform(input_data)
                
                # Timer
                start_time = time.time()
                
                # Predict
                prediction_idx = model.predict(input_scaled)[0]
                prediction_label = mapping[prediction_idx]
                
                end_time = time.time()
                duration = end_time - start_time
                
                st.success(f"Analisis Selesai dalam {duration:.4f} detik")
                
                # Logic warna result
                bg_class = "warning-bg" # default
                if "Sangat Sejahtera" in prediction_label: bg_class = "success-bg"
                elif "Sejahtera" in prediction_label: bg_class = "success-bg"
                elif "Tidak" in prediction_label: bg_class = "danger-bg"
                
                st.markdown(f"""
                <div class="prediction-result {bg_class}">
                    Status: {prediction_label}
                </div>
                """, unsafe_allow_html=True)
                
                # Show probability if available
                if hasattr(model, "predict_proba"):
                    proba = model.predict_proba(input_scaled)[0]
                    st.markdown("#### Confidence Score:")
                    
                    chart_data = pd.DataFrame({
                        'Status': list(mapping.values()),
                        'Probability': proba
                    })
                    st.bar_chart(chart_data.set_index('Status'))

    else:
        st.error("Model belum dimuat. Training model terlebih dahulu.")

# --- TAB 6: ABOUT ---
with tab6:
    st.header("ℹ️ Tentang Aplikasi")
    
    st.markdown("""
    ### Prediksi Kesejahteraan Daerah
    
    Aplikasi ini dikembangkan sebagai bagian dari Tugas UAS Machine Learning di STT Wastukancana Purwakarta.
    
    **Tujuan:**
    Memberikan alat bantu analitik untuk mengklasifikasikan tingkat kesejahteraan daerah berdasarkan data BPS.
    
    **Teknologi:**
    - **Python:** Core Logic
    - **Scikit-Learn:** Machine Learning (Random Forest)
    - **Streamlit:** User Interface
    - **Pandas & NumPy:** Data Processing
    
    **Pengembang:**
    - Team Machine Learning Semester 5
    - *Created with ❤️ by Magang PSI*
    """)
    
    st.image("https://streamlit.io/images/brand/streamlit-logo-secondary-colormark-darktext.png", width=200)

