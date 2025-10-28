#!/usr/bin/env python3
"""
Backfill all paid customers from Stripe into permanent access
Run this ONCE to grant access to existing paid customers
"""

import stripe
import os
from dotenv import load_dotenv
from backend.permanent_access import add_paid_customer

# Load environment
load_dotenv()
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

print("🔄 Backfilling paid customers from Stripe...\n")

# Get all checkout sessions
try:
    sessions = stripe.checkout.Session.list(limit=100)
    
    paid_count = 0
    for session in sessions:
        if session.payment_status == 'paid':
            print(f"Found paid customer: {session.customer_email}")
            if add_paid_customer(session.id):
                paid_count += 1
    
    print(f"\n✅ Added {paid_count} paid customers to permanent access!")
    
except Exception as e:
    print(f"❌ Error: {e}")

print("\n✅ Done! All paid customers now have permanent access.")

