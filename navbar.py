import streamlit as st

def show_navbar():
    # Initialize states
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'Dashboard'
    
    # Clickable tabs using columns + buttons
    col_logo, col1, col2, col3, col_spacer, col4, col5 = st.columns([2, 1, 1, 1, 3, 1, 1])
    
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
    
    with col4:
        st.button("⚙️ Filters", key="nav_filters")
    
    with col5:
        st.button("🔔", key="nav_notif")
    
    # Show current page
    st.caption(f"📍 {st.session_state.current_page}")
    st.divider()
