# 🔒 Stripe Payment Integration - Step by Step

## ✅ You Already Have:
- ✅ Stripe dashboard access (BRITMETRICS sandbox)
- ✅ Code updated to support Stripe
- ✅ Payment button ready

## 📋 What You Need To Do:

### Step 1: Get Your Stripe API Keys

1. In your Stripe dashboard, click **"API keys"** in the left sidebar
2. Copy your **Publishable key** (starts with `pk_test_`)
3. Copy your **Secret key** (starts with `sk_test_`)
   
   **Important:** Use TEST keys first, not live keys!

### Step 2: Install Stripe on Hostinger

SSH into your Hostinger server:

```bash
ssh root@srv1079042.hostinger.com
```

Then run:

```bash
cd /var/www/britmetrics
source venv/bin/activate
pip install stripe
```

Verify installation:
```bash
python -c "import stripe; print(stripe.__version__)"
```

### Step 3: Set Environment Variables

Create a `.env` file in the project root:

```bash
nano /var/www/britmetrics/.env
```

Add these lines (replace with YOUR actual keys from Stripe dashboard):

```bash
STRIPE_PUBLISHABLE_KEY=pk_test_YOUR_KEY_HERE
STRIPE_SECRET_KEY=sk_test_YOUR_KEY_HERE
```

Save with `Ctrl+X`, then `Y`, then `Enter`.

### Step 4: Update Python Code to Read Environment Variables

The `backend/stripe_payment.py` already reads from environment variables, so this should work automatically!

But verify by checking the file loads the keys:

```bash
python -c "import os; print('Keys loaded:', os.getenv('STRIPE_PUBLISHABLE_KEY')[:20] if os.getenv('STRIPE_PUBLISHABLE_KEY') else 'NOT FOUND')"
```

### Step 5: Pull Latest Code and Restart

```bash
cd /var/www/britmetrics
git pull origin main
sudo pkill -9 -f streamlit
sleep 2
source venv/bin/activate
nohup streamlit run app.py --server.port 8502 --server.address localhost --server.headless true > /var/log/britmetrics.log 2>&1 &
```

### Step 6: Test Payment Flow

1. Visit `https://britmetrics.com`
2. You should see two options:
   - **Left:** Access code entry
   - **Right:** "Pay £5 for Access" button
3. Click the payment button
4. You'll be redirected to Stripe Checkout
5. Use test card: `4242 4242 4242 4242`
6. Any future expiry date (e.g., 12/25)
7. Any 3-digit CVC (e.g., 123)
8. Complete payment
9. You'll be redirected back to britmetrics.com
10. You'll have access!

## 🧪 Testing

### Use These Test Cards:

**Success:** `4242 4242 4242 4242`  
**Decline:** `4000 0000 0000 0002`  
**3D Secure:** `4000 0025 0000 3155`

### Troubleshooting

**Problem:** "Stripe error: No API key provided"
- **Fix:** Environment variables not set. Run: `printenv STRIPE_PUBLISHABLE_KEY`

**Problem:** Payment button doesn't appear
- **Fix:** Check app logs: `tail -f /var/log/britmetrics.log`

**Problem:** Redirect doesn't work
- **Fix:** Check that `https://britmetrics.com` is the success_url in code

## 🔐 Switching to Live Mode

When ready to accept real payments:

1. In Stripe dashboard, toggle **"Exit sandbox"**
2. Copy the LIVE keys (starts with `pk_live_` and `sk_live_`)
3. Update your `.env` file with LIVE keys
4. Restart the app
5. **Remove test card** from your testing!

## 📊 Monitor Payments

View payments in Stripe dashboard:
- **Test Mode:** `https://dashboard.stripe.com/test/payments`
- **Live Mode:** `https://dashboard.stripe.com/payments`

## 🎯 Current Status

- ✅ Code ready for Stripe
- ✅ Payment button appears
- ⏳ Need to install Stripe package
- ⏳ Need to set API keys
- ⏳ Need to test payment flow

## 📞 Support

If you encounter issues:
1. Check `/var/log/britmetrics.log` for errors
2. Verify API keys are correct
3. Ensure internet connection (Stripe needs network access)
4. Test with Stripe test cards first

---

**Next Step:** Go to your Hostinger server and run Step 2 (install Stripe package)!

