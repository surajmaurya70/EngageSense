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

# Premium CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    * { font-family: 'Inter', sans-serif; }
    
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    }
    
    .block-container {
        padding: 2rem 2.5rem !important;
        max-width: 1400px;
    }
    
    /* Header */
    .main-header {
        background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 16px;
        padding: 2rem;
        margin-bottom: 2rem;
        text-align: center;
    }
    
    .header-title {
        font-size: 2.5rem;
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 0.5rem;
    }
    
    .header-subtitle {
        font-size: 1rem;
        color: rgba(255,255,255,0.7);
    }
    
    /* Metrics */
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.15);
        border-radius: 14px;
        padding: 1.5rem;
        transition: all 0.3s ease;
    }
    
    [data-testid="stMetric"]:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(255,255,255,0.1);
    }
    
    [data-testid="stMetric"] label {
        color: rgba(255,255,255,0.8) !important;
        font-size: 0.9rem !important;
        font-weight: 600 !important;
    }
    
    [data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-size: 2.5rem !important;
        font-weight: 800 !important;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
        border-right: 1px solid rgba(255,255,255,0.1);
    }
    
    [data-testid="stSidebar"] h3 {
        color: #ffffff !important;
        font-weight: 700 !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        background: rgba(255,255,255,0.05);
        padding: 0.5rem;
        border-radius: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: rgba(255,255,255,0.6);
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
    }
    
    .stTabs [aria-selected="true"] {
        background: rgba(255,255,255,0.15) !important;
        color: #ffffff !important;
    }
    
    h2 {
        color: #ffffff !important;
        font-weight: 700 !important;
        margin: 2rem 0 1rem 0 !important;
    }
    
    .stAlert {
        background: rgba(255,255,255,0.1) !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
        border-radius: 10px !important;
        color: #ffffff !important;
    }
    
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
    }
    
    /* Footer */
    .footer {
        margin-top: 4rem;
        padding: 2rem;
        text-align: center;
        background: rgba(255,255,255,0.05);
        border-radius: 12px;
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    .footer-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 0.5rem;
    }
    
    .footer-text {
        color: rgba(255,255,255,0.7);
        margin: 0.3rem 0;
    }
    
    #MainMenu, footer, header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
    <div class="main-header">
        <div class="header-title">📊 EngageSense Analytics</div>
        <div class="header-subtitle">AI-Powered Student Engagement Monitoring Platform</div>
    </div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
# SIDEBAR - SETTINGS PANEL
# ═══════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("### ⚙️ Settings & Filters")
    st.markdown("---")
    
    # Theme Selection
    theme = st.selectbox(
        "🎨 Color Theme",
        ["Dark Blue (Default)", "Dark Purple", "Dark Green"],
        help="Choose your preferred color theme"
    )
    
    st.markdown("---")
    
    # Data Source
    st.markdown("### 📁 Data Source")
    data_source = st.radio(
        "",
        ["CSV File", "MySQL Database"],
        help="Select data source"
    )
    
    st.markdown("---")
    
    # Filters
    st.markdown("### 🔍 Filters")
    
    filter_status = st.selectbox(
        "Student Status",
        ["All Students", "Active Only", "At Risk Only"]
    )
    
    min_score = st.slider(
        "Min Engagement Score",
        0.0, 10.0, 0.0,
        help="Filter students by minimum score"
    )
    
    search_id = st.text_input(
        "Search Student ID",
        placeholder="Enter Student ID..."
    )
    
    st.markdown("---")
    
    # Chart Settings
    st.markdown("### 📊 Chart Settings")
    
    show_charts = st.checkbox("Show Charts", value=True)
    chart_height = st.slider("Chart Height", 300, 600, 400)
    
    st.markdown("---")
    
    # Export Options
    st.markdown("### 📥 Export Options")
    include_anomalies = st.checkbox("Include Anomalies Only", value=False)
    
    st.markdown("---")
    st.info(f"**Last Updated**  \n{datetime.now().strftime('%B %d, %Y')}")

