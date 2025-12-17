import streamlit as st

def render_header(title, subtitle):
    st.markdown(f"""
    <div class="main-header">
        <h1>{title}</h1>
        <p>{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)

def card_begin():
    st.markdown('<div class="card">', unsafe_allow_html=True)

def card_end():
    st.markdown('</div>', unsafe_allow_html=True)

def result_box(text, css_class):
    st.markdown(f'<div class="result-box {css_class}">{text}</div>', unsafe_allow_html=True)
