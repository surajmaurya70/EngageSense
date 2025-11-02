import streamlit as st

def show_login_page():
    # Hide Streamlit UI elements
    st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* Base app styling */
        .stApp {
            background: white;
            display: flex;
            align-items: center;
            justify-content: center;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            padding: 0;
        }

        .block-container {
            padding: 2rem 1rem !important;
            max-width: 100% !important;
        }

        /* Center card */
        .login-card {
            background: white;
            border-radius: 16px;
            box-shadow: 0 8px 24px rgba(0,0,0,0.05);
            padding: 2.5rem;
            max-width: 400px;
            width: 100%;
            margin: auto;
        }

        .main-heading {
            font-size: 32px;
            font-weight: 700;
            color: #3d4f5d;
            text-align: center;
            margin-bottom: 10px;
            line-height: 1.3;
        }

        .subtitle {
            text-align: center;
            color: #9ca3af;
            font-size: 15px;
            margin-bottom: 30px;
        }

        /* Inputs */
        .stTextInput > label {
            color: #6b7280 !important;
            font-size: 13px !important;
            font-weight: 500 !important;
        }

        .stTextInput > div > div > input {
            background: white !important;
            border: 1.5px solid #6366f1 !important;
            border-radius: 8px !important;
            padding: 12px 14px !important;
            font-size: 15px !important;
            color: #374151 !important;
            transition: all 0.2s ease !important;
        }

        .stTextInput > div > div > input:focus {
            border-color: #4f46e5 !important;
            box-shadow: 0 0 0 3px rgba(99,102,241,0.1) !important;
        }

        /* Button */
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
        }

        .stButton > button:hover {
            background: #4f46e5 !important;
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(99,102,241,0.3) !important;
        }

        /* Responsive layout */
        @media (max-width: 600px) {
            .login-card {
                padding: 1.8rem 1.2rem;
                max-width: 90%;
            }
            .main-heading {
                font-size: 26px;
            }
            .subtitle {
                font-size: 14px;
                margin-bottom: 20px;
            }
            .stButton > button {
                font-size: 15px !important;
                padding: 12px !important;
            }
        }
    </style>
    """, unsafe_allow_html=True)

    # Centered content inside a "login-card"
    st.markdown("<div class='login-card'>", unsafe_allow_html=True)

    st.markdown('<div class="main-heading">Welcome to<br>EngageSense</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Sign in to access your student engagement dashboard</div>', unsafe_allow_html=True)

    # Inputs
    email = st.text_input("E-mail", placeholder="example@email.com", key="email")
    password = st.text_input("Password", type="password", placeholder="Your Password", key="password")

    # Remember me + Forgot password
    col1, col2 = st.columns([1, 1])
    with col1:
        remember = st.checkbox("Remember me")
    with col2:
        st.markdown(
            '<div style="text-align:right; color:#6366f1; font-size:14px; margin-top:8px; cursor:pointer;">Forgot Password?</div>',
            unsafe_allow_html=True
        )

    # Login button
    if st.button("Login", use_container_width=True):
        if email and password:
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.warning("⚠️ Please enter both email and password")

    st.markdown("</div>", unsafe_allow_html=True)
