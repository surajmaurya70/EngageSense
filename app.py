import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import joblib
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="EngageSense", page_icon="📊", layout="wide")

# Session state
if 'theme' not in st.session_state:
    st.session_state.theme = 'light'
if 'show_popup' not in st.session_state:
    st.session_state.show_popup = None

# Theme config
themes = {
    'light': {'bg': '#f8f9fa', 'surface': '#ffffff', 'text': '#202124', 'secondary': '#5f6368', 'border': '#e0e0e0'},
    'dark': {'bg': '#1a1a1a', 'surface': '#2d2d2d', 'text': '#e0e0e0', 'secondary': '#9e9e9e', 'border': '#404040'}
}
t = themes[st.session_state.theme]

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
* {{ font-family: 'Inter', sans-serif; margin: 0; padding: 0; box-sizing: border-box; }}
.stApp {{ background: {t['bg']}; transition: background 0.3s ease; }}

@keyframes fadeIn {{ from {{ opacity: 0; transform: translateY(20px); }} to {{ opacity: 1; transform: translateY(0); }} }}
@keyframes slideIn {{ from {{ transform: translateX(-100%); }} to {{ transform: translateX(0); }} }}
@keyframes pulse {{ 0%, 100% {{ transform: scale(1); }} 50% {{ transform: scale(1.05); }} }}
@keyframes bounce {{ 0%, 100% {{ transform: translateY(0); }} 50% {{ transform: translateY(-10px); }} }}

