import streamlit as st

def show_navbar():
    # Initialize states
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'Dashboard'
    
    # Custom CSS to remove blue background from logo
    st.markdown("""
    <style>
        /* Remove button styling from logo column */
        div[data-testid="column"] > div > div > div > p {
            background: transparent !important;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Clickable tabs using columns + buttons (ONLY 3 MAIN TABS)
    col_logo, col1, col2, col3 = st.columns([2, 1, 1, 1])
    
    with col_logo:
        st.markdown("### 📊 EngageSense")
    
    with col1:
        if st.button("Dashboard", key="nav_dash", use_container_width=True):
            st.session_state.current_page = "Dashboard"
            st.rerun()
    
    with col2:
        if st.button("Students", key="nav_students", use_container_width=True):
            st.session_state.current_page = "Students"
            st.rerun()
    
    with col3:
        if st.button("Reports", key="nav_reports", use_container_width=True):
            st.session_state.current_page = "Reports"
            st.rerun()
    
    # Divider only
    st.divider()

