import streamlit as st

def show_navbar():
    # Remove all old buttons / icons / filters
    # Just keep top space if needed for layout consistency
    st.markdown("""
        <style>
        /* Hide any default navbar items */
        div[data-testid="stHorizontalBlock"] button,
        div[data-testid="stHorizontalBlock"] svg,
        div[data-testid="stHorizontalBlock"] p {
            display: none !important;
        }
        </style>
    """, unsafe_allow_html=True)
