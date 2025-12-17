import streamlit as st
from src.components import render_header, card_begin, card_end

def show():
    render_header("ℹ️ About", "Tentang Sistem")
    
    card_begin()
    st.markdown("""
    **Sistem Prediksi Kesejahteraan Jawa Barat**
    
    Dikembangkan untuk memenuhi Tugas Akhir Mata Kuliah Machine Learning (UAS).
    
    **Tim Pengembang:**
    *   Teknologi: Python, Streamlit, Scikit-Learn
    *   Data Source: BPS Jawa Barat
    
    ---
    **Versi**: 1.0.0
    """)
    card_end()
