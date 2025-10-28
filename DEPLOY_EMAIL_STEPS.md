```bash
# Connect to Hostinger server
ssh your-username@your-hostinger-ip

# Go to your project
cd /var/www/britmetrics

# Create or edit .env file
nano .env

# Add these two lines (replace with YOUR gmail and password):
SENDER_EMAIL=your-gmail@gmail.com
SENDER_PASSWORD=your-16-character-app-password

# Save and exit (Ctrl+X, then Y, then Enter)

# Deploy the latest code
source venv/bin/activate
git pull origin main

# Restart the app
sudo pkill -9 -f streamlit
sleep 3
nohup streamlit run app.py --server.port 8503 --server.address localhost --server.headless true > /var/log/britmetrics.log 2>&1 &

# Check it's working
sleep 5
tail -20 /var/log/britmetrics.log
```