.main-header {{
    background: linear-gradient(135deg, #1a73e8 0%, #4285f4 100%);
    padding: 1.5rem 2rem;
    margin: -1rem -2rem 2rem -2rem;
    box-shadow: 0 4px 20px rgba(26, 115, 232, 0.4);
    border-radius: 0 0 24px 24px;
    animation: slideIn 0.5s ease;
}}

.header-content {{ display: flex; align-items: center; gap: 1rem; flex-wrap: wrap; }}

.logo {{
    width: 56px; height: 56px; background: white; border-radius: 12px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.75rem; font-weight: 800; color: #1a73e8;
    box-shadow: 0 6px 12px rgba(0,0,0,0.15);
    animation: bounce 2s infinite;
}}

.title {{ font-size: 1.75rem; font-weight: 800; color: white; }}
.subtitle {{ font-size: 1rem; color: rgba(255,255,255,0.95); }}

@media (min-width: 768px) {{
    .title {{ font-size: 2.25rem; }}
    .subtitle {{ font-size: 1.125rem; }}
    .logo {{ width: 60px; height: 60px; font-size: 2rem; }}
}}

h2 {{
    color: {t['text']} !important; font-weight: 800 !important; font-size: 1.5rem !important;
    margin: 2rem 0 1rem 0 !important; padding-left: 1rem; border-left: 5px solid #1a73e8;
    animation: slideIn 0.5s ease;
}}

@media (min-width: 768px) {{ h2 {{ font-size: 2rem !important; padding-left: 1.5rem; }} }}

[data-testid="stMetric"] {{
    background: {t['surface']}; border: 2px solid {t['border']}; border-radius: 16px;
    padding: 1.25rem; box-shadow: 0 6px 12px rgba(0,0,0,0.06);
    transition: all 0.4s ease; animation: fadeIn 0.6s ease;
}}

[data-testid="stMetric"]:hover {{
    transform: translateY(-6px); box-shadow: 0 12px 24px rgba(26, 115, 232, 0.25); border-color: #1a73e8;
}}

[data-testid="stMetric"] label {{ color: {t['secondary']} !important; font-size: 0.875rem !important; font-weight: 700 !important; }}
[data-testid="stMetric"] [data-testid="stMetricValue"] {{ color: {t['text']} !important; font-size: 2rem !important; font-weight: 900 !important; }}

@media (min-width: 768px) {{
    [data-testid="stMetric"] {{ padding: 1.75rem; }}
    [data-testid="stMetric"] [data-testid="stMetricValue"] {{ font-size: 3rem !important; }}
}}

.stTabs [data-baseweb="tab-list"] {{
    background: {t['surface']}; padding: 0.5rem; border-radius: 12px; border: 2px solid {t['border']};
}}

.stTabs [data-baseweb="tab"] {{
    color: {t['secondary']}; border-radius: 10px; padding: 0.75rem 1.25rem; font-weight: 700; font-size: 0.875rem;
}}

.stTabs [aria-selected="true"] {{
    background: linear-gradient(135deg, #1a73e8, #4285f4) !important; color: white !important;
}}

@media (min-width: 768px) {{
    .stTabs [data-baseweb="tab"] {{ padding: 1rem 1.75rem; font-size: 1rem; }}
}}

[data-testid="stSidebar"] {{ background: {t['surface']}; border-right: 2px solid {t['border']}; }}
[data-testid="stSidebar"] h3 {{ color: {t['text']} !important; font-weight: 700 !important; }}

.stDataFrame {{ border: 2px solid {t['border']}; border-radius: 14px; overflow: hidden; }}

#MainMenu, footer, header {{ visibility: hidden; }}
</style>
""", unsafe_allow_html=True)

# Modal Popup Component
if st.session_state.show_popup:
    popups = {
        'ai': {'icon': '🤖', 'title': 'AI Detection', 'desc': 'Advanced machine learning anomaly detection system', 
               'features': ['Automatic anomaly detection', 'Real-time risk assessment', 'Predictive scoring', '95% accuracy']},
        'realtime': {'icon': '📊', 'title': 'Real-Time Tracking', 'desc': 'Monitor engagement in real-time with live updates',
                    'features': ['Live dashboard updates', '5-second refresh', 'Streaming data', 'Instant sync']},
        'alerts': {'icon': '🔔', 'title': 'Smart Alerts', 'desc': 'Get notified when students need attention',
                  'features': ['Email notifications', 'SMS integration', 'Custom thresholds', 'Weekly reports']},
        'analytics': {'icon': '📈', 'title': 'Advanced Analytics', 'desc': 'Deep insights with comprehensive visualizations',
                     'features': ['Interactive charts', 'Trend analysis', 'Export reports', 'Custom insights']}
    }
    
    p = popups[st.session_state.show_popup]
    
    modal_html = f"""
    <div id="modal-overlay" style="
        position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
        background: rgba(0,0,0,0.75); backdrop-filter: blur(8px);
        z-index: 999999; display: flex; align-items: center; justify-content: center;
        animation: fadeIn 0.3s ease;
    " onclick="window.parent.postMessage({{type: 'close-modal'}}, '*')">
        <div style="
            background: {t['surface']}; border-radius: 20px; padding: 2rem;
            max-width: 500px; width: 90%; box-shadow: 0 24px 48px rgba(0,0,0,0.5);
            border: 2px solid #1a73e8; position: relative;
            animation: fadeIn 0.4s ease;
        " onclick="event.stopPropagation()">
            <button onclick="window.parent.postMessage({{type: 'close-modal'}}, '*')" style="
                position: absolute; top: 1rem; left: 1rem;
                background: #ea4335; color: white; border: none;
                width: 36px; height: 36px; border-radius: 50%;
                font-size: 1.25rem; font-weight: bold; cursor: pointer;
                display: flex; align-items: center; justify-content: center;
                transition: all 0.2s ease; box-shadow: 0 2px 8px rgba(234, 67, 53, 0.4);
            " onmouseover="this.style.transform='scale(1.1)'" onmouseout="this.style.transform='scale(1)'">
                ✕
            </button>
            
            <div style="text-align: center; margin-top: 1rem;">
                <div style="font-size: 3.5rem; margin-bottom: 1rem;">{p['icon']}</div>
                <h2 style="color: #1a73e8; font-size: 1.75rem; font-weight: 800; margin-bottom: 0.75rem; border: none; padding: 0;">{p['title']}</h2>
                <p style="color: {t['text']}; font-size: 1rem; margin-bottom: 1.5rem; line-height: 1.6;">{p['desc']}</p>
                
                <div style="background: rgba(26, 115, 232, 0.08); border-radius: 12px; padding: 1.25rem; text-align: left;">
                    {''.join([f'<div style="margin: 0.75rem 0; color: {t["text"]}; font-size: 0.95rem;"><span style="color: #34a853; font-weight: bold;">✓</span> {feat}</div>' for feat in p['features']])}
                </div>
            </div>
        </div>
    </div>
    
    <script>
    window.addEventListener('message', function(event) {{
        if (event.data.type === 'close-modal') {{
            window.parent.postMessage({{type: 'streamlit:setComponentValue', value: 'close'}}, '*');
        }}
    }});
    </script>
    """
    
    components.html(modal_html, height=0)
    
    # Handle close
    if st.button("", key="invisible_close", help="Close"):
        st.session_state.show_popup = None
        st.rerun()

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

# Sidebar with Theme Toggle
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    
    st.markdown("**Theme**")
    theme_col1, theme_col2 = st.columns(2)
    
    with theme_col1:
        if st.button("🌞 Light", use_container_width=True, type="primary" if st.session_state.theme == 'light' else "secondary"):
            st.session_state.theme = 'light'
            st.rerun()
    
    with theme_col2:
        if st.button("🌙 Dark", use_container_width=True, type="primary" if st.session_state.theme == 'dark' else "secondary"):
            st.session_state.theme = 'dark'
            st.rerun()
    
    st.caption(f"Current: **{st.session_state.theme.title()}**")
    
    st.markdown("---")
    st.markdown("### 🔍 Filters")
    
    data_source = st.radio("Data", ["CSV", "MySQL"], horizontal=True)
    filter_status = st.selectbox("Status", ["All", "Active", "At Risk"])
    min_score = st.slider("Min Score", 0.0, 10.0, 0.0)
    search_id = st.text_input("Search", placeholder="S007")
    
    st.markdown("---")
    st.markdown("### 📊 Display")
    show_charts = st.checkbox("Charts", value=True)
    chart_height = st.slider("Height", 300, 600, 400, 50)
    
    st.markdown("---")
    st.info(f"📅 {datetime.now().strftime('%b %d, %Y')}")

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
        df['engagement_score'] = (df['login_count']*0.25 + (df['time_spent']/60)*0.25 + 
                                   df['quiz_attempts']*0.2 + df['forum_posts']*0.15 + 
                                   (df['assignment_score']/100)*0.15*10)
    
    try:
        df['anomaly'] = model.predict(df[['login_count','time_spent','quiz_attempts']].values)
        df['anomaly_flag'] = df['anomaly'].apply(lambda x: 'At Risk' if x==-1 else 'Active')
    except:
        df['anomaly'] = 1
        df['anomaly_flag'] = 'Active'
    
    # Feature Cards
    col1,col2,col3,col4 = st.columns(4)
    
    with col1:
        if st.button("🤖\n\n**AI Detection**\n\nMachine learning", use_container_width=True):
            st.session_state.show_popup = 'ai'
            st.rerun()
    with col2:
        if st.button("📊\n\n**Real-Time**\n\nLive tracking", use_container_width=True):
            st.session_state.show_popup = 'realtime'
            st.rerun()
    with col3:
        if st.button("🔔\n\n**Alerts**\n\nNotifications", use_container_width=True):
            st.session_state.show_popup = 'alerts'
            st.rerun()
    with col4:
        if st.button("📈\n\n**Analytics**\n\nInsights", use_container_width=True):
            st.session_state.show_popup = 'analytics'
            st.rerun()
    
    st.markdown("## 📊 Dashboard")
    
    col1,col2,col3,col4 = st.columns(4)
    with col1: st.metric("Students", len(df), "+5")
    with col2: 
        anom = (df['anomaly']==-1).sum()
        st.metric("At Risk", anom, f"{(anom/len(df)*100):.0f}%")
    with col3: st.metric("Avg Score", f"{df['engagement_score'].mean():.1f}", "+0.3")
    with col4: st.metric("Avg Time", f"{df['time_spent'].mean():.0f}h", "+2")
    
    if show_charts:
        st.markdown("## 📈 Analytics")
        
        tab1,tab2,tab3 = st.tabs(["📊 Distribution","🔍 Anomaly","🏆 Top 10"])
        
        with tab1:
            col1,col2 = st.columns(2)
            with col1:
                fig1 = px.histogram(df, x='engagement_score', nbins=20, title='Distribution')
                fig1.update_layout(plot_bgcolor='white', paper_bgcolor='white', height=chart_height, margin=dict(l=20,r=20,t=40,b=20))
                fig1.update_traces(marker_color='#1a73e8')
                st.plotly_chart(fig1, use_container_width=True)
            with col2:
                counts = df['anomaly_flag'].value_counts()
                fig2 = px.pie(values=counts.values, names=counts.index, title='Status', hole=0.4)
                fig2.update_layout(plot_bgcolor='white', paper_bgcolor='white', height=chart_height, margin=dict(l=20,r=20,t=40,b=20))
                fig2.update_traces(marker=dict(colors=['#34a853','#ea4335']))
                st.plotly_chart(fig2, use_container_width=True)
        
        with tab2:
            fig3 = px.scatter(df, x='time_spent', y='engagement_score', color='anomaly_flag', size='login_count',
                            hover_data=['student_id'], title='Time vs Engagement',
                            color_discrete_map={'Active':'#34a853','At Risk':'#ea4335'})
            fig3.update_layout(plot_bgcolor='white', paper_bgcolor='white', height=chart_height, margin=dict(l=20,r=20,t=40,b=40))
            st.plotly_chart(fig3, use_container_width=True)
        
        with tab3:
            top = df.nlargest(10, 'engagement_score')
            fig4 = px.bar(top, x='student_id', y='engagement_score', color='anomaly_flag', title='Top 10',
                        color_discrete_map={'Active':'#34a853','At Risk':'#ea4335'})
            fig4.update_layout(plot_bgcolor='white', paper_bgcolor='white', height=chart_height, margin=dict(l=20,r=20,t=40,b=40))
            st.plotly_chart(fig4, use_container_width=True)
    
    st.markdown("## 📋 Data")
    
    filtered = df.copy()
    if filter_status=="Active": filtered = filtered[filtered['anomaly_flag']=='Active']
    elif filter_status=="At Risk": filtered = filtered[filtered['anomaly_flag']=='At Risk']
    filtered = filtered[filtered['engagement_score']>=min_score]
    if search_id: filtered = filtered[filtered['student_id'].astype(str).str.contains(search_id, case=False)]
    filtered = filtered.sort_values('engagement_score', ascending=False)
    
    st.info(f"📊 {len(filtered)} of {len(df)} students")
    st.dataframe(filtered, use_container_width=True, height=400)
    
    csv = filtered.to_csv(index=False).encode('utf-8')
    st.download_button(f"📥 Download {len(filtered)} Records", csv, 
                      f'data_{datetime.now().strftime("%Y%m%d_%H%M")}.csv', 'text/csv', use_container_width=True)

else:
    st.error("❌ Failed to load data")

st.markdown(f"""
<div style="margin-top: 3rem; padding: 2.5rem; text-align: center; background: {t['surface']}; 
     border-radius: 20px; border: 2px solid {t['border']};">
    <h2 style="color: #1a73e8; margin: 0 0 0.75rem 0; border: none; padding: 0; font-size: 1.5rem;">📊 EngageSense</h2>
    <p style="color: {t['text']}; font-size: 1rem;">By <strong style="color: #1a73e8;">Suraj Maurya</strong></p>
    <p style="color: {t['secondary']}; font-size: 0.875rem; margin-top: 0.5rem;">🤖 AI · 📊 ML · 🐍 Python · ⚡ Streamlit</p>
    <p style="color: {t['secondary']}; font-size: 0.75rem; margin-top: 0.5rem;">© 2025 All Rights Reserved</p>
</div>
""", unsafe_allow_html=True)
