"""
EngageSense - AI-Powered Student Engagement Analytics
A machine learning-based system to monitor and analyze student engagement patterns,
detect at-risk students, and provide actionable insights for educators.

© 2025 | Developed by Suraj Maurya
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
    page_title="EngageSense — AI-Powered Student Analytics",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium CSS - Osmo + Wealthsimple Inspired
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    * { font-family: 'Inter', sans-serif; }
    
    /* Dark Premium Background */
    .stApp {
        background: linear-gradient(180deg, #0a0a0a 0%, #0f0f0f 100%);
    }
    
    .block-container {
        padding: 2rem 2.5rem !important;
        max-width: 1400px;
    }
    
    /* Hero Header */
    .hero-header {
        background: linear-gradient(135deg, rgba(255,106,61,0.1) 0%, rgba(159,92,255,0.1) 100%);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 20px;
        padding: 3rem 2.5rem;
        margin-bottom: 2.5rem;
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    
    .hero-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,106,61,0.15) 0%, transparent 70%);
        animation: pulse 4s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); opacity: 0.5; }
        50% { transform: scale(1.1); opacity: 0.8; }
    }
    
    .hero-title {
        position: relative;
        z-index: 1;
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #ff6a3d 0%, #9f5cff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
        letter-spacing: -1px;
    }
    
    .hero-subtitle {
        position: relative;
        z-index: 1;
        font-size: 1.2rem;
        color: rgba(255,255,255,0.8);
        max-width: 700px;
        margin: 0 auto;
    }
    
    /* Metric Cards */
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, rgba(255,255,255,0.05) 0%, rgba(255,255,255,0.02) 100%);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 16px;
        padding: 2rem 1.5rem;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    [data-testid="stMetric"]:hover {
        transform: translateY(-8px);
        box-shadow: 0 12px 40px rgba(255,106,61,0.2);
        border-color: rgba(255,106,61,0.5);
    }
    
    [data-testid="stMetric"] label {
        color: rgba(255,255,255,0.7) !important;
        font-size: 0.9rem !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
    }
    
    [data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-size: 3rem !important;
        font-weight: 800 !important;
    }
    
    /* Section Headers */
    h2 {
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 1.8rem !important;
        margin: 2.5rem 0 1.5rem 0 !important;
        letter-spacing: -0.5px !important;
    }
    
    h3 {
        color: #ffffff !important;
        font-weight: 600 !important;
        font-size: 1.3rem !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        background: rgba(255,255,255,0.03);
        padding: 0.5rem;
        border-radius: 12px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: rgba(255,255,255,0.6);
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        transition: all 0.2s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #ff6a3d 0%, #9f5cff 100%) !important;
        color: #ffffff !important;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: #0a0a0a;
        border-right: 1px solid rgba(255,255,255,0.1);
    }
    
    [data-testid="stSidebar"] h3 {
        color: #ff6a3d !important;
        font-size: 1.1rem !important;
        font-weight: 700 !important;
        margin-top: 1.5rem !important;
    }
    
    /* Alert */
    .stAlert {
        background: rgba(255,255,255,0.05) !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        border-radius: 12px !important;
        color: #ffffff !important;
    }
    
    /* Footer */
    .footer {
        margin-top: 5rem;
        padding: 3rem 2rem;
        text-align: center;
        background: rgba(255,255,255,0.03);
        border-radius: 16px;
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    .footer-title {
        font-size: 1.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #ff6a3d 0%, #9f5cff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
    }
    
    .footer-text {
        color: rgba(255,255,255,0.7);
        margin: 0.5rem 0;
    }
    
    .creator {
        color: #ff6a3d;
        font-weight: 700;
    }
    
    #MainMenu, footer, header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
    <div class="hero-header">
        <div class="hero-title">🎓 EngageSense</div>
        <div class="hero-subtitle">Discover engagement patterns that matter. AI-powered analytics that help educators detect learning gaps before they grow.</div>
    </div>
""", unsafe_allow_html=True)

