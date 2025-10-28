"""
Permanent access system for BritMetrics
Stores paid customer emails for unlimited access
"""

import json
import os
from datetime import datetime
import stripe

# File to store paid customers
PAID_CUSTOMERS_FILE = "/var/www/britmetrics/paid_customers.json"

def load_paid_customers():
    """Load list of paid customers"""
    if os.path.exists(PAID_CUSTOMERS_FILE):
        try:
            with open(PAID_CUSTOMERS_FILE, 'r') as f:
                return json.load(f)
        except:
            return []
    return []

def save_paid_customers(customers):
    """Save list of paid customers"""
    os.makedirs(os.path.dirname(PAID_CUSTOMERS_FILE), exist_ok=True)
    with open(PAID_CUSTOMERS_FILE, 'w') as f:
        json.dump(customers, f, indent=2)

def add_paid_customer(session_id, email=None):
    """Add a customer who has paid"""
    customers = load_paid_customers()
    
    # Get payment details from Stripe
    try:
        session = stripe.checkout.Session.retrieve(session_id)
        if session.payment_status == 'paid':
            customer_data = {
                'session_id': session_id,
                'email': email or session.customer_email or 'unknown',
                'amount': session.amount_total / 100,
                'currency': session.currency,
                'paid_at': datetime.now().isoformat(),
                'stripe_customer_id': session.customer
            }
            
            # Check if already exists
            if not any(c['session_id'] == session_id for c in customers):
                customers.append(customer_data)
                save_paid_customers(customers)
                return True
    except Exception as e:
        print(f"Error adding paid customer: {e}")
    
    return False

def is_customer_paid(email=None, session_id=None):
    """Check if customer has paid"""
    customers = load_paid_customers()
    
    if email:
        return any(c['email'] == email for c in customers)
    
    if session_id:
        return any(c['session_id'] == session_id for c in customers)
    
    return False

def get_all_paid_session_ids():
    """Get all paid session IDs"""
    customers = load_paid_customers()
    return [c['session_id'] for c in customers if 'session_id' in c]

def get_paid_customers():
    """Get all paid customers"""
    return load_paid_customers()
