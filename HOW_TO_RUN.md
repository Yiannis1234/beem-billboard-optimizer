# 🚀 How to Run BritMetrics

## Local Development (On Your Computer)

### 1. Install Dependencies

```bash
# Make sure you're in the project directory
cd /Users/ioannisvamvakas/beem-billboard-optimizer

# Install Python packages
pip3 install -r requirements.txt
```

### 2. Run the Application

```bash
# Run Streamlit
streamlit run app.py
```

Or if you want to specify a port:

```bash
streamlit run app.py --server.port 8501
```

The app will automatically open in your browser at: **http://localhost:8501**

---

## Production (On Hostinger Server)

### 1. SSH into Your Server

```bash
ssh root@147.93.85.115
```

### 2. Navigate to Project Directory

```bash
cd /var/www/britmetrics
```

### 3. Pull Latest Changes

```bash
git pull origin main
```

### 4. Install/Update Dependencies (if needed)

```bash
# Activate virtual environment if you have one
source venv/bin/activate  # if using venv

# Install dependencies
pip3 install -r requirements.txt
```

### 5. Restart the Application

The app should be running via Supervisor. To restart:

```bash
# Stop the app
sudo supervisorctl stop britmetrics

# Kill any existing processes on port 8504
sudo fuser -k 8504/tcp 2>/dev/null || true

# Start the app
sudo supervisorctl start britmetrics

# Check status
sudo supervisorctl status britmetrics
```

### 6. Check Nginx Configuration

```bash
# Test Nginx config
sudo nginx -t

# Restart Nginx if needed
sudo systemctl restart nginx

# Check Nginx status
sudo systemctl status nginx
```

### 7. View Logs

```bash
# View application logs
sudo tail -f /var/www/britmetrics/logs/app.log

# Or check Supervisor logs
sudo tail -f /var/log/supervisor/britmetrics-stderr.log
```

---

## Quick Commands Reference

### Local Testing
```bash
# Run locally
streamlit run app.py

# Run on specific port
streamlit run app.py --server.port 8501

# Run in background
nohup streamlit run app.py --server.port 8501 > /dev/null 2>&1 &
```

### Production (Hostinger)
```bash
# Restart app
sudo supervisorctl restart britmetrics

# Check status
sudo supervisorctl status britmetrics

# View logs
sudo tail -f /var/log/supervisor/britmetrics-stderr.log

# Pull latest code
cd /var/www/britmetrics && git pull origin main && sudo supervisorctl restart britmetrics
```

---

## Troubleshooting

### Port Already in Use (Local)
```bash
# Kill process on port 8501
lsof -ti:8501 | xargs kill -9

# Or use a different port
streamlit run app.py --server.port 8502
```

### Port Already in Use (Server)
```bash
# Find process using port
sudo lsof -i :8504

# Kill process
sudo fuser -k 8504/tcp

# Restart
sudo supervisorctl restart britmetrics
```

### App Not Loading
1. Check if Streamlit is running: `ps aux | grep streamlit`
2. Check port: `netstat -tuln | grep 8504`
3. Check Nginx: `sudo systemctl status nginx`
4. Check logs: `sudo tail -f /var/log/supervisor/britmetrics-stderr.log`

---

## Access URLs

- **Local:** http://localhost:8501
- **Production:** https://britmetrics.com (or http://britmetrics.com)

---

## Environment Variables

Make sure these are set on the server (in `.env` file or environment):

- `WEATHER_API_KEY` - WeatherAPI.com key
- `TOMTOM_API_KEY` - TomTom Traffic API key
- `GOOGLE_PLACES_API_KEY` - Google Places API key
- `EVENTBRITE_API_TOKEN` - Eventbrite API token
- `STRIPE_SECRET_KEY` - Stripe secret key (if using payments)
- `STRIPE_PUBLISHABLE_KEY` - Stripe publishable key (if using payments)

