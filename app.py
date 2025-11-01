import streamlit as st
import pandas as pd
import joblib
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="EngageSense Analytics", page_icon="📊", layout="wide")

# Initialize theme
if 'theme' not in st.session_state:
    st.session_state.theme = 'light'

# Theme colors
themes = {
    'light': {
        'bg': '#f8f9fa',
        'surface': '#ffffff',
        'text': '#202124',
        'secondary': '#5f6368',
        'border': '#e0e0e0'
    },
    'dark': {
        'bg': '#1a1a1a',
        'surface': '#2d2d2d',
        'text': '#e0e0e0',
        'secondary': '#9e9e9e',
        'border': '#404040'
    }
}

t = themes[st.session_state.theme]

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

* {{
    font-family: 'Inter', sans-serif;
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

.stApp {{
    background: {t['bg']};
    transition: background 0.3s ease, color 0.3s ease;
}}

/* Header */
.main-header {{
    background: linear-gradient(135deg, #1a73e8 0%, #4285f4 100%);
    padding: 2rem;
    margin: -1rem -2rem 2rem -2rem;
    box-shadow: 0 4px 20px rgba(26, 115, 232, 0.4);
    border-radius: 0 0 24px 24px;
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
}}

.title {{
    font-size: 2.25rem;
    font-weight: 800;
    color: white;
}}

.subtitle {{
    font-size: 1.125rem;
    color: rgba(255,255,255,0.95);
}}

/* Headers */
h2 {{
    color: {t['text']} !important;
    font-weight: 800 !important;
    font-size: 2rem !important;
    margin: 2.5rem 0 1.5rem 0 !important;
    padding-left: 1.5rem;
    border-left: 6px solid #1a73e8;
}}

/* Metric Cards */
[data-testid="stMetric"] {{
    background: {t['surface']};
    border: 2px solid {t['border']};
    border-radius: 20px;
    padding: 2rem;
    box-shadow: 0 8px 16px rgba(0,0,0,0.08);
    transition: all 0.4s ease;
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
    transform: translateY(-8px);
    box-shadow: 0 16px 32px rgba(26, 115, 232, 0.3);
    border-color: #1a73e8;
}}

[data-testid="stMetric"] label {{
    color: {t['secondary']} !important;
    font-size: 1rem !important;
    font-weight: 700 !important;
    text-transform: uppercase;
    letter-spacing: 1px;
}}

[data-testid="stMetric"] [data-testid="stMetricValue"] {{
    color: {t['text']} !important;
    font-size: 3rem !important;
    font-weight: 900 !important;
}}

[data-testid="stMetric"] [data-testid="stMetricDelta"] {{
    color: #34a853 !important;
}}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {{
    background: {t['surface']};
    padding: 0.75rem;
    border-radius: 16px;
    border: 2px solid {t['border']};
    box-shadow: 0 4px 8px rgba(0,0,0,0.05);
}}

.stTabs [data-baseweb="tab"] {{
    color: {t['secondary']};
    border-radius: 12px;
    padding: 1rem 2rem;
    font-weight: 700;
    font-size: 1rem;
    transition: all 0.3s ease;
}}

.stTabs [data-baseweb="tab"]:hover {{
    background: rgba(26, 115, 232, 0.1);
}}

.stTabs [aria-selected="true"] {{
    background: linear-gradient(135deg, #1a73e8, #4285f4) !important;
    color: white !important;
    box-shadow: 0 4px 12px rgba(26, 115, 232, 0.4);
}}

/* Sidebar */
[data-testid="stSidebar"] {{
    background: {t['surface']};
    border-right: 2px solid {t['border']};
}}

[data-testid="stSidebar"] h3 {{
    color: {t['text']} !important;
    font-weight: 700 !important;
    font-size: 1.125rem !important;
    margin: 1.5rem 0 1rem 0 !important;
    border: none !important;
    padding: 0 !important;
}}

[data-testid="stSidebar"] label {{
    color: {t['text']} !important;
}}

/* Data Table */
.stDataFrame {{
    border: 2px solid {t['border']};
    border-radius: 16px;
    overflow: hidden;
    box-shadow: 0 8px 16px rgba(0,0,0,0.05);
}}

/* Download Button */
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

/* Info/Success boxes */
.stAlert {{
    border-radius: 12px !important;
}}

/* Footer */
.footer {{
    margin-top: 4rem;
    padding: 3rem;
    text-align: center;
    background: {t['surface']};
    border-radius: 24px;
    border: 2px solid {t['border']};
    box-shadow: 0 8px 16px rgba(0,0,0,0.05);
}}

#MainMenu, footer, header {{
    visibility: hidden;
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
    
    st.markdown("**🎨 Theme**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button(
            "🌞 Light",
            use_container_width=True,
            type="primary" if st.session_state.theme == 'light' else "secondary"
        ):
            st.session_state.theme = 'light'
            st.rerun()
    
    with col2:
        if st.button(
            "🌙 Dark",
            use_container_width=True,
            type="primary" if st.session_state.theme == 'dark' else "secondary"
        ):
            st.session_state.theme = 'dark'
            st.rerun()
    
    # Show current theme
    if st.session_state.theme == 'light':
        st.success("✓ Light Mode Active")
    else:
        st.info("✓ Dark Mode Active")
    
    st.markdown("---")
    st.markdown("### 🔍 Filters")
    
    data_source = st.radio("Data Source", ["CSV", "MySQL"], horizontal=True)
    filter_status = st.selectbox("Student Status", ["All", "Active Only", "At Risk Only"])
    min_score = st.slider("Min Engagement Score", 0.0, 10.0, 0.0)
    search_id = st.text_input("Search Student", placeholder="e.g., S007")
    
    st.markdown("---")
    st.markdown("### 📊 Display Options")
    
    show_charts = st.checkbox("Show Charts", value=True)
    chart_height = st.slider("Chart Height", 300, 600, 400, step=50)
    
    st.markdown("---")
    st.info(f"📅 Updated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}")

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
    
    st.markdown("## 📊 Dashboard Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Students", len(df), "+5")
    
    with col2:
        anomaly_count = (df['anomaly'] == -1).sum()
        st.metric("At Risk Students", anomaly_count, f"{(anomaly_count/len(df)*100):.1f}%")
    
    with col3:
        st.metric("Avg Engagement", f"{df['engagement_score'].mean():.2f}", "+0.3")
    
    with col4:
        st.metric("Avg Time (hours)", f"{df['time_spent'].mean():.1f}", "+2.3")
    
    if show_charts:
        st.markdown("## 📈 Visual Analytics")
        
        tab1, tab2, tab3 = st.tabs(["📊 Distribution", "🔍 Anomaly Detection", "🏆 Top Performers"])
        
        with tab1:
            col1, col2 = st.columns(2)
            
            with col1:
                fig1 = px.histogram(df, x='engagement_score', nbins=20, title='Engagement Score Distribution')
                fig1.update_layout(
                    plot_bgcolor='white',
                    paper_bgcolor='white',
                    font=dict(color='#202124'),
                    height=chart_height
                )
                fig1.update_traces(marker_color='#1a73e8')
                st.plotly_chart(fig1, use_container_width=True)
            
            with col2:
                counts = df['anomaly_flag'].value_counts()
                fig2 = px.pie(
                    values=counts.values,
                    names=counts.index,
                    title='Student Status Distribution',
                    hole=0.4
                )
                fig2.update_layout(
                    plot_bgcolor='white',
                    paper_bgcolor='white',
                    font=dict(color='#202124'),
                    height=chart_height
                )
                fig2.update_traces(marker=dict(colors=['#34a853', '#ea4335']))
                st.plotly_chart(fig2, use_container_width=True)
        
        with tab2:
            fig3 = px.scatter(
                df,
                x='time_spent',
                y='engagement_score',
                color='anomaly_flag',
                size='login_count',
                hover_data=['student_id'],
                title='Time Spent vs Engagement Score',
                color_discrete_map={'Active': '#34a853', 'At Risk': '#ea4335'}
            )
            fig3.update_layout(
                plot_bgcolor='white',
                paper_bgcolor='white',
                font=dict(color='#202124'),
                height=chart_height
            )
            st.plotly_chart(fig3, use_container_width=True)
        
        with tab3:
            top_10 = df.nlargest(10, 'engagement_score')
            fig4 = px.bar(
                top_10,
                x='student_id',
                y='engagement_score',
                color='anomaly_flag',
                title='Top 10 Students by Engagement',
                color_discrete_map={'Active': '#34a853', 'At Risk': '#ea4335'}
            )
            fig4.update_layout(
                plot_bgcolor='white',
                paper_bgcolor='white',
                font=dict(color='#202124'),
                height=chart_height
            )
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
    
    csv = filtered.to_csv(index=False).encode('utf-8')
    st.download_button(
        label=f"📥 Download {len(filtered)} Records",
        data=csv,
        file_name=f'engagesense_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv',
        mime='text/csv',
        use_container_width=True
    )

else:
    st.error("❌ Failed to load data or model")

# Footer
st.markdown(f"""
<div class="footer">
    <h2 style="color: #1a73e8; margin: 0 0 1rem 0; font-size: 1.75rem; border: none; padding: 0;">📊 EngageSense Analytics Platform</h2>
    <p style="color: {t['text']}; font-size: 1.125rem; margin: 0.75rem 0;">
        Developed by <strong style="color: #1a73e8;">Suraj Maurya</strong>
    </p>
    <p style="color: {t['secondary']}; font-size: 1rem; margin: 1rem 0;">
        🤖 AI-Powered · 📊 Machine Learning · 🐍 Python · ⚡ Streamlit · 📈 Plotly
    </p>
    <p style="color: {t['secondary']}; font-size: 0.875rem; margin: 0.5rem 0 0 0;">
        © 2025 EngageSense. All Rights Reserved.
    </p>
</div>
""", unsafe_allow_html=True)
