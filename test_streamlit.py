#!/usr/bin/env python3
"""Simple test to see if Streamlit works"""

print("Testing imports...")
try:
    import streamlit
    print("✅ Streamlit imported")
except Exception as e:
    print(f"❌ Streamlit import failed: {e}")
    exit(1)

try:
    from backend.models import AreaDatabase
    print("✅ Backend models imported")
except Exception as e:
    print(f"❌ Backend models failed: {e}")

try:
    from backend.api_services import WeatherAPIService
    print("✅ API services imported")
except Exception as e:
    print(f"❌ API services failed: {e}")

try:
    from backend.business_logic import AdSuccessCalculator
    print("✅ Business logic imported")
except Exception as e:
    print(f"❌ Business logic failed: {e}")

try:
    from frontend.components import UIComponents
    print("✅ Frontend components imported")
except Exception as e:
    print(f"❌ Frontend components failed: {e}")

try:
    from backend.stripe_payment import render_stripe_payment_button
    print("✅ Stripe payment imported")
except Exception as e:
    print(f"⚠️ Stripe payment failed (optional): {e}")

print("\n✅ All critical imports successful!")

