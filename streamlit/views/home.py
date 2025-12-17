import streamlit as st
from src.components import render_header, card_begin, card_end

def show():
    render_header("📊 Prediksi Kesejahteraan Masyarakat Jawa Barat", "Perhitungan Skor Manual & Validasi Random Forest")
    
    card_begin()
    st.markdown("""
    ### Selamat Datang
    
    Aplikasi ini dirancang untuk memprediksi tingkat kesejahteraan masyarakat di provinsi Jawa Barat.
    Metodologi yang digunakan menggabungkan **perhitungan skor manual** berdasarkan indikator ekonomi makro
    dan **Random Forest Classifier** sebagai validator prediksi Machine Learning.
    
    #### Fitur Utama:
    *   **Prediksi Kesejahteraan**: Analisa interaktif dengan input parameter realtime.
    *   **Visualisasi Data**: Eksplorasi dataset indikator kesejahteraan.
    *   **Evaluasi Model**: Metrik performa dan confusion matrix dari model Machine Learning.
    """)
    card_end()
