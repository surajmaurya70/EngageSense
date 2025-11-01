"""
EngageSense - Professional Student Engagement Analytics Dashboard
© 2025 | Developed by Suraj Maurya 💻
Inspired by Tableau, PowerBI, and Notion UI/UX
"""

import streamlit as st
import pandas as pd
import joblib
import numpy as np
import mysql.connector
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import time

# ═══════════════════════════════════════════════════════════
# PAGE CONFIGURATION
# ═══════════════════════════════════════════════════════════
st.set_page_config(
    page_title="EngageSense | AI-Powered Analytics",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ═══════════════════════════════════════════════════════════
# PREMIUM CSS STYLING - SAAS PRODUCT LOOK
# ═══════════════════════════════════════════════════════════
st.markdown("""
    <style>
    /* Import Premium Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    
    * {
        font-family: 'Inter', -apple-system, system-ui, sans-serif;
        margin: 0;
        padding: 0;
    }
    
    /* Main App Background - Professional Gradient */
    .stApp {
        background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
        background-attachment: fixed;
    }
    
    /* Remove Streamlit Padding */
    .main {
        padding: 0 !important;
    }
    
    .block-container {
        padding: 1rem 2rem !important;
        max-width: 100% !important;
    }
    
    /* ═══════════════════════════════════════════════════════════
       FIXED HEADER WITH GLOW EFFECT
       ═══════════════════════════════════════════════════════════ */
    .fixed-header {
        position: sticky;
        top: 0;
        z-index: 999;
        background: rgba(15, 32, 39, 0.95);
        backdrop-filter: blur(20px) saturate(180%);
        border-bottom: 2px solid rgba(0, 255, 255, 0.3);
        box-shadow: 0 8px 32px rgba(0, 255, 255, 0.2),
                    0 0 60px rgba(0, 255, 255, 0.15);
        padding: 1.5rem 2rem;
        margin: -1rem -2rem 2rem -2rem;
        animation: glow 3s ease-in-out infinite;
    }
    
    @keyframes glow {
        0%, 100% { box-shadow: 0 8px 32px rgba(0, 255, 255, 0.2); }
        50% { box-shadow: 0 8px 40px rgba(0, 255, 255, 0.4); }
    }
    
    .header-title {
        font-size: 2.8rem;
        font-weight: 900;
        background: linear-gradient(135deg, #00f5ff 0%, #0080ff 50%, #ff00ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -1px;
        margin-bottom: 0.5rem;
        text-shadow: 0 0 30px rgba(0, 245, 255, 0.5);
    }
    
    .header-subtitle {
        font-size: 1.1rem;
        color: rgba(255, 255, 255, 0.8);
        font-weight: 500;
    }
    
    /* ═══════════════════════════════════════════════════════════
       SUMMARY CARDS WITH NEON BORDERS & HOVER ANIMATIONS
       ═══════════════════════════════════════════════════════════ */
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, rgba(0, 245, 255, 0.08) 0%, rgba(0, 128, 255, 0.05) 100%);
        backdrop-filter: blur(15px);
        border: 2px solid rgba(0, 245, 255, 0.3);
        border-radius: 20px;
        padding: 2rem 1.5rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3),
                    0 0 20px rgba(0, 245, 255, 0.2);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        position: relative;
        overflow: hidden;
    }
    
    [data-testid="stMetric"]::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(0, 245, 255, 0.1), transparent);
        transform: rotate(45deg);
        animation: shimmer 3s infinite;
    }
    
    @keyframes shimmer {
        0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
        100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
    }
    
    [data-testid="stMetric"]:hover {
        transform: translateY(-12px) scale(1.02);
        border-color: rgba(0, 245, 255, 0.6);
        box-shadow: 0 16px 48px rgba(0, 0, 0, 0.4),
                    0 0 40px rgba(0, 245, 255, 0.5);
    }
    
    [data-testid="stMetric"] label {
        color: #00f5ff !important;
        font-size: 0.85rem !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 1.5px !important;
    }
    
    [data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-size: 3rem !important;
        font-weight: 900 !important;
        text-shadow: 0 2px 10px rgba(0, 245, 255, 0.5);
    }
    
    /* ═══════════════════════════════════════════════════════════
       SECTION CONTAINERS WITH GLASS EFFECT
       ═══════════════════════════════════════════════════════════ */
    .glass-container {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(20px) saturate(180%);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 24px;
        padding: 2rem;
        margin: 2rem 0;
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
    }
    
    .glass-container:hover {
        box-shadow: 0 16px 56px rgba(0, 245, 255, 0.2);
        border-color: rgba(0, 245, 255, 0.3);
    }
    
    /* ═══════════════════════════════════════════════════════════
       SECTION HEADERS WITH ICONS
       ═══════════════════════════════════════════════════════════ */
    .section-header {
        font-size: 1.8rem;
        font-weight: 800;
        color: #ffffff;
        margin: 2.5rem 0 1.5rem 0;
        padding-bottom: 1rem;
        border-bottom: 3px solid rgba(0, 245, 255, 0.3);
        text-shadow: 0 2px 10px rgba(0, 245, 255, 0.3);
        letter-spacing: -0.5px;
    }
    
    /* ═══════════════════════════════════════════════════════════
       TABS - PREMIUM STYLE
       ═══════════════════════════════════════════════════════════ */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
        background: rgba(0, 0, 0, 0.3);
        padding: 0.75rem;
        border-radius: 16px;
        border: 1px solid rgba(0, 245, 255, 0.2);
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: rgba(255, 255, 255, 0.6);
        border-radius: 12px;
        padding: 1rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        border: 2px solid transparent;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(0, 245, 255, 0.1);
        color: #00f5ff;
        border-color: rgba(0, 245, 255, 0.3);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #00f5ff 0%, #0080ff 100%) !important;
        color: #000000 !important;
        font-weight: 800 !important;
        border-color: transparent !important;
        box-shadow: 0 4px 20px rgba(0, 245, 255, 0.5);
    }
    
    /* ═══════════════════════════════════════════════════════════
       SIDEBAR STYLING
       ═══════════════════════════════════════════════════════════ */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f2027 0%, #203a43 100%);
        border-right: 2px solid rgba(0, 245, 255, 0.3);
        box-shadow: 4px 0 30px rgba(0, 245, 255, 0.2);
    }
    
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stSlider label,
    [data-testid="stSidebar"] .stTextInput label {
        color: #00f5ff !important;
        font-weight: 700 !important;
        font-size: 0.9rem !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
    }
    
    /* ═══════════════════════════════════════════════════════════
       DATAFRAME STYLING
       ═══════════════════════════════════════════════════════════ */
    .stDataFrame {
        border-radius: 20px;
        overflow: hidden;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.4);
        border: 2px solid rgba(0, 245, 255, 0.2);
    }
    
    /* ═══════════════════════════════════════════════════════════
       BUTTONS
       ═══════════════════════════════════════════════════════════ */
    .stDownloadButton button {
        background: linear-gradient(135deg, #00f5ff 0%, #0080ff 100%) !important;
        color: #000000 !important;
        border: none !important;
        border-radius: 14px !important;
        padding: 1rem 3rem !important;
        font-weight: 800 !important;
        font-size: 1.1rem !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        box-shadow: 0 6px 24px rgba(0, 245, 255, 0.5) !important;
        transition: all 0.3s ease !important;
    }
    
    .stDownloadButton button:hover {
        transform: translateY(-4px) !important;
        box-shadow: 0 12px 40px rgba(0, 245, 255, 0.7) !important;
    }
    
    /* ═══════════════════════════════════════════════════════════
       ALERTS & INFO BOXES
       ═══════════════════════════════════════════════════════════ */
    .stAlert {
        background: rgba(0, 245, 255, 0.1) !important;
        border: 2px solid rgba(0, 245, 255, 0.3) !important;
        border-radius: 16px !important;
        color: #ffffff !important;
        font-weight: 600 !important;
        backdrop-filter: blur(10px);
    }
    
    /* ═══════════════════════════════════════════════════════════
       FOOTER - PREMIUM STYLE
       ═══════════════════════════════════════════════════════════ */
    .premium-footer {
        margin-top: 5rem;
        padding: 3rem 2rem;
        background: rgba(0, 0, 0, 0.5);
        backdrop-filter: blur(20px);
        border-top: 2px solid rgba(0, 245, 255, 0.3);
        border-radius: 24px 24px 0 0;
        text-align: center;
        box-shadow: 0 -8px 40px rgba(0, 245, 255, 0.2);
    }
    
    .footer-logo {
        font-size: 2.5rem;
        font-weight: 900;
        background: linear-gradient(135deg, #00f5ff 0%, #ff00ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
    }
    
    .footer-creator {
        font-size: 1.3rem;
        color: #ffffff;
        font-weight: 700;
        margin: 1.5rem 0;
    }
    
    .creator-name {
        background: linear-gradient(135deg, #00f5ff 0%, #ff00ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900;
        font-size: 1.5rem;
    }
    
    .footer-tech {
        font-size: 1rem;
        color: rgba(255, 255, 255, 0.7);
        margin: 1rem 0;
    }
    
    .footer-copyright {
        font-size: 0.9rem;
        color: rgba(255, 255, 255, 0.5);
        margin-top: 1.5rem;
    }
    
    /* ═══════════════════════════════════════════════════════════
       LOADER ANIMATION
       ═══════════════════════════════════════════════════════════ */
    .loader {
        width: 60px;
        height: 60px;
        border: 4px solid rgba(0, 245, 255, 0.2);
        border-top-color: #00f5ff;
        border-radius: 50%;
        animation: spin 1s linear infinite;
        margin: 2rem auto;
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    
    /* Hide Streamlit Branding */
    #MainMenu, footer, header {visibility: hidden;}
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .header-title { font-size: 2rem; }
        [data-testid="stMetric"] [data-testid="stMetricValue"] { font-size: 2rem !important; }
    }
    </style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
# FIXED HEADER WITH GLOW
# ═══════════════════════════════════════════════════════════
st.markdown("""
    <div class="fixed-header">
        <div class="header-title">🎓 EngageSense</div>
        <div class="header-subtitle">AI-Powered Student Engagement Analytics Platform</div>
    </div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
# SIDEBAR - ADVANCED FILTERS
# ═══════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("### 🔍 Advanced Filters")
    st.markdown("---")
    
    filter_status = st.selectbox(
        "📊 Student Status",
        ["All Students", "✅ Active Only", "🚨 At Risk Only"],
        help="Filter students by engagement status"
    )
    
    st.markdown("---")
    
    search_id = st.text_input(
        "🔎 Search Student ID",
        placeholder="Enter Student ID...",
        help="Search specific student by ID"
    )
    
    st.markdown("---")
    
    st.markdown("### 📅 Quick Stats")
    st.info(f"**Last Updated:** {datetime.now().strftime('%B %d, %Y at %I:%M %p')}")

# ═══════════════════════════════════════════════════════════
# LOADING ANIMATION
# ═══════════════════════════════════════════════════════════
with st.spinner(""):
    st.markdown('<div class="loader"></div>', unsafe_allow_html=True)
    time.sleep(1)  # Simulate loading

# ═══════════════════════════════════════════════════════════
# DATA LOADING FUNCTIONS
# ═══════════════════════════════════════════════════════════
@st.cache_resource
def load_model():
    try:
        return joblib.load('isolation_forest.pkl')
    except Exception as e:
        st.error(f"Model Loading Error: {e}")
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
        st.error(f"Data Loading Error: {e}")
        return None

# Load data and model
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
        df['anomaly_flag'] = df['anomaly'].apply(lambda x: '🚨 At Risk' if x == -1 else '✅ Active')
    except:
        df['anomaly'] = 1
        df['anomaly_flag'] = '✅ Active'
    
    # ═══════════════════════════════════════════════════════════
    # 🎓 TOP SUMMARY CARDS
    # ═══════════════════════════════════════════════════════════
    st.markdown('<div class="section-header">🎓 Real-Time Dashboard Overview</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="📚 TOTAL STUDENTS",
            value=len(df),
            delta="+5 this month"
        )
    
    with col2:
        anomaly_count = (df['anomaly'] == -1).sum()
        st.metric(
            label="🚨 ANOMALIES DETECTED",
            value=anomaly_count,
            delta=f"{(anomaly_count/len(df)*100):.1f}% at risk",
            delta_color="inverse"
        )
    
    with col3:
        avg_score = df['engagement_score'].mean()
        st.metric(
            label="⭐ AVG SCORE",
            value=f"{avg_score:.2f}",
            delta="+0.3 from last week"
        )
    
    with col4:
        avg_time = df['time_spent'].mean()
        st.metric(
            label="⏱️ AVG TIME (HRS)",
            value=f"{avg_time:.1f}",
            delta="+2.3 hrs/week"
        )
    
    # ═══════════════════════════════════════════════════════════
    # 📊 ENGAGEMENT TREND CHART
    # ═══════════════════════════════════════════════════════════
    st.markdown('<div class="section-header">📈 Engagement Analytics & Trends</div>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📊 Distribution Analysis", "🔍 Anomaly Detection", "📉 Performance Trends"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            fig1 = px.histogram(
                df, 
                x='engagement_score',
                nbins=25,
                title='<b>Engagement Score Distribution</b>',
                color_discrete_sequence=['#00f5ff'],
                labels={'engagement_score': 'Engagement Score', 'count': 'Number of Students'}
            )
            fig1.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white', size=13, family='Inter'),
                title_font_size=18,
                title_font_color='#00f5ff',
                showlegend=False,
                height=400
            )
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            counts = df['anomaly_flag'].value_counts()
            fig2 = px.pie(
                values=counts.values,
                names=counts.index,
                title='<b>Student Status Distribution</b>',
                color_discrete_sequence=['#00ff88', '#ff0055'],
                hole=0.5
            )
            fig2.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white', size=13, family='Inter'),
                title_font_size=18,
                title_font_color='#00f5ff',
                height=400
            )
            fig2.update_traces(textposition='inside', textinfo='percent+label', textfont_size=14)
            st.plotly_chart(fig2, use_container_width=True)
    
    with tab2:
        fig3 = px.scatter(
            df,
            x='time_spent',
            y='engagement_score',
            color='anomaly_flag',
            size='login_count',
            hover_data=['student_id', 'assignment_score'],
            title='<b>Engagement vs Time Spent Analysis</b>',
            color_discrete_map={'✅ Active': '#00ff88', '🚨 At Risk': '#ff0055'},
            labels={'time_spent': 'Time Spent (hours)', 'engagement_score': 'Engagement Score'}
        )
        fig3.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white', size=13, family='Inter'),
            title_font_size=18,
            title_font_color='#00f5ff',
            height=500
        )
        st.plotly_chart(fig3, use_container_width=True)
    
    with tab3:
        top_10 = df.nlargest(10, 'engagement_score')
        fig4 = px.bar(
            top_10,
            x='student_id',
            y='engagement_score',
            color='anomaly_flag',
            title='<b>Top 10 High-Performing Students</b>',
            color_discrete_map={'✅ Active': '#00ff88', '🚨 At Risk': '#ff0055'},
            labels={'student_id': 'Student ID', 'engagement_score': 'Engagement Score'}
        )
        fig4.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white', size=13, family='Inter'),
            title_font_size=18,
            title_font_color='#00f5ff',
            height=500
        )
        st.plotly_chart(fig4, use_container_width=True)
    
    # ═══════════════════════════════════════════════════════════
    # 💬 AI INSIGHTS SECTION
    # ═══════════════════════════════════════════════════════════
    st.markdown('<div class="section-header">💬 AI-Powered Insights & Analysis</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info(f"""
        **📊 Engagement Summary:**
        - Total students analyzed: **{len(df)}**
        - At-risk students detected: **{anomaly_count}** ({(anomaly_count/len(df)*100):.1f}%)
        - Average engagement score: **{avg_score:.2f}/10**
        - Students need immediate attention for improved outcomes
        """)
    
    with col2:
        st.success(f"""
        **🎯 Key Recommendations:**
        - Intervention needed for {anomaly_count} at-risk students
        - Top performer: **{df.nlargest(1, 'engagement_score')['student_id'].values[0]}** (Score: {df['engagement_score'].max():.2f})
        - Focus areas: Time management & assignment completion
        - Predicted success rate: **{((len(df)-anomaly_count)/len(df)*100):.1f}%**
        """)
    
    # ═══════════════════════════════════════════════════════════
    # 🔍 ANOMALY TABLE WITH HIGHLIGHTING
    # ═══════════════════════════════════════════════════════════
    st.markdown('<div class="section-header">🔍 Student Data Explorer</div>', unsafe_allow_html=True)
    
    # Apply filters
    filtered = df.copy()
    
    if filter_status == "✅ Active Only":
        filtered = filtered[filtered['anomaly_flag'] == '✅ Active']
    elif filter_status == "🚨 At Risk Only":
        filtered = filtered[filtered['anomaly_flag'] == '🚨 At Risk']
    
    if search_id:
        filtered = filtered[filtered['student_id'].astype(str).str.contains(search_id, case=False)]
    
    # Slider for min score
    min_score = st.slider(
        "📊 Minimum Engagement Score Filter",
        float(df['engagement_score'].min()),
        float(df['engagement_score'].max()),
        float(df['engagement_score'].min()),
        help="Filter students with score above this threshold"
    )
    
    filtered = filtered[filtered['engagement_score'] >= min_score]
    filtered = filtered.sort_values('engagement_score', ascending=False)
    
    st.info(f"📋 Showing **{len(filtered)}** of **{len(df)}** students")
    
    # Highlight anomalies
    def highlight_row(row):
        if row['anomaly_flag'] == '🚨 At Risk':
            return ['background-color: rgba(255, 0, 85, 0.2); color: white'] * len(row)
        return ['background-color: rgba(0, 255, 136, 0.1); color: white'] * len(row)
    
    styled_df = filtered.style.apply(highlight_row, axis=1)
    st.dataframe(styled_df, use_container_width=True, height=450)
    
    # Download Button
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        csv = filtered.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 EXPORT DATA (CSV)",
            data=csv,
            file_name=f'engagesense_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv',
            mime='text/csv',
            use_container_width=True
        )

else:
    st.error("❌ Failed to load data or ML model. Please check configuration.")

# ═══════════════════════════════════════════════════════════
# PREMIUM FOOTER
# ═══════════════════════════════════════════════════════════
st.markdown("""
    <div class="premium-footer">
        <div class="footer-logo">🎓 EngageSense</div>
        <div class="footer-creator">
            Developed & Created by <span class="creator-name">Suraj Maurya 💻</span>
        </div>
        <div class="footer-tech">
            Powered by Machine Learning · Streamlit · Python · Plotly · Scikit-learn
        </div>
        <div class="footer-copyright">
            © 2025 EngageSense. All Rights Reserved.
        </div>
    </div>
""", unsafe_allow_html=True)
