#!/bin/bash
# Fix port conflict and restart Streamlit

echo "Killing processes on port 8502..."
sudo fuser -k 8502/tcp

echo "Killing all Streamlit processes..."
sudo pkill -9 -f streamlit
sudo pkill -9 python3

sleep 3

echo "Starting fresh Streamlit with Stripe..."
cd /var/www/britmetrics
source venv/bin/activate
nohup streamlit run app.py --server.port 8502 --server.address localhost --server.headless true > /var/log/britmetrics.log 2>&1 &

sleep 3

echo "Checking if it's running..."
ps aux | grep streamlit

echo "Check logs:"
tail -20 /var/log/britmetrics.log

