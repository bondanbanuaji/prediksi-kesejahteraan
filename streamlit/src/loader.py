import streamlit as st
import pandas as pd
import joblib
import json
import os
from src.config import MODEL_PATH, DATASET_PATH, METRICS_PATH

@st.cache_resource
def load_model():
    if not os.path.exists(MODEL_PATH):
        st.error(f"Model file not found at {MODEL_PATH}")
        return None
    return joblib.load(MODEL_PATH)

@st.cache_data
def load_dataset():
    if not os.path.exists(DATASET_PATH):
        st.error(f"Dataset file not found at {DATASET_PATH}")
        return pd.DataFrame()
    return pd.read_csv(DATASET_PATH)

@st.cache_data
def load_metrics():
    if not os.path.exists(METRICS_PATH):
        return {}
    with open(METRICS_PATH) as f:
        return json.load(f)

def load_all_artifacts():
    """Load all necessary artifacts at once."""
    artifacts = load_model()
    dataset = load_dataset()
    metrics = load_metrics()
    
    return {
        "model_artifacts": artifacts,
        "dataset": dataset,
        "metrics": metrics
    }
