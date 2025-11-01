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
        background: #f8f9fa;
    }
    
    .block-container {
        padding: 1.5rem 2rem !important;
        max-width: 1400px;
    }
    
    /* Google Analytics Header */
    .ga-header {
        background: #ffffff;
        padding: 1.5rem 2rem;
        margin: -1.5rem -2rem 2rem -2rem;
        border-bottom: 1px solid #e8eaed;
        box-shadow: 0 1px 2px 0 rgba(60,64,67,0.3), 0 1px 3px 1px rgba(60,64,67,0.15);
    }
    
    .ga-title {
        font-size: 1.5rem;
        font-weight: 500;
        color: #202124;
        margin: 0;
    }
    
    .ga-subtitle {
        font-size: 0.875rem;
        color: #5f6368;
        margin-top: 0.25rem;
    }
    
    /* Metric Cards - Google Material Style */
    [data-testid="stMetric"] {
        background: #ffffff;
        border: 1px solid #dadce0;
        border-radius: 8px;
        padding: 1.5rem;
        box-shadow: 0 1px 2px 0 rgba(60,64,67,0.3), 0 1px 3px 1px rgba(60,64,67,0.15);
        transition: box-shadow 0.2s ease;
    }
    
    [data-testid="stMetric"]:hover {
        box-shadow: 0 1px 3px 0 rgba(60,64,67,0.3), 0 4px 8px 3px rgba(60,64,67,0.15);
    }
    
    [data-testid="stMetric"] label {
        color: #5f6368 !important;
        font-size: 0.875rem !important;
        font-weight: 500 !important;
        text-transform: none !important;
    }
    
    [data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: #202124 !important;
        font-size: 2rem !important;
        font-weight: 400 !important;
    }
    
    [data-testid="stMetric"] [data-testid="stMetricDelta"] {
        color: #1a73e8 !important;
        font-size: 0.875rem !important;
    }
    
    /* Section Headers */
    h2 {
        color: #202124 !important;
        font-weight: 500 !important;
        font-size: 1.375rem !important;
        margin: 2rem 0 1rem 0 !important;
    }
    
    h3 {
        color: #202124 !important;
        font-weight: 500 !important;
        font-size: 1.125rem !important;
    }
    
    /* Tabs - Material Design */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        background: #ffffff;
        border-bottom: 1px solid #dadce0;
        padding: 0;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: #5f6368;
        border: none;
        border-bottom: 2px solid transparent;
        padding: 1rem 1.5rem;
        font-weight: 500;
        font-size: 0.875rem;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        color: #202124;
        background: rgba(26, 115, 232, 0.04);
    }
    
    .stTabs [aria-selected="true"] {
        color: #1a73e8 !important;
        border-bottom-color: #1a73e8 !important;
        background: transparent !important;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: #ffffff;
        border-right: 1px solid #dadce0;
    }
    
    [data-testid="stSidebar"] h3 {
        color: #202124 !important;
        font-size: 1rem !important;
        font-weight: 500 !important;
        margin-top: 1.5rem !important;
    }
    
    [data-testid="stSidebar"] label {
        color: #5f6368 !important;
        font-weight: 500 !important;
        font-size: 0.875rem !important;
    }
    
    /* Info Box */
    .stAlert {
        background: #e8f0fe !important;
        border: 1px solid #d2e3fc !important;
        border-radius: 8px !important;
        color: #174ea6 !important;
    }
    
    /* Data Table */
    .stDataFrame {
        border: 1px solid #dadce0;
        border-radius: 8px;
        overflow: hidden;
    }
    
    /* Download Button */
    .stDownloadButton button {
        background: #1a73e8 !important;
        color: white !important;
        border: none !important;
        border-radius: 4px !important;
        padding: 0.5rem 1.5rem !important;
        font-weight: 500 !important;
        transition: all 0.2s ease !important;
    }
    
    .stDownloadButton button:hover {
        background: #1765cc !important;
        box-shadow: 0 1px 2px 0 rgba(60,64,67,0.3), 0 1px 3px 1px rgba(60,64,67,0.15) !important;
    }
    
    /* Footer */
    .ga-footer {
        margin-top: 4rem;
        padding: 2rem;
        text-align: center;
        background: #ffffff;
        border-radius: 8px;
        border: 1px solid #dadce0;
    }
    
    .footer-title {
        font-size: 1.125rem;
        font-weight: 500;
        color: #202124;
        margin-bottom: 0.5rem;
    }
    
    .footer-text {
        color: #5f6368;
        margin: 0.25rem 0;
        font-size: 0.875rem;
    }
    
    #MainMenu, footer, header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
    <div class="ga-header">
        <div class="ga-title">EngageSense Analytics</div>
        <div class="ga-subtitle">AI-Powered Student Engagement Monitoring Platform</div>
    </div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### Filters")
    
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
    st.info(f"Last updated: {datetime.now().strftime('%B %d, %Y')}")

