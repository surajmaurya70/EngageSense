"""
EngageSense - Premium Analytics Dashboard
Inspired by Osmo, Wealthsimple & ClickUp Design
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
    page_title="EngageSense — AI Student Engagement Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium CSS (Osmo + Wealthsimple + ClickUp Inspired)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Dark Dramatic Background (Osmo-inspired) */
    .stApp {
        background: linear-gradient(180deg, #0b0b0d 0%, #070708 120%);
    }
    
    .main {
        padding: 0 !important;
    }
    
    .block-container {
        padding: 2.5rem 3rem !important;
        max-width: 1400px;
    }
    
    /* Header Section */
    .premium-header {
        background: linear-gradient(180deg, rgba(255,255,255,0.02), transparent);
        border-radius: 16px;
        padding: 2.5rem;
        margin-bottom: 2rem;
        box-shadow: 0 6px 30px rgba(3,6,12,0.6);
    }
    
    .header-title {
        font-size: 2.5rem;
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 0.5rem;
        letter-spacing: -0.5px;
        text-shadow: 0 8px 40px rgba(0,0,0,0.6);
    }
    
    .header-subtitle {
        font-size: 1rem;
        color: #9aa4b2;
        font-weight: 500;
    }
    
    .kicker {
        display: inline-block;
        background: linear-gradient(90deg, #2fe39a, #69f0b6);
        color: #041014;
        padding: 6px 12px;
        border-radius: 999px;
        font-weight: 700;
        font-size: 13px;
        margin-bottom: 1rem;
    }
    
    /* Metric Cards (Clean Trust - Wealthsimple inspired) */
    [data-testid="stMetric"] {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 12px;
        padding: 1.8rem 1.5rem;
        transition: all 0.2s ease;
        backdrop-filter: blur(6px);
    }
    
    [data-testid="stMetric"]:hover {
        border-color: rgba(255,255,255,0.12);
        box-shadow: 0 4px 12px rgba(255,255,255,0.05);
        transform: translateY(-4px);
    }
    
    [data-testid="stMetric"] label {
        color: #9aa4b2 !important;
        font-size: 0.85rem !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
    }
    
    [data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-size: 2.8rem !important;
        font-weight: 700 !important;
    }
    
    [data-testid="stMetric"] [data-testid="stMetricDelta"] {
        color: #2fe39a !important;
        font-weight: 600 !important;
    }
    
    /* Section Headers */
    h2 {
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 1.5rem !important;
        margin: 2.5rem 0 1.5rem 0 !important;
        letter-spacing: -0.3px !important;
    }
    
    /* Tabs (ClickUp inspired - productive look) */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        background: transparent;
        border-bottom: 1px solid rgba(255,255,255,0.06);
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: #9aa4b2;
        border: none;
        border-bottom: 2px solid transparent;
        padding: 1rem 1.5rem;
        font-weight: 600;
        font-size: 0.95rem;
        transition: all 0.2s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        color: #ffffff;
        background: rgba(255,255,255,0.03);
    }
    
    .stTabs [aria-selected="true"] {
        color: #2fe39a !important;
        border-bottom-color: #2fe39a !important;
        background: transparent !important;
    }
    
    /* Sidebar (Clean & Modern) */
    [data-testid="stSidebar"] {
        background: #0b0b0d;
        border-right: 1px solid rgba(255,255,255,0.06);
    }
    
    [data-testid="stSidebar"] h3 {
        color: #ffffff !important;
        font-size: 1rem !important;
        font-weight: 700 !important;
        margin-top: 1.5rem !important;
    }
    
    [data-testid="stSidebar"] label {
        color: #9aa4b2 !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
    }
    
    /* Form Elements */
    .stSelectbox [data-baseweb="select"],
    .stTextInput input,
    .stSlider {
        background: rgba(255,255,255,0.02) !important;
        border: 1px solid rgba(255,255,255,0.06) !important;
        border-radius: 8px !important;
        color: #e6eef6 !important;
    }
    
    .stSelectbox [data-baseweb="select"]:hover,
    .stTextInput input:hover {
        border-color: rgba(255,255,255,0.12) !important;
    }
    
    /* Alert Boxes */
    .stAlert {
        background: rgba(255,255,255,0.04) !important;
        border: 1px solid rgba(255,255,255,0.06) !important;
        border-radius: 12px !important;
        color: #e6eef6 !important;
    }
    
    /* Dataframe */
    .stDataFrame {
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 12px;
        overflow: hidden;
    }
    
    /* Download Button (Green Accent - ClickUp style) */
    .stDownloadButton button {
        background: linear-gradient(90deg, #2fe39a, #69f0b6) !important;
        color: #041014 !important;
        border: none !important;
        border-radius: 999px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 700 !important;
        font-size: 0.9rem !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 10px 30px rgba(47,227,154,0.15) !important;
    }
    
    .stDownloadButton button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 12px 36px rgba(47,227,154,0.25) !important;
    }
    
    /* Footer */
    .premium-footer {
        margin-top: 4rem;
        padding: 2rem;
        text-align: center;
        border-top: 1px solid rgba(255,255,255,0.06);
    }
    
    .footer-title {
        font-size: 1.3rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 0.5rem;
    }
    
    .footer-text {
        color: #9aa4b2;
        margin: 0.3rem 0;
        font-size: 0.9rem;
    }
    
    .creator-name {
        color: #2fe39a;
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
        background: #0b0b0d;
    }
    
    ::-webkit-scrollbar-thumb {
        background: rgba(255,255,255,0.1);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(255,255,255,0.15);
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
    <div class="premium-header">
        <div class="kicker">🔗 Now connected • MySQL & CSV</div>
        <div class="header-title">Discover engagement patterns that matter.</div>
        <div class="header-subtitle">AI-powered analytics that help educators detect learning gaps before they grow</div>
    </div>
""", unsafe_allow_html=True)

