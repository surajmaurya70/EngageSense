import streamlit as st
import pandas as pd
import joblib
import numpy as np
import mysql.connector
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(
    page_title="EngageSense Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Google+Sans:wght@400;500;700&family=Roboto:wght@300;400;500;700&display=swap');
    
    * {
        font-family: 'Google Sans', 'Roboto', Arial, sans-serif;
    }
    
    .stApp {
        background: #ffffff;
    }
    
    .block-container {
        padding: 0 !important;
        max-width: 100% !important;
    }
    
    /* Top Navigation Bar */
    .top-nav {
        background: #ffffff;
        padding: 0.75rem 2rem;
        border-bottom: 1px solid #e8eaed;
        display: flex;
        align-items: center;
        justify-content: space-between;
        position: sticky;
        top: 0;
        z-index: 1000;
        box-shadow: 0 1px 2px rgba(0,0,0,0.1);
    }
    
    .logo-section {
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    
    .logo-icon {
        width: 44px;
        height: 44px;
        background: linear-gradient(135deg, #f4b400 0%, #ffa726 100%);
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        font-weight: 700;
        color: white;
        box-shadow: 0 3px 6px rgba(244, 180, 0, 0.3);
    }
    
    .logo-text {
        font-size: 1.25rem;
        font-weight: 600;
        color: #202124;
    }
    
    .nav-links {
        display: flex;
        gap: 2rem;
        align-items: center;
    }
    
    .nav-link {
        color: #5f6368;
        font-size: 0.9rem;
        font-weight: 500;
        cursor: pointer;
        transition: color 0.2s ease;
    }
    
    .nav-link:hover {
        color: #f4b400;
    }
    
    .user-section {
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    
    .nav-btn {
        padding: 0.5rem 1rem;
        background: white;
        border: 1px solid #dadce0;
        border-radius: 20px;
        color: #5f6368;
        font-size: 0.875rem;
        font-weight: 500;
        cursor: pointer;
    }
    
    .nav-btn.primary {
        background: #f4b400;
        color: white;
        border-color: #f4b400;
    }
    
    .user-avatar {
        width: 36px;
        height: 36px;
        background: linear-gradient(135deg, #f4b400, #ff9800);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: 600;
        font-size: 0.875rem;
    }
    
    /* Hero Banner - Yellow/Golden */
    .hero-banner {
        background: linear-gradient(135deg, #f4b400 0%, #ffa726 50%, #ff9800 100%);
        padding: 3rem 2rem;
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    
    .hero-banner::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: 
            radial-gradient(circle at 20% 50%, rgba(255,255,255,0.1) 0%, transparent 50%),
            radial-gradient(circle at 80% 50%, rgba(255,255,255,0.1) 0%, transparent 50%);
    }
    
    .hero-content {
        position: relative;
        z-index: 1;
    }
    
    .hero-stats {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1a1a1a;
        margin-bottom: 0.5rem;
    }
    
    .hero-label {
        font-size: 1rem;
        color: #1a1a1a;
        opacity: 0.8;
        margin-bottom: 2rem;
    }
    
    .hero-title {
        font-size: 3rem;
        font-weight: 700;
        color: #1a1a1a;
        margin-bottom: 1rem;
    }
    
    .hero-author {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 1rem;
        margin-top: 2rem;
    }
    
    .author-avatar {
        width: 48px;
        height: 48px;
        background: white;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        color: #f4b400;
    }
    
    .author-info {
        text-align: left;
    }
    
    .author-name {
        font-weight: 600;
        color: #1a1a1a;
    }
    
    .author-date {
        font-size: 0.875rem;
        color: #1a1a1a;
        opacity: 0.7;
    }
    
    /* Content Layout with Sidebar */
    .content-wrapper {
        display: flex;
        max-width: 1400px;
        margin: 0 auto;
        padding: 2rem;
        gap: 2rem;
    }
    
    /* Left Sidebar TOC */
    .toc-sidebar {
        width: 280px;
        flex-shrink: 0;
        position: sticky;
        top: 100px;
        height: fit-content;
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    
    .toc-title {
        font-size: 1.125rem;
        font-weight: 600;
        color: #202124;
        margin-bottom: 1rem;
        padding-bottom: 0.75rem;
        border-bottom: 2px solid #e8eaed;
    }
    
    .toc-item {
        padding: 0.75rem 0;
        color: #5f6368;
        font-size: 0.9rem;
        cursor: pointer;
        border-left: 3px solid transparent;
        padding-left: 1rem;
        margin-left: -1rem;
        transition: all 0.2s ease;
    }
    
    .toc-item:hover {
        color: #f4b400;
        border-left-color: #f4b400;
        background: rgba(244, 180, 0, 0.05);
    }
    
    .toc-item.active {
        color: #f4b400;
        border-left-color: #f4b400;
        font-weight: 600;
        background: rgba(244, 180, 0, 0.05);
    }
    
    /* Main Content Area */
    .main-content {
        flex: 1;
        min-width: 0;
    }
    
    /* Section Headers */
    h2 {
        color: #202124 !important;
        font-weight: 600 !important;
        font-size: 1.75rem !important;
        margin: 2rem 0 1.5rem 0 !important;
        padding-bottom: 0.75rem;
        border-bottom: 2px solid #f4b400;
    }
    
    /* Metric Cards */
    [data-testid="stMetric"] {
        background: white;
        border: 1px solid #e8eaed;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
    }
    
    [data-testid="stMetric"]:hover {
        transform: translateY(-4px);
        box-shadow: 0 4px 12px rgba(244, 180, 0, 0.15);
        border-color: #f4b400;
    }
    
    [data-testid="stMetric"] label {
        color: #5f6368 !important;
        font-size: 0.875rem !important;
        font-weight: 500 !important;
    }
    
    [data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: #202124 !important;
        font-size: 2rem !important;
        font-weight: 600 !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        background: white;
        border-bottom: 2px solid #e8eaed;
        padding: 0;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: #5f6368;
        border-bottom: 3px solid transparent;
        padding: 1rem 1.5rem;
        font-weight: 500;
    }
    
    .stTabs [aria-selected="true"] {
        color: #f4b400 !important;
        border-bottom-color: #f4b400 !important;
    }
    
    /* Sidebar Filters */
    [data-testid="stSidebar"] {
        background: white;
        border-right: 1px solid #e8eaed;
    }
    
    [data-testid="stSidebar"] h3 {
        color: #202124 !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
    }
    
    /* Data Table */
    .stDataFrame {
        border: 1px solid #e8eaed;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    /* Download Button */
    .stDownloadButton button {
        background: #f4b400 !important;
        color: white !important;
        border: none !important;
        border-radius: 24px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 600 !important;
        transition: all 0.2s ease !important;
    }
    
    .stDownloadButton button:hover {
        background: #ff9800 !important;
        box-shadow: 0 4px 12px rgba(244, 180, 0, 0.3) !important;
    }
    
    /* Footer */
    .custom-footer {
        background: #f8f9fa;
        padding: 3rem 2rem;
        margin-top: 4rem;
        border-top: 1px solid #e8eaed;
        text-align: center;
    }
    
    .footer-title {
        font-size: 1.25rem;
        font-weight: 600;
        color: #202124;
        margin-bottom: 0.75rem;
    }
    
    .footer-text {
        color: #5f6368;
        font-size: 0.875rem;
        margin: 0.25rem 0;
    }
    
    .creator-highlight {
        color: #f4b400;
        font-weight: 600;
    }
    
    #MainMenu, footer, header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# Top Navigation
st.markdown("""
    <div class="top-nav">
        <div class="logo-section">
            <div class="logo-icon">ES</div>
            <div class="logo-text">EngageSense</div>
        </div>
        <div class="nav-links">
            <div class="nav-link">Dashboard</div>
            <div class="nav-link">Analytics</div>
            <div class="nav-link">Reports</div>
            <div class="nav-link">Settings</div>
        </div>
        <div class="user-section">
            <button class="nav-btn">Help</button>
            <button class="nav-btn primary">Export</button>
            <div class="user-avatar">SM</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# Hero Banner
total_students = 40  # Will be dynamic
st.markdown(f"""
    <div class="hero-banner">
        <div class="hero-content">
            <div class="hero-stats">{total_students:,}</div>
            <div class="hero-label">Active Students</div>
            <div class="hero-title">EngageSense Analytics Platform</div>
            <div class="hero-author">
                <div class="author-avatar">SM</div>
                <div class="author-info">
                    <div class="author-name">Suraj Maurya</div>
                    <div class="author-date">Updated {datetime.now().strftime('%b %d, %Y')}</div>
                </div>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# Content Wrapper Start
st.markdown('<div class="content-wrapper">', unsafe_allow_html=True)

# Left Sidebar TOC
st.markdown("""
    <div class="toc-sidebar">
        <div class="toc-title">Table of Contents</div>
        <div class="toc-item active">Overview Dashboard</div>
        <div class="toc-item">Student Analytics</div>
        <div class="toc-item">Engagement Distribution</div>
        <div class="toc-item">Anomaly Detection</div>
        <div class="toc-item">Top Performers</div>
        <div class="toc-item">Student Data Explorer</div>
        <div class="toc-item">Export & Reports</div>
    </div>
""", unsafe_allow_html=True)

# Main Content
st.markdown('<div class="main-content">', unsafe_allow_html=True)

# Sidebar Filters (Right Panel)
with st.sidebar:
    st.markdown("### Filters & Options")
    
    data_source = st.radio("Data Source", ["CSV File", "MySQL Database"])
    
    st.markdown("---")
    
    filter_status = st.selectbox("Student Status", ["All Students", "Active Only", "At Risk Only"])
    min_score = st.slider("Min Engagement Score", 0.0, 10.0, 0.0)
    search_id = st.text_input("Search Student ID", placeholder="e.g., S007")
    
    st.markdown("---")
    st.markdown("### Display Options")
    
    show_charts = st.checkbox("Show Charts", value=True)
    chart_height = st.slider("Chart Height", 300, 600, 400)
    
    st.markdown("---")
    st.info(f"📅 Last updated: {datetime.now().strftime('%B %d, %Y')}")

@st.cache_resource
def load_model():
    try:
        return joblib.load('isolation_forest.pkl')
    except:
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
    except:
        return None

model = load_model()
df = load_data_from_mysql() if data_source == "MySQL Database" else load_data_from_csv()

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
        df['anomaly_flag'] = df['anomaly'].apply(lambda x: 'At Risk' if x == -1 else 'Active')
    except:
        df['anomaly'] = 1
        df['anomaly_flag'] = 'Active'
    
    st.markdown("## Overview Dashboard")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Students", len(df), "+5")
    
    with col2:
        anomaly_count = (df['anomaly'] == -1).sum()
        st.metric("At Risk Students", anomaly_count, f"{(anomaly_count/len(df)*100):.1f}%")
    
    with col3:
        st.metric("Avg Engagement", f"{df['engagement_score'].mean():.2f}", "+0.3")
    
    with col4:
        st.metric("Avg Time (hours)", f"{df['time_spent'].mean():.1f}", "+2.3")
    
    if show_charts:
        st.markdown("## Student Analytics")
        
        tab1, tab2, tab3 = st.tabs(["📊 Distribution", "🔍 Anomaly Detection", "🏆 Top Performers"])
        
        with tab1:
            col1, col2 = st.columns(2)
            
            with col1:
                fig1 = px.histogram(df, x='engagement_score', nbins=25, title='Engagement Score Distribution')
                fig1.update_layout(plot_bgcolor='white', paper_bgcolor='white', font=dict(color='#202124'), height=chart_height, showlegend=False)
                fig1.update_traces(marker_color='#f4b400')
                st.plotly_chart(fig1, use_container_width=True)
            
            with col2:
                counts = df['anomaly_flag'].value_counts()
                fig2 = px.pie(values=counts.values, names=counts.index, title='Student Status', hole=0.4)
                fig2.update_layout(plot_bgcolor='white', paper_bgcolor='white', font=dict(color='#202124'), height=chart_height)
                fig2.update_traces(marker=dict(colors=['#4caf50', '#f44336']))
                st.plotly_chart(fig2, use_container_width=True)
        
        with tab2:
            fig3 = px.scatter(df, x='time_spent', y='engagement_score', color='anomaly_flag', size='login_count', hover_data=['student_id'], title='Time vs Engagement', color_discrete_map={'Active': '#4caf50', 'At Risk': '#f44336'})
            fig3.update_layout(plot_bgcolor='white', paper_bgcolor='white', font=dict(color='#202124'), height=chart_height)
            st.plotly_chart(fig3, use_container_width=True)
        
        with tab3:
            top_10 = df.nlargest(10, 'engagement_score')
            fig4 = px.bar(top_10, x='student_id', y='engagement_score', color='anomaly_flag', title='Top 10 Students', color_discrete_map={'Active': '#4caf50', 'At Risk': '#f44336'})
            fig4.update_layout(plot_bgcolor='white', paper_bgcolor='white', font=dict(color='#202124'), height=chart_height)
            st.plotly_chart(fig4, use_container_width=True)
    
    st.markdown("## Student Data Explorer")
    
    filtered = df.copy()
    
    if filter_status == "Active Only":
        filtered = filtered[filtered['anomaly_flag'] == 'Active']
    elif filter_status == "At Risk Only":
        filtered = filtered[filtered['anomaly_flag'] == 'At Risk']
    
    filtered = filtered[filtered['engagement_score'] >= min_score]
    
    if search_id:
        filtered = filtered[filtered['student_id'].astype(str).str.contains(search_id, case=False)]
    
    filtered = filtered.sort_values('engagement_score', ascending=False)
    
    st.info(f"📊 Showing {len(filtered)} of {len(df)} students")
    
    st.dataframe(filtered, use_container_width=True, height=400)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        csv = filtered.to_csv(index=False).encode('utf-8')
        st.download_button(
            label=f"📥 Download {len(filtered)} Records",
            data=csv,
            file_name=f'engagesense_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv',
            mime='text/csv',
            use_container_width=True
        )

else:
    st.error("❌ Failed to load data or model")

st.markdown('</div>', unsafe_allow_html=True)  # Close main-content
st.markdown('</div>', unsafe_allow_html=True)  # Close content-wrapper

# Footer
st.markdown("""
    <div class="custom-footer">
        <div class="footer-title">📊 EngageSense Analytics Platform</div>
        <div class="footer-text">Developed by <span class="creator-highlight">Suraj Maurya</span></div>
        <div class="footer-text">AI-Powered Student Engagement Monitoring · Machine Learning · Python · Streamlit</div>
        <div class="footer-text">© 2025 EngageSense. All Rights Reserved.</div>
    </div>
""", unsafe_allow_html=True)
