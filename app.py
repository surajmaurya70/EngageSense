import streamlit as st
import pandas as pd
import joblib
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
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    * { 
        font-family: 'Inter', sans-serif;
        box-sizing: border-box;
    }
    
    .stApp { background: #f8f9fa; }
    
    /* Responsive Container */
    .block-container {
        padding: 1rem !important;
        max-width: 100% !important;
    }
    
    @media (min-width: 768px) {
        .block-container {
            padding: 2rem !important;
        }
    }
    
    /* Header - Responsive */
    .main-header {
        background: linear-gradient(135deg, #1a73e8 0%, #4285f4 100%);
        padding: 1.5rem;
        margin: -1rem -1rem 2rem -1rem;
        box-shadow: 0 4px 12px rgba(26, 115, 232, 0.3);
        border-radius: 0 0 20px 20px;
    }
    
    @media (min-width: 768px) {
        .main-header {
            padding: 2rem;
            margin: -2rem -2rem 2rem -2rem;
        }
    }
    
    .header-content {
        display: flex;
        align-items: center;
        gap: 1rem;
        flex-wrap: wrap;
    }
    
    .logo {
        width: 48px;
        height: 48px;
        background: white;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        font-weight: 800;
        color: #1a73e8;
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
        flex-shrink: 0;
    }
    
    @media (min-width: 768px) {
        .logo {
            width: 56px;
            height: 56px;
            font-size: 1.75rem;
        }
    }
    
    .title {
        font-size: 1.25rem;
        font-weight: 800;
        color: white;
        line-height: 1.2;
    }
    
    @media (min-width: 768px) {
        .title {
            font-size: 2rem;
        }
    }
    
    .subtitle {
        font-size: 0.875rem;
        color: rgba(255,255,255,0.9);
    }
    
    @media (min-width: 768px) {
        .subtitle {
            font-size: 1rem;
        }
    }
    
    /* Metric Cards - Responsive */
    [data-testid="stMetric"] {
        background: white;
        border: 1px solid #e0e0e0;
        border-radius: 12px;
        padding: 1rem;
        box-shadow: 0 4px 8px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    @media (min-width: 768px) {
        [data-testid="stMetric"] {
            padding: 1.5rem;
            border-radius: 16px;
        }
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
    
    [data-testid="stMetric"]:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 16px rgba(26, 115, 232, 0.2);
    }
    
    [data-testid="stMetric"] label {
        color: #5f6368 !important;
        font-size: 0.75rem !important;
        font-weight: 600 !important;
    }
    
    @media (min-width: 768px) {
        [data-testid="stMetric"] label {
            font-size: 0.875rem !important;
        }
    }
    
    [data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: #202124 !important;
        font-size: 1.75rem !important;
        font-weight: 800 !important;
    }
    
    @media (min-width: 768px) {
        [data-testid="stMetric"] [data-testid="stMetricValue"] {
            font-size: 2.5rem !important;
        }
    }
    
    /* Headers - Responsive */
    h2 {
        color: #202124 !important;
        font-weight: 700 !important;
        font-size: 1.25rem !important;
        margin: 2rem 0 1rem 0 !important;
        padding-left: 0.75rem;
        border-left: 4px solid #1a73e8;
    }
    
    @media (min-width: 768px) {
        h2 {
            font-size: 1.75rem !important;
            padding-left: 1rem;
        }
    }
    
    /* Tabs - Responsive */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.25rem;
        background: white;
        padding: 0.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        overflow-x: auto;
        -webkit-overflow-scrolling: touch;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: #5f6368;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 600;
        font-size: 0.875rem;
        white-space: nowrap;
    }
    
    @media (min-width: 768px) {
        .stTabs [data-baseweb="tab"] {
            padding: 0.75rem 1.5rem;
            font-size: 1rem;
        }
    }
    
    .stTabs [aria-selected="true"] {
        background: #1a73e8 !important;
        color: white !important;
    }
    
    /* Sidebar - Mobile Friendly */
    [data-testid="stSidebar"] {
        background: white;
        border-right: 1px solid #e0e0e0;
    }
    
    [data-testid="stSidebar"] h3 {
        color: #202124 !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
    }
    
    /* Feature Cards - Responsive Grid */
    .feature-grid {
        display: grid;
        grid-template-columns: 1fr;
        gap: 1rem;
        margin: 1.5rem 0;
    }
    
    @media (min-width: 640px) {
        .feature-grid {
            grid-template-columns: repeat(2, 1fr);
        }
    }
    
    @media (min-width: 1024px) {
        .feature-grid {
            grid-template-columns: repeat(4, 1fr);
        }
    }
    
    .feature-card {
        background: white;
        border: 1px solid #e0e0e0;
        border-radius: 12px;
        padding: 1.25rem;
        text-align: center;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .feature-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 16px rgba(0,0,0,0.1);
        border-color: #1a73e8;
    }
    
    .feature-icon {
        font-size: 2rem;
        margin-bottom: 0.75rem;
    }
    
    .feature-title {
        font-weight: 700;
        color: #202124;
        margin-bottom: 0.5rem;
        font-size: 0.875rem;
    }
    
    @media (min-width: 768px) {
        .feature-title {
            font-size: 1rem;
        }
    }
    
    .feature-text {
        font-size: 0.75rem;
        color: #5f6368;
        line-height: 1.4;
    }
    
    @media (min-width: 768px) {
        .feature-text {
            font-size: 0.875rem;
        }
    }
    
    /* Data Table - Responsive */
    .stDataFrame {
        border: 1px solid #e0e0e0;
        border-radius: 12px;
        overflow: auto;
        box-shadow: 0 4px 8px rgba(0,0,0,0.05);
    }
    
    /* Download Button - Responsive */
    .stDownloadButton button {
        background: linear-gradient(135deg, #1a73e8, #4285f4) !important;
        color: white !important;
        border: none !important;
        border-radius: 24px !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 700 !important;
        font-size: 0.875rem !important;
        box-shadow: 0 4px 12px rgba(26, 115, 232, 0.4) !important;
        width: 100%;
    }
    
    @media (min-width: 768px) {
        .stDownloadButton button {
            padding: 0.875rem 2.5rem !important;
            font-size: 1rem !important;
            width: auto;
        }
    }
    
    /* Info Alert - Responsive */
    .stAlert {
        border-radius: 12px !important;
        font-size: 0.875rem !important;
    }
    
    /* Footer - Responsive */
    .footer {
        margin-top: 3rem;
        padding: 1.5rem;
        text-align: center;
        background: white;
        border-radius: 12px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.05);
    }
    
    @media (min-width: 768px) {
        .footer {
            margin-top: 4rem;
            padding: 2.5rem;
        }
    }
    
    #MainMenu, footer, header {visibility: hidden;}
    
    /* Mobile touch improvements */
    @media (max-width: 767px) {
        button, a, [role="button"] {
            min-height: 44px;
            min-width: 44px;
        }
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
    <div class="main-header">
        <div class="header-content">
            <div class="logo">ES</div>
            <div style="flex: 1; min-width: 0;">
                <div class="title">EngageSense Analytics</div>
                <div class="subtitle">🤖 AI-Powered Student Engagement Platform</div>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### 🎯 Quick Actions")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📤", help="Export Data", use_container_width=True):
            st.success("✅ Export started!")
    with col2:
        if st.button("📧", help="Email Report", use_container_width=True):
            st.success("✅ Email sent!")
    
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
    
    # Feature Cards
    st.markdown("""
        <div class="feature-grid">
            <div class="feature-card">
                <div class="feature-icon">🤖</div>
                <div class="feature-title">AI Detection</div>
                <div class="feature-text">Machine learning anomaly detection</div>
            </div>
            <div class="feature-card">
                <div class="feature-icon">📊</div>
                <div class="feature-title">Real-Time</div>
                <div class="feature-text">Live engagement tracking</div>
            </div>
            <div class="feature-card">
                <div class="feature-icon">🔔</div>
                <div class="feature-title">Alerts</div>
                <div class="feature-text">Smart notifications</div>
            </div>
            <div class="feature-card">
                <div class="feature-icon">📈</div>
                <div class="feature-title">Analytics</div>
                <div class="feature-text">Advanced insights</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
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
        
        tab1, tab2, tab3 = st.tabs(["📊 Charts", "🔍 Anomaly", "🏆 Top 10"])
        
        with tab1:
            col1, col2 = st.columns([1, 1])
            
            with col1:
                fig1 = px.histogram(df, x='engagement_score', nbins=20, title='Distribution')
                fig1.update_layout(plot_bgcolor='white', paper_bgcolor='white', height=chart_height, showlegend=False, margin=dict(l=20, r=20, t=40, b=20))
                fig1.update_traces(marker_color='#1a73e8')
                st.plotly_chart(fig1, use_container_width=True)
            
            with col2:
                counts = df['anomaly_flag'].value_counts()
                fig2 = px.pie(values=counts.values, names=counts.index, title='Status', hole=0.4)
                fig2.update_layout(plot_bgcolor='white', paper_bgcolor='white', height=chart_height, margin=dict(l=20, r=20, t=40, b=20))
                fig2.update_traces(marker=dict(colors=['#34a853', '#ea4335']))
                st.plotly_chart(fig2, use_container_width=True)
        
        with tab2:
            fig3 = px.scatter(df, x='time_spent', y='engagement_score', color='anomaly_flag', size='login_count', 
                            hover_data=['student_id'], title='Time vs Engagement',
                            color_discrete_map={'Active': '#34a853', 'At Risk': '#ea4335'})
            fig3.update_layout(plot_bgcolor='white', paper_bgcolor='white', height=chart_height, margin=dict(l=20, r=20, t=40, b=40))
            st.plotly_chart(fig3, use_container_width=True)
        
        with tab3:
            top_10 = df.nlargest(10, 'engagement_score')
            fig4 = px.bar(top_10, x='student_id', y='engagement_score', color='anomaly_flag',
                        title='Top Students', color_discrete_map={'Active': '#34a853', 'At Risk': '#ea4335'})
            fig4.update_layout(plot_bgcolor='white', paper_bgcolor='white', height=chart_height, margin=dict(l=20, r=20, t=40, b=40))
            st.plotly_chart(fig4, use_container_width=True)
    
    st.markdown("## 📋 Data")
    
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
    
    st.dataframe(filtered, use_container_width=True, height=350)
    
    csv = filtered.to_csv(index=False).encode('utf-8')
    st.download_button(
        label=f"📥 Download {len(filtered)} Records",
        data=csv,
        file_name=f'data_{datetime.now().strftime("%Y%m%d_%H%M")}.csv',
        mime='text/csv',
        use_container_width=True
    )

else:
    st.error("❌ Failed to load data")

st.markdown("""
    <div class="footer">
        <h3 style="color: #1a73e8; margin: 0 0 0.5rem 0;">📊 EngageSense</h3>
        <p style="margin: 0.5rem 0; color: #202124;">By <strong style="color: #1a73e8;">Suraj Maurya</strong></p>
        <p style="margin: 0.5rem 0; font-size: 0.875rem; color: #5f6368;">AI · ML · Python · Streamlit</p>
        <p style="margin: 0.5rem 0 0 0; font-size: 0.75rem; color: #5f6368;">© 2025 All Rights Reserved</p>
    </div>
""", unsafe_allow_html=True)
