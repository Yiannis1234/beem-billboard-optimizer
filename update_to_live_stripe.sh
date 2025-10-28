#!/bin/bash
# Update to LIVE Stripe keys for real payments

echo "⚠️  WARNING: Switching to LIVE Stripe keys - REAL PAYMENTS WILL BE PROCESSED!"

# Create .env file with LIVE keys
cat > /var/www/britmetrics/.env << 'EOF'
STRIPE_PUBLISHABLE_KEY=pk_live_51SNA0ZB7i59qxjV3dUapqNrnPk743EbWV4w7QNqllzcutma0G3OpQIPV6BUc1anpVYXZdaCM5WRgx9sBRIH6qTHT008tJlryaw
STRIPE_SECRET_KEY=sk_live_YOUR_SECRET_KEY_HERE
EOF

echo "✅ LIVE keys set!"
echo "⚠️  Make sure to add your LIVE secret key to the .env file!"
echo "⚠️  This will process REAL payments now!"

