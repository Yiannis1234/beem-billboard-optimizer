"""
Simpler permanent access - save to cookie/localStorage
"""

import json
import streamlit as st

def save_access_to_cookie(session_id):
    """Save access to browser cookie"""
    # Store in Streamlit session state
    st.session_state['paid_access'] = session_id
    
    # Also store in query params so it persists
    st.query_params['paid'] = 'true'
    st.query_params['access_id'] = session_id

def has_paid_cookie():
    """Check if user has paid access cookie"""
    # Check session state first
    if st.session_state.get('paid_access'):
        return True
    
    # Check query params
    if st.query_params.get('paid') == 'true':
        access_id = st.query_params.get('access_id')
        if access_id:
            st.session_state['paid_access'] = access_id
            return True
    
    return False

def get_access_id():
    """Get the access ID from cookie"""
    return st.session_state.get('paid_access') or st.query_params.get('access_id')

