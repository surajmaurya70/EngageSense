import streamlit as st

def show_login_page():
    # Hide Streamlit branding
    st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* Full-screen black background */
        .stApp {
            background: #000000;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        /* Remove default padding */
        .block-container {
            padding: 0 !important;
            max-width: 100% !important;
        }
        
        /* Login box container */
        .login-box {
            background: #000000;
            max-width: 350px;
            width: 100%;
            text-align: center;
            animation: fadeIn 0.6s ease;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        
        /* Instagram logo styling */
        .insta-logo {
            font-family: 'Billabong', 'Brush Script MT', cursive;
            font-size: 52px;
            color: #ffffff;
            margin-bottom: 35px;
            font-weight: 400;
            letter-spacing: 2px;
        }
        
        /* Input container */
        .input-container {
            margin-bottom: 8px;
        }
        
        /* Input fields */
        .stTextInput > div > div > input {
            background: #121212 !important;
            border: 1px solid #262626 !important;
            border-radius: 3px !important;
            padding: 12px 10px !important;
            font-size: 14px !important;
            color: #ffffff !important;
            transition: border-color 0.2s ease !important;
        }
        
        .stTextInput > div > div > input::placeholder {
            color: #8e8e8e !important;
        }
        
        .stTextInput > div > div > input:focus {
            border-color: #555555 !important;
        }
        
        /* Hide labels */
        .stTextInput > label {
            display: none;
        }
        
        /* Login button */
        .stButton > button {
            width: 100%;
            background: #0095f6 !important;
            color: white !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 10px !important;
            font-size: 14px !important;
            font-weight: 600 !important;
            cursor: pointer !important;
            transition: background 0.2s ease !important;
            margin-top: 12px !important;
        }
        
        .stButton > button:hover {
            background: #1877f2 !important;
        }
        
        /* OR divider */
        .divider {
            display: flex;
            align-items: center;
            margin: 25px 0 20px 0;
            color: #8e8e8e;
            font-size: 13px;
            font-weight: 600;
        }
        
        .divider::before,
        .divider::after {
            content: '';
            flex: 1;
            height: 1px;
            background: #262626;
        }
        
        .divider span {
            padding: 0 18px;
        }
        
        /* Facebook login button */
        .fb-login {
            color: #385185;
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
            margin-bottom: 20px;
        }
        
        /* Forgot password */
        .forgot-password {
            color: #00376b;
            font-size: 12px;
            margin-top: 18px;
        }
        
        /* Signup box */
        .signup-box {
            background: #121212;
            border: 1px solid #262626;
            padding: 20px;
            margin-top: 10px;
            border-radius: 3px;
            color: #ffffff;
            font-size: 14px;
        }
        
        .signup-box a {
            color: #0095f6;
            font-weight: 600;
            text-decoration: none;
        }
        
        /* Error styling */
        .stAlert {
            background: #121212 !important;
            border: 1px solid #ed4956 !important;
            color: #ed4956 !important;
            border-radius: 3px !important;
            font-size: 12px !important;
            padding: 8px !important;
        }
        
        /* Info box (demo credentials) */
        div[data-testid="stInfo"] {
            background: #121212 !important;
            border: 1px solid #262626 !important;
            color: #a8a8a8 !important;
            border-radius: 3px !important;
            font-size: 12px !important;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Center everything
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col2:
        # Logo
        st.markdown('<div class="login-box">', unsafe_allow_html=True)
        st.markdown('<div class="insta-logo">EngageSense</div>', unsafe_allow_html=True)
        
        # Input fields
        username = st.text_input("Username", placeholder="Phone number, username or email address", 
                                  key="username", label_visibility="collapsed")
        password = st.text_input("Password", type="password", placeholder="Password", 
                                  key="password", label_visibility="collapsed")
        
        # Login button
        if st.button("Log in", use_container_width=True):
            if username == "admin" and password == "admin123":
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Incorrect credentials. Please try again.")
        
        # OR divider
        st.markdown('<div class="divider"><span>OR</span></div>', unsafe_allow_html=True)
        
        # Facebook login (non-functional, just for UI)
        st.markdown('<div class="fb-login">🔵 Log in with Facebook</div>', unsafe_allow_html=True)
        
        # Forgot password
        st.markdown('<div class="forgot-password">Forgotten your password?</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Signup box
        st.markdown('''
        <div class="signup-box">
            Don't have an account? <a href="#">Sign up</a>
        </div>
        ''', unsafe_allow_html=True)
        
        # Demo credentials (optional - remove if not needed)
        st.info("💡 Demo: admin / admin123")
