import streamlit as st
import pandas as pd
import joblib
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(page_title="EngageSense Analytics", page_icon="📊", layout="wide")

# Session state
if 'theme' not in st.session_state:
    st.session_state.theme = 'light'

# Theme colors
def get_theme():
    if st.session_state.theme == 'dark':
        return {'bg': '#1a1a1a', 'surface': '#2d2d2d', 'text': '#e0e0e0', 'secondary': '#9e9e9e', 'border': '#404040'}
    return {'bg': '#f8f9fa', 'surface': '#ffffff', 'text': '#202124', 'secondary': '#5f6368', 'border': '#e0e0e0'}

t = get_theme()

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
* {{ font-family: 'Inter', sans-serif; }}
.stApp {{ background: {t['bg']}; }}

@keyframes fadeInUp {{
    from {{ opacity: 0; transform: translateY(30px); }}
    to {{ opacity: 1; transform: translateY(0); }}
}}

@keyframes slideIn {{
    from {{ opacity: 0; transform: translateX(-50px); }}
    to {{ opacity: 1; transform: translateX(0); }}
}}

@keyframes pulse {{
    0%, 100% {{ transform: scale(1); }}
    50% {{ transform: scale(1.05); }}
}}

.main-header {{
    background: linear-gradient(135deg, #1a73e8 0%, #4285f4 100%);
    padding: 2rem; margin: -1rem -2rem 2rem -2rem;
    box-shadow: 0 4px 20px rgba(26, 115, 232, 0.4);
    border-radius: 0 0 24px 24px;
    animation: slideIn 0.6s ease;
}}

.header-content {{ display: flex; align-items: center; gap: 1rem; }}
.logo {{ 
    width: 60px; height: 60px; background: white; border-radius: 14px;
    display: flex; align-items: center; justify-content: center;
    font-size: 2rem; font-weight: 800; color: #1a73e8; 
    box-shadow: 0 6px 12px rgba(0,0,0,0.15);
    animation: pulse 2s infinite;
}}
.title {{ font-size: 2.25rem; font-weight: 800; color: white; }}
.subtitle {{ font-size: 1.125rem; color: rgba(255,255,255,0.95); }}

h2 {{ 
    color: {t['text']} !important; font-weight: 800 !important; font-size: 2rem !important;
    margin: 2.5rem 0 1.5rem 0 !important; padding-left: 1.5rem; border-left: 6px solid #1a73e8;
    animation: fadeInUp 0.5s ease;
}}

[data-testid="stMetric"] {{
    background: {t['surface']}; border: 2px solid {t['border']}; border-radius: 20px;
    padding: 2rem; box-shadow: 0 8px 16px rgba(0,0,0,0.08); 
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    cursor: pointer;
    animation: fadeInUp 0.7s ease;
    position: relative;
    overflow: hidden;
}}

[data-testid="stMetric"]::before {{
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 100%; height: 4px;
    background: linear-gradient(90deg, #1a73e8, #34a853, #fbbc04, #ea4335);
    transform: scaleX(0);
    transition: transform 0.3s ease;
}}

[data-testid="stMetric"]:hover::before {{
    transform: scaleX(1);
}}

[data-testid="stMetric"]:hover {{ 
    transform: translateY(-10px) scale(1.02); 
    box-shadow: 0 20px 40px rgba(26, 115, 232, 0.35); 
    border-color: #1a73e8;
}}

[data-testid="stMetric"] label {{ 
    color: {t['secondary']} !important; font-size: 1rem !important; 
    font-weight: 700 !important; text-transform: uppercase; letter-spacing: 0.5px;
}}

[data-testid="stMetric"] [data-testid="stMetricValue"] {{ 
    color: {t['text']} !important; font-size: 3rem !important; font-weight: 900 !important; 
}}

.stTabs [data-baseweb="tab-list"] {{ 
    background: {t['surface']}; padding: 0.75rem; border-radius: 16px; 
    border: 2px solid {t['border']}; animation: fadeInUp 0.8s ease;
}}

.stTabs [data-baseweb="tab"] {{ 
    color: {t['secondary']}; border-radius: 12px; padding: 1rem 2rem; 
    font-weight: 700; transition: all 0.3s ease;
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

[data-testid="stSidebar"] {{ background: {t['surface']}; border-right: 2px solid {t['border']}; }}
[data-testid="stSidebar"] h3 {{ color: {t['text']} !important; font-weight: 700 !important; }}
[data-testid="stSidebar"] label {{ color: {t['text']} !important; }}

.stDataFrame {{ 
    border: 2px solid {t['border']}; border-radius: 16px; overflow: hidden; 
    animation: fadeInUp 1s ease;
}}

#MainMenu, footer, header {{ visibility: hidden; }}
</style>
""", unsafe_allow_html=True)

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

# Sidebar
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    
    st.markdown("**🎨 Theme**")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🌞 Light", key="light_theme", use_container_width=True,
                    type="primary" if st.session_state.theme == 'light' else "secondary"):
            st.session_state.theme = 'light'
            st.rerun()
    
    with col2:
        if st.button("🌙 Dark", key="dark_theme", use_container_width=True,
                    type="primary" if st.session_state.theme == 'dark' else "secondary"):
            st.session_state.theme = 'dark'
            st.rerun()
    
    current = "🌞 Light Mode" if st.session_state.theme == 'light' else "🌙 Dark Mode"
    st.caption(f"Active: **{current}**")
    
    st.markdown("---")
    st.markdown("### 📅 Time Range")
    time_range = st.selectbox("Period", ["Last 7 Days", "Last 30 Days", "Last 90 Days", "All Time"])
    
    st.markdown("---")
    st.markdown("### 🔍 Filters")
    
    data_source = st.radio("Data", ["CSV", "MySQL"], horizontal=True)
    filter_status = st.selectbox("Status", ["All", "Active Only", "At Risk Only"])
    min_score = st.slider("Min Score", 0.0, 10.0, 0.0)
    search_id = st.text_input("Search", placeholder="S007")
    
    st.markdown("---")
    st.markdown("### 🔔 Alerts")
    alert_threshold = st.slider("At-Risk Threshold", 0.0, 10.0, 5.0, 0.5)
    
    st.markdown("---")
    st.markdown("### 📊 Display")
    show_charts = st.checkbox("Show Charts", value=True)
    chart_height = st.slider("Height", 300, 600, 400, 50)
    
    st.markdown("---")
    st.info(f"📅 {datetime.now().strftime('%b %d, %Y at %I:%M %p')}")

@st.cache_resource
def load_model():
    try: return joblib.load('isolation_forest.pkl')
    except: return None

@st.cache_data
def load_data():
    try: return pd.read_csv('student_engagement.csv')
    except: return None

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
    
    df['custom_risk'] = df['engagement_score'] < alert_threshold
    
    # Anchor points for scrolling
    st.markdown('<div id="dashboard"></div>', unsafe_allow_html=True)
    st.markdown("## 📊 Dashboard Overview")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        if st.button(f"**Total Students**\n\n{len(df)}", key="metric1", use_container_width=True):
            st.markdown('<script>document.getElementById("data-table").scrollIntoView({behavior: "smooth"});</script>', unsafe_allow_html=True)
        st.caption("👆 Click to view all students")
    
    with col2:
        anomaly_count = (df['anomaly'] == -1).sum()
        if st.button(f"**AI At Risk**\n\n{anomaly_count}", key="metric2", use_container_width=True):
            st.session_state.filter_status = "At Risk Only"
        st.caption(f"{(anomaly_count/len(df)*100):.0f}% of total")
    
    with col3:
        custom_risk = df['custom_risk'].sum()
        if st.button(f"**Below Threshold**\n\n{custom_risk}", key="metric3", use_container_width=True):
            pass
        st.caption(f"{(custom_risk/len(df)*100):.0f}% flagged")
    
    with col4:
        avg_score = df['engagement_score'].mean()
        if st.button(f"**Avg Engagement**\n\n{avg_score:.2f}", key="metric4", use_container_width=True):
            pass
        st.caption("↑ +0.3 from last week")
    
    with col5:
        avg_time = df['time_spent'].mean()
        if st.button(f"**Avg Time**\n\n{avg_time:.0f}h", key="metric5", use_container_width=True):
            pass
        st.caption("↑ +2.3 hours")
    
    # Quick Insights
    st.markdown("## 📈 Quick Insights")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        top_student = df.loc[df['engagement_score'].idxmax()]
        st.info(f"**🎯 Top Performer**\n\n{top_student['student_id']} - {top_student['engagement_score']:.2f}")
    
    with col2:
        bottom_student = df.loc[df['engagement_score'].idxmin()]
        st.warning(f"**⚠️ Needs Attention**\n\n{bottom_student['student_id']} - {bottom_student['engagement_score']:.2f}")
    
    with col3:
        active_pct = ((df['anomaly_flag'] == 'Active').sum() / len(df) * 100)
        active_count = (df['anomaly_flag'] == 'Active').sum()
        st.success(f"**✅ Active Rate**\n\n{active_pct:.1f}% ({active_count} students)")
    
    if show_charts:
        st.markdown("## 📈 Visual Analytics")
        
        # 4 TABS
        tab1, tab2, tab3, tab4 = st.tabs([
            "📊 Distribution", 
            "🔍 Anomaly Detection", 
            "📈 Activity Metrics",
            "🎯 Performance Analysis"
        ])
        
        with tab1:
            col1, col2 = st.columns(2)
            
            with col1:
                fig1 = px.histogram(df, x='engagement_score', nbins=20, 
                                  title='📊 Engagement Score Distribution')
                fig1.update_layout(plot_bgcolor='white', paper_bgcolor='white', height=chart_height)
                fig1.update_traces(marker_color='#1a73e8')
                st.plotly_chart(fig1, use_container_width=True)
            
            with col2:
                counts = df['anomaly_flag'].value_counts()
                fig2 = px.pie(values=counts.values, names=counts.index, 
                            title='🥧 Student Status', hole=0.4)
                fig2.update_layout(plot_bgcolor='white', paper_bgcolor='white', height=chart_height)
                fig2.update_traces(marker=dict(colors=['#34a853', '#ea4335']))
                st.plotly_chart(fig2, use_container_width=True)
        
        with tab2:
            fig3 = px.scatter(df, x='time_spent', y='engagement_score', color='anomaly_flag',
                            size='login_count', hover_data=['student_id'], 
                            title='🔍 Time Spent vs Engagement Score',
                            color_discrete_map={'Active': '#34a853', 'At Risk': '#ea4335'})
            fig3.update_layout(plot_bgcolor='white', paper_bgcolor='white', height=chart_height)
            st.plotly_chart(fig3, use_container_width=True)
        
        with tab3:
            # Login Count Analysis
            fig4 = px.bar(df.nlargest(15, 'login_count'), x='student_id', y='login_count',
                        title='📈 Top 15 Students by Login Count',
                        color='login_count', color_continuous_scale='Blues')
            fig4.update_layout(plot_bgcolor='white', paper_bgcolor='white', height=chart_height)
            st.plotly_chart(fig4, use_container_width=True)
        
        with tab4:
            # Quiz vs Assignment Performance
            fig5 = px.scatter(df, x='quiz_attempts', y='assignment_score',
                            size='engagement_score', color='anomaly_flag',
                            hover_data=['student_id'],
                            title='🎯 Quiz Attempts vs Assignment Score',
                            color_discrete_map={'Active': '#34a853', 'At Risk': '#ea4335'})
            fig5.update_layout(plot_bgcolor='white', paper_bgcolor='white', height=chart_height)
            st.plotly_chart(fig5, use_container_width=True)
    
    # Data Table with anchor
    st.markdown('<div id="data-table"></div>', unsafe_allow_html=True)
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
    
    csv = filtered.to_csv(index=False).encode('utf-8')
    st.download_button(
        f"📥 Download {len(filtered)} Records",
        csv,
        f'engagesense_{datetime.now().strftime("%Y%m%d_%H%M")}.csv',
        'text/csv',
        use_container_width=True
    )

else:
    st.error("❌ Failed to load data")

st.markdown(f"""
<div style="margin-top: 4rem; padding: 3rem; text-align: center; background: {t['surface']};
     border-radius: 24px; border: 2px solid {t['border']}; animation: fadeInUp 1.2s ease;">
    <h2 style="color: #1a73e8; margin: 0 0 1rem 0; font-size: 1.75rem; border: none; padding: 0;">📊 EngageSense</h2>
    <p style="color: {t['text']}; font-size: 1.125rem;">By <strong style="color: #1a73e8;">Suraj Maurya</strong></p>
    <p style="color: {t['secondary']}; font-size: 1rem; margin: 1rem 0;">🤖 AI · 📊 ML · 🐍 Python · ⚡ Streamlit</p>
    <p style="color: {t['secondary']}; font-size: 0.875rem;">© 2025 All Rights Reserved</p>
</div>
""", unsafe_allow_html=True)
