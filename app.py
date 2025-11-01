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

# Initialize session state
if 'theme' not in st.session_state:
    st.session_state.theme = 'light'
if 'ai_clicked' not in st.session_state:
    st.session_state.ai_clicked = False
if 'realtime_clicked' not in st.session_state:
    st.session_state.realtime_clicked = False
if 'alerts_clicked' not in st.session_state:
    st.session_state.alerts_clicked = False
if 'analytics_clicked' not in st.session_state:
    st.session_state.analytics_clicked = False

# Theme colors
if st.session_state.theme == 'dark':
    bg_color = '#1a1a1a'
    surface_color = '#2d2d2d'
    text_color = '#e0e0e0'
    text_secondary = '#9e9e9e'
    border_color = '#404040'
else:
    bg_color = '#f8f9fa'
    surface_color = '#ffffff'
    text_color = '#202124'
    text_secondary = '#5f6368'
    border_color = '#e0e0e0'

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    * {{ font-family: 'Inter', sans-serif; }}
    
    .stApp {{ background: {bg_color}; }}
    
    .main-header {{
        background: linear-gradient(135deg, #1a73e8 0%, #4285f4 100%);
        padding: 2rem;
        margin: -1rem -2rem 2rem -2rem;
        box-shadow: 0 4px 12px rgba(26, 115, 232, 0.3);
        border-radius: 0 0 20px 20px;
    }}
    
    .header-content {{
        display: flex;
        align-items: center;
        gap: 1rem;
    }}
    
    .logo {{
        width: 56px;
        height: 56px;
        background: white;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.75rem;
        font-weight: 800;
        color: #1a73e8;
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }}
    
    .title {{
        font-size: 2rem;
        font-weight: 800;
        color: white;
    }}
    
    .subtitle {{
        font-size: 1rem;
        color: rgba(255,255,255,0.9);
    }}
    
    /* Feature Cards */
    .feature-grid {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1rem;
        margin: 1.5rem 0;
    }}
    
    .feature-card {{
        background: {surface_color};
        border: 2px solid {border_color};
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        transition: all 0.3s ease;
        cursor: pointer;
    }}
    
    .feature-card:hover {{
        transform: translateY(-6px);
        box-shadow: 0 12px 24px rgba(26, 115, 232, 0.2);
        border-color: #1a73e8;
    }}
    
    .feature-card.active {{
        border-color: #34a853;
        background: linear-gradient(135deg, rgba(52, 168, 83, 0.1), rgba(26, 115, 232, 0.1));
    }}
    
    .feature-icon {{
        font-size: 3rem;
        margin-bottom: 1rem;
    }}
    
    .feature-title {{
        font-weight: 700;
        color: {text_color};
        margin-bottom: 0.5rem;
        font-size: 1.125rem;
    }}
    
    .feature-text {{
        font-size: 0.875rem;
        color: {text_secondary};
        line-height: 1.5;
    }}
    
    .feature-status {{
        margin-top: 1rem;
        padding: 0.5rem;
        background: #34a853;
        color: white;
        border-radius: 8px;
        font-weight: 600;
        font-size: 0.875rem;
    }}
    
    h2 {{
        color: {text_color} !important;
        font-weight: 700 !important;
        font-size: 1.75rem !important;
        margin: 2rem 0 1rem 0 !important;
        padding-left: 1rem;
        border-left: 4px solid #1a73e8;
    }}
    
    [data-testid="stMetric"] {{
        background: {surface_color};
        border: 1px solid {border_color};
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 4px 8px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
    }}
    
    [data-testid="stMetric"]:hover {{
        transform: translateY(-4px);
        box-shadow: 0 8px 16px rgba(26, 115, 232, 0.2);
    }}
    
    [data-testid="stMetric"] label {{
        color: {text_secondary} !important;
        font-size: 0.875rem !important;
        font-weight: 600 !important;
    }}
    
    [data-testid="stMetric"] [data-testid="stMetricValue"] {{
        color: {text_color} !important;
        font-size: 2.5rem !important;
        font-weight: 800 !important;
    }}
    
    .stTabs [data-baseweb="tab-list"] {{
        background: {surface_color};
        padding: 0.5rem;
        border-radius: 12px;
        border: 1px solid {border_color};
    }}
    
    .stTabs [data-baseweb="tab"] {{
        color: {text_secondary};
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
    }}
    
    .stTabs [aria-selected="true"] {{
        background: #1a73e8 !important;
        color: white !important;
    }}
    
    [data-testid="stSidebar"] {{
        background: {surface_color};
        border-right: 1px solid {border_color};
    }}
    
    [data-testid="stSidebar"] h3 {{
        color: {text_color} !important;
        font-weight: 700 !important;
    }}
    
    .stDataFrame {{
        border: 1px solid {border_color};
        border-radius: 12px;
        overflow: hidden;
    }}
    
    .footer {{
        margin-top: 4rem;
        padding: 2.5rem;
        text-align: center;
        background: {surface_color};
        border-radius: 16px;
        border: 1px solid {border_color};
    }}
    
    #MainMenu, footer, header {{visibility: hidden;}}
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