# ═══════════════════════════════════════════════════════════
# LOAD DATA & MODEL
# ═══════════════════════════════════════════════════════════
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
    
    # ═══════════════════════════════════════════════════════════
    # TOP METRICS
    # ═══════════════════════════════════════════════════════════
    st.markdown("## 📊 Dashboard Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Students", len(df), "+5")
    
    with col2:
        anomaly_count = (df['anomaly'] == -1).sum()
        st.metric("At Risk", anomaly_count, f"{(anomaly_count/len(df)*100):.0f}%")
    
    with col3:
        st.metric("Avg Score", f"{df['engagement_score'].mean():.2f}", "+0.3")
    
    with col4:
        st.metric("Avg Time (hrs)", f"{df['time_spent'].mean():.1f}", "+2.3")
    
    # ═══════════════════════════════════════════════════════════
    # CHARTS (IF ENABLED)
    # ═══════════════════════════════════════════════════════════
    if show_charts:
        st.markdown("## 📈 Visual Analytics")
        
        tab1, tab2, tab3 = st.tabs(["Distribution", "Anomaly Detection", "Top Performers"])
        
        with tab1:
            col1, col2 = st.columns(2)
            
            with col1:
                fig1 = px.histogram(df, x='engagement_score', nbins=25, title='Engagement Distribution', color_discrete_sequence=['#4a90e2'])
                fig1.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='white'), height=chart_height)
                st.plotly_chart(fig1, use_container_width=True)
            
            with col2:
                counts = df['anomaly_flag'].value_counts()
                fig2 = px.pie(values=counts.values, names=counts.index, title='Student Status', hole=0.5, color_discrete_sequence=['#50c878', '#ff6b6b'])
                fig2.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='white'), height=chart_height)
                st.plotly_chart(fig2, use_container_width=True)
        
        with tab2:
            fig3 = px.scatter(df, x='time_spent', y='engagement_score', color='anomaly_flag', size='login_count', 
                            hover_data=['student_id'], title='Time vs Engagement', 
                            color_discrete_map={'Active': '#50c878', 'At Risk': '#ff6b6b'})
            fig3.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='white'), height=chart_height)
            st.plotly_chart(fig3, use_container_width=True)
        
        with tab3:
            top_10 = df.nlargest(10, 'engagement_score')
            fig4 = px.bar(top_10, x='student_id', y='engagement_score', color='anomaly_flag', title='Top 10 Students',
                        color_discrete_map={'Active': '#50c878', 'At Risk': '#ff6b6b'})
            fig4.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='white'), height=chart_height)
            st.plotly_chart(fig4, use_container_width=True)
    
    # ═══════════════════════════════════════════════════════════
    # DATA TABLE
    # ═══════════════════════════════════════════════════════════
    st.markdown("## 📋 Student Data")
    
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
            return ['background-color: rgba(255, 107, 107, 0.2)'] * len(row)
        return ['background-color: rgba(80, 200, 120, 0.1)'] * len(row)
    
    styled_df = filtered.style.apply(highlight_row, axis=1)
    st.dataframe(styled_df, use_container_width=True, height=400)
    
    # ═══════════════════════════════════════════════════════════
    # EXPORT
    # ═══════════════════════════════════════════════════════════
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        export_df = filtered[filtered['anomaly'] == -1] if include_anomalies else filtered
        csv = export_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label=f"📥 Export {len(export_df)} Records",
            data=csv,
            file_name=f'engagesense_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv',
            mime='text/csv',
            use_container_width=True
        )

else:
    st.error("❌ Failed to load data or model")

# ═══════════════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════════════
st.markdown("""
    <div class="footer">
        <div class="footer-title">EngageSense Analytics</div>
        <div class="footer-text">Developed by <strong>Suraj Maurya</strong></div>
        <div class="footer-text">Machine Learning · Python · Streamlit · Plotly</div>
        <div class="footer-text">© 2025 All Rights Reserved</div>
    </div>
""", unsafe_allow_html=True)
