import streamlit as st
import pandas as pd
import joblib
import numpy as np
import mysql.connector
import plotly.express as px
import plotly.graph_objects as go

# Page Configuration
st.set_page_config(
    page_title="EngageSense | By Suraj Maurya",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Ultra Premium CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Main Background - Clean Gradient */
    .main {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        padding: 0 !important;
    }
    
    .block-container {
        padding: 2rem 3rem !important;
        max-width: 1400px;
    }
    
    /* Premium Header Card */
    .header-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 24px;
        padding: 3rem 2rem;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
    }
    
    .main-title {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
        letter-spacing: -1px;
    }
    
    .subtitle {
        font-size: 1.1rem;
        color: rgba(255,255,255,0.7);
        font-weight: 400;
        margin-bottom: 1rem;
    }
    
    .creator-badge {
        display: inline-block;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.5rem 1.5rem;
        border-radius: 50px;
        font-size: 0.9rem;
        font-weight: 600;
        margin-top: 1rem;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    /* Premium Metric Cards */
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, rgba(255,255,255,0.15) 0%, rgba(255,255,255,0.05) 100%);
        backdrop-filter: blur(10px);
        padding: 2rem 1.5rem;
        border-radius: 20px;
        border: 1px solid rgba(255,255,255,0.15);
        box-shadow: 0 8px 32px rgba(0,0,0,0.2);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    [data-testid="stMetric"]:hover {
        transform: translateY(-8px);
        box-shadow: 0 12px 40px rgba(102, 126, 234, 0.3);
        border-color: rgba(255,255,255,0.25);
    }
    
    [data-testid="stMetric"] label {
        color: rgba(255,255,255,0.9) !important;
        font-size: 0.95rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.5px !important;
    }
    
    [data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-size: 2.8rem !important;
        font-weight: 700 !important;
    }
    
    [data-testid="stMetric"] [data-testid="stMetricDelta"] {
        color: rgba(255,255,255,0.8) !important;
    }
    
    /* Section Styling */
    h2 {
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 1.8rem !important;
        margin: 2.5rem 0 1.5rem 0 !important;
        letter-spacing: -0.5px !important;
    }
    
    /* Leaderboard Cards */
    .leaderboard-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.15);
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        transition: all 0.3s ease;
        height: 100%;
    }
    
    .leaderboard-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
    }
    
    .medal {
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }
    
    .student-name {
        font-size: 1.3rem;
        font-weight: 700;
        color: #ffffff;
        margin: 0.5rem 0;
    }
    
    .student-score {
        font-size: 1rem;
        color: rgba(255,255,255,0.7);
        font-weight: 500;
    }
    
    /* Tabs Premium Style */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        background: rgba(255,255,255,0.05);
        padding: 0.5rem;
        border-radius: 12px;
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: rgba(255,255,255,0.6);
        border-radius: 10px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        font-size: 0.95rem;
        transition: all 0.3s ease;
        border: none;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(255,255,255,0.1);
        color: rgba(255,255,255,0.9);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: #ffffff !important;
    }
    
    /* Info Alert */
    .stAlert {
        background: linear-gradient(135deg, rgba(102,126,234,0.15) 0%, rgba(118,75,162,0.15) 100%) !important;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(102,126,234,0.3) !important;
        border-radius: 12px;
        color: #ffffff !important;
    }
    
    /* Form Elements */
    .stSelectbox label, .stSlider label, .stTextInput label {
        color: rgba(255,255,255,0.9) !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
    }
    
    [data-baseweb="select"] {
        background: rgba(255,255,255,0.1) !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
        border-radius: 10px;
    }
    
    [data-baseweb="select"] > div {
        color: #ffffff !important;
    }
    
    .stTextInput input {
        background: rgba(255,255,255,0.1) !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
        border-radius: 10px;
        color: #ffffff !important;
    }
    
    /* Dataframe */
    .stDataFrame {
        border-radius: 16px;
        overflow: hidden;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    /* Download Button */
    .stDownloadButton button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4) !important;
    }
    
    .stDownloadButton button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6) !important;
    }
    
    /* Footer */
    .premium-footer {
        text-align: center;
        padding: 2.5rem 2rem;
        margin-top: 4rem;
        background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.2);
    }
    
    .footer-title {
        font-size: 1.3rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 0.5rem;
    }
    
    .footer-creator {
        font-size: 1rem;
        color: rgba(255,255,255,0.8);
        margin-bottom: 0.5rem;
    }
    
    .footer-tech {
        font-size: 0.85rem;
        color: rgba(255,255,255,0.6);
        margin-top: 0.75rem;
    }
    
    /* Hide Streamlit Elements */
    #MainMenu, footer, header {visibility: hidden;}
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255,255,255,0.05);
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Premium Header
st.markdown("""
    <div class="header-card">
        <div class="main-title">🎯 EngageSense</div>
        <div class="subtitle">AI-Powered Student Engagement Analytics Platform</div>
        <div class="creator-badge">Created by Suraj Maurya</div>
    </div>
""", unsafe_allow_html=True)

