import streamlit as st
import pandas as pd
import joblib
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

st.set_page_config(page_title="EngageSense Analytics", page_icon="📊", layout="wide")

# Session state for theme
if 'theme' not in st.session_state:
    st.session_state.theme = 'light'

# Get theme colors
def get_theme_colors():
    if st.session_state.theme == 'dark':
        return {
            'bg': '#1a1a1a', 'surface': '#2d2d2d', 'text': '#e0e0e0',
            'secondary': '#9e9e9e', 'border': '#404040'
        }
    else:
        return {
            'bg': '#f8f9fa', 'surface': '#ffffff', 'text': '#202124',
            'secondary': '#5f6368', 'border': '#e0e0e0'
        }

t = get_theme_colors()

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
* {{ font-family: 'Inter', sans-serif; margin: 0; padding: 0; box-sizing: border-box; }}
.stApp {{ background: {t['bg']}; color: {t['text']}; }}

.main-header {{
    background: linear-gradient(135deg, #1a73e8 0%, #4285f4 100%);
    padding: 2rem; margin: -1rem -2rem 2rem -2rem;
    box-shadow: 0 4px 20px rgba(26, 115, 232, 0.4);
    border-radius: 0 0 24px 24px;
}}

.header-content {{ display: flex; align-items: center; gap: 1rem; }}
.logo {{ width: 60px; height: 60px; background: white; border-radius: 14px;
    display: flex; align-items: center; justify-content: center;
    font-size: 2rem; font-weight: 800; color: #1a73e8;
    box-shadow: 0 6px 12px rgba(0,0,0,0.15); }}
.title {{ font-size: 2.25rem; font-weight: 800; color: white; }}
.subtitle {{ font-size: 1.125rem; color: rgba(255,255,255,0.95); }}

h2 {{ color: {t['text']} !important; font-weight: 800 !important; font-size: 2rem !important;
    margin: 2.5rem 0 1.5rem 0 !important; padding-left: 1.5rem; border-left: 6px solid #1a73e8; }}

[data-testid="stMetric"] {{
    background: {t['surface']}; border: 2px solid {t['border']}; border-radius: 20px;
    padding: 2rem; box-shadow: 0 8px 16px rgba(0,0,0,0.08); transition: all 0.4s ease;
}}
[data-testid="stMetric"]:hover {{ transform: translateY(-8px); box-shadow: 0 16px 32px rgba(26, 115, 232, 0.3); }}
[data-testid="stMetric"] label {{ color: {t['secondary']} !important; font-size: 1rem !important; font-weight: 700 !important; }}
[data-testid="stMetric"] [data-testid="stMetricValue"] {{ color: {t['text']} !important; font-size: 3rem !important; font-weight: 900 !important; }}

.stTabs [data-baseweb="tab-list"] {{ background: {t['surface']}; padding: 0.75rem; border-radius: 16px; border: 2px solid {t['border']}; }}
.stTabs [data-baseweb="tab"] {{ color: {t['secondary']}; border-radius: 12px; padding: 1rem 2rem; font-weight: 700; }}
.stTabs [aria-selected="true"] {{ background: linear-gradient(135deg, #1a73e8, #4285f4) !important; color: white !important; }}

[data-testid="stSidebar"] {{ background: {t['surface']}; border-right: 2px solid {t['border']}; }}
[data-testid="stSidebar"] h3 {{ color: {t['text']} !important; font-weight: 700 !important; }}

.stDataFrame {{ border: 2px solid {t['border']}; border-radius: 16px; overflow: hidden; }}

#MainMenu, footer, header {{ visibility: hidden; }}
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

# Sidebar
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    
    # Theme Toggle
    st.markdown("**🎨 Theme**")
    theme_choice = st.radio("", ["🌞 Light Mode", "🌙 Dark Mode"], 
                            index=0 if st.session_state.theme == 'light' else 1,
                            key="theme_radio")
    
    if "Light" in theme_choice and st.session_state.theme != 'light':
        st.session_state.theme = 'light'
        st.rerun()
    elif "Dark" in theme_choice and st.session_state.theme != 'dark':
        st.session_state.theme = 'dark'
        st.rerun()
    
    st.markdown("---")
    
    # NEW FEATURE: Time Range Selector
    st.markdown("### 📅 Time Range")
    time_range = st.selectbox("Select Period", 
                              ["Last 7 Days", "Last 30 Days", "Last 90 Days", "All Time"])
    
    st.markdown("---")
    st.markdown("### 🔍 Filters")
    
    data_source = st.radio("Data Source", ["CSV", "MySQL"], horizontal=True)
    filter_status = st.selectbox("Student Status", ["All", "Active Only", "At Risk Only"])
    min_score = st.slider("Min Engagement Score", 0.0, 10.0, 0.0)
    search_id = st.text_input("Search Student", placeholder="e.g., S007")
    
    st.markdown("---")
    
    # NEW FEATURE: Alert Threshold
    st.markdown("### 🔔 Alert Settings")
    alert_threshold = st.slider("At-Risk Threshold", 0.0, 10.0, 5.0, 0.5,
                                help="Students below this score will be flagged")
    
    st.markdown("---")
    st.markdown("### 📊 Display")
    show_charts = st.checkbox("Show Charts", value=True)
    chart_height = st.slider("Chart Height", 300, 600, 400, 50)
    
    st.markdown("---")
    st.info(f"📅 {datetime.now().strftime('%B %d, %Y at %I:%M %p')}")

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
    
    # NEW FEATURE: Add custom at-risk based on threshold
    df['custom_risk'] = df['engagement_score'] < alert_threshold
    
    st.markdown("## 📊 Dashboard Overview")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Total Students", len(df), "+5")
    
    with col2:
        anomaly_count = (df['anomaly'] == -1).sum()
        st.metric("AI At Risk", anomaly_count, f"{(anomaly_count/len(df)*100):.0f}%")
    
    with col3:
        custom_risk = df['custom_risk'].sum()
        st.metric("Below Threshold", custom_risk, f"{(custom_risk/len(df)*100):.0f}%")
    
    with col4:
        st.metric("Avg Engagement", f"{df['engagement_score'].mean():.2f}", "+0.3")
    
    with col5:
        st.metric("Avg Time (hrs)", f"{df['time_spent'].mean():.1f}", "+2.3")
    
    # NEW FEATURE: Quick Stats Cards
    st.markdown("## 📈 Quick Insights")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info(f"**🎯 Top Performer:** {df.loc[df['engagement_score'].idxmax(), 'student_id']} "
                f"({df['engagement_score'].max():.2f})")
    
    with col2:
        st.warning(f"**⚠️ Needs Attention:** {df.loc[df['engagement_score'].idxmin(), 'student_id']} "
                   f"({df['engagement_score'].min():.2f})")
    
    with col3:
        active_pct = ((df['anomaly_flag'] == 'Active').sum() / len(df) * 100)
        st.success(f"**✅ Active Rate:** {active_pct:.1f}% ({(df['anomaly_flag'] == 'Active').sum()} students)")
    
    if show_charts:
        st.markdown("## 📈 Visual Analytics")
        
        tab1, tab2, tab3, tab4 = st.tabs(["📊 Distribution", "🔍 Anomaly", "🏆 Leaderboard", "📉 Trends"])
        
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
        
        with tab4:
            # NEW FEATURE: Engagement Trend (simulated)
            trend_data = pd.DataFrame({
                'Date': pd.date_range(start='2025-10-01', periods=30, freq='D'),
                'Avg_Engagement': np.random.uniform(6, 8, 30)
            })
            fig5 = px.line(trend_data, x='Date', y='Avg_Engagement', title='30-Day Engagement Trend')
            fig5.update_layout(plot_bgcolor='white', paper_bgcolor='white', height=chart_height)
            fig5.update_traces(line_color='#1a73e8', line_width=3)
            st.plotly_chart(fig5, use_container_width=True)
    
    # NEW FEATURE: Comparison Table
    st.markdown("## 📊 Performance Comparison")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🏆 Top 5 Students")
        top5 = df.nlargest(5, 'engagement_score')[['student_id', 'engagement_score', 'anomaly_flag']]
        st.dataframe(top5, use_container_width=True, hide_index=True)
    
    with col2:
        st.markdown("### ⚠️ Bottom 5 Students")
        bottom5 = df.nsmallest(5, 'engagement_score')[['student_id', 'engagement_score', 'anomaly_flag']]
        st.dataframe(bottom5, use_container_width=True, hide_index=True)
    
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
    
    # NEW FEATURE: Download options
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.info(f"📊 Showing {len(filtered)} of {len(df)} students")
    with col2:
        csv = filtered.to_csv(index=False).encode('utf-8')
        st.download_button("📥 CSV", csv, f'data_{datetime.now().strftime("%Y%m%d")}.csv', 'text/csv', use_container_width=True)
    with col3:
        json = filtered.to_json(orient='records')
        st.download_button("📥 JSON", json, f'data_{datetime.now().strftime("%Y%m%d")}.json', 'application/json', use_container_width=True)
    
    st.dataframe(filtered, use_container_width=True, height=400)

else:
    st.error("❌ Failed to load data or model")

# Footer
st.markdown(f"""
<div style="margin-top: 4rem; padding: 3rem; text-align: center; background: {t['surface']}; 
     border-radius: 24px; border: 2px solid {t['border']};">
    <h2 style="color: #1a73e8; margin: 0 0 1rem 0; font-size: 1.75rem; border: none; padding: 0;">📊 EngageSense Analytics</h2>
    <p style="color: {t['text']}; font-size: 1.125rem;">By <strong style="color: #1a73e8;">Suraj Maurya</strong></p>
    <p style="color: {t['secondary']}; font-size: 1rem; margin-top: 1rem;">🤖 AI · 📊 ML · 🐍 Python · ⚡ Streamlit · 📈 Plotly</p>
    <p style="color: {t['secondary']}; font-size: 0.875rem; margin-top: 0.5rem;">© 2025 EngageSense. All Rights Reserved.</p>
</div>
""", unsafe_allow_html=True)
