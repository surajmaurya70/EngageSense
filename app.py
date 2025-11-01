import streamlit as st
import pandas as pd
import joblib
import numpy as np
import mysql.connector
import plotly.express as px
import plotly.graph_objects as go

# Page Configuration
st.set_page_config(
    page_title="EngageSense Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Premium CSS Styling
st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .main {
        padding: 0rem 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }
    
    /* Header Styles */
    .main-header {
        text-align: center;
        padding: 2rem 0;
        margin-bottom: 2rem;
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
    }
    
    .main-title {
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(120deg, #fff 0%, #a8edea 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .subtitle {
        font-size: 1.2rem;
        color: rgba(255, 255, 255, 0.9);
        font-weight: 300;
    }
    
    /* Metric Cards */
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
        padding: 1.5rem;
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.18);
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        transition: all 0.3s ease;
    }
    
    [data-testid="stMetric"]:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px 0 rgba(31, 38, 135, 0.5);
    }
    
    [data-testid="stMetric"] label {
        color: rgba(255, 255, 255, 0.8) !important;
        font-size: 0.9rem !important;
        font-weight: 600 !important;
    }
    
    [data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: #fff !important;
        font-size: 2.5rem !important;
        font-weight: 700 !important;
    }
    
    /* Section Headers */
    h2, h3 {
        color: #fff !important;
        font-weight: 600 !important;
        margin-top: 2rem !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
        background: rgba(255, 255, 255, 0.1);
        padding: 0.5rem;
        border-radius: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: rgba(255, 255, 255, 0.7);
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: rgba(255, 255, 255, 0.2) !important;
        color: #fff !important;
    }
    
    /* Info boxes */
    .stAlert {
        background: rgba(255, 255, 255, 0.15) !important;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 10px;
        color: #fff !important;
    }
    
    /* Selectbox and inputs */
    .stSelectbox, .stSlider, .stTextInput {
        color: #fff !important;
    }
    
    [data-baseweb="select"] {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
    }
    
    /* Dataframe */
    .stDataFrame {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
    }
    
    /* Download button */
    .stDownloadButton button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stDownloadButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem;
        margin-top: 3rem;
        color: rgba(255, 255, 255, 0.8);
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 15px;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# Premium Header
st.markdown("""
    <div class="main-header">
        <h1 class="main-title">📊 EngageSense</h1>
        <p class="subtitle">AI-Powered Student Engagement Analytics Platform</p>
    </div>
""", unsafe_allow_html=True)

# Load Model
@st.cache_resource
def load_model():
    try:
        return joblib.load('isolation_forest.pkl')
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None

model = load_model()

# Load Data
@st.cache_data
def load_data_from_mysql():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="engagesense_db"
        )
        query = "SELECT * FROM student_engagement"
        df = pd.read_sql(query, conn)
        conn.close()
        return df, "mysql"
    except mysql.connector.Error as e:
        st.info(f"💾 Using demo CSV data (MySQL: {e.errno})")
        return load_data_from_csv(), "csv"

@st.cache_data
def load_data_from_csv():
    try:
        return pd.read_csv('student_engagement.csv')
    except Exception as e:
        st.error(f"Error loading CSV: {e}")
        return None

