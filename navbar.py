import streamlit as st

def show_navbar():
    # Session state for page navigation
    if 'page' not in st.session_state:
        st.session_state.page = 'Dashboard'
    
    # Clickable navigation with invisible buttons positioned ABOVE HTML
    col1, col2, col3, col4, col5, col6, col7 = st.columns([1.5, 0.8, 0.8, 0.8, 2, 0.8, 0.8])
    
    with col2:
        if st.button("📊", key="dash", help="Dashboard", use_container_width=True):
            st.session_state.page = "Dashboard"
            st.rerun()
    with col3:
        if st.button("👥", key="stud", help="Students", use_container_width=True):
            st.session_state.page = "Students"
            st.rerun()
    with col4:
        if st.button("📈", key="rep", help="Reports", use_container_width=True):
            st.session_state.page = "Reports"
            st.rerun()
    with col6:
        if st.button("⚙️", key="filt", help="Filters", use_container_width=True):
            st.toast("⚙️ Filters panel!")
    with col7:
        if st.button("🔔", key="notif", help="Notifications", use_container_width=True):
            st.toast("🔔 3 new alerts!")
    
    # Beautiful HTML navbar (visual only, buttons above are functional)
    st.markdown("""
    <style>
    .navbar {
        background: white;
        padding: 1rem 2rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
        border-bottom: 1px solid #e5e5e5;
        margin: -6rem -2rem 2rem -2rem;
        position: relative;
        z-index: 1;
    }
    .navbar-left {
        display: flex;
        align-items: center;
        gap: 3rem;
    }
    .navbar-logo {
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    .navbar-logo-icon {
        width: 48px;
        height: 48px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
    }
    .navbar-brand h1 {
        margin: 0;
        font-size: 1.5rem;
        font-weight: 700;
        color: #1a1a1a;
    }
    .navbar-brand p {
        margin: 0;
        font-size: 0.85rem;
        color: #666;
    }
    .navbar-tabs {
        display: flex;
        gap: 0.5rem;
    }
    .nav-tab {
        padding: 0.5rem 1rem;
        border-radius: 8px;
        font-weight: 500;
        color: #666;
    }
    .nav-tab.active {
        color: #1a1a1a;
        font-weight: 600;
    }
    .navbar-right {
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    .nav-btn {
        padding: 0.6rem 1.2rem;
        border-radius: 10px;
        border: 1px solid #e5e5e5;
        background: white;
        font-weight: 500;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .notification-badge {
        position: relative;
    }
    .notification-badge::after {
        content: '3';
        position: absolute;
        top: -5px;
        right: -5px;
        background: #ff4444;
        color: white;
        border-radius: 50%;
        width: 20px;
        height: 20px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.75rem;
        font-weight: 600;
    }
    </style>
    
    <div class="navbar">
        <div class="navbar-left">
            <div class="navbar-logo">
                <div class="navbar-logo-icon">📊</div>
                <div class="navbar-brand">
                    <h1>EngageSense</h1>
                    <p>AI-Powered Analytics</p>
                </div>
            </div>
            <div class="navbar-tabs">
                <div class="nav-tab active">Dashboard</div>
                <div class="nav-tab">Students</div>
                <div class="nav-tab">Reports</div>
            </div>
        </div>
        <div class="navbar-right">
            <div class="nav-btn">⚙️ Filters</div>
            <div class="nav-btn notification-badge">🔔</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Show current page indicator
    st.caption(f"📍 Current page: **{st.session_state.page}**")
