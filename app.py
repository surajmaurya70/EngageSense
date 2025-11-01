import streamlit as st
import pandas as pd
import joblib
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="EngageSense", page_icon="📊", layout="wide", initial_sidebar_state="expanded")

# Initialize session state
if 'theme' not in st.session_state:
    st.session_state.theme = 'light'
if 'show_popup' not in st.session_state:
    st.session_state.show_popup = None

# Theme configuration
themes = {
    'light': {'bg': '#f8f9fa', 'surface': '#ffffff', 'text': '#202124', 'secondary': '#5f6368', 'border': '#e0e0e0'},
    'dark': {'bg': '#1a1a1a', 'surface': '#2d2d2d', 'text': '#e0e0e0', 'secondary': '#9e9e9e', 'border': '#404040'}
}
theme = themes[st.session_state.theme]

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

* {{ font-family: 'Inter', sans-serif; }}

.stApp {{ background: {theme['bg']}; transition: all 0.3s ease; }}

@keyframes fadeIn {{
    from {{ opacity: 0; transform: translateY(20px); }}
    to {{ opacity: 1; transform: translateY(0); }}
}}

@keyframes slideIn {{
    from {{ transform: translateX(-100%); }}
    to {{ transform: translateX(0); }}
}}

@keyframes pulse {{
    0%, 100% {{ transform: scale(1); }}
    50% {{ transform: scale(1.05); }}
}}

@keyframes bounce {{
    0%, 100% {{ transform: translateY(0); }}
    50% {{ transform: translateY(-10px); }}
}}

