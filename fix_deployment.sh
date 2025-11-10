#!/bin/bash
# Quick deployment fix script - run this on your Hostinger server

echo "🔍 Checking deployment status..."

# Check if in right directory
cd /var/www/britmetrics || { echo "❌ /var/www/britmetrics not found!"; exit 1; }

# Pull latest code
echo "📥 Pulling latest code..."
git pull origin main

# Check if Login.jsx exists
if [ ! -f "frontend-react/src/pages/Login.jsx" ]; then
    echo "❌ Login.jsx not found! Code may not be pulled correctly."
    exit 1
fi

# Rebuild React
echo "🔨 Building React frontend..."
cd frontend-react
npm run build

# Check if build succeeded
if [ ! -f "dist/index.html" ]; then
    echo "❌ Build failed! dist/index.html not found."
    exit 1
fi

# Restart API
echo "🔄 Restarting API..."
cd ..
sudo supervisorctl restart britmetrics-api

# Reload Nginx
echo "🔄 Reloading Nginx..."
sudo systemctl reload nginx

# Check status
echo ""
echo "✅ Deployment complete!"
echo ""
echo "📊 Status check:"
sudo supervisorctl status britmetrics-api
echo ""
echo "🌐 Test in browser (use Incognito mode):"
echo "   https://britmetrics.com"
echo "   https://britmetrics.com/login"

