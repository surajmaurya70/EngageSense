import streamlit as st

def show_navbar():
    # Initialize states only
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'Dashboard'
    
    # Nothing visible - completely empty navbar
    pass


