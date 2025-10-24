#!/bin/bash

# Deployment script for Hostinger
# Run this on your Hostinger VPS

echo "🚀 Deploying Ad Success Predictor to britmetrics.com"
echo "=================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check if we're in the right directory
if [ ! -f "simple_ad_success.py" ]; then
    print_error "simple_ad_success.py not found. Are you in the right directory?"
    exit 1
fi

print_status "Pulling latest changes from GitHub..."
git pull origin main

if [ $? -ne 0 ]; then
    print_error "Failed to pull from GitHub"
    exit 1
fi

# Check if Docker is available
if command -v docker &> /dev/null && command -v docker-compose &> /dev/null; then
    print_status "Using Docker deployment..."
    
    # Stop existing containers
    print_status "Stopping existing containers..."
    docker-compose down
    
    # Build and start new containers
    print_status "Building and starting new containers..."
    docker-compose up -d --build
    
    if [ $? -eq 0 ]; then
        print_status "Docker deployment successful!"
    else
        print_error "Docker deployment failed"
        exit 1
    fi
    
else
    print_warning "Docker not available, using direct Python deployment..."
    
    # Install/update dependencies
    print_status "Installing Python dependencies..."
    pip install -r requirements.txt
    
    # Kill existing Streamlit processes
    print_status "Stopping existing Streamlit processes..."
    pkill -f "streamlit run"
    
    # Start Streamlit app
    print_status "Starting Streamlit application..."
    nohup streamlit run simple_ad_success.py --server.port=8501 --server.address=0.0.0.0 > streamlit.log 2>&1 &
    
    if [ $? -eq 0 ]; then
        print_status "Streamlit application started successfully!"
    else
        print_error "Failed to start Streamlit application"
        exit 1
    fi
fi

# Check if Nginx is running
if command -v nginx &> /dev/null; then
    print_status "Reloading Nginx configuration..."
    sudo nginx -t && sudo systemctl reload nginx
    
    if [ $? -eq 0 ]; then
        print_status "Nginx reloaded successfully!"
    else
        print_warning "Nginx reload failed. Check configuration manually."
    fi
else
    print_warning "Nginx not found. You may need to set up reverse proxy manually."
fi

print_status "Deployment completed!"
print_status "Your app should be available at: https://britmetrics.com"
print_status "Check logs with: docker-compose logs -f (if using Docker)"
print_status "Or: tail -f streamlit.log (if using direct Python)"
