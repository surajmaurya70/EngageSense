import streamlit as st
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Demo credentials (replace with SQL later)
DEMO_USERS = {
    "instructor@university.edu": {
        "password": hash_password("demo123"),
        "role": "instructor"
    },
    "admin@university.edu": {
        "password": hash_password("admin123"),
        "role": "admin"
    }
}

def check_credentials(email, password):
    hashed = hash_password(password)
    user = DEMO_USERS.get(email)
    if user and user["password"] == hashed:
        return user["role"]
    return None

def show_login_page():
    st.markdown("""
    <style>
    .login-container {
        max-width: 450px;
        margin: 0 auto;
        padding: 3rem 2rem;
    }
    .logo-container {
        text-align: center;
        margin-bottom: 2rem;
    }
    .logo {
        width: 80px;
        height: 80px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-size: 2.5rem;
        margin-bottom: 1rem;
    }
    .app-title {
        font-size: 2.5rem;
        font-weight: 800;
        color: #1a1a1a;
        margin-bottom: 0.5rem;
    }
    .app-subtitle {
        font-size: 1rem;
        color: #666;
        margin-bottom: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="login-container">
        <div class="logo-container">
            <div class="logo">📊</div>
            <h1 class="app-title">EngageSense</h1>
            <p class="app-subtitle">AI-Powered Student Engagement Analytics</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("login_form"):
        st.markdown("📧 **Email Address**")
        email = st.text_input("", placeholder="instructor@university.edu", label_visibility="collapsed")
        
        st.markdown("🔒 **Password**")
        password = st.text_input("", type="password", placeholder="••••••••", label_visibility="collapsed")
        
        submit = st.form_submit_button("Sign In to Dashboard", use_container_width=True)
        
        if submit:
            role = check_credentials(email, password)
            if role:
                st.session_state.logged_in = True
                st.session_state.user_email = email
                st.session_state.user_role = role
                st.rerun()
            else:
                st.error("❌ Invalid credentials!")
    
    st.markdown("<p style='text-align:center;'><a href='#'>Forgot your password?</a></p>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)
    st.caption("**Demo credentials:** Any email and password will work")
    st.caption("© 2025 EngageSense • Privacy-first analytics for educators")
