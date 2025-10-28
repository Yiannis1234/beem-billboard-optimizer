"""
Stripe payment integration for BritMetrics
Requires: pip install stripe
"""

import streamlit as st
import stripe
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Stripe configuration
STRIPE_PUBLISHABLE_KEY = os.getenv("STRIPE_PUBLISHABLE_KEY", "")
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY", "")

if STRIPE_SECRET_KEY:
    stripe.api_key = STRIPE_SECRET_KEY
else:
    st.error("Stripe API keys not configured. Please set up .env file.")


def create_payment_session(amount: float, description: str, currency: str = "gbp"):
    """
    Create a Stripe checkout session
    
    Args:
        amount: Amount in pounds (£)
        description: Product description
        currency: Currency code (default: gbp)
    
    Returns:
        checkout_session_id and url
    """
    try:
        # Convert pounds to pence (Stripe uses smallest currency unit)
        amount_pence = int(amount * 100)
        
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': currency,
                    'product_data': {
                        'name': 'BritMetrics Premium Access',
                        'description': description,
                    },
                    'unit_amount': amount_pence,
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url='https://britmetrics.com?session_id={CHECKOUT_SESSION_ID}',
            cancel_url='https://britmetrics.com',
        )
        
        return checkout_session.id, checkout_session.url
        
    except Exception as e:
        st.error(f"Payment error: {str(e)}")
        return None, None


def verify_payment(session_id: str):
    """
    Verify if a payment was successful
    
    Args:
        session_id: Stripe checkout session ID
    
    Returns:
        True if payment successful, False otherwise
    """
    try:
        session = stripe.checkout.Session.retrieve(session_id)
        return session.payment_status == 'paid'
    except Exception as e:
        st.error(f"Payment verification error: {str(e)}")
        return False


def render_stripe_payment_button(amount: float, description: str):
    """
    Render a Stripe payment button that directly redirects to Stripe checkout
    
    Args:
        amount: Amount in pounds
        description: Product description
    """
    # Create Stripe checkout session immediately
    session_id, checkout_url = create_payment_session(amount, description)
    
    if checkout_url:
        # Direct redirect button - no intermediate steps
        st.markdown(f"""
        <div style='text-align: center; margin: 1rem 0;'>
            <a href="{checkout_url}" target="_blank" style='display: inline-block; background: #00d4aa; color: white; padding: 15px 30px; text-decoration: none; border-radius: 10px; font-weight: bold; font-size: 16px; box-shadow: 0 4px 8px rgba(0,0,0,0.2);'>
                💳 Pay £{amount} for Access
            </a>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.error("Payment system unavailable. Please contact support.")


def check_payment_status():
    """
    Check if user has completed payment based on session and email
    """
    # Check query params for session_id (returned from Stripe)
    session_id = st.query_params.get('session_id')
    email = st.query_params.get('email', st.query_params.get('customer_email', ''))
    
    if session_id and email and verify_payment(session_id):
        # Import and use cookie_access to save email
        from backend.cookie_access import save_access_to_cookie
        save_access_to_cookie(email, session_id)
        
        # Mark as permanently authenticated
        st.session_state.payment_completed = True
        st.session_state.authenticated = True
        st.session_state.permanent_access = True
        return True
    
    return False


def is_permanently_authenticated():
    """
    Check if user has permanent access (paid or code)
    """
    # Check session state first
    if st.session_state.get('permanent_access', False):
        return True
    
    return (st.session_state.get('authenticated', False) or 
            st.session_state.get('payment_completed', False))