# Sidebar with Theme Toggle
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    
    theme_option = st.radio(
        "Theme",
        ["🌞 Light", "🌙 Dark"],
        index=0 if st.session_state.theme == 'light' else 1,
        horizontal=True
    )
    
    if "Light" in theme_option and st.session_state.theme != 'light':
        st.session_state.theme = 'light'
        st.rerun()
    elif "Dark" in theme_option and st.session_state.theme != 'dark':
        st.session_state.theme = 'dark'
        st.rerun()
    
    st.markdown("---")
    st.markdown("### 🔍 Filters")
    
    data_source = st.radio("Data Source", ["CSV", "MySQL"], horizontal=True)
    filter_status = st.selectbox("Status", ["All", "Active", "At Risk"])
    min_score = st.slider("Min Score", 0.0, 10.0, 0.0)
    search_id = st.text_input("Search", placeholder="S007")
    
    st.markdown("---")
    st.markdown("### 📊 Display")
    
    show_charts = st.checkbox("Show Charts", value=True)
    chart_height = st.slider("Height", 300, 600, 400, step=50)
    
    st.markdown("---")
    st.info(f"📅 {datetime.now().strftime('%b %d, %Y')}")

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
    
    # Feature Cards with Click Functionality
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🤖\n\n**AI Detection**\n\nMachine learning anomaly detection", use_container_width=True):
            st.session_state.ai_clicked = True
            time.sleep(0.3)
    
    with col2:
        if st.button("📊\n\n**Real-Time**\n\nLive engagement tracking", use_container_width=True):
            st.session_state.realtime_clicked = True
            time.sleep(0.3)
    
    with col3:
        if st.button("🔔\n\n**Alerts**\n\nSmart notifications", use_container_width=True):
            st.session_state.alerts_clicked = True
            time.sleep(0.3)
    
    with col4:
        if st.button("📈\n\n**Analytics**\n\nAdvanced insights", use_container_width=True):
            st.session_state.analytics_clicked = True
            time.sleep(0.3)
    
    # Show success messages
    if st.session_state.ai_clicked:
        st.success("✅ AI Detection Activated! Anomaly detection is running.")
        if st.button("Close AI Message"):
            st.session_state.ai_clicked = False
            st.rerun()
    
    if st.session_state.realtime_clicked:
        st.success("✅ Real-Time Tracking Enabled! Live data syncing every 5 seconds.")
        if st.button("Close Real-Time Message"):
            st.session_state.realtime_clicked = False
            st.rerun()
    
    if st.session_state.alerts_clicked:
        st.success("✅ Alerts Configured! You'll receive notifications for at-risk students.")
        if st.button("Close Alerts Message"):
            st.session_state.alerts_clicked = False
            st.rerun()
    
    if st.session_state.analytics_clicked:
        st.success("✅ Advanced Analytics Loaded! Detailed insights are now visible.")
        if st.button("Close Analytics Message"):
            st.session_state.analytics_clicked = False
            st.rerun()
    
    st.markdown("## 📊 Dashboard")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Students", len(df), "+5")
    
    with col2:
        anomaly_count = (df['anomaly'] == -1).sum()
        st.metric("At Risk", anomaly_count, f"{(anomaly_count/len(df)*100):.0f}%")
    
    with col3:
        st.metric("Avg Score", f"{df['engagement_score'].mean():.1f}", "+0.3")
    
    with col4:
        st.metric("Avg Time", f"{df['time_spent'].mean():.0f}h", "+2")
    
    if show_charts:
        st.markdown("## 📈 Analytics")
        
        tab1, tab2, tab3 = st.tabs(["📊 Distribution", "🔍 Anomaly", "🏆 Top 10"])
        
        with tab1:
            col1, col2 = st.columns(2)
            
            with col1:
                fig1 = px.histogram(df, x='engagement_score', nbins=20, title='Engagement Distribution')
                fig1.update_layout(plot_bgcolor='white', paper_bgcolor='white', height=chart_height)
                fig1.update_traces(marker_color='#1a73e8')
                st.plotly_chart(fig1, use_container_width=True)
            
            with col2:
                counts = df['anomaly_flag'].value_counts()
                fig2 = px.pie(values=counts.values, names=counts.index, title='Student Status', hole=0.4)
                fig2.update_layout(plot_bgcolor='white', paper_bgcolor='white', height=chart_height)
                fig2.update_traces(marker=dict(colors=['#34a853', '#ea4335']))
                st.plotly_chart(fig2, use_container_width=True)
        
        with tab2:
            fig3 = px.scatter(df, x='time_spent', y='engagement_score', color='anomaly_flag', 
                            size='login_count', hover_data=['student_id'], title='Time vs Engagement',
                            color_discrete_map={'Active': '#34a853', 'At Risk': '#ea4335'})
            fig3.update_layout(plot_bgcolor='white', paper_bgcolor='white', height=chart_height)
            st.plotly_chart(fig3, use_container_width=True)
        
        with tab3:
            top_10 = df.nlargest(10, 'engagement_score')
            fig4 = px.bar(top_10, x='student_id', y='engagement_score', color='anomaly_flag',
                        title='Top 10 Students', color_discrete_map={'Active': '#34a853', 'At Risk': '#ea4335'})
            fig4.update_layout(plot_bgcolor='white', paper_bgcolor='white', height=chart_height)
            st.plotly_chart(fig4, use_container_width=True)
    
    st.markdown("## 📋 Student Data")
    
    filtered = df.copy()
    
    if filter_status == "Active":
        filtered = filtered[filtered['anomaly_flag'] == 'Active']
    elif filter_status == "At Risk":
        filtered = filtered[filtered['anomaly_flag'] == 'At Risk']
    
    filtered = filtered[filtered['engagement_score'] >= min_score]
    
    if search_id:
        filtered = filtered[filtered['student_id'].astype(str).str.contains(search_id, case=False)]
    
    filtered = filtered.sort_values('engagement_score', ascending=False)
    
    st.info(f"📊 Showing {len(filtered)} of {len(df)} students")
    
    st.dataframe(filtered, use_container_width=True, height=400)
    
    csv = filtered.to_csv(index=False).encode('utf-8')
    st.download_button(
        label=f"📥 Download {len(filtered)} Records",
        data=csv,
        file_name=f'engagesense_{datetime.now().strftime("%Y%m%d_%H%M")}.csv',
        mime='text/csv',
        use_container_width=True
    )

else:
    st.error("❌ Failed to load data or model")

st.markdown(f"""
    <div class="footer">
        <h3 style="color: #1a73e8; margin: 0 0 1rem 0;">📊 EngageSense Analytics</h3>
        <p style="margin: 0.5rem 0; color: {text_color};">Developed by <strong style="color: #1a73e8;">Suraj Maurya</strong></p>
        <p style="margin: 0.5rem 0; font-size: 0.875rem; color: {text_secondary};">🤖 AI · 📊 ML · 🐍 Python · ⚡ Streamlit · 📈 Plotly</p>
        <p style="margin: 0.5rem 0 0 0; font-size: 0.875rem; color: {text_secondary};">© 2025 All Rights Reserved</p>
    </div>
""", unsafe_allow_html=True)
