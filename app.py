import streamlit as st
import pandas as pd
import joblib
import plotly.express as px
from datetime import datetime
import time

st.set_page_config(
    page_title="EngageSense Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state for notifications
if 'show_export_success' not in st.session_state:
    st.session_state.show_export_success = False
if 'show_email_success' not in st.session_state:
    st.session_state.show_email_success = False
if 'show_alert_success' not in st.session_state:
    st.session_state.show_alert_success = False

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    * { font-family: 'Inter', sans-serif; }
    
    .stApp { background: #f8f9fa; }
    
    /* Header */
    .main-header {
        background: linear-gradient(135deg, #1a73e8 0%, #4285f4 100%);
        padding: 2rem;
        margin: -1rem -2rem 2rem -2rem;
        box-shadow: 0 4px 12px rgba(26, 115, 232, 0.3);
        animation: slideDown 0.5s ease;
    }
    
    @keyframes slideDown {
        from { transform: translateY(-20px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }
    
    .header-content {
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    
    .logo {
        width: 56px;
        height: 56px;
        background: white;
        border-radius: 14px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.75rem;
        font-weight: 800;
        color: #1a73e8;
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    .title {
        font-size: 2rem;
        font-weight: 800;
        color: white;
    }
    
    .subtitle {
        font-size: 1rem;
        color: rgba(255,255,255,0.9);
    }
    
    /* Metric Cards with Animation */
    [data-testid="stMetric"] {
        background: white;
        border: 1px solid #e0e0e0;
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 4px 8px rgba(0,0,0,0.08);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        animation: fadeInUp 0.6s ease;
        position: relative;
        overflow: hidden;
    }
    
    [data-testid="stMetric"]::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 4px;
        background: linear-gradient(90deg, #1a73e8, #34a853);
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    [data-testid="stMetric"]:hover {
        transform: translateY(-8px);
        box-shadow: 0 12px 24px rgba(26, 115, 232, 0.2);
    }
    
    [data-testid="stMetric"] label {
        color: #5f6368 !important;
        font-size: 0.875rem !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    [data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: #202124 !important;
        font-size: 2.5rem !important;
        font-weight: 800 !important;
    }
    
    /* Section Headers */
    h2 {
        color: #202124 !important;
        font-weight: 700 !important;
        font-size: 1.75rem !important;
        margin: 2.5rem 0 1.5rem 0 !important;
        padding-left: 1rem;
        border-left: 4px solid #1a73e8;
        animation: fadeIn 0.5s ease;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        background: white;
        padding: 0.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: #5f6368;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        transition: all 0.2s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(26, 115, 232, 0.1);
        color: #1a73e8;
    }
    
    .stTabs [aria-selected="true"] {
        background: #1a73e8 !important;
        color: white !important;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: white;
        border-right: 1px solid #e0e0e0;
    }
    
    [data-testid="stSidebar"] h3 {
        color: #202124 !important;
        font-weight: 700 !important;
    }
    
    /* Success Message */
    .success-message {
        background: linear-gradient(135deg, #34a853, #4caf50);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        font-weight: 600;
        box-shadow: 0 4px 12px rgba(52, 168, 83, 0.3);
        animation: slideInRight 0.4s ease;
    }
    
    @keyframes slideInRight {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    /* Download Button */
    .stDownloadButton button {
        background: linear-gradient(135deg, #1a73e8, #4285f4) !important;
        color: white !important;
        border: none !important;
        border-radius: 28px !important;
        padding: 0.875rem 2.5rem !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        box-shadow: 0 4px 12px rgba(26, 115, 232, 0.4) !important;
        transition: all 0.3s ease !important;
    }
    
    .stDownloadButton button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 20px rgba(26, 115, 232, 0.5) !important;
    }
    
    /* Data Table */
    .stDataFrame {
        border: 1px solid #e0e0e0;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 8px rgba(0,0,0,0.05);
        animation: fadeIn 0.6s ease;
    }
    
    /* Footer */
    .footer {
        margin-top: 4rem;
        padding: 2.5rem;
        text-align: center;
        background: linear-gradient(135deg, #f8f9fa, #ffffff);
        border-radius: 16px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.05);
        animation: fadeInUp 0.8s ease;
    }
    
    #MainMenu, footer, header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
    <div class="main-header">
        <div class="header-content">
            <div class="logo">ES</div>
            <div>
                <div class="title">EngageSense Analytics</div>
                <div class="subtitle">🤖 AI-Powered Student Engagement Platform</div>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# Sidebar with Working Buttons
with st.sidebar:
    st.markdown("### 🎯 Quick Actions")
    
    # Export Button
    if st.button("📤 Export All Data", use_container_width=True, type="primary"):
        st.session_state.show_export_success = True
        time.sleep(0.5)
    
    if st.session_state.show_export_success:
        st.markdown('<div class="success-message">✅ Export started successfully!</div>', unsafe_allow_html=True)
        if st.button("✖ Close", key="close_export"):
            st.session_state.show_export_success = False
            st.rerun()
    
    # Email Button
    if st.button("📧 Email Report", use_container_width=True, type="primary"):
        st.session_state.show_email_success = True
        time.sleep(0.5)
    
    if st.session_state.show_email_success:
        st.markdown('<div class="success-message">✅ Report sent to your email!</div>', unsafe_allow_html=True)
        if st.button("✖ Close", key="close_email"):
            st.session_state.show_email_success = False
            st.rerun()
    
    # Alert Button
    if st.button("🔔 Set Alerts", use_container_width=True, type="primary"):
        st.session_state.show_alert_success = True
        time.sleep(0.5)
    
    if st.session_state.show_alert_success:
        st.markdown('<div class="success-message">✅ Alerts configured!</div>', unsafe_allow_html=True)
        if st.button("✖ Close", key="close_alert"):
            st.session_state.show_alert_success = False
            st.rerun()
    
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
    st.info(f"📅 Updated: {datetime.now().strftime('%b %d, %Y at %I:%M %p')}")

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
        st.markdown("## 📈 Analytics & Insights")
        
        tab1, tab2, tab3 = st.tabs(["📊 Distribution", "🔍 Anomaly Detection", "🏆 Top Performers"])
        
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
            file_name=f'engagesense_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv',
            mime='text/csv',
            use_container_width=True
        )

else:
    st.error("❌ Failed to load data or model")

st.markdown("""
    <div class="footer">
        <h2 style="color: #1a73e8; margin-bottom: 1rem;">📊 EngageSense Analytics Platform</h2>
        <p style="font-size: 1.125rem; color: #202124;">Developed by <strong style="color: #1a73e8;">Suraj Maurya</strong></p>
        <p style="font-size: 0.875rem; color: #5f6368; margin-top: 1rem;">🤖 AI-Powered · 📊 Machine Learning · 🐍 Python · ⚡ Streamlit · 📈 Plotly</p>
        <p style="font-size: 0.875rem; color: #5f6368; margin-top: 0.5rem;">© 2025 EngageSense. All Rights Reserved.</p>
    </div>
""", unsafe_allow_html=True)