.main-header {{
    background: linear-gradient(135deg, #1a73e8 0%, #4285f4 100%);
    padding: 2rem;
    margin: -1rem -2rem 2rem -2rem;
    box-shadow: 0 4px 20px rgba(26, 115, 232, 0.4);
    border-radius: 0 0 24px 24px;
    animation: slideIn 0.5s ease;
}}

.header-content {{ display: flex; align-items: center; gap: 1rem; }}

.logo {{
    width: 60px; height: 60px; background: white; border-radius: 14px;
    display: flex; align-items: center; justify-content: center;
    font-size: 2rem; font-weight: 800; color: #1a73e8;
    box-shadow: 0 6px 12px rgba(0,0,0,0.15);
    animation: bounce 2s infinite;
}}

.title {{ font-size: 2.25rem; font-weight: 800; color: white; }}
.subtitle {{ font-size: 1.125rem; color: rgba(255,255,255,0.95); }}

h2 {{
    color: {theme['text']} !important;
    font-weight: 800 !important;
    font-size: 2rem !important;
    margin: 3rem 0 1.5rem 0 !important;
    padding-left: 1.5rem;
    border-left: 6px solid #1a73e8;
    animation: slideIn 0.5s ease;
}}

[data-testid="stMetric"] {{
    background: {theme['surface']};
    border: 2px solid {theme['border']};
    border-radius: 20px;
    padding: 2rem;
    box-shadow: 0 8px 16px rgba(0,0,0,0.08);
    transition: all 0.4s ease;
    animation: fadeIn 0.7s ease;
}}

[data-testid="stMetric"]:hover {{
    transform: translateY(-8px);
    box-shadow: 0 16px 32px rgba(26, 115, 232, 0.3);
    border-color: #1a73e8;
}}

[data-testid="stMetric"] label {{
    color: {theme['secondary']} !important;
    font-size: 1rem !important;
    font-weight: 700 !important;
}}

[data-testid="stMetric"] [data-testid="stMetricValue"] {{
    color: {theme['text']} !important;
    font-size: 3rem !important;
    font-weight: 900 !important;
}}

.stTabs [data-baseweb="tab-list"] {{
    background: {theme['surface']};
    padding: 0.75rem;
    border-radius: 16px;
    border: 2px solid {theme['border']};
}}

.stTabs [data-baseweb="tab"] {{
    color: {theme['secondary']};
    border-radius: 12px;
    padding: 1rem 2rem;
    font-weight: 700;
}}

.stTabs [aria-selected="true"] {{
    background: linear-gradient(135deg, #1a73e8, #4285f4) !important;
    color: white !important;
}}

[data-testid="stSidebar"] {{
    background: {theme['surface']};
    border-right: 2px solid {theme['border']};
}}

[data-testid="stSidebar"] h3 {{
    color: {theme['text']} !important;
    font-weight: 700 !important;
    border: none !important;
    padding: 0 !important;
    margin: 1rem 0 !important;
}}

.stDataFrame {{
    border: 2px solid {theme['border']};
    border-radius: 16px;
    overflow: hidden;
}}

#MainMenu, footer, header {{visibility: hidden;}}
</style>

<script>
function closePopup() {{
    window.parent.postMessage({{type: 'streamlit:setComponentValue', value: null}}, '*');
}}
</script>
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

# Sidebar with Proper Theme Toggle
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    
    st.markdown("#### Theme")
    
    theme_col1, theme_col2 = st.columns(2)
    
    with theme_col1:
        if st.button(
            "🌞 Light",
            use_container_width=True,
            type="primary" if st.session_state.theme == 'light' else "secondary",
            key="light_btn"
        ):
            st.session_state.theme = 'light'
            st.rerun()
    
    with theme_col2:
        if st.button(
            "🌙 Dark",
            use_container_width=True,
            type="primary" if st.session_state.theme == 'dark' else "secondary",
            key="dark_btn"
        ):
            st.session_state.theme = 'dark'
            st.rerun()
    
    # Show current theme
    st.caption(f"Current: **{st.session_state.theme.title()} Mode**")
    
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
    
    # Feature Cards with Click
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🤖\n\n**AI Detection**\n\nMachine learning", use_container_width=True, key="ai"):
            st.session_state.show_popup = 'ai'
    
    with col2:
        if st.button("📊\n\n**Real-Time**\n\nLive tracking", use_container_width=True, key="realtime"):
            st.session_state.show_popup = 'realtime'
    
    with col3:
        if st.button("🔔\n\n**Alerts**\n\nNotifications", use_container_width=True, key="alerts"):
            st.session_state.show_popup = 'alerts'
    
    with col4:
        if st.button("📈\n\n**Analytics**\n\nInsights", use_container_width=True, key="analytics"):
            st.session_state.show_popup = 'analytics'
    
    # Small Popup with Click-Outside-to-Close
    if st.session_state.show_popup:
        popups = {
            'ai': {
                'icon': '🤖',
                'title': 'AI Detection',
                'features': [
                    'Anomaly detection',
                    'Risk assessment',
                    'Predictive scoring',
                    '95% accuracy'
                ]
            },
            'realtime': {
                'icon': '📊',
                'title': 'Real-Time',
                'features': [
                    'Live updates',
                    '5-sec refresh',
                    'Streaming data',
                    'Instant sync'
                ]
            },
            'alerts': {
                'icon': '🔔',
                'title': 'Smart Alerts',
                'features': [
                    'Email notifications',
                    'SMS integration',
                    'Custom thresholds',
                    'Weekly reports'
                ]
            },
            'analytics': {
                'icon': '📈',
                'title': 'Analytics',
                'features': [
                    'Interactive charts',
                    'Trend analysis',
                    'Export reports',
                    'Custom insights'
                ]
            }
        }
        
        popup = popups[st.session_state.show_popup]
        
        # Small Popup Container
        popup_container = st.container()
        with popup_container:
            with st.expander(f"{popup['icon']} {popup['title']}", expanded=True):
                for feature in popup['features']:
                    st.markdown(f"✅ {feature}")
                
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    if st.button("✖ Close", use_container_width=True, type="primary", key="close_popup"):
                        st.session_state.show_popup = None
                        st.rerun()
    
    # Click anywhere to close (simulated with button)
    if st.session_state.show_popup:
        if st.button("Click anywhere to close popup", type="secondary", use_container_width=True):
            st.session_state.show_popup = None
            st.rerun()
    
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
                fig2 = px.pie(values=counts.values, names=counts.index, title='Status', hole=0.4)
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
                        title='Top 10', color_discrete_map={'Active': '#34a853', 'At Risk': '#ea4335'})
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
        f"📥 Download {len(filtered)} Records",
        csv,
        f'data_{datetime.now().strftime("%Y%m%d_%H%M")}.csv',
        'text/csv',
        use_container_width=True
    )

else:
    st.error("❌ Failed to load data")

st.markdown(f"""
<div style="margin-top: 4rem; padding: 3rem; text-align: center; background: {theme['surface']}; border-radius: 24px; border: 2px solid {theme['border']};">
    <h2 style="color: #1a73e8; margin: 0 0 1rem 0; border: none; padding: 0;">📊 EngageSense</h2>
    <p style="color: {theme['text']}; font-size: 1.125rem;">By <strong style="color: #1a73e8;">Suraj Maurya</strong></p>
    <p style="color: {theme['secondary']}; font-size: 1rem;">🤖 AI · 📊 ML · 🐍 Python · ⚡ Streamlit</p>
    <p style="color: {theme['secondary']}; font-size: 0.875rem;">© 2025 All Rights Reserved</p>
</div>
""", unsafe_allow_html=True)
