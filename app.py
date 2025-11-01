"""
EngageSense - Professional Analytics Dashboard
Developed by Suraj Maurya
"""

import streamlit as st
import pandas as pd
import joblib
import numpy as np
import mysql.connector
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Page Config
st.set_page_config(
    page_title="EngageSense Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional Minimalist CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Clean Dark Background */
    .stApp {
        background: #0a0a0a;
    }
    
    .main {
        padding: 0 !important;
    }
    
    .block-container {
        padding: 2rem 3rem !important;
        max-width: 1600px !important;
    }
    
    /* Professional Header */
    .professional-header {
        background: #121212;
        border-bottom: 1px solid #2a2a2a;
        padding: 2rem 3rem;
        margin: -2rem -3rem 3rem -3rem;
    }
    
    .header-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 0.5rem;
        letter-spacing: -0.5px;
    }
    
    .header-subtitle {
        font-size: 1rem;
        color: #8a8a8a;
        font-weight: 500;
    }
    
    /* Metric Cards - Clean & Professional */
    [data-testid="stMetric"] {
        background: #121212;
        border: 1px solid #2a2a2a;
        border-radius: 12px;
        padding: 1.8rem 1.5rem;
        transition: all 0.2s ease;
    }
    
    [data-testid="stMetric"]:hover {
        border-color: #4a4a4a;
        box-shadow: 0 4px 12px rgba(255, 255, 255, 0.05);
    }
    
    [data-testid="stMetric"] label {
        color: #8a8a8a !important;
        font-size: 0.85rem !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
    }
    
    [data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-size: 2.5rem !important;
        font-weight: 700 !important;
    }
    
    [data-testid="stMetric"] [data-testid="stMetricDelta"] {
        color: #8a8a8a !important;
        font-size: 0.9rem !important;
    }
    
    /* Section Headers */
    h2 {
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 1.5rem !important;
        margin: 3rem 0 1.5rem 0 !important;
        letter-spacing: -0.3px !important;
    }
    
    h3 {
        color: #ffffff !important;
        font-weight: 600 !important;
        font-size: 1.2rem !important;
    }
    
    /* Tabs - Minimal & Clean */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        background: transparent;
        border-bottom: 1px solid #2a2a2a;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: #8a8a8a;
        border: none;
        border-bottom: 2px solid transparent;
        padding: 1rem 1.5rem;
        font-weight: 600;
        font-size: 0.95rem;
        transition: all 0.2s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        color: #ffffff;
        background: rgba(255, 255, 255, 0.03);
    }
    
    .stTabs [aria-selected="true"] {
        color: #ffffff !important;
        border-bottom-color: #ffffff !important;
        background: transparent !important;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: #0a0a0a;
        border-right: 1px solid #2a2a2a;
    }
    
    [data-testid="stSidebar"] h3 {
        color: #ffffff !important;
        font-size: 1rem !important;
        font-weight: 700 !important;
        margin-top: 2rem !important;
    }
    
    [data-testid="stSidebar"] label {
        color: #8a8a8a !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
    }
    
    /* Form Elements */
    .stSelectbox [data-baseweb="select"],
    .stTextInput input {
        background: #121212 !important;
        border: 1px solid #2a2a2a !important;
        border-radius: 8px !important;
        color: #ffffff !important;
    }
    
    .stSelectbox [data-baseweb="select"]:hover,
    .stTextInput input:hover {
        border-color: #4a4a4a !important;
    }
    
    /* Info/Alert Boxes */
    .stAlert {
        background: #121212 !important;
        border: 1px solid #2a2a2a !important;
        border-radius: 8px !important;
        color: #ffffff !important;
    }
    
    /* Dataframe */
    .stDataFrame {
        border: 1px solid #2a2a2a;
        border-radius: 12px;
        overflow: hidden;
    }
    
    /* Download Button */
    .stDownloadButton button {
        background: #ffffff !important;
        color: #000000 !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 700 !important;
        font-size: 0.9rem !important;
        transition: all 0.2s ease !important;
    }
    
    .stDownloadButton button:hover {
        background: #e0e0e0 !important;
    }
    
    /* Footer */
    .minimal-footer {
        margin-top: 5rem;
        padding: 3rem 0;
        border-top: 1px solid #2a2a2a;
        text-align: center;
    }
    
    .footer-brand {
        font-size: 1.5rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 1rem;
    }
    
    .footer-text {
        font-size: 0.95rem;
        color: #8a8a8a;
        margin: 0.5rem 0;
    }
    
    .creator-name {
        color: #ffffff;
        font-weight: 700;
    }
    
    /* Hide Streamlit Branding */
    #MainMenu, footer, header {visibility: hidden;}
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #0a0a0a;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #2a2a2a;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #4a4a4a;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
    <div class="professional-header">
        <div class="header-title">EngageSense Analytics</div>
        <div class="header-subtitle">Student Engagement Monitoring Platform</div>
    </div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### Filters")
    
    filter_status = st.selectbox(
        "Status",
        ["All Students", "Active Only", "At Risk Only"]
    )
    
    search_id = st.text_input(
        "Search Student ID",
        placeholder="Enter ID..."
    )
    
    st.markdown("---")
    st.markdown(f"**Last Updated**  \n{datetime.now().strftime('%B %d, %Y')}")

