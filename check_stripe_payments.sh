# CHECK STRIPE PAYMENTS - RUN THESE COMMANDS

# 1. Check if you're in LIVE mode on Stripe dashboard
echo "Go to: https://dashboard.stripe.com"
echo "Look for 'LIVE' mode toggle (not 'Test')"

# 2. Check payments in Stripe dashboard
echo "Go to: https://dashboard.stripe.com/payments"
echo "Look for recent £5 payments"

# 3. Check your .env file has LIVE keys
echo "Checking .env file on server:"
cat /var/www/britmetrics/.env

# 4. Check Stripe logs
echo "Checking application logs:"
tail -50 /var/log/britmetrics.log | grep -i stripe

# 5. Test payment creation
echo "Testing payment session creation:"
cd /var/www/britmetrics
source venv/bin/activate
python3 -c "
import stripe
import os
from dotenv import load_dotenv
load_dotenv()
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')
print('API Key starts with:', stripe.api_key[:20] if stripe.api_key else 'NOT SET')
print('Mode:', 'LIVE' if stripe.api_key.startswith('sk_live_') else 'TEST')
"
