# Stripe API Key Setup

## Required Environment Variables

To enable payment functionality, you need to set BOTH Stripe keys:

```bash
export STRIPE_PUBLISHABLE_KEY="pk_test_51SQ4hnBoIqMUQLys40me9RfJxojooBK8LBGkDDgfCrwcflo78YDQ2DebdCunXRPGCNA0P4bL1HBznhcepuz3Nnf000kHrOsGa0"
export STRIPE_SECRET_KEY="sk_test_YOUR_SECRET_KEY_HERE"
```

**⚠️ SECURITY:** 
- The publishable key is configured in code (safe to expose)
- The secret key must be set as an environment variable on your server
- Never commit secret keys to git!
- Get your secret key from: https://dashboard.stripe.com/apikeys

## How to Get Your Stripe API Key

1. Go to https://dashboard.stripe.com/apikeys
2. Sign up or log in to your Stripe account
3. Copy your **Secret key** (starts with `sk_live_` for production or `sk_test_` for testing)
4. Set it as an environment variable on your server

## For Hostinger Server

Add to your environment variables or `.env` file:

```bash
STRIPE_SECRET_KEY=sk_live_your_actual_key_here
```

Then restart the API server:
```bash
sudo supervisorctl restart britmetrics-api
```

## Testing

- Use `sk_test_...` keys for testing
- Use `sk_live_...` keys for production
- Test cards: https://stripe.com/docs/testing

## Current Status

⚠️ **Stripe API key not found in codebase** - You need to set it up manually.

The system will work without Stripe (free trials only), but payment functionality will be disabled until you add the key.