# Load Functions
@st.cache_resource
def load_model():
    try:
        return joblib.load('isolation_forest.pkl')
    except Exception as e:
        st.error(f"Model Error: {e}")
        return None

@st.cache_data
def load_data_from_mysql():
    try:
        conn = mysql.connector.connect(host="localhost", user="root", password="", database="engagesense_db")
        df = pd.read_sql("SELECT * FROM student_engagement", conn)
        conn.close()
        return df
    except:
        return load_data_from_csv()

@st.cache_data
def load_data_from_csv():
    try:
        return pd.read_csv('student_engagement.csv')
    except Exception as e:
        st.error(f"Data Error: {e}")
        return None

model = load_model()
df = load_data_from_mysql()

if df is not None and model is not None:
    
    # Calculate engagement score
    if 'engagement_score' not in df.columns:
        df['engagement_score'] = (
            df['login_count'] * 0.25 +
            (df['time_spent'] / 60) * 0.25 +
            df['quiz_attempts'] * 0.2 +
            df['forum_posts'] * 0.15 +
            (df['assignment_score'] / 100) * 0.15 * 10
        )
    
    # Predict anomalies
    try:
        df['anomaly'] = model.predict(df[['login_count', 'time_spent', 'quiz_attempts']].values)
        df['anomaly_flag'] = df['anomaly'].apply(lambda x: 'At Risk' if x == -1 else 'Active')
    except:
        df['anomaly'] = 1
        df['anomaly_flag'] = 'Active'
    
    # Top Metrics
    st.markdown("## Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Students",
            value=len(df),
            delta="+5 this month"
        )
    
    with col2:
        anomaly_count = (df['anomaly'] == -1).sum()
        st.metric(
            label="At Risk",
            value=anomaly_count,
            delta=f"{(anomaly_count/len(df)*100):.1f}%",
            delta_color="inverse"
        )
    
    with col3:
        avg_score = df['engagement_score'].mean()
        st.metric(
            label="Avg Score",
            value=f"{avg_score:.2f}",
            delta="+0.3"
        )
    
    with col4:
        avg_time = df['time_spent'].mean()
        st.metric(
            label="Avg Time (hrs)",
            value=f"{avg_time:.1f}",
            delta="+2.3"
        )
    
    # Charts
    st.markdown("## Analytics")
    
    tab1, tab2, tab3 = st.tabs(["Distribution", "Anomaly Detection", "Performance"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            fig1 = px.histogram(
                df, 
                x='engagement_score',
                nbins=25,
                title='Engagement Score Distribution',
                color_discrete_sequence=['#ffffff']
            )
            fig1.update_layout(
                plot_bgcolor='#0a0a0a',
                paper_bgcolor='#0a0a0a',
                font=dict(color='#8a8a8a', size=12, family='Inter'),
                title_font=dict(color='#ffffff', size=16),
                showlegend=False,
                height=400,
                margin=dict(l=40, r=40, t=60, b=40)
            )
            fig1.update_xaxes(gridcolor='#2a2a2a', zeroline=False)
            fig1.update_yaxes(gridcolor='#2a2a2a', zeroline=False)
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            counts = df['anomaly_flag'].value_counts()
            fig2 = px.pie(
                values=counts.values,
                names=counts.index,
                title='Student Status',
                color_discrete_sequence=['#ffffff', '#4a4a4a'],
                hole=0.5
            )
            fig2.update_layout(
                plot_bgcolor='#0a0a0a',
                paper_bgcolor='#0a0a0a',
                font=dict(color='#8a8a8a', size=12, family='Inter'),
                title_font=dict(color='#ffffff', size=16),
                height=400,
                showlegend=True,
                legend=dict(font=dict(color='#8a8a8a'))
            )
            fig2.update_traces(textfont=dict(color='#0a0a0a'))
            st.plotly_chart(fig2, use_container_width=True)
    
    with tab2:
        fig3 = px.scatter(
            df,
            x='time_spent',
            y='engagement_score',
            color='anomaly_flag',
            size='login_count',
            hover_data=['student_id'],
            title='Time vs Engagement Analysis',
            color_discrete_map={'Active': '#ffffff', 'At Risk': '#8a8a8a'}
        )
        fig3.update_layout(
            plot_bgcolor='#0a0a0a',
            paper_bgcolor='#0a0a0a',
            font=dict(color='#8a8a8a', size=12, family='Inter'),
            title_font=dict(color='#ffffff', size=16),
            height=500,
            legend=dict(font=dict(color='#8a8a8a'))
        )
        fig3.update_xaxes(gridcolor='#2a2a2a', zeroline=False)
        fig3.update_yaxes(gridcolor='#2a2a2a', zeroline=False)
        st.plotly_chart(fig3, use_container_width=True)
    
    with tab3:
        top_10 = df.nlargest(10, 'engagement_score')
        fig4 = px.bar(
            top_10,
            x='student_id',
            y='engagement_score',
            color='anomaly_flag',
            title='Top 10 Students',
            color_discrete_map={'Active': '#ffffff', 'At Risk': '#8a8a8a'}
        )
        fig4.update_layout(
            plot_bgcolor='#0a0a0a',
            paper_bgcolor='#0a0a0a',
            font=dict(color='#8a8a8a', size=12, family='Inter'),
            title_font=dict(color='#ffffff', size=16),
            height=500,
            showlegend=True,
            legend=dict(font=dict(color='#8a8a8a'))
        )
        fig4.update_xaxes(gridcolor='#2a2a2a', zeroline=False)
        fig4.update_yaxes(gridcolor='#2a2a2a', zeroline=False)
        st.plotly_chart(fig4, use_container_width=True)
    
    # Data Table
    st.markdown("## Student Data")
    
    # Apply filters
    filtered = df.copy()
    
    if filter_status == "Active Only":
        filtered = filtered[filtered['anomaly_flag'] == 'Active']
    elif filter_status == "At Risk Only":
        filtered = filtered[filtered['anomaly_flag'] == 'At Risk']
    
    if search_id:
        filtered = filtered[filtered['student_id'].astype(str).str.contains(search_id, case=False)]
    
    min_score = st.slider(
        "Minimum Score",
        float(df['engagement_score'].min()),
        float(df['engagement_score'].max()),
        float(df['engagement_score'].min())
    )
    
    filtered = filtered[filtered['engagement_score'] >= min_score]
    filtered = filtered.sort_values('engagement_score', ascending=False)
    
    st.info(f"Showing {len(filtered)} of {len(df)} students")
    
    # Display table
    def highlight_row(row):
        if row['anomaly_flag'] == 'At Risk':
            return ['background-color: #1a1a1a'] * len(row)
        return ['background-color: transparent'] * len(row)
    
    styled_df = filtered.style.apply(highlight_row, axis=1)
    st.dataframe(styled_df, use_container_width=True, height=400)
    
    # Download
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        csv = filtered.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Export Data",
            data=csv,
            file_name=f'engagesense_{datetime.now().strftime("%Y%m%d")}.csv',
            mime='text/csv',
            use_container_width=True
        )

else:
    st.error("Failed to load data or model")

# Footer
st.markdown("""
    <div class="minimal-footer">
        <div class="footer-brand">EngageSense</div>
        <div class="footer-text">Developed by <span class="creator-name">Suraj Maurya</span></div>
        <div class="footer-text">Machine Learning · Python · Streamlit</div>
        <div class="footer-text">© 2025 All Rights Reserved</div>
    </div>
""", unsafe_allow_html=True)
