# 🚀 Quick Deploy to britmetrics.com

## TL;DR - Fast Track Deployment

### Step 1: Push to GitHub (On Your Mac)

```bash
cd /Users/ioannisvamvakas/beem-billboard-optimizer
git add .
git commit -m "BritMetrics ready for deployment"
git push origin main
```

### Step 2: SSH to Your Hostinger VPS

```bash
ssh root@YOUR_VPS_IP
# Replace YOUR_VPS_IP with your actual Hostinger VPS IP
```

### Step 3: One-Time Setup (First Deploy Only)

Run this entire block:

```bash
# Install requirements
sudo apt update && sudo apt upgrade -y
sudo apt install python3 python3-pip python3-venv nginx supervisor certbot python3-certbot-nginx -y

# Clone app
cd /var/www
sudo git clone https://github.com/Yiannis1234/beem-billboard-optimizer.git britmetrics
cd britmetrics

# Setup Python
sudo python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure Nginx
sudo tee /etc/nginx/sites-available/britmetrics.com << 'EOF'
server {
    listen 80;
    server_name britmetrics.com www.britmetrics.com;
    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 86400;
    }
    location /_stcore/stream {
        proxy_pass http://localhost:8501/_stcore/stream;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
EOF

sudo ln -s /etc/nginx/sites-available/britmetrics.com /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx

# Configure Supervisor
sudo tee /etc/supervisor/conf.d/britmetrics.conf << 'EOF'
[program:britmetrics]
command=/var/www/britmetrics/venv/bin/streamlit run app.py --server.port 8501 --server.address localhost --server.headless true
directory=/var/www/britmetrics
user=root
autostart=true
autorestart=true
stderr_logfile=/var/log/britmetrics.err.log
stdout_logfile=/var/log/britmetrics.out.log
environment=PATH="/var/www/britmetrics/venv/bin"
EOF

sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start britmetrics

# Install SSL
sudo certbot --nginx -d britmetrics.com -d www.britmetrics.com --non-interactive --agree-tos -m your-email@example.com
```

Replace `your-email@example.com` with your actual email!

### Step 4: Verify It's Working

```bash
# Check app status
sudo supervisorctl status britmetrics

# Should say "RUNNING"
```

### Step 5: Visit Your Site

Open browser: **https://britmetrics.com**

---

## 🔄 Future Updates (Quick Deploy)

When you make changes:

```bash
# On your Mac:
cd /Users/ioannisvamvakas/beem-billboard-optimizer
git add .
git commit -m "Updates"
git push origin main

# On Hostinger VPS:
cd /var/www/britmetrics
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
sudo supervisorctl restart britmetrics
```

Or use the automated script:

```bash
# On your Mac:
./deploy_to_hostinger.sh
```

---

## 🆘 Troubleshooting

### Site Not Loading?

```bash
# Check if app is running
sudo supervisorctl status britmetrics

# Check logs
sudo tail -f /var/log/britmetrics.err.log

# Restart
sudo supervisorctl restart britmetrics
```

### 502 Bad Gateway?

```bash
# App probably crashed - check logs
sudo tail -f /var/log/britmetrics.err.log

# Restart
sudo supervisorctl restart britmetrics
```

### Domain Not Resolving?

1. Check DNS in Hostinger panel
2. Make sure A records point to your VPS IP:
   - `@` → YOUR_VPS_IP
   - `www` → YOUR_VPS_IP
3. Wait 10-30 minutes for DNS propagation

---

## 📝 Important Info

- **App Location:** `/var/www/britmetrics`
- **Logs:** `/var/log/britmetrics.*.log`
- **Config:** `/etc/supervisor/conf.d/britmetrics.conf`
- **Nginx Config:** `/etc/nginx/sites-available/britmetrics.com`

---

**Full detailed guide:** See `HOSTINGER_DEPLOYMENT.md`

