#!/usr/bin/env python3
"""
Add vamvak@outlook.com to paid customers list
"""

import json
import os
from datetime import datetime

def add_vamvak_to_paid_customers():
    """Add vamvak@outlook.com to paid customers"""
    
    PAID_CUSTOMERS_FILE = "paid_customers.json"
    
    # Load existing customers
    if os.path.exists(PAID_CUSTOMERS_FILE):
        try:
            with open(PAID_CUSTOMERS_FILE, 'r') as f:
                customers = json.load(f)
        except:
            customers = {}
    else:
        customers = {}
    
    # Add vamvak@outlook.com
    customers["vamvak@outlook.com"] = {
        "session_id": "manual_admin_access",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "email": "vamvak@outlook.com"
    }
    
    # Save back to file
    with open(PAID_CUSTOMERS_FILE, 'w') as f:
        json.dump(customers, f, indent=2)
    
    print("✅ Added vamvak@outlook.com to paid customers!")
    print(f"📧 Email: vamvak@outlook.com")
    print(f"🕒 Added: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📁 File: {PAID_CUSTOMERS_FILE}")

if __name__ == "__main__":
    add_vamvak_to_paid_customers()
