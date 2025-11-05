# Stripe API Key Setup

## Required Environment Variable

To enable payment functionality, you need to set the Stripe Secret Key:

```bash
export STRIPE_SECRET_KEY="sk_live_..."  # or sk_test_... for testing
```

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

