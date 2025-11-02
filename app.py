import streamlit as st

def show_login_page():
    st.markdown("""
    <style>
        .stApp { background: white; display: flex; align-items: center; justify-content: center; }
        .main-heading { font-size: 36px; font-weight: 700; color: #3d4f5d; text-align: center; margin-bottom: 12px; }
        .subtitle { text-align: center; color: #9ca3af; font-size: 15px; margin-bottom: 40px; }
    </style>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1.2, 1])
    
    with col2:
        st.markdown('<div class="main-heading">Welcome to<br>EngageSense</div>', unsafe_allow_html=True)
        st.markdown('<div class="subtitle">Enter any email & password to continue</div>', unsafe_allow_html=True)
        
        email = st.text_input("E-mail", placeholder="test@email.com")
        password = st.text_input("Password", type="password", placeholder="password")
        
        if st.button("Login", use_container_width=True):
            if email and password:
                st.session_state.logged_in = True
                st.rerun()