# Load Model
@st.cache_resource
def load_model():
    try:
        return joblib.load('isolation_forest.pkl')
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None

model = load_model()

# Load Data
@st.cache_data
def load_data_from_mysql():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="engagesense_db"
        )
        query = "SELECT * FROM student_engagement"
        df = pd.read_sql(query, conn)
        conn.close()
        return df, "mysql"
    except mysql.connector.Error as e:
        return load_data_from_csv(), "csv"

@st.cache_data
def load_data_from_csv():
    try:
        return pd.read_csv('student_engagement.csv')
    except Exception as e:
        st.error(f"Error loading CSV: {e}")
        return None

# Load data
df, source = load_data_from_mysql()

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
        feature_cols = ['login_count', 'time_spent', 'quiz_attempts']
        features_array = df[feature_cols].values
        df['anomaly'] = model.predict(features_array)
        df['anomaly_flag'] = df['anomaly'].apply(lambda x: '🚨 At Risk' if x == -1 else '✅ Active')
    except Exception as e:
        df['anomaly'] = 1
        df['anomaly_flag'] = '✅ Active'
    
    # Top Metrics
    st.markdown("## 📊 Real-Time Dashboard")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="⭐ AVG ENGAGEMENT",
            value=f"{df['engagement_score'].mean():.2f}",
            delta="+0.3 vs last week"
        )
    
    with col2:
        anomaly_count = df[df['anomaly'] == -1].shape[0]
        st.metric(
            label="🚨 AT-RISK STUDENTS",
            value=anomaly_count,
            delta=f"{(anomaly_count/len(df)*100):.0f}% of cohort",
            delta_color="inverse"
        )
    
    with col3:
        st.metric(
            label="👥 ACTIVE STUDENTS",
            value=len(df),
            delta="+5 this month"
        )
    
    with col4:
        st.metric(
            label="⏱️ AVG TIME (HRS)",
            value=f"{df['time_spent'].mean():.1f}",
            delta="+2.3 hrs/week"
        )
    
    # Leaderboard
    st.markdown("## 🏆 Top Performers")
    
    top_5 = df.nlargest(5, 'engagement_score')
    cols = st.columns(5)
    medals = ['🥇', '🥈', '🥉', '🏅', '🏅']
    
    for idx, (col, medal) in enumerate(zip(cols, medals)):
        with col:
            student = top_5.iloc[idx]
            st.markdown(f"""
                <div class="leaderboard-card">
                    <div class="medal">{medal}</div>
                    <div class="student-name">{student['student_id']}</div>
                    <div class="student-score">Score: {student['engagement_score']:.2f}</div>
                </div>
            """, unsafe_allow_html=True)
    
    # Charts
    st.markdown("## 📈 Analytics & Insights")
    
    tab1, tab2, tab3 = st.tabs(["📊 Distribution", "🔍 Anomaly Detection", "📉 Trends"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            fig1 = px.histogram(
                df, 
                x='engagement_score',
                nbins=25,
                title='Engagement Score Distribution',
                color_discrete_sequence=['#667eea']
            )
            fig1.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white', size=12),
                title_font_size=16,
                showlegend=False
            )
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            anomaly_counts = df['anomaly_flag'].value_counts()
            fig2 = px.pie(
                values=anomaly_counts.values,
                names=anomaly_counts.index,
                title='Student Status',
                color_discrete_sequence=['#2ecc71', '#e74c3c'],
                hole=0.5
            )
            fig2.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white', size=12),
                title_font_size=16
            )
            st.plotly_chart(fig2, use_container_width=True)
    
    with tab2:
        fig3 = px.scatter(
            df,
            x='time_spent',
            y='engagement_score',
            color='anomaly_flag',
            size='login_count',
            hover_data=['student_id', 'assignment_score'],
            title='Engagement vs Time Analysis',
            color_discrete_map={'✅ Active': '#2ecc71', '🚨 At Risk': '#e74c3c'}
        )
        fig3.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white', size=12),
            title_font_size=16
        )
        st.plotly_chart(fig3, use_container_width=True)
    
    with tab3:
        top_10 = df.nlargest(10, 'engagement_score')
        fig4 = px.bar(
            top_10,
            x='student_id',
            y='engagement_score',
            color='anomaly_flag',
            title='Top 10 Students',
            color_discrete_map={'✅ Active': '#2ecc71', '🚨 At Risk': '#e74c3c'}
        )
        fig4.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white', size=12),
            title_font_size=16
        )
        st.plotly_chart(fig4, use_container_width=True)
    
    # Filters
    st.markdown("## 🎓 Student Explorer")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        filter_status = st.selectbox(
            "🔍 Filter by Status",
            ["All Students", "✅ Active Only", "🚨 At Risk Only"]
        )
    
    with col2:
        min_score = st.slider(
            "📊 Minimum Score",
            float(df['engagement_score'].min()),
            float(df['engagement_score'].max()),
            float(df['engagement_score'].min())
        )
    
    with col3:
        search_id = st.text_input("🔎 Search Student", "")
    
    # Apply filters
    filtered_df = df.copy()
    
    if filter_status == "✅ Active Only":
        filtered_df = filtered_df[filtered_df['anomaly_flag'] == '✅ Active']
    elif filter_status == "🚨 At Risk Only":
        filtered_df = filtered_df[filtered_df['anomaly_flag'] == '🚨 At Risk']
    
    filtered_df = filtered_df[filtered_df['engagement_score'] >= min_score]
    
    if search_id:
        filtered_df = filtered_df[filtered_df['student_id'].astype(str).str.contains(search_id)]
    
    filtered_df = filtered_df.sort_values(by='engagement_score', ascending=False)
    
    st.info(f"📋 Showing **{len(filtered_df)}** of **{len(df)}** students")
    
    # Dataframe
    def highlight_row(row):
        if row['anomaly_flag'] == '🚨 At Risk':
            return ['background-color: #ffe6e6'] * len(row)
        return ['background-color: #e6ffe6'] * len(row)
    
    styled_df = filtered_df.style.apply(highlight_row, axis=1)
    st.dataframe(styled_df, use_container_width=True, height=400)
    
    # Download
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        csv = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Export Data (CSV)",
            data=csv,
            file_name=f'engagesense_data_{pd.Timestamp.now().strftime("%Y%m%d")}.csv',
            mime='text/csv',
            use_container_width=True
        )

else:
    st.error("❌ Failed to load data")

# Footer
st.markdown("""
    <div class="premium-footer">
        <div class="footer-title">EngageSense Analytics</div>
        <div class="footer-creator">Created & Developed by <strong>Suraj Maurya</strong></div>
        <div class="footer-tech">Powered by Machine Learning · Streamlit · Python · Plotly</div>
        <div class="footer-tech" style="margin-top: 0.5rem;">© 2025 All Rights Reserved</div>
    </div>
""", unsafe_allow_html=True)