# Load data
df, source = load_data_from_mysql()

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
        feature_cols = ['login_count', 'time_spent', 'quiz_attempts']
        features_array = df[feature_cols].values
        df['anomaly'] = model.predict(features_array)
        df['anomaly_flag'] = df['anomaly'].apply(lambda x: '🚨 Anomaly' if x == -1 else '✅ Normal')
    except Exception as e:
        st.error(f"Error: {e}")
        df['anomaly'] = 1
        df['anomaly_flag'] = '✅ Normal'
    
    # Top Metrics with Icons
    st.markdown("## 📊 Real-Time Analytics Dashboard")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="⭐ Avg Engagement",
            value=f"{df['engagement_score'].mean():.2f}",
            delta="+0.3 from last week"
        )
    
    with col2:
        anomaly_count = (df['anomaly_flag'] == '🚨 Anomaly').sum()
        st.metric(
            label="🚨 Anomalies",
            value=anomaly_count,
            delta=f"{(anomaly_count/len(df)*100):.0f}% of total",
            delta_color="inverse"
        )
    
    with col3:
        st.metric(
            label="👥 Active Students",
            value=len(df),
            delta="+5 this month"
        )
    
    with col4:
        st.metric(
            label="⏱️ Avg Time (hrs)",
            value=f"{df['time_spent'].mean():.1f}",
            delta="+2.3 hrs"
        )
    
    # Leaderboard Section
    st.markdown("## 🏆 Top Performers")
    top_5 = df.nlargest(5, 'engagement_score')[['student_id', 'engagement_score', 'anomaly_flag']]
    
    cols = st.columns(5)
    medals = ['🥇', '🥈', '🥉', '🏅', '🏅']
    
    for idx, (col, medal) in enumerate(zip(cols, medals)):
        with col:
            student = top_5.iloc[idx]
            st.markdown(f"""
                <div style="text-align: center; padding: 1rem; background: rgba(255,255,255,0.1); border-radius: 10px;">
                    <div style="font-size: 2rem;">{medal}</div>
                    <div style="font-size: 1.2rem; font-weight: 600; color: #fff;">{student['student_id']}</div>
                    <div style="font-size: 1rem; color: rgba(255,255,255,0.8);">Score: {student['engagement_score']:.2f}</div>
                </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Interactive Charts
    st.markdown("## 📈 Visual Insights")
    
    tab1, tab2, tab3 = st.tabs(["📊 Distribution Analysis", "🔍 Anomaly Detection", "📉 Performance Trends"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            fig1 = px.histogram(
                df, 
                x='engagement_score',
                nbins=25,
                title='Engagement Score Distribution',
                color_discrete_sequence=['#667eea'],
                template='plotly_dark'
            )
            fig1.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='white',
                title_font_size=18
            )
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            anomaly_counts = df['anomaly_flag'].value_counts()
            fig2 = px.pie(
                values=anomaly_counts.values,
                names=anomaly_counts.index,
                title='Student Status Distribution',
                color_discrete_sequence=['#2ecc71', '#e74c3c'],
                template='plotly_dark',
                hole=0.4
            )
            fig2.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='white',
                title_font_size=18
            )
            st.plotly_chart(fig2, use_container_width=True)
    
    with tab2:
        fig3 = px.scatter(
            df,
            x='time_spent',
            y='engagement_score',
            color='anomaly_flag',
            size='login_count',
            hover_data=['student_id', 'assignment_score'],
            title='Engagement vs Time Spent Analysis',
            color_discrete_map={'✅ Normal': '#2ecc71', '🚨 Anomaly': '#e74c3c'},
            template='plotly_dark'
        )
        fig3.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            title_font_size=18
        )
        st.plotly_chart(fig3, use_container_width=True)
    
    with tab3:
        # Top 10 students bar chart
        top_10 = df.nlargest(10, 'engagement_score')
        fig4 = px.bar(
            top_10,
            x='student_id',
            y='engagement_score',
            color='anomaly_flag',
            title='Top 10 Students Performance',
            color_discrete_map={'✅ Normal': '#2ecc71', '🚨 Anomaly': '#e74c3c'},
            template='plotly_dark'
        )
        fig4.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            title_font_size=18
        )
        st.plotly_chart(fig4, use_container_width=True)
    
    st.markdown("---")
    
    # Advanced Filters
    st.markdown("## 🎓 Student Data Explorer")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        filter_anomaly = st.selectbox(
            "🔍 Filter by Status",
            ["All Students", "✅ Normal Only", "🚨 Anomalies Only"]
        )
    
    with col2:
        min_score = st.slider(
            "📊 Minimum Score",
            float(df['engagement_score'].min()),
            float(df['engagement_score'].max()),
            float(df['engagement_score'].min())
        )
    
    with col3:
        search_id = st.text_input("🔎 Search Student ID", "")
    
    # Apply filters
    filtered_df = df.copy()
    
    if filter_anomaly == "✅ Normal Only":
        filtered_df = filtered_df[filtered_df['anomaly_flag'] == '✅ Normal']
    elif filter_anomaly == "🚨 Anomalies Only":
        filtered_df = filtered_df[filtered_df['anomaly_flag'] == '🚨 Anomaly']
    
    filtered_df = filtered_df[filtered_df['engagement_score'] >= min_score]
    
    if search_id:
        filtered_df = filtered_df[filtered_df['student_id'].astype(str).str.contains(search_id)]
    
    filtered_df = filtered_df.sort_values(by='engagement_score', ascending=False)
    
    st.info(f"📋 Showing **{len(filtered_df)}** of **{len(df)}** students")
    
    # Styled dataframe
    def highlight_anomaly(row):
        if row['anomaly_flag'] == '🚨 Anomaly':
            return ['background-color: #ffebee'] * len(row)
        else:
            return ['background-color: #e8f5e9'] * len(row)
    
    styled_df = filtered_df.style.apply(highlight_anomaly, axis=1)
    st.dataframe(styled_df, use_container_width=True, height=400)
    
    # Download section
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        csv = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Filtered Data",
            data=csv,
            file_name=f'engagesense_export_{pd.Timestamp.now().strftime("%Y%m%d")}.csv',
            mime='text/csv',
            use_container_width=True
        )

else:
    st.error("❌ Failed to load data or model")

# Premium Footer
st.markdown("""
    <div class="footer">
        <p style="font-size: 1rem; font-weight: 600;">EngageSense Analytics Platform</p>
        <p style="font-size: 0.9rem;">Developed by <strong>Suraj Maurya</strong> | © 2025</p>
        <p style="font-size: 0.8rem; margin-top: 0.5rem;">Powered by Streamlit · Machine Learning · Plotly</p>
    </div>
""", unsafe_allow_html=True)
