# Stripe Payment Setup for BritMetrics

## Current Status
✅ **Demo Mode Active** - Payment button works but doesn't charge real money  
✅ **Access Code Active** - Use code `tatakas101` to enter

## To Enable Real Payments (£5)

### Step 1: Create Stripe Account
1. Go to https://stripe.com
2. Sign up for a free account
3. You'll get test keys immediately, real keys after verification

### Step 2: Get Your API Keys
1. Login to Stripe Dashboard
2. Go to Developers → API keys
3. Copy your **Publishable key** (starts with `pk_test_`)
4. Copy your **Secret key** (starts with `sk_test_`)

### Step 3: Install Stripe Package
```bash
pip install stripe
```

### Step 4: Set Environment Variables

**On Local Machine:**
```bash
export STRIPE_PUBLISHABLE_KEY="pk_test_your_key_here"
export STRIPE_SECRET_KEY="sk_test_your_key_here"
```

**On Hostinger Server:**
```bash
# SSH into server
ssh root@srv1079042.hostinger.com

# Edit environment file
nano /var/www/britmetrics/.env

# Add these lines:
STRIPE_PUBLISHABLE_KEY=pk_test_your_key_here
STRIPE_SECRET_KEY=sk_test_your_key_here

# Save and exit (Ctrl+X, Y, Enter)
```

### Step 5: Update Code to Use Real Stripe

Edit `app.py` to import and use the Stripe payment module:

```python
from backend.stripe_payment import render_stripe_payment_button, check_payment_status

# In the payment section, replace the demo button with:
render_stripe_payment_button(PAYMENT_AMOUNT, PAYMENT_DESCRIPTION)

# Check payment status on page load
if check_payment_status():
    st.session_state.payment_completed = True
```

### Step 6: Test Payment Flow

1. Visit britmetrics.com
2. Click "Pay £5 for Access"
3. You'll be redirected to Stripe checkout
4. Use test card: **4242 4242 4242 4242**
5. Any future expiry date, any CVC
6. Complete payment
7. You'll be redirected back to the app

### Step 7: Test vs Live Keys

**Test Mode:**
- Keys start with `pk_test_` and `sk_test_`
- No real charges
- Use test card numbers

**Live Mode:**
- Keys start with `pk_live_` and `sk_live_`
- Real charges
- Need verified account
- Switch in Stripe Dashboard

## Alternative: PayPal Integration

If you prefer PayPal over Stripe:

1. Use PayPal Buttons API
2. Or use services like Gumroad, Paddle
3. Simpler setup, less customization

## Current Implementation

The app currently works in **demo mode**:
- Shows payment button
- Explains Stripe setup needed
- Users can use access code `tatakas101` instead
- No real payments processed

## Access Control Methods

**1. Access Code (Currently Active)**
- Code: `tatakas101`
- Instant access
- No payment

**2. Stripe Payment (Setup Required)**
- Real £5 payment
- Automatic access after payment
- Requires Stripe account setup

## Security Notes

- Never commit API keys to GitHub
- Use environment variables
- Test with test keys first
- Rotate keys if compromised

## Support

If you need help setting up Stripe:
1. Read official docs: https://stripe.com/docs
2. Contact support: support@britmetrics.com
3. For demo access, use code: `tatakas101`
