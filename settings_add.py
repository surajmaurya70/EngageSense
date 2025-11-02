# Add this to app.py manually

# After line: st.session_state.trigger_scroll = False
# Add settings initialization:

if 'show_anomalies' not in st.session_state:
    st.session_state.show_anomalies = True
if 'refresh_rate' not in st.session_state:
    st.session_state.refresh_rate = 'Medium'

# After get_theme() function, add settings sidebar
with st.sidebar:
    st.markdown(f"<h2 style='color: #1a73e8;'>⚙️ Settings</h2>", unsafe_allow_html=True)
    
    # Theme Toggle
    st.markdown("### 🎨 Theme")
    theme_val = st.toggle("Dark Mode", value=(st.session_state.theme == 'dark'))
    st.session_state.theme = 'dark' if theme_val else 'light'
    
    st.divider()
    
    # Anomaly Toggle
    st.markdown("### 🚨 Anomalies")
    st.session_state.show_anomalies = st.toggle("Show Anomalies", value=st.session_state.show_anomalies)
    
    st.divider()
    
    # Refresh Rate
    st.markdown("### 🔄 Refresh")
    st.session_state.refresh_rate = st.selectbox("Rate", ['Low', 'Medium', 'High'], index=1)

