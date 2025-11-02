import streamlit as st

def show_login_page():
    # Hide Streamlit default UI
    st.markdown("""
    <style>
        #MainMenu, footer, header {visibility: hidden;}
        .stApp {
            background: #f9fafb;
            display: flex;
            align-items: center;
            justify-content: center;
            font-family: 'Poppins', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        }
        .block-container {
            padding-top: 2rem !important;
            padding-bottom: 2rem !important;
            max-width: 420px !important;
        }
        .main-heading {
            font-size: 38px;
            font-weight: 700;
            color: #111827;
            text-align: center;
            margin-bottom: 10px;
        }
        .subtitle {
            text-align: center;
            color: #6b7280;
            font-size: 15px;
            margin-bottom: 36px;
        }
        .stTextInput > label {
            color: #374151 !important;
            font-weight: 500 !important;
            font-size: 14px !important;
        }
        .stTextInput input {
            border: 1.5px solid #6366f1 !important;
            border-radius: 8px !important;
            padding: 12px 14px !important;
            color: #374151 !important;
            background-color: white !important;
            font-size: 15px !important;
        }
        .stTextInput input:focus {
            border-color: #4f46e5 !important;
            box-shadow: 0 0 0 3px rgba(99,102,241,0.15) !important;
        }
        .stButton > button {
            width: 100%;
            background: linear-gradient(90deg, #6366f1, #8b5cf6) !important;
            color: white !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 12px !important;
            font-size: 16px !important;
            font-weight: 600 !important;
            cursor: pointer !important;
            transition: 0.25s ease !important;
        }
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 14px rgba(99,102,241,0.25) !important;
        }
        .extra-links {
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 13.5px;
            color: #6b7280;
            margin-bottom: 25px;
        }
        .forgot-link {
            color: #4f46e5;
            text-decoration: none;
        }
        .forgot-link:hover {
            text-decoration: underline;
        }
    </style>
    """, unsafe_allow_html=True)

    # Title & Subtitle
    st.markdown('<div class="main-heading">Welcome to EngageSense</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Sign in to access your engagement analytics dashboard</div>', unsafe_allow_html=True)

    # Email & Password
    email = st.text_input("Email Address", placeholder="example@email.com")
    password = st.text_input("Password", type="password", placeholder="••••••••")

    # Remember Me + Forgot Password
    c1, c2 = st.columns([1, 1])
    with c1:
        remember = st.checkbox("Remember me")
    with c2:
        st.markdown('<div style="text-align:right;"><a href="#" class="forgot-link">Forgot Password?</a></div>', unsafe_allow_html=True)

    # Login button
    if st.button("Login"):
        if email and password:
            st.session_state.logged_in = True
            st.success("✅ Login successful! Redirecting...")
            st.rerun()
        else:
            st.warning("⚠️ Please enter both email and password")

    # Footer credits
    st.markdown("<p style='text-align:center; color:#9ca3af; font-size:13px; margin-top:35px;'>EngageSense © 2025 | Developed by Suraj Maurya</p>", unsafe_allow_html=True)
