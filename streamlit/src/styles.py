import streamlit as st

def apply_custom_css():
    st.markdown("""
    <style>
    /* GLOBAL THEME OVERRIDES - DARK MODE */
    
    /* Force Dark Theme Background and Text */
    .stApp {
        background-color: #0e1117 !important;
        color: #ffffff !important;
    }
    
    /* Text Color Overrides */
    h1, h2, h3, h4, h5, h6, p, label, .stMarkdown, .stText, li {
        color: #ffffff !important;
    }

    /* Main Header */
    .main-header {
        padding: 3rem;
        background: linear-gradient(135deg, #2b324a, #161b22);
        border: 1px solid #30363d;
        border-radius: 12px;
        color: white;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0,0,0,0.5);
    }
    .main-header h1 {
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        font-weight: 700;
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
        color: #ffffff !important;
    }
    .main-header p {
        font-size: 1.2rem;
        color: #c9d1d9 !important;
    }

    /* Cards */
    .card {
        background: #161b22;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        margin-bottom: 1.5rem;
        border: 1px solid #30363d;
    }
    .card-title {
        font-size: 1.25rem;
        font-weight: 600;
        margin-bottom: 1.5rem;
        color: #ffffff;
        border-bottom: 2px solid #30363d;
        padding-bottom: 0.5rem;
    }

    /* Streamlit Widgets Overrides for Dark Mode */
    /* Input fields (Number Input, Text Input) */
    .stNumberInput input, .stTextInput input, .stSelectbox div[data-baseweb="select"] > div {
        background-color: #0d1117 !important;
        color: #ffffff !important;
        border-color: #30363d !important;
        caret-color: white;
    }
    
    /* Input Labels */
    .stNumberInput label, .stSelectbox label, .stSlider label {
        color: #ffffff !important;
    }
    
    /* Selectbox Dropdown Options */
    ul[data-baseweb="menu"] {
        background-color: #161b22 !important;
    }
    li[data-baseweb="option"] {
        color: #ffffff !important;
    }

    /* Sliders */
    .stSlider > div > div > div > div {
        color: #ffffff !important;
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #161b22;
        border-right: 1px solid #30363d;
    }
    section[data-testid="stSidebar"] .stMarkdown, section[data-testid="stSidebar"] h1, section[data-testid="stSidebar"] h2, section[data-testid="stSidebar"] h3 {
        color: #ffffff !important;
    }

    /* Result Box */
    .result-box {
        padding: 2rem;
        border-radius: 12px;
        font-size: 2rem;
        font-weight: 800;
        text-align: center;
        color: white;
        box-shadow: 0 8px 20px rgba(0,0,0,0.3);
        margin-bottom: 1.5rem;
    }
    
    /* Status Colors */
    .success { background: linear-gradient(135deg, #0f5132, #198754); color: white; border: 1px solid #146c43; }
    .warning { background: linear-gradient(135deg, #664d03, #ffc107); color: white; border: 1px solid #997404; }
    .danger { background: linear-gradient(135deg, #842029, #dc3545); color: white; border: 1px solid #b02a37; }
    
    /* BUTTON STYLES OVERRIDE - DARK */
    .stButton > button {
        background-color: #21262d !important;
        color: #c9d1d9 !important;
        border: 1px solid #30363d !important;
        border-radius: 8px !important;
        transition: all 0.2s ease;
        box-shadow: none !important;
    }
    
    .stButton > button:hover {
        background-color: #30363d !important;
        color: #ffffff !important;
        border-color: #8b949e !important;
    }
    
    /* Active/Focus states */
    .stButton > button:focus, .stButton > button:active {
        background-color: #30363d !important;
        color: #ffffff !important;
        border-color: #8b949e !important;
    }

    /* Form Submit Button */
    div[data-testid="stFormSubmitButton"] > button {
        background-color: #238636 !important; /* GitHub Green-ish */
        color: #ffffff !important;
        border: 1px solid #2ea043 !important;
    }
    div[data-testid="stFormSubmitButton"] > button:hover {
        background-color: #2ea043 !important;
    }
    
    /* Ensure other text inputs and widgets are clearly dark theme */
    div[data-testid="stToolbar"] {
        background-color: #0e1117 !important;
        color: white !important;
    }
    
    /* DataFrame */
    div[data-testid="stDataFrame"] {
        color: #ffffff !important;
    }
    
    /* Slider Text */
    .stSlider div[data-baseweb="slider"] {
        color: #ffffff !important;
    }
    
    /* Expander Headers */
    .streamlit-expanderHeader {
        background-color: #161b22 !important;
        color: #ffffff !important;
    }
    
    /* Tabs Overrides */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #0e1117 !important;
    }
    .stTabs [data-baseweb="tab"] {
        color: #c9d1d9 !important;
    }
    .stTabs [aria-selected="true"] {
        color: #58a6ff !important; /* Blue for active */
    }
    
    /* Standard Streamlit Alerts */
    div[data-baseweb="notification"] {
        background-color: #161b22 !important;
        color: #ffffff !important;
        border: 1px solid #30363d !important;
    }
    
    /* Toast */
    div[data-baseweb="toast"] {
        background-color: #161b22 !important;
        color: #ffffff !important;
    }
    
    </style>
    """, unsafe_allow_html=True)
