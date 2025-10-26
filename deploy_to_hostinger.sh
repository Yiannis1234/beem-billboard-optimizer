#!/bin/bash

# BritMetrics Deployment Script for Hostinger
# This script helps deploy updates to your Hostinger VPS

echo "📊 BritMetrics - Hostinger Deployment Script"
echo "=============================================="
echo ""

# Configuration
read -p "Enter your Hostinger VPS IP address: " VPS_IP
read -p "Enter your SSH username (default: root): " SSH_USER
SSH_USER=${SSH_USER:-root}

echo ""
echo "🔍 Deployment Configuration:"
echo "   VPS IP: $VPS_IP"
echo "   SSH User: $SSH_USER"
echo "   Domain: britmetrics.com"
echo ""

read -p "Does this look correct? (y/n): " CONFIRM
if [ "$CONFIRM" != "y" ]; then
    echo "❌ Deployment cancelled"
    exit 1
fi

echo ""
echo "📦 Step 1: Committing local changes..."
git add .
git commit -m "Deploy BritMetrics to production" || echo "No changes to commit"
git push origin main

echo ""
echo "🚀 Step 2: Connecting to VPS and deploying..."

ssh $SSH_USER@$VPS_IP << 'ENDSSH'
    echo "📥 Pulling latest code..."
    cd /var/www/britmetrics
    git pull origin main
    
    echo "📦 Installing dependencies..."
    source venv/bin/activate
    pip install -r requirements.txt
    
    echo "🔄 Restarting application..."
    sudo supervisorctl restart britmetrics
    
    echo "✅ Checking status..."
    sudo supervisorctl status britmetrics
    
    echo ""
    echo "📊 Recent logs:"
    sudo tail -n 20 /var/log/britmetrics.out.log
ENDSSH

echo ""
echo "✅ Deployment complete!"
echo ""
echo "🌐 Your site should be live at: https://britmetrics.com"
echo "📊 Check status: ssh $SSH_USER@$VPS_IP 'sudo supervisorctl status britmetrics'"
echo ""

