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
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main { padding: 0rem 1rem; }
    h1 { color: #1f77b4; }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("# 📊 EngageSense — Student Engagement Analytics (Demo)")
st.markdown("### *AI-Powered Insights into Student Activity*")
st.markdown("---")

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
        st.warning(f"⚠️ Error loading data from MySQL: {e.errno}: {e.msg}")
        st.info("Falling back to demo CSV data instead.")
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
    # Calculate engagement score if not present
    if 'engagement_score' not in df.columns:
        df['engagement_score'] = (
            df['login_count'] * 0.25 +
            (df['time_spent'] / 60) * 0.25 +
            df['quiz_attempts'] * 0.2 +
            df['forum_posts'] * 0.15 +
            (df['assignment_score'] / 100) * 0.15 * 10
        )
    
    # Predict anomalies - use numpy array to avoid feature name mismatch
    try:
        feature_cols = ['login_count', 'time_spent', 'quiz_attempts', 'forum_posts', 'assignment_score']
        features_array = df[feature_cols].values
        df['anomaly'] = model.predict(features_array)
        df['anomaly_flag'] = df['anomaly'].apply(lambda x: 'Anomaly' if x == -1 else 'Normal')
    except Exception as e:
        st.error(f"Error in anomaly prediction: {e}")
        df['anomaly'] = 1
        df['anomaly_flag'] = 'Normal'
    
    # Top Metrics
    st.markdown("## 📊 Top: Engagement Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Avg Engagement Score", f"{df['engagement_score'].mean():.2f}")
    
    with col2:
        anomaly_count = (df['anomaly_flag'] == 'Anomaly').sum()
        st.metric("Anomalies Detected", anomaly_count)
    
    with col3:
        st.metric("Students", len(df))
    
    with col4:
        st.metric("Avg Time Spent (hrs)", f"{df['time_spent'].mean():.1f}")
    
    st.markdown("---")
    
    # Charts
    st.markdown("## 📈 Visual Analytics")
    
    tab1, tab2 = st.tabs(["📊 Distribution", "🔍 Anomaly Analysis"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            fig1 = px.histogram(
                df, 
                x='engagement_score',
                nbins=20,
                title='Engagement Score Distribution',
                color_discrete_sequence=['#1f77b4']
            )
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            anomaly_counts = df['anomaly_flag'].value_counts()
            fig2 = px.pie(
                values=anomaly_counts.values,
                names=anomaly_counts.index,
                title='Normal vs Anomaly Students',
                color_discrete_sequence=['#2ecc71', '#e74c3c']
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
            title='Engagement Score vs Time Spent',
            color_discrete_map={'Normal': '#2ecc71', 'Anomaly': '#e74c3c'}
        )
        st.plotly_chart(fig3, use_container_width=True)
    
    st.markdown("---")
    
    # Students Table
    st.markdown("## 🎓 Students Table (sorted by engagement score)")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        filter_anomaly = st.selectbox(
            "Filter by Status:",
            ["All Students", "Normal Only", "Anomalies Only"]
        )
    
    with col2:
        min_score = st.slider(
            "Min Engagement Score:",
            float(df['engagement_score'].min()),
            float(df['engagement_score'].max()),
            float(df['engagement_score'].min())
        )
    
    with col3:
        search_id = st.text_input("Search Student ID:", "")
    
    # Apply Filters
    filtered_df = df.copy()
    
    if filter_anomaly == "Normal Only":
        filtered_df = filtered_df[filtered_df['anomaly_flag'] == 'Normal']
    elif filter_anomaly == "Anomalies Only":
        filtered_df = filtered_df[filtered_df['anomaly_flag'] == 'Anomaly']
    
    filtered_df = filtered_df[filtered_df['engagement_score'] >= min_score]
    
    if search_id:
        filtered_df = filtered_df[filtered_df['student_id'].astype(str).str.contains(search_id)]
    
    filtered_df = filtered_df.sort_values(by='engagement_score', ascending=False)
    
    st.info(f"📋 Showing {len(filtered_df)} of {len(df)} students")
    
    # Display table
    def highlight_anomaly(row):
        if row['anomaly_flag'] == 'Anomaly':
            return ['background-color: #ffebee'] * len(row)
        else:
            return ['background-color: #e8f5e9'] * len(row)
    
    styled_df = filtered_df.style.apply(highlight_anomaly, axis=1)
    st.dataframe(styled_df, use_container_width=True, height=400)
    
    # Download Button
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Filtered Data as CSV",
        data=csv,
        file_name='filtered_students.csv',
        mime='text/csv',
    )

else:
    st.error("Failed to load data or model.")

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #7f8c8d;'>
        <p>EngageSense © 2025 | Developed by Suraj Maurya</p>
    </div>
""", unsafe_allow_html=True)
