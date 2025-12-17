import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from src.components import render_header, card_begin, card_end, result_box
from src.loader import load_all_artifacts
from src.logic import hitung_skor_kesejahteraan, tentukan_kategori, get_css_class

def show():
    render_header("🔮 Prediksi Kesejahteraan", "Analisis Manual & Validasi Machine Learning")
    
    data = load_all_artifacts()
    artifacts = data["model_artifacts"]
    
    if not artifacts:
        st.error("Model artifacts could not be loaded.")
        return

    # ML artifacts unpacking skipped as unused
    
    col_input, col_result = st.columns([1, 1.2])
    
    with col_input:
        card_begin()
        st.markdown('<div class="card-title">📝 Input Indikator</div>', unsafe_allow_html=True)
        
        with st.form("prediction_form"):
            P = st.number_input("Jumlah Penduduk (Jiwa)", min_value=1, max_value=50_000_000, value=1_000_000, step=1000)
            M = st.number_input("Penduduk Miskin (Jiwa)", min_value=0, max_value=5_000_000, value=80_000, step=1000)
            U = st.number_input("Pengangguran Terbuka (Jiwa)", min_value=0, max_value=5_000_000, value=50_000, step=1000)
            Y = st.number_input("PDRB ADHK (Rupiah)", min_value=0.0, max_value=1e16, value=120_000_000_000.0, step=1_000_000_000.0, format="%.2f")
            S = st.selectbox("Skor Rata-rata Lama Sekolah (1-4)", [1, 2, 3, 4], help="1: Rendah, 4: Tinggi")
            
            submit = st.form_submit_button("🔍 Analisis Kesejahteraan", use_container_width=True)
        card_end()
        
    if submit:
        with col_result:
            # 1. Calculate Score
            skor_final, pdrb_score, edu_score, poverty_impact, unemployment_impact = hitung_skor_kesejahteraan(P, M, U, Y, S)
            kategori = tentukan_kategori(skor_final)
            css_class = get_css_class(kategori)

            
            # Display Result
            card_begin()
            st.markdown('<div class="card-title">📌 Hasil Analisis</div>', unsafe_allow_html=True)
            
            st.markdown("### Status Kesejahteraan")
            result_box(kategori, css_class)
            
            st.metric("Skor Kesejahteraan", f"{skor_final:.2f}")
            
            # Visualization Logic
            st.divider()
            st.markdown("#### Analisis Komponen")
            
            # Data for charts
            categories = ['PDRB (+)', 'Pendidikan (+)', 'Kemiskinan (-)', 'Pengangguran (-)']
            values = [pdrb_score, edu_score, poverty_impact, unemployment_impact]
            
            # Bar Chart with Color Logic
            colors = ['#38ef7d', '#38ef7d', '#ef473a', '#ef473a']
            fig_bar = go.Figure(go.Bar(
                x=categories,
                y=values,
                marker_color=colors,
                text=[f"{v:.2f}" for v in values],
                textposition='auto'
            ))
            fig_bar.update_layout(
                title="Kontribusi Variabel terhadap Skor",
                yaxis_title="Poin Kontribusi",
                template="plotly_white",
                height=300,
                margin=dict(l=20, r=20, t=40, b=20)
            )
            st.plotly_chart(fig_bar, use_container_width=True)

            card_end()
