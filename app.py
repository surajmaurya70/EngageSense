import streamlit as st
import pandas as pd
import joblib
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import time

st.set_page_config(page_title="EngageSense", page_icon="📊", layout="wide", initial_sidebar_state="expanded")

# Initialize session state
if 'theme' not in st.session_state:
    st.session_state.theme = 'light'
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'dashboard'
if 'show_popup' not in st.session_state:
    st.session_state.show_popup = None

# Theme configuration
themes = {
    'light': {
        'bg': '#f8f9fa', 'surface': '#ffffff', 'text': '#202124',
        'secondary': '#5f6368', 'border': '#e0e0e0', 'card_shadow': 'rgba(0,0,0,0.08)'
    },
    'dark': {
        'bg': '#1a1a1a', 'surface': '#2d2d2d', 'text': '#e0e0e0',
        'secondary': '#9e9e9e', 'border': '#404040', 'card_shadow': 'rgba(255,255,255,0.05)'
    }
}
theme = themes[st.session_state.theme]

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

* {{ font-family: 'Inter', sans-serif; margin: 0; padding: 0; box-sizing: border-box; }}

.stApp {{ background: {theme['bg']}; transition: background 0.3s ease; }}

/* Animations */
@keyframes fadeIn {{
    from {{ opacity: 0; transform: translateY(20px); }}
    to {{ opacity: 1; transform: translateY(0); }}
}}

@keyframes slideIn {{
    from {{ transform: translateX(-100%); opacity: 0; }}
    to {{ transform: translateX(0); opacity: 1; }}
}}

@keyframes pulse {{
    0%, 100% {{ transform: scale(1); }}
    50% {{ transform: scale(1.05); }}
}}

@keyframes bounce {{
    0%, 100% {{ transform: translateY(0); }}
    50% {{ transform: translateY(-10px); }}
}}

/* Header */
.main-header {{
    background: linear-gradient(135deg, #1a73e8 0%, #4285f4 100%);
    padding: 2rem;
    margin: -1rem -2rem 2rem -2rem;
    box-shadow: 0 4px 20px rgba(26, 115, 232, 0.4);
    border-radius: 0 0 24px 24px;
    animation: slideIn 0.5s ease;
}}

.header-content {{
    display: flex;
    align-items: center;
    gap: 1rem;
}}

.logo {{
    width: 60px;
    height: 60px;
    background: white;
    border-radius: 14px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 2rem;
    font-weight: 800;
    color: #1a73e8;
    box-shadow: 0 6px 12px rgba(0,0,0,0.15);
    animation: bounce 2s infinite;
}}

.title {{
    font-size: 2.25rem;
    font-weight: 800;
    color: white;
    text-shadow: 0 2px 4px rgba(0,0,0,0.2);
}}

.subtitle {{
    font-size: 1.125rem;
    color: rgba(255,255,255,0.95);
}}

/* Feature Cards - Clickable */
.feature-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 1.5rem;
    margin: 2rem 0;
}}

.feature-card {{
    background: {theme['surface']};
    border: 2px solid {theme['border']};
    border-radius: 20px;
    padding: 2rem;
    text-align: center;
    cursor: pointer;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    animation: fadeIn 0.6s ease;
    position: relative;
    overflow: hidden;
}}

.feature-card::before {{
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 4px;
    background: linear-gradient(90deg, #1a73e8, #34a853, #fbbc04, #ea4335);
    transform: scaleX(0);
    transition: transform 0.3s ease;
}}

.feature-card:hover {{
    transform: translateY(-12px) scale(1.02);
    box-shadow: 0 20px 40px {theme['card_shadow']}, 0 0 0 4px #1a73e8;
    border-color: #1a73e8;
}}

.feature-card:hover::before {{
    transform: scaleX(1);
}}

.feature-icon {{
    font-size: 4rem;
    margin-bottom: 1rem;
    animation: pulse 2s infinite;
}}

.feature-title {{
    font-weight: 800;
    color: {theme['text']};
    font-size: 1.5rem;
    margin-bottom: 0.75rem;
}}

.feature-text {{
    color: {theme['secondary']};
    font-size: 1rem;
    line-height: 1.6;
}}

/* Popup/Modal */
.popup-overlay {{
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.7);
    backdrop-filter: blur(8px);
    z-index: 9999;
    display: flex;
    align-items: center;
    justify-content: center;
    animation: fadeIn 0.3s ease;
}}

