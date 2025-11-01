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
    
    /* Enhanced Header with Logo & User Menu */
    .ga-header {
        background: #ffffff;
        padding: 1rem 2rem;
        margin: -1.5rem -2rem 2rem -2rem;
        border-bottom: 1px solid #e8eaed;
        box-shadow: 0 1px 2px 0 rgba(60,64,67,0.3), 0 1px 3px 1px rgba(60,64,67,0.15);
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    
    .logo-container {
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    
    .logo-icon {
        width: 48px;
        height: 48px;
        background: linear-gradient(135deg, #1a73e8 0%, #4285f4 50%, #34a853 100%);
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.75rem;
        font-weight: 700;
        color: white;
        box-shadow: 0 4px 8px rgba(26, 115, 232, 0.25);
        position: relative;
        overflow: hidden;
    }
    
    .logo-icon::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(255,255,255,0.3), transparent);
        animation: shimmer 3s infinite;
    }
    
    @keyframes shimmer {
        0%, 100% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
        50% { transform: translateX(100%) translateY(100%) rotate(45deg); }
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
        margin-top: 0.125rem;
    }
    
    /* Right Side User Menu */
    .user-menu {
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    
    .action-btn {
        padding: 0.5rem 1rem;
        background: #ffffff;
        border: 1px solid #dadce0;
        border-radius: 20px;
        color: #5f6368;
        font-size: 0.875rem;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.2s ease;
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .action-btn:hover {
        background: #f8f9fa;
        border-color: #1a73e8;
        color: #1a73e8;
    }
    
    .user-avatar {
        width: 36px;
        height: 36px;
        background: linear-gradient(135deg, #1a73e8, #34a853);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: 600;
        font-size: 0.875rem;
        cursor: pointer;
    }
    
    /* Metric Cards */
    [data-testid="stMetric"] {
        background: #ffffff;
        border: 1px solid #dadce0;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 1px 2px 0 rgba(60,64,67,0.3), 0 1px 3px 1px rgba(60,64,67,0.15);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    [data-testid="stMetric"]::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
        background: linear-gradient(180deg, #1a73e8, #34a853);
    }
    
    [data-testid="stMetric"]:hover {
        transform: translateY(-4px);
        box-shadow: 0 4px 12px 0 rgba(60,64,67,0.3), 0 8px 16px 4px rgba(60,64,67,0.15);
    }
    
    [data-testid="stMetric"] label {
        color: #5f6368 !important;
        font-size: 0.875rem !important;
        font-weight: 500 !important;
        text-transform: none !important;
    }
    
    [data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: #202124 !important;
        font-size: 2.25rem !important;
        font-weight: 400 !important;
    }
    
    [data-testid="stMetric"] [data-testid="stMetricDelta"] {
        color: #34a853 !important;
        font-size: 0.875rem !important;
    }
    
    /* Section Headers */
    h2 {
        color: #202124 !important;
        font-weight: 500 !important;
        font-size: 1.5rem !important;
        margin: 2.5rem 0 1.5rem 0 !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        background: #ffffff;
        border-bottom: 1px solid #dadce0;
        padding: 0;
        border-radius: 8px 8px 0 0;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: #5f6368;
        border: none;
        border-bottom: 3px solid transparent;
        padding: 1rem 1.5rem;
        font-weight: 500;
        font-size: 0.875rem;
        transition: all 0.2s ease;
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
        font-weight: 600 !important;
        margin-top: 1.5rem !important;
    }
    
    /* Quick Actions Card */
    .quick-actions {
        background: linear-gradient(135deg, #e8f0fe 0%, #f1f8f4 100%);
        border: 1px solid #d2e3fc;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
    }
    
    .action-title {
        font-size: 0.875rem;
        font-weight: 600;
        color: #202124;
        margin-bottom: 1rem;
    }
    
    .action-item {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        padding: 0.75rem;
        background: white;
        border-radius: 8px;
        margin-bottom: 0.5rem;
        cursor: pointer;
        transition: all 0.2s ease;
        border: 1px solid transparent;
    }
    
    .action-item:hover {
        border-color: #1a73e8;
        box-shadow: 0 2px 4px rgba(26, 115, 232, 0.15);
    }
    
    .action-icon {
        font-size: 1.25rem;
    }
    
    .action-text {
        font-size: 0.875rem;
        color: #5f6368;
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
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 1px 2px 0 rgba(60,64,67,0.3);
    }
    
    /* Download Button */
    .stDownloadButton button {
        background: #1a73e8 !important;
        color: white !important;
        border: none !important;
        border-radius: 24px !important;
        padding: 0.625rem 2rem !important;
        font-weight: 500 !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 2px 4px rgba(26, 115, 232, 0.3) !important;
    }
    
    .stDownloadButton button:hover {
        background: #1765cc !important;
        box-shadow: 0 4px 8px rgba(26, 115, 232, 0.4) !important;
        transform: translateY(-2px);
    }
    
    /* Footer */
    .ga-footer {
        margin-top: 4rem;
        padding: 2.5rem;
        text-align: center;
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        border-radius: 12px;
        border: 1px solid #dadce0;
        box-shadow: 0 1px 2px 0 rgba(60,64,67,0.3);
    }
    
    .footer-title {
        font-size: 1.25rem;
        font-weight: 600;
        color: #202124;
        margin-bottom: 0.75rem;
    }
    
    .footer-text {
        color: #5f6368;
        margin: 0.25rem 0;
        font-size: 0.875rem;
    }
    
    .creator-highlight {
        color: #1a73e8;
        font-weight: 600;
    }
    
    #MainMenu, footer, header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# Enhanced Header with User Menu
st.markdown("""
    <div class="ga-header">
        <div class="logo-container">
            <div class="logo-icon">ES</div>
            <div>
                <div class="ga-title">EngageSense Analytics</div>
                <div class="ga-subtitle">AI-Powered Student Engagement Platform</div>
            </div>
        </div>
        <div class="user-menu">
            <div class="action-btn">📊 Reports</div>
            <div class="action-btn">⚙️ Settings</div>
            <div class="action-btn">🔔 Alerts</div>
            <div class="user-avatar">SM</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# Sidebar with Quick Actions
with st.sidebar:
    st.markdown("""
        <div class="quick-actions">
            <div class="action-title">⚡ Quick Actions</div>
            <div class="action-item">
                <span class="action-icon">📤</span>
                <span class="action-text">Export All Data</span>
            </div>
            <div class="action-item">
                <span class="action-icon">🔍</span>
                <span class="action-text">Generate Report</span>
            </div>
            <div class="action-item">
                <span class="action-icon">📧</span>
                <span class="action-text">Email Summary</span>
            </div>
            <div class="action-item">
                <span class="action-icon">🎯</span>
                <span class="action-text">Set Alerts</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
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
    st.info(f"📅 Last updated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}")

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
    
    st.markdown("## 📊 Overview Dashboard")
    
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
        st.markdown("## 📈 Analytics & Insights")
        
        tab1, tab2, tab3 = st.tabs(["📊 Distribution", "🔍 Anomaly Detection", "🏆 Top Performers"])
        
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
    
    st.markdown("## 📋 Student Data Explorer")
    
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
            file_name=f'engagesense_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv',
            mime='text/csv',
            use_container_width=True
        )

else:
    st.error("❌ Failed to load data or model")

st.markdown("""
    <div class="ga-footer">
        <div class="footer-title">📊 EngageSense Analytics Platform</div>
        <div class="footer-text">Developed with ❤️ by <span class="creator-highlight">Suraj Maurya</span></div>
        <div class="footer-text">Machine Learning · Python · Streamlit · Plotly · Scikit-learn</div>
        <div class="footer-text">© 2025 EngageSense. All Rights Reserved.</div>
    </div>
""", unsafe_allow_html=True)