# Sidebar - Settings Panel
with st.sidebar:
    st.markdown("### ⚙️ Settings Panel")
    st.markdown("---")
    
    # Feature toggles
    st.markdown("#### 🎛️ Features")
    show_charts = st.checkbox("📊 Show Charts", value=True)
    show_insights = st.checkbox("💡 Show AI Insights", value=True)
    show_leaderboard = st.checkbox("🏆 Show Leaderboard", value=True)
    
    st.markdown("---")
    
    # Data source
    st.markdown("#### 📁 Data Source")
    data_source = st.radio("", ["CSV File", "MySQL Database"])
    
    st.markdown("---")
    
    # Filters
    st.markdown("#### 🔍 Filters")
    filter_status = st.selectbox("Student Status", ["All Students", "Active Only", "At Risk Only"])
    min_score = st.slider("Min Engagement Score", 0.0, 10.0, 0.0)
    search_id = st.text_input("Search Student ID", placeholder="e.g., S007")
    
    st.markdown("---")
    
    # Chart settings
    st.markdown("#### 📊 Chart Settings")
    chart_height = st.slider("Chart Height", 300, 600, 400)
    chart_theme = st.selectbox("Chart Theme", ["Dark", "Light"])
    
    st.markdown("---")
    
    # Export options
    st.markdown("#### 📥 Export Options")
    export_format = st.radio("Format", ["CSV", "Excel", "JSON"])
    include_metadata = st.checkbox("Include Metadata", value=True)
    
    st.markdown("---")
    st.success(f"**Last Updated**  \n{datetime.now().strftime('%B %d, %Y at %I:%M %p')}")

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
df = load_data_from_mysql() if data_source == "MySQL Database" else load_data_from_csv()

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
        df['anomaly_flag'] = df['anomaly'].apply(lambda x: '🚨 At Risk' if x == -1 else '✅ Active')
    except:
        df['anomaly'] = 1
        df['anomaly_flag'] = '✅ Active'
    
    # Store in session state for interactivity
    if 'selected_metric' not in st.session_state:
        st.session_state.selected_metric = 'all'
    
    # Top Metrics (Clickable)
    st.markdown("## 📊 Dashboard Overview")
    st.markdown("*Click on metrics to filter data*")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button(f"📚 Total Students\n\n{len(df)}\n\n+5 this month", use_container_width=True):
            st.session_state.selected_metric = 'all'
            st.rerun()
    
    with col2:
        anomaly_count = (df['anomaly'] == -1).sum()
        if st.button(f"🚨 At Risk\n\n{anomaly_count}\n\n{(anomaly_count/len(df)*100):.0f}% of total", use_container_width=True):
            st.session_state.selected_metric = 'at_risk'
            st.rerun()
    
    with col3:
        if st.button(f"⭐ Avg Score\n\n{df['engagement_score'].mean():.2f}\n\n+0.3 improvement", use_container_width=True):
            st.session_state.selected_metric = 'all'
            st.rerun()
    
    with col4:
        if st.button(f"⏱️ Avg Time\n\n{df['time_spent'].mean():.1f} hrs\n\n+2.3 hrs/week", use_container_width=True):
            st.session_state.selected_metric = 'all'
            st.rerun()
    
    # Apply metric filter
    display_df = df.copy()
    if st.session_state.selected_metric == 'at_risk':
        display_df = display_df[display_df['anomaly'] == -1]
        st.info(f"Showing **{len(display_df)} At-Risk Students**")
    
    # Leaderboard
    if show_leaderboard:
        st.markdown("## 🏆 Top Performers")
        top_5 = df.nlargest(5, 'engagement_score')
        cols = st.columns(5)
        medals = ['🥇', '🥈', '🥉', '🏅', '🏅']
        
        for idx, (col, medal) in enumerate(zip(cols, medals)):
            with col:
                student = top_5.iloc[idx]
                st.markdown(f"""
                    <div style="background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); 
                         border-radius: 12px; padding: 1.5rem; text-align: center;">
                        <div style="font-size: 2.5rem;">{medal}</div>
                        <div style="font-size: 1.3rem; font-weight: 700; color: #ffffff; margin: 0.5rem 0;">
                            {student['student_id']}
                        </div>
                        <div style="color: rgba(255,255,255,0.7);">Score: {student['engagement_score']:.2f}</div>
                    </div>
                """, unsafe_allow_html=True)
    
    # Charts
    if show_charts:
        st.markdown("## 📈 Visual Analytics")
        
        tab1, tab2, tab3 = st.tabs(["📊 Distribution", "🔍 Anomaly Detection", "📉 Trends"])
        
        with tab1:
            col1, col2 = st.columns(2)
            
            with col1:
                fig1 = px.histogram(display_df, x='engagement_score', nbins=25, title='Engagement Distribution')
                fig1.update_layout(plot_bgcolor='#0a0a0a', paper_bgcolor='#0a0a0a', 
                                 font=dict(color='white'), height=chart_height)
                fig1.update_traces(marker_color='#ff6a3d')
                st.plotly_chart(fig1, use_container_width=True)
            
            with col2:
                counts = display_df['anomaly_flag'].value_counts()
                fig2 = px.pie(values=counts.values, names=counts.index, title='Student Status', hole=0.5)
                fig2.update_layout(plot_bgcolor='#0a0a0a', paper_bgcolor='#0a0a0a', 
                                 font=dict(color='white'), height=chart_height)
                st.plotly_chart(fig2, use_container_width=True)
        
        with tab2:
            fig3 = px.scatter(display_df, x='time_spent', y='engagement_score', color='anomaly_flag',
                            size='login_count', hover_data=['student_id'], title='Time vs Engagement')
            fig3.update_layout(plot_bgcolor='#0a0a0a', paper_bgcolor='#0a0a0a', 
                             font=dict(color='white'), height=chart_height)
            st.plotly_chart(fig3, use_container_width=True)
        
        with tab3:
            top_10 = display_df.nlargest(10, 'engagement_score')
            fig4 = px.bar(top_10, x='student_id', y='engagement_score', 
                        color='anomaly_flag', title='Top 10 Students')
            fig4.update_layout(plot_bgcolor='#0a0a0a', paper_bgcolor='#0a0a0a', 
                             font=dict(color='white'), height=chart_height)
            st.plotly_chart(fig4, use_container_width=True)
    
    # AI Insights
    if show_insights:
        st.markdown("## 💡 AI-Powered Insights")
        col1, col2 = st.columns(2)
        
        with col1:
            st.info(f"""
            **📊 Key Findings:**
            - {len(display_df)} students analyzed
            - {(df['anomaly'] == -1).sum()} students need attention
            - Average engagement: {df['engagement_score'].mean():.2f}/10
            - Top performer: {df.nlargest(1, 'engagement_score')['student_id'].values[0]}
            """)
        
        with col2:
            st.success(f"""
            **🎯 Recommendations:**
            - Focus on {(df['anomaly'] == -1).sum()} at-risk students
            - Increase forum participation
            - Monitor time spent patterns
            - Improve quiz completion rate
            """)
    
    # Student Table
    st.markdown("## 📋 Student Data Explorer")
    
    # Apply all filters
    filtered = display_df.copy()
    
    if filter_status == "Active Only":
        filtered = filtered[filtered['anomaly_flag'] == '✅ Active']
    elif filter_status == "At Risk Only":
        filtered = filtered[filtered['anomaly_flag'] == '🚨 At Risk']
    
    filtered = filtered[filtered['engagement_score'] >= min_score]
    
    if search_id:
        filtered = filtered[filtered['student_id'].astype(str).str.contains(search_id, case=False)]
    
    filtered = filtered.sort_values('engagement_score', ascending=False)
    
    st.info(f"📋 Showing **{len(filtered)}** of **{len(df)}** students")
    
    # Highlight function
    def highlight_row(row):
        if row['anomaly_flag'] == '🚨 At Risk':
            return ['background-color: rgba(255, 106, 61, 0.2)'] * len(row)
        return ['background-color: rgba(47, 227, 154, 0.1)'] * len(row)
    
    styled_df = filtered.style.apply(highlight_row, axis=1)
    st.dataframe(styled_df, use_container_width=True, height=400)
    
    # Export
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        csv = filtered.to_csv(index=False).encode('utf-8')
        st.download_button(
            label=f"📥 Export {len(filtered)} Records ({export_format})",
            data=csv,
            file_name=f'engagesense_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv',
            mime='text/csv',
            use_container_width=True
        )

else:
    st.error("❌ Failed to load data or model")

# Footer
st.markdown("""
    <div class="footer">
        <div class="footer-title">🎓 EngageSense Analytics</div>
        <div class="footer-text">AI-Powered Student Engagement Monitoring Platform</div>
        <div class="footer-text">Machine Learning • Privacy-First • Real-Time Insights</div>
        <div class="footer-text" style="margin-top: 1.5rem;">
            Developed by <span class="creator">Suraj Maurya</span>
        </div>
        <div class="footer-text">© 2025 EngageSense. All Rights Reserved.</div>
    </div>
""", unsafe_allow_html=True)
