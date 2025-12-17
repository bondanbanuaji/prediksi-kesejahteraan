import streamlit as st
import os
from src.components import render_header, card_begin, card_end
from src.loader import load_metrics
from src.config import IMG_DIR

def show():
    render_header("📈 Evaluasi Model", "Metrik Performa & Analisis Feature Importance")
    
    metrics = load_metrics()
    
    # Metrics Evaluation
    card_begin()
    st.markdown("### Performa Model")
    col1, col2, col3 = st.columns(3)
    
    accuracy = metrics.get('accuracy', 0) * 100
    
    with col1:
        st.metric("Akurasi Model", f"{accuracy:.2f}%")
    
    st.info("Model Random Forest mencapai akurasi yang sangat tinggi validasi pola data yang dipelajari.")
    card_end()
    
    # Visualizations
    col_img1, col_img2 = st.columns(2)
    
    with col_img1:
        card_begin()
        st.markdown("#### Confusion Matrix")
        cm_path = os.path.join(IMG_DIR, "confusion_matrix.png")
        if os.path.exists(cm_path):
            st.image(cm_path, use_container_width=True)
        else:
            st.warning("Confusion Matrix image not found.")
        card_end()
        
    with col_img2:
        card_begin()
        st.markdown("#### Feature Importance")
        fi_path = os.path.join(IMG_DIR, "feature_importance.png")
        if os.path.exists(fi_path):
            st.image(fi_path, use_container_width=True)
        else:
            st.warning("Feature Importance image not found.")
        card_end()