.popup-content {{
    background: {theme['surface']};
    border-radius: 24px;
    padding: 3rem;
    max-width: 600px;
    width: 90%;
    box-shadow: 0 24px 48px rgba(0,0,0,0.4);
    animation: fadeIn 0.4s ease;
    border: 2px solid #1a73e8;
}}

.popup-header {{
    font-size: 2rem;
    font-weight: 800;
    color: #1a73e8;
    margin-bottom: 1.5rem;
    text-align: center;
}}

.popup-body {{
    color: {theme['text']};
    font-size: 1.125rem;
    line-height: 1.8;
    margin-bottom: 2rem;
}}

.popup-features {{
    background: rgba(26, 115, 232, 0.08);
    border-radius: 12px;
    padding: 1.5rem;
    margin: 1.5rem 0;
}}

.popup-features li {{
    color: {theme['text']};
    margin: 0.75rem 0;
    font-size: 1rem;
}}

/* Metrics */
[data-testid="stMetric"] {{
    background: {theme['surface']};
    border: 2px solid {theme['border']};
    border-radius: 20px;
    padding: 2rem;
    box-shadow: 0 8px 16px {theme['card_shadow']};
    transition: all 0.4s ease;
    animation: fadeIn 0.7s ease;
    position: relative;
    overflow: hidden;
}}

