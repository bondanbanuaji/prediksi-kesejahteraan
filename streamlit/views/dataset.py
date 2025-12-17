import streamlit as st
from src.components import render_header, card_begin, card_end
from src.loader import load_dataset

def show():
    render_header("📊 Dataset Kesejahteraan", "Data Historis Indikator Ekonomi & Sosial")
    
    df = load_dataset()
    
    card_begin()
    st.markdown("### Preview Data")
    st.dataframe(df, use_container_width=True)
    
    st.markdown(f"**Total Data:** {df.shape[0]} baris, {df.shape[1]} kolom")
    card_end()
