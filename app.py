import streamlit as st
import os
import sys

# Redirect from this app.py to app_code.py
st.markdown("""
<meta http-equiv="refresh" content="0;url=http://localhost:8501?name=app_code.py">
""", unsafe_allow_html=True)

st.error("### This file is deprecated! Please run 'streamlit run app_code.py' directly or use the run_app.sh script.")

# Additional CSS specifically for the Area dropdown buttons
st.markdown("""
<style>
    /* Force ALL buttons in the sidebar to be orange */
    section[data-testid="stSidebar"] button,
    section[data-testid="stSidebar"] .stButton button,
    section[data-testid="stSidebar"] div[data-testid="StyledLinkButton"] button,
    section[data-testid="stSidebar"] .stSelectbox button,
    section[data-testid="stSidebar"] .css-1cpxqw2,
    section[data-testid="stSidebar"] .css-1d8xkn3,
    section[data-testid="stSidebar"] .css-12ozogq,
    section[data-testid="stSidebar"] .css-cio0dv,
    section[data-testid="stSidebar"] .css-qrbaxs {
        background-color: #FF6600 !important;
        color: white !important;
        border: none !important;
        font-weight: bold !important;
        padding: 0.5rem 1rem !important;
    }
</style>
""", unsafe_allow_html=True)

# Add this after the CSS to create a sidebar toggle button

# Try to execute the app_code.py file directly
try:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    app_code_path = os.path.join(current_dir, "app_code.py")
    
    # Import the app_code.py as a module to run it
    sys.path.insert(0, current_dir)
    import app_code
except Exception as e:
    st.error(f"Error running app_code.py: {e}")
    st.info("Please run the app correctly using: streamlit run app_code.py")