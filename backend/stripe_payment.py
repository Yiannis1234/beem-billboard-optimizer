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
    Render a Stripe payment button that redirects to Stripe checkout
    
    Args:
        amount: Amount in pounds
        description: Product description
    """
    if st.button(f"💳 Pay £{amount} for Access", type="secondary", use_container_width=True):
        # Store current URL for success redirect
        st.session_state['current_url'] = st.query_params.get('payment_success', '')
        
        # Create Stripe checkout session
        session_id, checkout_url = create_payment_session(amount, description)
        
        if checkout_url:
            # Redirect to Stripe checkout
            st.markdown(f"""
            <script>
                window.location.href = '{checkout_url}';
            </script>
            """, unsafe_allow_html=True)
            
            st.info("Redirecting to secure payment...")
        else:
            st.error("Failed to create payment session. Please try again.")


def check_payment_status():
    """
    Check if user has completed payment based on session
    """
    # Check query params for session_id (returned from Stripe)
    session_id = st.query_params.get('session_id')
    
    if session_id and verify_payment(session_id):
        return True
    
    return False
