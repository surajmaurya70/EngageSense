login_content = '''import streamlit as st
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# DEMO MODE - Any credentials work
def check_credentials(email, password):
    # Accept ANY email and password for demo
    if email and password:
        return "instructor"
    return None

def show_login_page():
    st.markdown("""
    <style>
    .stApp { background: #f8f9fa; }
    .login-box {
        max-width: 480px;
        margin: 5rem auto;
        padding: 3rem;
        background: white;
        border-radius: 20px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    }
    .logo-circle {
        width: 90px;
        height: 90px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 22px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 3rem;
        margin: 0 auto 1.5rem;
    }
    .app-title {
        text-align: center;
        font-size: 2.8rem;
        font-weight: 800;
        color: #1a1a1a;
        margin-bottom: 0.5rem;
    }
    .app-subtitle {
        text-align: center;
        font-size: 1.1rem;
        color: #666;
        margin-bottom: 3rem;
    }
    .stButton>button {
        width: 100%;
        background: #667eea;
        color: white;
        padding: 0.8rem;
        border-radius: 12px;
        font-weight: 600;
        border: none;
        font-size: 1.05rem;
    }
    .stButton>button:hover {
        background: #5568d3;
    }
    </style>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<div class="logo-circle">📊</div>', unsafe_allow_html=True)
        st.markdown('<h1 class="app-title">EngageSense</h1>', unsafe_allow_html=True)
        st.markdown('<p class="app-subtitle">AI-Powered Student Engagement Analytics</p>', unsafe_allow_html=True)
        
        with st.form("login_form"):
            st.markdown("📧 **Email Address**")
            email = st.text_input("", placeholder="instructor@university.edu", label_visibility="collapsed", key="email")
            
            st.markdown("🔒 **Password**")
            password = st.text_input("", type="password", placeholder="••••••••", label_visibility="collapsed", key="password")
            
            submit = st.form_submit_button("Sign In to Dashboard")
            
            if submit:
                role = check_credentials(email, password)
                if role:
                    st.session_state.logged_in = True
                    st.session_state.user_email = email
                    st.session_state.user_role = role
                    st.success("✅ Login successful!")
                    st.rerun()
                else:
                    st.error("❌ Please enter both email and password!")
        
        st.markdown("<p style='text-align:center; margin-top:1rem;'><a href='#' style='color:#667eea;'>Forgot your password?</a></p>", unsafe_allow_html=True)
        st.markdown("<hr style='margin:2rem 0;'>", unsafe_allow_html=True)
        st.caption("**Demo credentials:** Any email and password will work")
        st.caption("© 2025 EngageSense • Privacy-first analytics for educators")
'''

with open('login.py', 'w') as f:
    f.write(login_content)

print("✅ Login fixed - any credentials now work!")
