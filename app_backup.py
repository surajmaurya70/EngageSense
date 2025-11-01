import streamlit as st
import pandas as pd
import joblib
import numpy as np
import mysql.connector

st.set_page_config(page_title="EngageSense (Demo)", layout="wide")

st.title("EngageSense — Student Engagement Analytics (Demo)")
st.markdown("Now connected with MySQL database instead of CSV 🚀")

# -------- DATABASE CONNECTION --------
def load_data_from_db():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root1234",  # ← Your MySQL password
        database="engagement_db"  # ← Your database name
    )
    query = "SELECT * FROM student_engagement;"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# -------- MODEL LOADER --------
@st.cache_resource
def load_model(path):
    return joblib.load(path)

# -------- LOAD DATA --------
try:
    df = load_data_from_db()
    st.success("✅ Data loaded successfully from MySQL database!")
except Exception as e:
    st.error(f"⚠️ Error loading data from MySQL: {e}")
    st.warning("Falling back to demo CSV data instead.")
    df = pd.read_csv("student_engagement.csv")

# -------- ENGAGEMENT SCORE CALCULATION --------
df['engagement_score'] = (
    df['login_count'] * 0.25 +
    (df['time_spent'] / 60) * 0.25 +
    df['quiz_attempts'] * 0.2 +
    df['forum_posts'] * 0.15 +
    (df['assignment_score'] / 100) * 0.15 * 10
)

features = ['login_count', 'time_spent', 'quiz_attempts']

# -------- LOAD MODEL & PREDICT --------
model = load_model("isolation_forest.pkl")
df['anomaly'] = model.predict(df[features])
df['anomaly_flag'] = df['anomaly'].map({1: 'Normal', -1: 'Anomaly'})

# -------- DASHBOARD SECTIONS --------
st.subheader("Top: Engagement Summary")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Avg Engagement Score", f"{df['engagement_score'].mean():.2f}")
with col2:
    st.metric("Anomalies Detected", int((df['anomaly'] == -1).sum()))
with col3:
    st.metric("Students", df.shape[0])

st.subheader("Students Table (sorted by engagement score)")
st.dataframe(df.sort_values('engagement_score', ascending=False).reset_index(drop=True), use_container_width=True)

st.subheader("Engagement Distribution")
st.bar_chart(df['engagement_score'])

st.subheader("Flagged Students (Anomalies)")
st.table(df[df['anomaly'] == -1][['student_id', 'engagement_score', 'login_count', 'time_spent', 'quiz_attempts']])

st.markdown("---")
st.markdown("**Connected to:** MySQL → `engagement_db.student_engagement`")
st.markdown("**If database unavailable, fallback → CSV (demo data).**")
