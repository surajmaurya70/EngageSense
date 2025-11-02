import streamlit as st

def show_login_page():
    # Hide Streamlit default elements
    st.markdown("""
    <style>
        /* Hide Streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* Full-screen gradient background */
        .stApp {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        /* Main login container with glassmorphism */
        .login-container {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 50px 40px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            max-width: 400px;
            width: 100%;
            animation: slideIn 0.6s ease-out;
        }
        
        /* Slide-in animation */
        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateY(-30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        /* Logo/Title styling */
        .login-title {
            text-align: center;
            margin-bottom: 10px;
        }
        
        .login-title h1 {
            font-size: 48px;
            font-weight: 800;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin: 0;
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.05); }
        }
        
        .login-subtitle {
            text-align: center;
            color: #666;
            font-size: 14px;
            margin-bottom: 30px;
            font-weight: 500;
        }
        
        /* Input field styling */
        .stTextInput > div > div > input {
            border-radius: 12px;
            border: 2px solid #e0e0e0;
            padding: 14px 18px;
            font-size: 15px;
            transition: all 0.3s ease;
            background: #f8f9fa;
        }
        
        .stTextInput > div > div > input:focus {
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
            background: white;
        }
        
        /* Label styling */
        .stTextInput > label {
            font-weight: 600;
            color: #333;
            font-size: 14px;
            margin-bottom: 8px;
        }
        
        /* Login button styling */
        .stButton > button {
            width: 100%;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 12px;
            padding: 14px;
            font-size: 16px;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
            margin-top: 10px;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
        }
        
        .stButton > button:active {
            transform: translateY(0);
        }
        
        /* Error message styling */
        .stAlert {
            border-radius: 12px;
            animation: shake 0.5s;
        }
        
        @keyframes shake {
            0%, 100% { transform: translateX(0); }
            25% { transform: translateX(-10px); }
            75% { transform: translateX(10px); }
        }
        
        /* Divider styling */
        .divider {
            text-align: center;
            margin: 30px 0;
            position: relative;
        }
        
        .divider::before,
        .divider::after {
            content: '';
            position: absolute;
            top: 50%;
            width: 40%;
            height: 1px;
            background: #e0e0e0;
        }
        
        .divider::before { left: 0; }
        .divider::after { right: 0; }
        
        .divider span {
            background: white;
            padding: 0 15px;
            color: #999;
            font-size: 13px;
            font-weight: 600;
        }
        
        /* Footer text */
        .login-footer {
            text-align: center;
            margin-top: 25px;
            color: #999;
            font-size: 13px;
        }
        
        /* Remove extra spacing */
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Center container
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Logo/Title
        st.markdown("""
        <div class="login-container">
            <div class="login-title">
                <h1>📊 EngageSense</h1>
            </div>
            <p class="login-subtitle">AI-Powered Student Engagement Analytics</p>
        """, unsafe_allow_html=True)
        
        # Login form
        username = st.text_input("👤 Username", placeholder="Enter your username", key="login_username")
        password = st.text_input("🔒 Password", type="password", placeholder="Enter your password", key="login_password")
        
        # Login button
        if st.button("🚀 Log In", use_container_width=True):
            if username == "admin" and password == "admin123":
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("❌ Invalid credentials! Please try again.")
        
        # Divider
        st.markdown("""
        <div class="divider">
            <span>OR</span>
        </div>
        """, unsafe_allow_html=True)
        
        # Demo credentials
        st.info("💡 **Demo Credentials**\n\n👤 Username: `admin`  \n🔑 Password: `admin123`")
        
        # Footer
        st.markdown("""
        <div class="login-footer">
            <p>© 2025 EngageSense. All rights reserved.</p>
        </div>
        </div>
        """, unsafe_allow_html=True)

