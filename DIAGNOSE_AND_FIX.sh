#!/bin/bash
# COMPLETE DIAGNOSTIC AND FIX SCRIPT
# Run this on Hostinger - it will find and fix everything

echo "=== DIAGNOSING BRITMETRICS ISSUE ==="

cd /var/www/britmetrics

# 1. Check if directory exists
if [ ! -d "/var/www/britmetrics" ]; then
    echo "ERROR: Directory /var/www/britmetrics doesn't exist!"
    exit 1
fi

# 2. Activate venv
source venv/bin/activate

# 3. Check Python version
echo "Python version:"
python3 --version

# 4. Install/upgrade all dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# 5. Test if we can import Streamlit
echo "Testing imports..."
python3 -c "import streamlit; print('Streamlit OK')" || echo "ERROR: Streamlit import failed!"

# 6. Test if app.py can be parsed
echo "Testing app.py syntax..."
python3 -m py_compile app.py || echo "ERROR: app.py has syntax errors!"

# 7. Kill all existing processes
echo "Killing old processes..."
sudo pkill -9 -f streamlit
sudo pkill -9 -f python3
sleep 3

# 8. Check what's using port 8504
echo "Checking port 8504..."
sudo lsof -i :8504 || echo "Port 8504 is free"

# 9. Create log directory if needed
mkdir -p /var/log
touch /var/log/britmetrics.log

# 10. Start Streamlit with full error output
echo "Starting Streamlit..."
cd /var/www/britmetrics
source venv/bin/activate
nohup streamlit run app.py --server.port 8504 --server.address 0.0.0.0 --server.headless true 2>&1 | tee /var/log/britmetrics.log &
STREAMLIT_PID=$!

sleep 8

# 11. Check if Streamlit is running
echo "Checking if Streamlit started..."
ps aux | grep streamlit | grep -v grep

# 12. Check logs
echo "=== LAST 50 LINES OF LOG ==="
tail -50 /var/log/britmetrics.log

# 13. Test if port is listening
echo "=== TESTING PORT 8504 ==="
curl -v http://localhost:8504 2>&1 | head -20

# 14. Check Nginx config
echo "=== CHECKING NGINX ==="
sudo nginx -t

# 15. Restart Nginx
sudo systemctl restart nginx
sudo systemctl status nginx | head -10

echo "=== DIAGNOSIS COMPLETE ==="
echo "Check the output above for errors!"

