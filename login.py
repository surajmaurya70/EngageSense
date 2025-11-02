import streamlit as st

def show_login_page():
    # Hide Streamlit branding
    st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* White background */
        .stApp {
            background: #f8f9fa;
            display: flex;
            align-items: center;
            justify-content: center;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        }
        
        /* Remove padding */
        .block-container {
            padding: 0 !important;
            max-width: 100% !important;
        }
        
        /* Logo at top left */
        .top-logo {
            position: fixed;
            top: 30px;
            left: 40px;
            display: flex;
            align-items: center;
            gap: 10px;
            font-size: 22px;
            font-weight: 700;
            color: #1a1f36;
            z-index: 1000;
        }
        
        .logo-icon {
            width: 40px;
            height: 40px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 24px;
            font-weight: 700;
        }
        
        /* Login box */
        .login-box {
            background: white;
            max-width: 450px;
            width: 100%;
            padding: 50px 45px;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
            animation: slideUp 0.5s ease;
        }
        
        @keyframes slideUp {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        /* Heading styles */
        .tagline {
            color: #6366f1;
            font-size: 15px;
            font-weight: 600;
            margin-bottom: 10px;
            text-align: center;
        }
        
        .main-heading {
            font-size: 32px;
            font-weight: 700;
            color: #1a1f36;
            text-align: center;
            margin-bottom: 35px;
        }
        
        /* Input labels */
        .input-label {
            color: #6366f1;
            font-size: 13px;
            font-weight: 600;
            margin-bottom: 8px;
            margin-left: 4px;
            display: block;
        }
        
        /* Input fields */
        .stTextInput > div > div > input {
            background: white !important;
            border: 1.5px solid #e0e4e8 !important;
            border-radius: 8px !important;
            padding: 14px 16px !important;
            font-size: 15px !important;
            color: #1a1f36 !important;
            transition: all 0.2s ease !important;
        }
        
        .stTextInput > div > div > input::placeholder {
            color: #9ca3af !important;
        }
        
        .stTextInput > div > div > input:focus {
            border-color: #6366f1 !important;
            box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1) !important;
        }
        
        /* Hide default labels */
        .stTextInput > label {
            display: none;
        }
        
        /* Sign Up button */
        .stButton > button {
            width: 100%;
            background: #6366f1 !important;
            color: white !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 14px !important;
            font-size: 16px !important;
            font-weight: 600 !important;
            cursor: pointer !important;
            transition: all 0.2s ease !important;
            margin-top: 10px !important;
        }
        
        .stButton > button:hover {
            background: #4f46e5 !important;
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3) !important;
        }
        
        /* OR divider */
        .divider {
            display: flex;
            align-items: center;
            margin: 28px 0;
            color: #6b7280;
            font-size: 13px;
            font-weight: 500;
        }
        
        .divider::before,
        .divider::after {
            content: '';
            flex: 1;
            height: 1px;
            background: #e5e7eb;
        }
        
        .divider span {
            padding: 0 16px;
        }
        
        /* Social login buttons */
        .social-buttons {
            display: flex;
            gap: 12px;
            margin-bottom: 25px;
        }
        
        .social-btn {
            flex: 1;
            background: white;
            border: 1.5px solid #e0e4e8;
            border-radius: 8px;
            padding: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            transition: all 0.2s ease;
            font-size: 22px;
        }
        
        .social-btn:hover {
            border-color: #6366f1;
            box-shadow: 0 2px 8px rgba(99, 102, 241, 0.15);
            transform: translateY(-1px);
        }
        
        /* Bottom text */
        .bottom-text {
            text-align: center;
            margin-top: 25px;
            color: #6b7280;
            font-size: 14px;
        }
        
        .bottom-text a {
            color: #6366f1;
            font-weight: 600;
            text-decoration: none;
        }
        
        /* Error/Info styling */
        .stAlert {
            border-radius: 8px !important;
            font-size: 13px !important;
        }
        
        div[data-testid="stInfo"] {
            background: #eff6ff !important;
            border: 1px solid #bfdbfe !important;
            color: #1e40af !important;
            border-radius: 8px !important;
            margin-top: 20px !important;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Logo at top left
    st.markdown('''
    <div class="top-logo">
        <div class="logo-icon">📊</div>
        <span>EngageSense</span>
    </div>
    ''', unsafe_allow_html=True)
    
    # Center container
    col1, col2, col3 = st.columns([1, 1.2, 1])
    
    with col2:
        st.markdown('<div class="login-box">', unsafe_allow_html=True)
        
        # Heading
        st.markdown('<div class="tagline">Start your journey</div>', unsafe_allow_html=True)
        st.markdown('<div class="main-heading">Sign Up to EngageSense</div>', unsafe_allow_html=True)
        
        # Email input
        st.markdown('<label class="input-label">E-mail</label>', unsafe_allow_html=True)
        email = st.text_input("Email", placeholder="example@email.com", 
                             key="email", label_visibility="collapsed")
        
        # Password input
        st.markdown('<label class="input-label">Password</label>', unsafe_allow_html=True)
        password = st.text_input("Password", type="password", placeholder="••••••••", 
                                key="password", label_visibility="collapsed")
        
        # Sign Up button
        if st.button("Sign Up", use_container_width=True):
            if email == "admin@engagesense.com" and password == "admin123":
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("❌ Invalid credentials. Please try again.")
        
        # OR divider
        st.markdown('<div class="divider"><span>or sign up with</span></div>', unsafe_allow_html=True)
        
        # Social login buttons
        st.markdown('''
        <div class="social-buttons">
            <div class="social-btn">📘</div>
            <div class="social-btn">🔍</div>
            <div class="social-btn">🍎</div>
        </div>
        ''', unsafe_allow_html=True)
        
        # Bottom text
        st.markdown('''
        <div class="bottom-text">
            Have an account? <a href="#">Sign in</a>
        </div>
        ''', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Demo credentials
        st.info("💡 **Demo Login**  \nadmin@engagesense.com / admin123")