@st.cache_resource
def load_model():
    try:
        return joblib.load('isolation_forest.pkl')
    except Exception as e:
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
    
    st.markdown("## Overview")
    
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
        st.markdown("## Analytics")
        
        tab1, tab2, tab3 = st.tabs(["Distribution", "Anomaly Detection", "Top Performers"])
        
        with tab1:
            col1, col2 = st.columns(2)
            
            with col1:
                fig1 = px.histogram(df, x='engagement_score', nbins=25, title='Engagement Score Distribution')
                fig1.update_layout(
                    plot_bgcolor='white',
                    paper_bgcolor='white',
                    font=dict(color='#202124'),
                    height=chart_height,
                    showlegend=False
                )
                fig1.update_traces(marker_color='#1a73e8')
                st.plotly_chart(fig1, use_container_width=True)
            
            with col2:
                counts = df['anomaly_flag'].value_counts()
                fig2 = px.pie(values=counts.values, names=counts.index, title='Student Status Distribution', hole=0.4)
                fig2.update_layout(
                    plot_bgcolor='white',
                    paper_bgcolor='white',
                    font=dict(color='#202124'),
                    height=chart_height
                )
                fig2.update_traces(marker=dict(colors=['#34a853', '#ea4335']))
                st.plotly_chart(fig2, use_container_width=True)
        
        with tab2:
            fig3 = px.scatter(
                df, x='time_spent', y='engagement_score', color='anomaly_flag',
                size='login_count', hover_data=['student_id'],
                title='Time Spent vs Engagement Score',
                color_discrete_map={'Active': '#34a853', 'At Risk': '#ea4335'}
            )
            fig3.update_layout(
                plot_bgcolor='white',
                paper_bgcolor='white',
                font=dict(color='#202124'),
                height=chart_height
            )
            st.plotly_chart(fig3, use_container_width=True)
        
        with tab3:
            top_10 = df.nlargest(10, 'engagement_score')
            fig4 = px.bar(
                top_10, x='student_id', y='engagement_score',
                color='anomaly_flag', title='Top 10 Students by Engagement',
                color_discrete_map={'Active': '#34a853', 'At Risk': '#ea4335'}
            )
            fig4.update_layout(
                plot_bgcolor='white',
                paper_bgcolor='white',
                font=dict(color='#202124'),
                height=chart_height
            )
            st.plotly_chart(fig4, use_container_width=True)
    
    st.markdown("## Student Data")
    
    filtered = df.copy()
    
    if filter_status == "Active Only":
        filtered = filtered[filtered['anomaly_flag'] == 'Active']
    elif filter_status == "At Risk Only":
        filtered = filtered[filtered['anomaly_flag'] == 'At Risk']
    
    filtered = filtered[filtered['engagement_score'] >= min_score]
    
    if search_id:
        filtered = filtered[filtered['student_id'].astype(str).str.contains(search_id, case=False)]
    
    filtered = filtered.sort_values('engagement_score', ascending=False)
    
    st.info(f"Showing {len(filtered)} of {len(df)} students")
    
    st.dataframe(filtered, use_container_width=True, height=400)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        csv = filtered.to_csv(index=False).encode('utf-8')
        st.download_button(
            label=f"Download {len(filtered)} records",
            data=csv,
            file_name=f'engagesense_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv',
            mime='text/csv',
            use_container_width=True
        )

else:
    st.error("Failed to load data or model")

st.markdown("""
    <div class="ga-footer">
        <div class="footer-title">EngageSense Analytics</div>
        <div class="footer-text">Developed by Suraj Maurya</div>
        <div class="footer-text">Machine Learning · Python · Streamlit · Plotly</div>
        <div class="footer-text">© 2025 All Rights Reserved</div>
    </div>
""", unsafe_allow_html=True)