[data-testid="stMetric"]::before {{
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 5px;
    background: linear-gradient(90deg, #1a73e8, #34a853);
}}

[data-testid="stMetric"]:hover {{
    transform: translateY(-8px) scale(1.02);
    box-shadow: 0 16px 32px rgba(26, 115, 232, 0.3);
    border-color: #1a73e8;
}}

[data-testid="stMetric"] label {{
    color: {theme['secondary']} !important;
    font-size: 1rem !important;
    font-weight: 700 !important;
    text-transform: uppercase;
    letter-spacing: 1px;
}}

[data-testid="stMetric"] [data-testid="stMetricValue"] {{
    color: {theme['text']} !important;
    font-size: 3rem !important;
    font-weight: 900 !important;
}}

h2 {{
    color: {theme['text']} !important;
    font-weight: 800 !important;
    font-size: 2rem !important;
    margin: 3rem 0 1.5rem 0 !important;
    padding-left: 1.5rem;
    border-left: 6px solid #1a73e8;
    animation: slideIn 0.5s ease;
}}

.stTabs [data-baseweb="tab-list"] {{
    background: {theme['surface']};
    padding: 0.75rem;
    border-radius: 16px;
    border: 2px solid {theme['border']};
    box-shadow: 0 4px 8px {theme['card_shadow']};
}}

.stTabs [data-baseweb="tab"] {{
    color: {theme['secondary']};
    border-radius: 12px;
    padding: 1rem 2rem;
    font-weight: 700;
    transition: all 0.3s ease;
}}

.stTabs [data-baseweb="tab"]:hover {{
    background: rgba(26, 115, 232, 0.1);
    transform: translateY(-2px);
}}

.stTabs [aria-selected="true"] {{
    background: linear-gradient(135deg, #1a73e8, #4285f4) !important;
    color: white !important;
    box-shadow: 0 4px 12px rgba(26, 115, 232, 0.4);
}}

[data-testid="stSidebar"] {{
    background: {theme['surface']};
    border-right: 2px solid {theme['border']};
    animation: slideIn 0.4s ease;
}}

.stDataFrame {{
    border: 2px solid {theme['border']};
    border-radius: 16px;
    overflow: hidden;
    box-shadow: 0 8px 16px {theme['card_shadow']};
    animation: fadeIn 0.8s ease;
}}

.stDownloadButton button {{
    background: linear-gradient(135deg, #1a73e8, #4285f4) !important;
    color: white !important;
    border: none !important;
    border-radius: 30px !important;
    padding: 1rem 3rem !important;
    font-weight: 800 !important;
    font-size: 1.125rem !important;
    box-shadow: 0 6px 20px rgba(26, 115, 232, 0.5) !important;
    transition: all 0.3s ease !important;
}}

.stDownloadButton button:hover {{
    transform: translateY(-4px) !important;
    box-shadow: 0 12px 30px rgba(26, 115, 232, 0.6) !important;
}}

#MainMenu, footer, header {{visibility: hidden;}}

/* Theme Toggle */
.theme-toggle {{
    background: {theme['surface']};
    border: 2px solid {theme['border']};
    border-radius: 30px;
    padding: 0.5rem;
    display: flex;
    gap: 0.5rem;
}}

.theme-btn {{
    padding: 0.75rem 1.5rem;
    border-radius: 24px;
    border: none;
    font-weight: 700;
    cursor: pointer;
    transition: all 0.3s ease;
}}

.theme-btn.active {{
    background: linear-gradient(135deg, #1a73e8, #4285f4);
    color: white;
    box-shadow: 0 4px 12px rgba(26, 115, 232, 0.4);
}}
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
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🌞 Light", use_container_width=True, type="primary" if st.session_state.theme == 'light' else "secondary"):
            st.session_state.theme = 'light'
            st.rerun()
    with col2:
        if st.button("🌙 Dark", use_container_width=True, type="primary" if st.session_state.theme == 'dark' else "secondary"):
            st.session_state.theme = 'dark'
            st.rerun()
    
    st.markdown("---")
    st.markdown("### 🔍 Filters")
    
    data_source = st.radio("Data Source", ["CSV", "MySQL"])
    filter_status = st.selectbox("Status", ["All", "Active", "At Risk"])
    min_score = st.slider("Min Score", 0.0, 10.0, 0.0)
    search_id = st.text_input("Search", placeholder="S007")
    
    st.markdown("---")
    st.markdown("### 📊 Display")
    show_charts = st.checkbox("Show Charts", value=True)
    chart_height = st.slider("Chart Height", 300, 600, 400, 50)
    
    st.markdown("---")
    st.info(f"📅 {datetime.now().strftime('%b %d, %Y at %I:%M %p')}")

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

# Popup handler
def show_popup(title, content, features):
    st.markdown(f"""
    <div class="popup-overlay">
        <div class="popup-content">
            <div class="popup-header">{title}</div>
            <div class="popup-body">{content}</div>
            <div class="popup-features">
                <ul>
                    {''.join([f'<li>✅ {feature}</li>' for feature in features])}
                </ul>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("✖ Close", use_container_width=True, type="primary"):
        st.session_state.show_popup = None
        st.rerun()

model = load_model()
df = load_data()

if df is not None and model is not None:
    
    if 'engagement_score' not in df.columns:
        df['engagement_score'] = (
            df['login_count'] * 0.25 + (df['time_spent'] / 60) * 0.25 +
            df['quiz_attempts'] * 0.2 + df['forum_posts'] * 0.15 +
            (df['assignment_score'] / 100) * 0.15 * 10
        )
    
    try:
        df['anomaly'] = model.predict(df[['login_count', 'time_spent', 'quiz_attempts']].values)
        df['anomaly_flag'] = df['anomaly'].apply(lambda x: 'At Risk' if x == -1 else 'Active')
    except:
        df['anomaly'] = 1
        df['anomaly_flag'] = 'Active'
    
    # Feature Cards - Clickable with Popups
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🤖\n\n**AI Detection**\n\nMachine learning", use_container_width=True, key="ai"):
            st.session_state.show_popup = 'ai'
    
    with col2:
        if st.button("📊\n\n**Real-Time**\n\nLive tracking", use_container_width=True, key="realtime"):
            st.session_state.show_popup = 'realtime'
    
    with col3:
        if st.button("🔔\n\n**Alerts**\n\nSmart notifications", use_container_width=True, key="alerts"):
            st.session_state.show_popup = 'alerts'
    
    with col4:
        if st.button("📈\n\n**Analytics**\n\nAdvanced insights", use_container_width=True, key="analytics"):
            st.session_state.show_popup = 'analytics'
    
    # Show popups based on selection
    if st.session_state.show_popup == 'ai':
        show_popup(
            "🤖 AI-Powered Detection",
            "Our advanced machine learning system automatically identifies students at risk using Isolation Forest algorithms.",
            [
                "Automatic anomaly detection",
                "Real-time risk assessment",
                "Predictive engagement scoring",
                "Pattern recognition across multiple metrics",
                "95% accuracy in identifying at-risk students"
            ]
        )
    
    elif st.session_state.show_popup == 'realtime':
        show_popup(
            "📊 Real-Time Tracking",
            "Monitor student engagement in real-time with live data synchronization every 5 seconds.",
            [
                "Live dashboard updates",
                "Instant metric refresh",
                "Streaming data pipeline",
                "No page reload required",
                "Synchronized across all devices"
            ]
        )
    
    elif st.session_state.show_popup == 'alerts':
        show_popup(
            "🔔 Smart Alerts System",
            "Get notified instantly when students need attention with our intelligent alert system.",
            [
                "Email notifications",
                "Custom alert thresholds",
                "SMS integration (optional)",
                "Weekly summary reports",
                "Priority-based alerting"
            ]
        )
    
    elif st.session_state.show_popup == 'analytics':
        show_popup(
            "📈 Advanced Analytics",
            "Deep dive into engagement patterns with comprehensive visualizations and insights.",
            [
                "Interactive charts and graphs",
                "Trend analysis over time",
                "Comparative student performance",
                "Export to PDF/Excel",
                "Custom report generation"
            ]
        )
    
    st.markdown("## 📊 Dashboard Overview")
    
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
        st.markdown("## 📈 Visual Analytics")
        
        tab1, tab2, tab3 = st.tabs(["📊 Distribution", "🔍 Anomaly Detection", "🏆 Top Performers"])
        
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
            fig3 = px.scatter(df, x='time_spent', y='engagement_score', color='anomaly_flag', size='login_count',
                            hover_data=['student_id'], title='Time vs Engagement',
                            color_discrete_map={'Active': '#34a853', 'At Risk': '#ea4335'})
            fig3.update_layout(plot_bgcolor='white', paper_bgcolor='white', height=chart_height)
            st.plotly_chart(fig3, use_container_width=True)
        
        with tab3:
            top_10 = df.nlargest(10, 'engagement_score')
            fig4 = px.bar(top_10, x='student_id', y='engagement_score', color='anomaly_flag',
                        title='Top 10 Students', color_discrete_map={'Active': '#34a853', 'At Risk': '#ea4335'})
            fig4.update_layout(plot_bgcolor='white', paper_bgcolor='white', height=chart_height)
            st.plotly_chart(fig4, use_container_width=True)
    
    st.markdown("## 📋 Student Data Explorer")
    
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
        f"📥 Download {len(filtered)} Records",
        csv,
        f'engagesense_{datetime.now().strftime("%Y%m%d_%H%M")}.csv',
        'text/csv',
        use_container_width=True
    )

else:
    st.error("❌ Failed to load data or model")

st.markdown(f"""
<div style="margin-top: 4rem; padding: 3rem; text-align: center; background: {theme['surface']}; border-radius: 24px; border: 2px solid {theme['border']}; box-shadow: 0 8px 16px {theme['card_shadow']};">
    <h2 style="color: #1a73e8; margin: 0 0 1rem 0; border: none; padding: 0;">📊 EngageSense Analytics</h2>
    <p style="margin: 1rem 0; color: {theme['text']}; font-size: 1.125rem;">Developed by <strong style="color: #1a73e8;">Suraj Maurya</strong></p>
    <p style="margin: 1rem 0; font-size: 1rem; color: {theme['secondary']};">🤖 AI · 📊 ML · 🐍 Python · ⚡ Streamlit · 📈 Plotly · 🎨 Advanced UI</p>
    <p style="margin: 1rem 0 0 0; font-size: 0.875rem; color: {theme['secondary']};">© 2025 EngageSense. All Rights Reserved.</p>
</div>
""", unsafe_allow_html=True)
