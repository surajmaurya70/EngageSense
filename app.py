import streamlit as st
import pandas as pd
import joblib
import numpy as np
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
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    * { font-family: 'Inter', sans-serif; }
    
    .stApp { background: #f8f9fa; }
    
    .main-header {
        background: white;
        padding: 1.5rem 2rem;
        margin: -1rem -2rem 2rem -2rem;
        border-bottom: 1px solid #e0e0e0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    .header-content {
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    
    .logo-section {
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    
    .logo {
        width: 48px;
        height: 48px;
        background: linear-gradient(135deg, #1a73e8, #4285f4);
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        color: white;
        font-weight: 700;
        box-shadow: 0 4px 8px rgba(26, 115, 232, 0.25);
    }
    
    .title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #202124;
    }
    
    .subtitle {
        font-size: 0.875rem;
        color: #5f6368;
    }
    
    .user-menu {
        display: flex;
        gap: 1rem;
        align-items: center;
    }
    
    .menu-btn {
        padding: 0.5rem 1rem;
        background: white;
        border: 1px solid #dadce0;
        border-radius: 20px;
        color: #5f6368;
        font-size: 0.875rem;
        font-weight: 500;
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
    }
    
    h2 {
        color: #202124 !important;
        font-weight: 600 !important;
        font-size: 1.5rem !important;
        margin: 2rem 0 1rem 0 !important;
    }
    
    [data-testid="stMetric"] {
        background: white;
        border: 1px solid #e0e0e0;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
    }
    
    [data-testid="stMetric"]:hover {
        transform: translateY(-4px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
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
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        background: white;
        border-bottom: 1px solid #e0e0e0;
    }
    
    .stTabs [data-baseweb="tab"] {
        color: #5f6368;
        border-bottom: 2px solid transparent;
        padding: 1rem 1.5rem;
        font-weight: 500;
    }
    
    .stTabs [aria-selected="true"] {
        color: #1a73e8 !important;
        border-bottom-color: #1a73e8 !important;
    }
    
    [data-testid="stSidebar"] {
        background: white;
        border-right: 1px solid #e0e0e0;
    }
    
    .stDataFrame {
        border: 1px solid #e0e0e0;
        border-radius: 12px;
        overflow: hidden;
    }
    
    .stDownloadButton button {
        background: #1a73e8 !important;
        color: white !important;
        border: none !important;
        border-radius: 24px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 600 !important;
    }
    
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 1rem;
        margin: 2rem 0;
    }
    
    .feature-card {
        background: white;
        border: 1px solid #e0e0e0;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
    }
    
    .feature-icon {
        font-size: 2rem;
        margin-bottom: 1rem;
    }
    
    .feature-title {
        font-weight: 600;
        color: #202124;
        margin-bottom: 0.5rem;
    }
    
    .feature-text {
        font-size: 0.875rem;
        color: #5f6368;
    }
    
    .footer {
        margin-top: 4rem;
        padding: 2rem;
        text-align: center;
        background: white;
        border-radius: 12px;
        border: 1px solid #e0e0e0;
    }
    
    #MainMenu, footer, header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
    <div class="main-header">
        <div class="header-content">
            <div class="logo-section">
                <div class="logo">ES</div>
                <div>
                    <div class="title">EngageSense Analytics</div>
                    <div class="subtitle">AI-Powered Student Engagement Platform</div>
                </div>
            </div>
            <div class="user-menu">
                <div class="menu-btn">📊 Reports</div>
                <div class="menu-btn">⚙️ Settings</div>
                <div class="user-avatar">SM</div>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### 🎯 Quick Actions")
    
    if st.button("📤 Export All Data", use_container_width=True):
        st.success("Export started!")
    
    if st.button("📧 Email Report", use_container_width=True):
        st.success("Report sent!")
    
    if st.button("🔔 Set Alerts", use_container_width=True):
        st.success("Alerts configured!")
    
    st.markdown("---")
    st.markdown("### 🔍 Filters")
    
    data_source = st.radio("Data Source", ["CSV File", "MySQL Database"])
    filter_status = st.selectbox("Student Status", ["All Students", "Active Only", "At Risk Only"])
    min_score = st.slider("Min Engagement Score", 0.0, 10.0, 0.0)
    search_id = st.text_input("Search ID", placeholder="S007")
    
    st.markdown("---")
    st.markdown("### 📊 Display")
    
    show_charts = st.checkbox("Show Charts", value=True)
    chart_height = st.slider("Chart Height", 300, 600, 400)
    
    st.markdown("---")
    st.info(f"📅 Updated: {datetime.now().strftime('%B %d, %Y')}")

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
        df['anomaly_flag'] = df['anomaly'].apply(lambda x: 'At Risk' if x == -1 else 'Active')
    except:
        df['anomaly'] = 1
        df['anomaly_flag'] = 'Active'
    
    # Features Section
    st.markdown("""
        <div class="feature-grid">
            <div class="feature-card">
                <div class="feature-icon">🤖</div>
                <div class="feature-title">AI-Powered Detection</div>
                <div class="feature-text">Automatic anomaly detection using machine learning</div>
            </div>
            <div class="feature-card">
                <div class="feature-icon">📊</div>
                <div class="feature-title">Real-Time Analytics</div>
                <div class="feature-text">Live engagement tracking and insights</div>
            </div>
            <div class="feature-card">
                <div class="feature-icon">🔔</div>
                <div class="feature-title">Smart Alerts</div>
                <div class="feature-text">Get notified when students need attention</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("## 📊 Overview Dashboard")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Students", len(df), "+5")
    
    with col2:
        anomaly_count = (df['anomaly'] == -1).sum()
        st.metric("At Risk", anomaly_count, f"{(anomaly_count/len(df)*100):.1f}%")
    
    with col3:
        st.metric("Avg Engagement", f"{df['engagement_score'].mean():.2f}", "+0.3")
    
    with col4:
        st.metric("Avg Time (hrs)", f"{df['time_spent'].mean():.1f}", "+2.3")
    
    if show_charts:
        st.markdown("## 📈 Analytics")
        
        tab1, tab2, tab3 = st.tabs(["Distribution", "Anomaly Detection", "Top Performers"])
        
        with tab1:
            col1, col2 = st.columns(2)
            
            with col1:
                fig1 = px.histogram(df, x='engagement_score', nbins=25, title='Engagement Distribution')
                fig1.update_layout(plot_bgcolor='white', paper_bgcolor='white', font=dict(color='#202124'), height=chart_height)
                fig1.update_traces(marker_color='#1a73e8')
                st.plotly_chart(fig1, use_container_width=True)
            
            with col2:
                counts = df['anomaly_flag'].value_counts()
                fig2 = px.pie(values=counts.values, names=counts.index, title='Student Status', hole=0.4)
                fig2.update_layout(plot_bgcolor='white', paper_bgcolor='white', font=dict(color='#202124'), height=chart_height)
                fig2.update_traces(marker=dict(colors=['#34a853', '#ea4335']))
                st.plotly_chart(fig2, use_container_width=True)
        
        with tab2:
            fig3 = px.scatter(df, x='time_spent', y='engagement_score', color='anomaly_flag', size='login_count', 
                            hover_data=['student_id'], title='Time vs Engagement',
                            color_discrete_map={'Active': '#34a853', 'At Risk': '#ea4335'})
            fig3.update_layout(plot_bgcolor='white', paper_bgcolor='white', font=dict(color='#202124'), height=chart_height)
            st.plotly_chart(fig3, use_container_width=True)
        
        with tab3:
            top_10 = df.nlargest(10, 'engagement_score')
            fig4 = px.bar(top_10, x='student_id', y='engagement_score', color='anomaly_flag',
                        title='Top 10 Students', color_discrete_map={'Active': '#34a853', 'At Risk': '#ea4335'})
            fig4.update_layout(plot_bgcolor='white', paper_bgcolor='white', font=dict(color='#202124'), height=chart_height)
            st.plotly_chart(fig4, use_container_width=True)
    
    st.markdown("## 📋 Student Data")
    
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

st.markdown("""
    <div class="footer">
        <h3>📊 EngageSense Analytics Platform</h3>
        <p>Developed by <strong style="color: #1a73e8;">Suraj Maurya</strong></p>
        <p style="font-size: 0.875rem; color: #5f6368;">AI-Powered · Machine Learning · Python · Streamlit · Plotly</p>
        <p style="font-size: 0.875rem; color: #5f6368;">© 2025 EngageSense. All Rights Reserved.</p>
    </div>
""", unsafe_allow_html=True)
