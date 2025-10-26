#!/bin/bash

# Kill any existing Streamlit processes
killall -9 streamlit 2>/dev/null || true
sleep 1

# Clear all cache
cd /Users/ioannisvamvakas/beem-billboard-optimizer
rm -rf .streamlit __pycache__ backend/__pycache__ frontend/__pycache__
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true

# Clear Streamlit cache
rm -rf ~/.streamlit/cache 2>/dev/null || true

echo "✅ Cache cleared"
echo "🚀 Starting Streamlit..."
echo ""
echo "Your app will be available at: http://localhost:8501"
echo ""

# Start Streamlit
streamlit run app.py --server.port 8501

