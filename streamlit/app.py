import streamlit as st
import importlib

# 1. Config & Style must be loaded first
from src.config import PAGE_CONFIG
st.set_page_config(**PAGE_CONFIG)

from src.styles import apply_custom_css

# 2. Apply Custom CSS
apply_custom_css()

# 3. Sidebar Navigation Structure
views = {
    "🏠 Home": "views.home",
    "🔮 Prediksi": "views.prediction",
    "📊 Dataset": "views.dataset",
    "📈 Evaluasi Model": "views.evaluation",
    "ℹ️ About": "views.about"
}

# 4. Render Sidebar
with st.sidebar:
    st.markdown("## 📊 Welfare Dashboard")
    selected_view = st.radio("Navigasi", list(views.keys()))
    
    st.divider()
    from src.loader import load_metrics
    metrics = load_metrics()
    if metrics:
        st.metric("Akurasi Model", f"{metrics.get('accuracy', 0)*100:.2f}%")
    st.caption("v1.0.0 Refactored")

# 5. Dynamic Module Loading
# This allows us to load only the code for the page we are viewing
try:
    module_path = views[selected_view]
    module = importlib.import_module(module_path)
    module.show()
except Exception as e:
    st.error(f"Error loading view '{selected_view}': {e}")
    st.code(str(e))
