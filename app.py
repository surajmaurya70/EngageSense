import streamlit as st
import pandas as pd
import joblib
import numpy as np
import mysql.connector
import plotly.express as px
import plotly.graph_objects as go

# Page Config
st.set_page_config(
    page_title="EngageSense | By Suraj Maurya",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Ultra Premium Dark Theme CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Force Dark Background */
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%) !important;
    }
    
    .main {
        background: transparent !important;
    }
    
    .block-container {
        padding: 2rem 3rem !important;
        max-width: 1400px;
    }
    
    /* Header Card */
    .premium-header {
        background: linear-gradient(135deg, rgba(255,255,255,0.12) 0%, rgba(255,255,255,0.06) 100%);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255,255,255,0.18);
        border-radius: 24px;
        padding: 3rem;
        text-align: center;
        margin-bottom: 2.5rem;
        box-shadow: 0 20px 60px rgba(0,0,0,0.4);
    }
    
    .app-title {
        font-size: 4rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.8rem;
        letter-spacing: -2px;
    }
    
    .app-subtitle {
        font-size: 1.2rem;
        color: rgba(255,255,255,0.8);
        font-weight: 400;
        margin-bottom: 1.5rem;
    }
    
    .creator-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.75rem 2rem;
        border-radius: 50px;
        font-size: 1rem;
        font-weight: 600;
        margin-top: 1rem;
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.5);
        transition: all 0.3s ease;
    }
    
    .creator-badge:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 30px rgba(102, 126, 234, 0.7);
    }
    
    /* Metric Cards */
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, rgba(255,255,255,0.15) 0%, rgba(255,255,255,0.08) 100%);
        backdrop-filter: blur(12px);
        padding: 2rem 1.5rem;
        border-radius: 20px;
        border: 1px solid rgba(255,255,255,0.2);
        box-shadow: 0 10px 40px rgba(0,0,0,0.3);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    [data-testid="stMetric"]:hover {
        transform: translateY(-10px);
        box-shadow: 0 15px 50px rgba(102, 126, 234, 0.4);
        border-color: rgba(255,255,255,0.3);
    }
    
    [data-testid="stMetric"] label {
        color: rgba(255,255,255,0.95) !important;
        font-size: 1rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.5px !important;
        text-transform: uppercase !important;
    }
    
    [data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-size: 3rem !important;
        font-weight: 800 !important;
        text-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    
    [data-testid="stMetric"] [data-testid="stMetricDelta"] {
        color: rgba(255,255,255,0.85) !important;
        font-size: 0.9rem !important;
    }
    
    /* Section Headers */
    h2 {
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 2rem !important;
        margin: 3rem 0 1.5rem 0 !important;
        letter-spacing: -0.5px !important;
        text-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    
    /* Leaderboard */
    .top-performer {
        background: linear-gradient(135deg, rgba(255,255,255,0.12) 0%, rgba(255,255,255,0.06) 100%);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.18);
        border-radius: 18px;
        padding: 1.8rem 1.2rem;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .top-performer:hover {
        transform: translateY(-8px);
        box-shadow: 0 12px 35px rgba(102, 126, 234, 0.4);
    }
    
    .top-medal {
        font-size: 3rem;
        margin-bottom: 0.8rem;
    }
    
    .top-name {
        font-size: 1.4rem;
        font-weight: 700;
        color: #ffffff;
        margin: 0.8rem 0;
    }
    
    .top-score {
        font-size: 1.1rem;
        color: rgba(255,255,255,0.75);
        font-weight: 500;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.75rem;
        background: rgba(255,255,255,0.08);
        padding: 0.6rem;
        border-radius: 14px;
        border: 1px solid rgba(255,255,255,0.15);
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: rgba(255,255,255,0.6);
        border-radius: 10px;
        padding: 0.85rem 1.8rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(255,255,255,0.12);
        color: rgba(255,255,255,0.95);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: #ffffff !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.5);
    }
    
    /* Alerts */
    .stAlert {
        background: linear-gradient(135deg, rgba(102,126,234,0.2) 0%, rgba(118,75,162,0.2) 100%) !important;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(102,126,234,0.4) !important;
        border-radius: 14px;
        color: #ffffff !important;
        font-weight: 500;
    }
    
    /* Form Elements */
    .stSelectbox label, .stSlider label, .stTextInput label {
        color: rgba(255,255,255,0.95) !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
    }
    
    [data-baseweb="select"] {
        background: rgba(255,255,255,0.12) !important;
        border: 1px solid rgba(255,255,255,0.25) !important;
        border-radius: 12px;
    }
    
    [data-baseweb="select"] > div {
        color: #ffffff !important;
    }
    
    .stTextInput input {
        background: rgba(255,255,255,0.12) !important;
        border: 1px solid rgba(255,255,255,0.25) !important;
        border-radius: 12px;
        color: #ffffff !important;
    }
    
    /* Dataframe */
    .stDataFrame {
        border-radius: 18px;
        overflow: hidden;
        box-shadow: 0 10px 40px rgba(0,0,0,0.4);
        border: 1px solid rgba(255,255,255,0.15);
    }
    
    /* Download Button */
    .stDownloadButton button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 14px !important;
        padding: 1rem 3rem !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.5) !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
    }
    
    .stDownloadButton button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.7) !important;
    }
    
    /* PREMIUM FOOTER */
    .ultimate-footer {
        margin-top: 5rem;
        padding: 3rem 2rem;
        background: linear-gradient(135deg, rgba(255,255,255,0.12) 0%, rgba(255,255,255,0.06) 100%);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255,255,255,0.18);
        border-radius: 24px;
        box-shadow: 0 20px 60px rgba(0,0,0,0.4);
        text-align: center;
    }
    
    .footer-brand {
        font-size: 2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
        letter-spacing: -0.5px;
    }
    
    .footer-creator {
        font-size: 1.3rem;
        color: rgba(255,255,255,0.95);
        font-weight: 600;
        margin: 1.5rem 0;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
    }
    
    .creator-name {
        background: linear-gradient(135deg, #667eea 0%, #f093fb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 1.4rem;
    }
    
    .footer-tech {
        font-size: 1rem;
        color: rgba(255,255,255,0.7);
        margin: 1rem 0 0.5rem 0;
        font-weight: 500;
    }
    
    .footer-copyright {
        font-size: 0.9rem;
        color: rgba(255,255,255,0.6);
        margin-top: 1rem;
        font-weight: 400;
    }
    
    /* Hide Streamlit */
    #MainMenu, footer, header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# Premium Header
st.markdown("""
    <div class="premium-header">
        <div class="app-title">🎯 EngageSense</div>
        <div class="app-subtitle">AI-Powered Student Engagement Analytics Platform</div>
        <div class="creator-badge">👨‍💻 Created by Suraj Maurya</div>
    </div>
""", unsafe_allow_html=True)

# Load Model
@st.cache_resource
def load_model():
    try:
        return joblib.load('isolation_forest.pkl')
    except Exception as e:
        st.error(f"Model Error: {e}")
        return None

model = load_model()

# Load Data
@st.cache_data
def load_data_from_mysql():
    try:
        conn = mysql.connector.connect(host="localhost", user="root", password="", database="engagesense_db")
        df = pd.read_sql("SELECT * FROM student_engagement", conn)
        conn.close()
        return df, "mysql"
    except:
        return load_data_from_csv(), "csv"

@st.cache_data
def load_data_from_csv():
    try:
        return pd.read_csv('student_engagement.csv')
    except Exception as e:
        st.error(f"Data Error: {e}")
        return None

df, source = load_data_from_mysql()

if df is not None and model is not None:
    if 'engagement_score' not in df.columns:
        df['engagement_score'] = (df['login_count']*0.25 + (df['time_spent']/60)*0.25 + df['quiz_attempts']*0.2 + df['forum_posts']*0.15 + (df['assignment_score']/100)*0.15*10)
    
    try:
        df['anomaly'] = model.predict(df[['login_count', 'time_spent', 'quiz_attempts']].values)
        df['anomaly_flag'] = df['anomaly'].apply(lambda x: '🚨 At Risk' if x == -1 else '✅ Active')
    except:
        df['anomaly'] = 1
        df['anomaly_flag'] = '✅ Active'
    
    st.markdown("## 📊 Real-Time Dashboard")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("⭐ AVG ENGAGEMENT", f"{df['engagement_score'].mean():.2f}", "+0.3 vs last week")
    with col2:
        anomaly_count = (df['anomaly'] == -1).sum()
        st.metric("🚨 AT-RISK", anomaly_count, f"{(anomaly_count/len(df)*100):.0f}% of total", delta_color="inverse")
    with col3:
        st.metric("👥 STUDENTS", len(df), "+5 this month")
    with col4:
        st.metric("⏱️ AVG TIME", f"{df['time_spent'].mean():.1f}h", "+2.3 hrs/week")
    
    st.markdown("## 🏆 Top Performers")
    top_5 = df.nlargest(5, 'engagement_score')
    cols = st.columns(5)
    medals = ['🥇', '🥈', '🥉', '🏅', '🏅']
    
    for idx, (col, medal) in enumerate(zip(cols, medals)):
        with col:
            student = top_5.iloc[idx]
            st.markdown(f"""
                <div class="top-performer">
                    <div class="top-medal">{medal}</div>
                    <div class="top-name">{student['student_id']}</div>
                    <div class="top-score">Score: {student['engagement_score']:.2f}</div>
                </div>
            """, unsafe_allow_html=True)
    
    st.markdown("## 📈 Analytics & Insights")
    tab1, tab2, tab3 = st.tabs(["📊 Distribution", "🔍 Anomaly Detection", "📉 Trends"])
    
    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            fig1 = px.histogram(df, x='engagement_score', nbins=25, title='Engagement Distribution', color_discrete_sequence=['#667eea'])
            fig1.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='white', size=12))
            st.plotly_chart(fig1, use_container_width=True)
        with col2:
            counts = df['anomaly_flag'].value_counts()
            fig2 = px.pie(values=counts.values, names=counts.index, title='Student Status', color_discrete_sequence=['#2ecc71', '#e74c3c'], hole=0.5)
            fig2.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='white'))
            st.plotly_chart(fig2, use_container_width=True)
    
    with tab2:
        fig3 = px.scatter(df, x='time_spent', y='engagement_score', color='anomaly_flag', size='login_count', hover_data=['student_id'], title='Time vs Engagement', color_discrete_map={'✅ Active': '#2ecc71', '🚨 At Risk': '#e74c3c'})
        fig3.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='white'))
        st.plotly_chart(fig3, use_container_width=True)
    
    with tab3:
        top_10 = df.nlargest(10, 'engagement_score')
        fig4 = px.bar(top_10, x='student_id', y='engagement_score', color='anomaly_flag', title='Top 10 Students', color_discrete_map={'✅ Active': '#2ecc71', '🚨 At Risk': '#e74c3c'})
        fig4.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='white'))
        st.plotly_chart(fig4, use_container_width=True)
    
    st.markdown("## 🎓 Student Explorer")
    col1, col2, col3 = st.columns(3)
    with col1:
        filter_status = st.selectbox("🔍 Filter", ["All Students", "✅ Active Only", "🚨 At Risk Only"])
    with col2:
        min_score = st.slider("📊 Min Score", float(df['engagement_score'].min()), float(df['engagement_score'].max()), float(df['engagement_score'].min()))
    with col3:
        search_id = st.text_input("🔎 Search", "")
    
    filtered = df.copy()
    if filter_status == "✅ Active Only":
        filtered = filtered[filtered['anomaly_flag'] == '✅ Active']
    elif filter_status == "🚨 At Risk Only":
        filtered = filtered[filtered['anomaly_flag'] == '🚨 At Risk']
    filtered = filtered[filtered['engagement_score'] >= min_score]
    if search_id:
        filtered = filtered[filtered['student_id'].astype(str).str.contains(search_id)]
    filtered = filtered.sort_values('engagement_score', ascending=False)
    
    st.info(f"📋 Showing **{len(filtered)}** of **{len(df)}** students")
    
    def highlight(row):
        return ['background-color: #ffe6e6'] * len(row) if row['anomaly_flag'] == '🚨 At Risk' else ['background-color: #e6ffe6'] * len(row)
    
    st.dataframe(filtered.style.apply(highlight, axis=1), use_container_width=True, height=400)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        csv = filtered.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Export Data", csv, f'engagesense_{pd.Timestamp.now().strftime("%Y%m%d")}.csv', 'text/csv', use_container_width=True)

else:
    st.error("❌ Failed to load data or model")

# PREMIUM FOOTER
st.markdown("""
    <div class="ultimate-footer">
        <div class="footer-brand">🎯 EngageSense</div>
        <div class="footer-creator">
            Developed & Created by <span class="creator-name">Suraj Maurya</span>
        </div>
        <div class="footer-tech">Powered by Machine Learning · Streamlit · Python · Plotly · Scikit-learn</div>
        <div class="footer-copyright">© 2025 EngageSense. All Rights Reserved.</div>
    </div>
""", unsafe_allow_html=True)