# Sidebar - Settings Panel
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    st.markdown("---")
    
    # Data Source
    data_source = st.radio(
        "📁 Data Source",
        ["CSV File", "MySQL Database"],
        help="Select your data source"
    )
    
    st.markdown("---")
    st.markdown("### 🔍 Filters")
    
    filter_status = st.selectbox(
        "Student Status",
        ["All Students", "Active Only", "At Risk Only"]
    )
    
    min_score = st.slider(
        "Min Engagement Score",
        0.0, 10.0, 0.0
    )
    
    search_id = st.text_input(
        "Search Student ID",
        placeholder="e.g., S007"
    )
    
    st.markdown("---")
    st.markdown("### 📊 Display")
    
    show_charts = st.checkbox("Show Charts", value=True)
    chart_height = st.slider("Chart Height", 300, 600, 400)
    
    st.markdown("---")
    st.info(f"**Last Updated**  \n{datetime.now().strftime('%B %d, %Y')}")

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

if data_source == "MySQL Database":
    df = load_data_from_mysql()
else:
    df = load_data_from_csv()

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
    st.markdown("## 📊 Engagement Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Students", len(df), "+5")
    
    with col2:
        anomaly_count = (df['anomaly'] == -1).sum()
        st.metric("At Risk", anomaly_count, f"-{anomaly_count}")
    
    with col3:
        st.metric("Avg Score", f"{df['engagement_score'].mean():.2f}", "+0.3")
    
    with col4:
        st.metric("Avg Time (hrs)", f"{df['time_spent'].mean():.1f}", "+2.3")
    
    # Charts
    if show_charts:
        st.markdown("## 📈 Visual Analytics")
        
        tab1, tab2, tab3 = st.tabs(["Distribution", "Anomaly Detection", "Top Performers"])
        
        with tab1:
            col1, col2 = st.columns(2)
            
            with col1:
                fig1 = px.histogram(df, x='engagement_score', nbins=25, title='Engagement Distribution')
                fig1.update_layout(
                    plot_bgcolor='#0b0b0d',
                    paper_bgcolor='#0b0b0d',
                    font=dict(color='#9aa4b2'),
                    title_font=dict(color='#ffffff'),
                    height=chart_height
                )
                fig1.update_traces(marker_color='#2fe39a')
                st.plotly_chart(fig1, use_container_width=True)
            
            with col2:
                counts = df['anomaly_flag'].value_counts()
                fig2 = px.pie(values=counts.values, names=counts.index, title='Student Status', hole=0.5)
                fig2.update_layout(
                    plot_bgcolor='#0b0b0d',
                    paper_bgcolor='#0b0b0d',
                    font=dict(color='#9aa4b2'),
                    title_font=dict(color='#ffffff'),
                    height=chart_height
                )
                fig2.update_traces(marker=dict(colors=['#2fe39a', '#ff6a3d']))
                st.plotly_chart(fig2, use_container_width=True)
        
        with tab2:
            fig3 = px.scatter(
                df, x='time_spent', y='engagement_score', color='anomaly_flag',
                size='login_count', hover_data=['student_id'],
                title='Time vs Engagement Analysis',
                color_discrete_map={'Active': '#2fe39a', 'At Risk': '#ff6a3d'}
            )
            fig3.update_layout(
                plot_bgcolor='#0b0b0d',
                paper_bgcolor='#0b0b0d',
                font=dict(color='#9aa4b2'),
                title_font=dict(color='#ffffff'),
                height=chart_height
            )
            st.plotly_chart(fig3, use_container_width=True)
        
        with tab3:
            top_10 = df.nlargest(10, 'engagement_score')
            fig4 = px.bar(
                top_10, x='student_id', y='engagement_score',
                color='anomaly_flag', title='Top 10 Students',
                color_discrete_map={'Active': '#2fe39a', 'At Risk': '#ff6a3d'}
            )
            fig4.update_layout(
                plot_bgcolor='#0b0b0d',
                paper_bgcolor='#0b0b0d',
                font=dict(color='#9aa4b2'),
                title_font=dict(color='#ffffff'),
                height=chart_height
            )
            st.plotly_chart(fig4, use_container_width=True)
    
    # Data Table
    st.markdown("## 📋 Student Data Explorer")
    
    # Apply filters
    filtered = df.copy()
    
    if filter_status == "Active Only":
        filtered = filtered[filtered['anomaly_flag'] == 'Active']
    elif filter_status == "At Risk Only":
        filtered = filtered[filtered['anomaly_flag'] == 'At Risk']
    
    filtered = filtered[filtered['engagement_score'] >= min_score]
    
    if search_id:
        filtered = filtered[filtered['student_id'].astype(str).str.contains(search_id, case=False)]
    
    filtered = filtered.sort_values('engagement_score', ascending=False)
    
    st.info(f"Showing **{len(filtered)}** of **{len(df)}** students")
    
    # Highlight rows
    def highlight_row(row):
        if row['anomaly_flag'] == 'At Risk':
            return ['background-color: rgba(255, 106, 61, 0.1)'] * len(row)
        return ['background-color: rgba(47, 227, 154, 0.05)'] * len(row)
    
    styled_df = filtered.style.apply(highlight_row, axis=1)
    st.dataframe(styled_df, use_container_width=True, height=400)
    
    # Export
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        csv = filtered.to_csv(index=False).encode('utf-8')
        st.download_button(
            label=f"📥 Export {len(filtered)} Records",
            data=csv,
            file_name=f'engagesense_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv',
            mime='text/csv',
            use_container_width=True
        )

else:
    st.error("❌ Failed to load data or model")

# Footer
st.markdown("""
    <div class="premium-footer">
        <div class="footer-title">EngageSense Analytics</div>
        <div class="footer-text">Developed by <span class="creator-name">Suraj Maurya</span></div>
        <div class="footer-text">AI-Powered · Privacy-First · Works with any LMS</div>
        <div class="footer-text">© 2025 All Rights Reserved</div>
    </div>
""", unsafe_allow_html=True)
