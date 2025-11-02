import streamlit as st

def show_login_page():
    st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .stApp {
            background: white;
            display: flex;
            align-items: center;
            justify-content: center;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        }
        .block-container {
            padding: 0 !important;
            max-width: 100% !important;
        }
        .main-heading {
            font-size: 36px;
            font-weight: 700;
            color: #3d4f5d;
            text-align: center;
            margin-bottom: 12px;
            line-height: 1.3;
        }
        .subtitle {
            text-align: center;
            color: #9ca3af;
            font-size: 15px;
            margin-bottom: 40px;
        }
        .stTextInput { margin-bottom: 20px; }
        .stTextInput > label {
            color: #6b7280 !important;
            font-size: 13px !important;
            font-weight: 500 !important;
        }
        .stTextInput > div > div > input {
            background: white !important;
            border: 1.5px solid #6366f1 !important;
            border-radius: 8px !important;
            padding: 14px 16px !important;
            font-size: 15px !important;
            color: #6b7280 !important;
        }
        .stTextInput > div > div > input:focus {
            border-color: #6366f1 !important;
            box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1) !important;
        }
        .stButton > button {
            width: 100%;
            background: #6366f1 !important;
            color: white !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 14px !important;
            font-size: 16px !important;
            font-weight: 600 !important;
        }
        .stButton > button:hover {
            background: #4f46e5 !important;
        }
        .stCheckbox { margin: 0 !important; }
        .stCheckbox > label { color: #6b7280 !important; font-size: 14px !important; }
    </style>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1.2, 1])
    
    with col2:
        st.markdown('<div class="main-heading">Welcome to<br>EngageSense</div>', unsafe_allow_html=True)
        st.markdown('<div class="subtitle">Sign in to access your student engagement dashboard</div>', unsafe_allow_html=True)
        
        email = st.text_input("E-mail", placeholder="example@email.com", key="email")
        password = st.text_input("Password", type="password", placeholder="Your Password", key="password")
        
        col_check, col_forgot = st.columns([1, 1])
        with col_check:
            st.checkbox("Remember me")
        with col_forgot:
            st.markdown('<div style="text-align: right; color: #6b7280; font-size: 14px; margin-top: 8px;">Forgot Password?</div>', unsafe_allow_html=True)
        
        # DEMO MODE - Accept any credentials
        if st.button("Login", use_container_width=True):
            if email and password:
                st.session_state.logged_in = True
                st.rerun()
