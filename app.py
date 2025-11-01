import streamlit as st
import pandas as pd
import joblib
import numpy as np
import mysql.connector
from datetime import datetime

st.set_page_config(page_title="EngageSense", page_icon="📊", layout="wide")

st.markdown("""
    <style>
    .stApp { background: #ffffff; }
    h1 { color: #1f1f1f; font-weight: 700; }
    h2 { color: #1f1f1f; font-weight: 600; margin-top: 2rem; }
    [data-testid="stMetric"] { background: #f8f9fa; padding: 1rem; border-radius: 8px; }
    [data-testid="stMetric"] label { color: #6c757d; font-size: 0.9rem; }
    [data-testid="stMetric"] [data-testid="stMetricValue"] { color: #1f1f1f; font-size: 2rem; font-weight: 700; }
    .footer { margin-top: 3rem; padding: 2rem; text-align: center; color: #6c757d; border-top: 1px solid #dee2e6; }
    #MainMenu, footer, header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_model():
    try:
        return joblib.load('isolation_forest.pkl')
    except:
        return None

@st.cache_data
def load_data():
    try:
        return pd.read_csv('student_engagement.csv')
    except:
        return None

model = load_model()
df = load_data()

if df is not None and model is not None:
    
    if 'engagement_score' not in df.columns:
        df['engagement_score'] = (
            df['login_count'] * 0.25 +
            (df['time_spent'] / 60) * 0.25 +
            df['quiz_attempts'] * 0.2 +
            df['forum_posts'] * 0.15 +
            (df['assignment_score'] / 100) * 0.15 * 10
        )
    
    try:
        df['anomaly'] = model.predict(df[['login_count', 'time_spent', 'quiz_attempts']].values)
        df['anomaly_flag'] = df['anomaly'].apply(lambda x: 'Anomaly' if x == -1 else 'Normal')
    except:
        df['anomaly'] = 1
        df['anomaly_flag'] = 'Normal'
    
    st.title("EngageSense (Demo)")
    
    st.markdown("## Top: Engagement Summary")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Avg Engagement Score", f"{df['engagement_score'].mean():.2f}")
    
    with col2:
        anomaly_count = (df['anomaly'] == -1).sum()
        st.metric("Anomalies Detected", anomaly_count)
    
    with col3:
        st.metric("Students", len(df))
    
    st.markdown("## Students Table (sorted by engagement score)")
    
    df_display = df.sort_values('engagement_score', ascending=False)
    st.dataframe(df_display, use_container_width=True, height=400)
    
    st.markdown("""
        <div class="footer">
            <strong>EngageSense © 2025</strong> | Developed by Suraj Maurya
        </div>
    """, unsafe_allow_html=True)

else:
    st.error("Failed to load data or model")
