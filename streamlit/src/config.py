import os

# Base Directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Paths
MODEL_PATH = os.path.join(BASE_DIR, "../modelling/rf_model_kesejahteraan.pkl")
DATASET_PATH = os.path.join(BASE_DIR, "../preprocessing/dataset_preprocessed.csv")
METRICS_PATH = os.path.join(BASE_DIR, "../modelling/metrics.json")
IMG_DIR = os.path.join(BASE_DIR, "../modelling")

# Page Config
PAGE_CONFIG = {
    "page_title": "Prediksi Kesejahteraan Jawa Barat",
    "page_icon": "📊",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}
