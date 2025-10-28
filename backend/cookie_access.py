"""
Simpler permanent access - save email and session to file
"""

import json
import os
import streamlit as st
from datetime import datetime

PAID_CUSTOMERS_FILE = "paid_customers.json"

def load_paid_customers():
    """Load paid customers from file"""
    if os.path.exists(PAID_CUSTOMERS_FILE):
        try:
            with open(PAID_CUSTOMERS_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_paid_customers(customers):
    """Save paid customers to file"""
    with open(PAID_CUSTOMERS_FILE, 'w') as f:
        json.dump(customers, f, indent=2)

def add_paid_customer(email, session_id):
    """Add a customer to paid list"""
    customers = load_paid_customers()
    customers[email] = {
        'session_id': session_id,
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'email': email
    }
    save_paid_customers(customers)

def is_customer_paid(email):
    """Check if customer has paid"""
    customers = load_paid_customers()
    return email in customers

def save_access_to_cookie(email, session_id):
    """Save access with email"""
    # Store in Streamlit session state
    st.session_state['paid_access'] = session_id
    st.session_state['paid_email'] = email
    
    # Save to file
    add_paid_customer(email, session_id)

def has_paid_cookie():
    """Check if user has paid access"""
    # Check session state
    email = st.session_state.get('paid_email')
    if email and is_customer_paid(email):
        return True
    
    # Check query params
    if st.query_params.get('paid') == 'true':
        email = st.query_params.get('email')
        if email and is_customer_paid(email):
            st.session_state['paid_access'] = email
            st.session_state['paid_email'] = email
            return True
    
    return False

def get_access_email():
    """Get the paid email"""
    return st.session_state.get('paid_email') or st.query_params.get('email')
