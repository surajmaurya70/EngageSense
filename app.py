import streamlit as st
import pandas as pd
import joblib
import plotly.express as px
from datetime import datetime
import io

st.set_page_config(page_title="EngageSense Analytics", page_icon="📊", layout="wide")

# Initialize session states
if 'theme' not in st.session_state:
    st.session_state.theme = 'light'
if 'selected_filter' not in st.session_state:
    st.session_state.selected_filter = 'All'
if 'show_anomalies' not in st.session_state:
    st.session_state.show_anomalies = True
if 'refresh_rate' not in st.session_state:
    st.session_state.refresh_rate = 'Medium'
if 'show_modal' not in st.session_state:
    st.session_state.show_modal = False
if 'selected_student' not in st.session_state:
    st.session_state.selected_student = None

# Theme function
def get_theme():
    if st.session_state.theme == 'dark':
        return {'bg': '#1a1a1a', 'surface': '#2d2d2d', 'text': '#e0e0e0', 'secondary': '#9e9e9e', 'border': '#404040'}
    return {'bg': '#f8f9fa', 'surface': '#ffffff', 'text': '#202124', 'secondary': '#5f6368', 'border': '#e0e0e0'}

# Export function
def export_to_csv(df, filter_status='All'):
    if filter_status == 'Active':
        export_df = df[df['engagement_score'] >= 50]
    elif filter_status == 'At-Risk':
        export_df = df[df['engagement_score'] < 50]
    else:
        export_df = df
    
    csv_buffer = io.StringIO()
    export_df.to_csv(csv_buffer, index=False)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"engagement_data_{filter_status.lower()}_{timestamp}.csv"
    return csv_buffer.getvalue(), filename

t = get_theme()

# Custom CSS with animations
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
* {{ font-family: 'Inter', sans-serif; }}
.stApp {{ background: {t['bg']}; scroll-behavior: smooth; }}

@keyframes fadeInUp {{ from {{ opacity: 0; transform: translateY(30px); }} to {{ opacity: 1; transform: translateY(0); }} }}
@keyframes slideIn {{ from {{ opacity: 0; transform: translateX(-50px); }} to {{ opacity: 1; transform: translateX(0); }} }}
@keyframes pulse {{ 0%, 100% {{ transform: scale(1); }} 50% {{ transform: scale(1.05); }} }}

