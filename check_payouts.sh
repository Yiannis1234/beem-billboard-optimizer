# CHECK STRIPE PAYOUTS - RUN THESE COMMANDS

cd /var/www/britmetrics
source venv/bin/activate

python3 << 'EOF'
import stripe
import os
from dotenv import load_dotenv
load_dotenv()
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

print("=== CHECKING STRIPE ACCOUNT STATUS ===\n")

# Get account details
account = stripe.Account.retrieve()
print(f"Account ID: {account.id}")
print(f"Country: {account.country}")
print(f"Default currency: {account.default_currency}")
print(f"Charges enabled: {account.charges_enabled}")
print(f"Payouts enabled: {account.payouts_enabled}")
print()

# Check payouts
print("=== RECENT PAYOUTS ===")
try:
    payouts = stripe.Payout.list(limit=5)
    for payout in payouts:
        print(f"Amount: {payout.amount/100}£, Status: {payout.status}, Date: {payout.created}")
except:
    print("No payouts yet")
print()

# Check balance
print("=== BALANCE ===")
balance = stripe.Balance.retrieve()
print(f"Available: {balance.available[0].amount/100} {balance.available[0].currency}")
print(f"Pending: {balance.pending[0].amount/100} {balance.pending[0].currency}")
print()

print("=== NEXT STEPS ===")
print("1. Go to: https://dashboard.stripe.com/settings/account")
print("2. Complete account verification")
print("3. Add your bank account for payouts")
print("4. Payments will transfer to your bank 2-7 days after they're made")
EOF

