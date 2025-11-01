import streamlit as st
import pandas as pd
import joblib
import plotly.express as px
import mysql.connector

# -----------------------------
# 🎓 PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="EngageSense — Student Engagement Dashboard",
    page_icon="🎓",
    layout="wide",
)

# -----------------------------
# 💅 CUSTOM STYLING
# -----------------------------
st.markdown("""
    <style>
        body { background-color: #0E1117; color: white; }
        .main { background-color: #0E1117; }
        h1, h2, h3 { color: #FF4B4B; }
        .stMetric { background-color: #1E222A; border-radius: 10px; padding: 10px; }
        footer {visibility: hidden;}
        #MainMenu {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

st.title("🎓 EngageSense — Student Engagement Analytics (Demo)")
st.markdown("#### _AI-Powered Insights into Student Activity_")
st.divider()

# -----------------------------
# 📦 DATABASE LOADER
# -----------------------------
def load_data_from_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root1234",  # Change if needed
            database="engagement_db"
        )
        query = "SELECT * FROM student_engagement;"
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"⚠️ Error loading data from MySQL: {e}")
        st.warning("Falling back to demo CSV data instead.")
        return pd.read_csv("student_engagement.csv")

# -----------------------------
# 🤖 MODEL LOADER
# -----------------------------
@st.cache_resource
def load_model(path):
    return joblib.load(path)

# -----------------------------
# 📊 LOAD DATA
# -----------------------------
df = load_data_from_db()

# Engagement Score Calculation
df['engagement_score'] = (
    df['login_count'] * 0.25 +
    (df['time_spent'] / 60) * 0.25 +
    df['quiz_attempts'] * 0.2 +
    df['forum_posts'] * 0.15 +
    (df['assignment_score'] / 100) * 0.15 * 10
)

# -----------------------------
# 🧮 SUMMARY METRICS
# -----------------------------
col1, col2, col3 = st.columns(3)
col1.metric("Avg Engagement Score", f"{df['engagement_score'].mean():.2f}")
col2.metric("Anomalies Detected", df[df['anomaly_flag'] == 'Anomaly'].shape[0])
col3.metric("Students", df.shape[0])

# -----------------------------
# 📊 INTERACTIVE CHARTS
# -----------------------------
colA, colB = st.columns(2)

with colA:
    st.subheader("📈 Engagement vs Assignment Score")
    fig1 = px.scatter(df, x='assignment_score', y='engagement_score',
                      color='anomaly_flag', hover_data=['student_id'],
                      color_discrete_map={'Normal': 'green', 'Anomaly': 'red'})
    st.plotly_chart(fig1, use_container_width=True)

with colB:
    st.subheader("📊 Login Count Distribution")
    fig2 = px.histogram(df, x='login_count', nbins=10, color='anomaly_flag')
    st.plotly_chart(fig2, use_container_width=True)

# -----------------------------
# 🔍 SEARCH FILTER
# -----------------------------
st.sidebar.header("🔍 Filter Students")
search = st.sidebar.text_input("Enter Student ID or Name:")

if search:
    df_filtered = df[df['student_id'].str.contains(search, case=False, na=False)]
else:
    df_filtered = df

# -----------------------------
# 🚨 ANOMALY HIGHLIGHT
# -----------------------------
def highlight_anomaly(row):
    color = 'background-color: #FFB3B3' if row['anomaly_flag'] == 'Anomaly' else ''
    return [color] * len(row)

st.subheader("📋 Student Engagement Table")
st.dataframe(df_filtered.style.apply(highlight_anomaly, axis=1), use_container_width=True)

# -----------------------------
# 🦋 FOOTER
# -----------------------------
st.markdown("""
---
✅ *Developed by Suraj Maurya — EngageSense (AI-Powered LMS Analytics)*  
📧 [Contact Me](mailto:surajmauryaa70@gmail.com) | 🌐 [GitHub](https://github.com/surajmaurya70)
""")