.main-header {{
    background: linear-gradient(135deg, #1a73e8 0%, #4285f4 100%);
    padding: 2rem; margin: -1rem -2rem 2rem -2rem;
    box-shadow: 0 4px 20px rgba(26, 115, 232, 0.4);
    border-radius: 0 0 24px 24px; animation: slideIn 0.6s ease;
}}
.header-content {{ display: flex; align-items: center; gap: 1rem; }}
.logo {{ width: 60px; height: 60px; background: white; border-radius: 14px; display: flex; align-items: center; justify-content: center;
    font-size: 2rem; font-weight: 800; color: #1a73e8; box-shadow: 0 6px 12px rgba(0,0,0,0.15); animation: pulse 2s infinite; }}
.title {{ font-size: 2.25rem; font-weight: 800; color: white; }}
.subtitle {{ font-size: 1.125rem; color: rgba(255,255,255,0.95); }}

div[data-testid="stMetric"] {{
    background: {t['surface']}; padding: 1.5rem; border-radius: 16px; 
    border: 2px solid {t['border']}; box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    transition: all 0.3s ease; animation: fadeInUp 0.5s ease;
}}
div[data-testid="stMetric"]:hover {{
    transform: translateY(-5px); box-shadow: 0 8px 20px rgba(26, 115, 232, 0.3);
    border-color: #1a73e8; cursor: pointer;
}}

button[kind="primary"] {{
    background: linear-gradient(135deg, #1a73e8 0%, #4285f4 100%) !important;
    border: none !important; color: white !important;
    box-shadow: 0 4px 12px rgba(26, 115, 232, 0.4) !important;
    transition: all 0.3s ease !important;
}}
button[kind="primary"]:hover {{
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 16px rgba(26, 115, 232, 0.5) !important;
}}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown(f"""
<div class="main-header">
    <div class="header-content">
        <div class="logo">ES</div>
        <div>
            <div class="title">📊 EngageSense Analytics</div>
            <div class="subtitle">AI-Powered Student Engagement Insights</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Enhanced Settings Sidebar
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #1a73e8;'>⚙️ Settings</h2>", unsafe_allow_html=True)
    st.divider()
    
    # Theme Toggle
    st.markdown("### 🎨 Appearance")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🌞 Light", use_container_width=True, type="primary" if st.session_state.theme == 'light' else "secondary"):
            st.session_state.theme = 'light'
            st.rerun()
    with col2:
        if st.button("🌙 Dark", use_container_width=True, type="primary" if st.session_state.theme == 'dark' else "secondary"):
            st.session_state.theme = 'dark'
            st.rerun()
    
    st.divider()
    
    # Anomaly Toggle
    st.markdown("### 🚨 Detection")
    show_anomalies = st.toggle("Show Anomalies", value=st.session_state.show_anomalies)
    st.session_state.show_anomalies = show_anomalies
    
    st.divider()
    
    # Refresh Rate
    st.markdown("### 🔄 Refresh")
    refresh_rate = st.selectbox("Rate", ['Low (30s)', 'Medium (15s)', 'High (5s)'], index=1)
    st.session_state.refresh_rate = refresh_rate
    
    st.divider()
    
    # Export
    st.markdown("### 📥 Export")
    if st.button("📊 Download CSV", use_container_width=True, type="primary"):
        st.session_state.trigger_export = True
    
    st.divider()
    
    # About
    with st.expander("ℹ️ About"):
        st.markdown("""
        **EngageSense v1.0**
        
        AI-Powered Analytics
        
        **Developer:** Suraj Maurya
        
        © 2025
        """)

# Load data
try:
    df = pd.read_csv('student_engagement.csv')
except:
    st.error("Data file not found!")
    st.stop()

# Calculate metrics
total_students = len(df)
active_students = len(df[df['engagement_score'] >= 50])
at_risk_students = len(df[df['engagement_score'] < 50])

# Enhanced Metric Cards with Click Actions
st.markdown("## 📈 Key Metrics")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("📊 Total Students", total_students)
    if st.button("View All", key="btn_all", use_container_width=True):
        st.session_state.selected_filter = 'All'
        st.rerun()

with col2:
    st.metric("✅ Active Students", active_students)
    if st.button("View Active", key="btn_active", use_container_width=True):
        st.session_state.selected_filter = 'Active'
        st.rerun()

with col3:
    st.metric("⚠️ At-Risk Students", at_risk_students)
    if st.button("View At-Risk", key="btn_risk", use_container_width=True):
        st.session_state.selected_filter = 'At-Risk'
        st.rerun()

# Filter display
if st.session_state.selected_filter != 'All':
    st.info(f"🔍 Showing: **{st.session_state.selected_filter}** students")

# Apply filter
if st.session_state.selected_filter == 'Active':
    filtered_df = df[df['engagement_score'] >= 50]
elif st.session_state.selected_filter == 'At-Risk':
    filtered_df = df[df['engagement_score'] < 50]
else:
    filtered_df = df

# Export functionality
if st.session_state.get('trigger_export', False):
    csv_data, filename = export_to_csv(df, st.session_state.selected_filter)
    st.download_button(
        label="⬇️ Download CSV",
        data=csv_data,
        file_name=filename,
        mime="text/csv",
        use_container_width=True
    )
    st.session_state.trigger_export = False

# Interactive Editable Table
st.markdown("## 📋 Student Data")

if 'edited_df' not in st.session_state:
    st.session_state.edited_df = filtered_df.copy()

edited_data = st.data_editor(
    st.session_state.edited_df,
    num_rows="dynamic",
    use_container_width=True,
    hide_index=True,
    column_config={
        "engagement_score": st.column_config.ProgressColumn(
            "Engagement",
            min_value=0,
            max_value=100,
        ),
    }
)

col_a, col_b = st.columns([1, 1])
with col_a:
    if st.button("💾 Save Changes", type="primary"):
        st.session_state.edited_df = edited_data
        st.success("✅ Changes saved!")

with col_b:
    if st.button("🔄 Reset Data"):
        st.session_state.edited_df = filtered_df.copy()
        st.rerun()

# Tabs for analytics
tab1, tab2, tab3 = st.tabs(["📊 Distribution", "🚨 Anomalies", "📈 Activity"])

with tab1:
    st.markdown("### Engagement Distribution")
    fig = px.histogram(filtered_df, x='engagement_score', nbins=20, 
                       title="Engagement Score Distribution",
                       color_discrete_sequence=['#1a73e8'])
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    if st.session_state.show_anomalies:
        st.markdown("### Anomaly Detection")
        anomaly_df = filtered_df[filtered_df['engagement_score'] < 30]
        st.dataframe(anomaly_df, use_container_width=True)
    else:
        st.info("Anomaly detection is disabled in settings")

with tab3:
    st.markdown("### Activity Metrics")
    fig = px.scatter(filtered_df, x='login_count', y='time_spent',
                     size='engagement_score', color='engagement_score',
                     title="Login vs Time Spent",
                     color_continuous_scale='Blues')
    st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
st.markdown(f"""
<div style='text-align: center; color: {t['secondary']}; padding: 2rem 0;'>
    <p style='font-size: 1rem; margin: 0.5rem 0;'>EngageSense © 2025 | Developed by <strong style='color: #1a73e8;'>Suraj Maurya</strong></p>
    <p style='font-size: 0.9rem; margin: 0.75rem 0;'>Empowering Educators through Data & AI 💡</p>
</div>
""", unsafe_allow_html=True)
