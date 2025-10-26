# 🚀 Deploy BritMetrics to Hostinger + britmetrics.com

## Overview
We'll deploy your Streamlit app to Hostinger VPS and connect it to britmetrics.com

---

## 📋 Prerequisites

1. **Hostinger VPS** account active
2. **britmetrics.com** domain (should already point to your Hostinger server)
3. **SSH access** to your Hostinger VPS
4. **Python 3.9+** on the server

---

## Step 1: Prepare Your Code for Deployment

### 1.1 Create Production Requirements File

```bash
cd /Users/ioannisvamvakas/beem-billboard-optimizer
```

Check that `requirements.txt` has all dependencies:
```
streamlit
pandas
numpy
plotly
requests
matplotlib
```

### 1.2 Create .gitignore (if not exists)

```bash
cat > .gitignore << 'EOF'
__pycache__/
*.py[cod]
*$py.class
.Python
env/
venv/
.env
.venv/
.streamlit/
*.log
.DS_Store
EOF
```

### 1.3 Commit Your Changes

```bash
git add .
git commit -m "Rebrand to BritMetrics - ready for deployment"
git push origin main
```

---

## Step 2: Connect to Hostinger VPS

### 2.1 SSH into Your Server

```bash
ssh root@your-hostinger-ip
# OR if you have a user account:
ssh yourusername@your-hostinger-ip
```

If you don't know your IP:
- Log into Hostinger panel → VPS → Details
- Copy the IP address

---

## Step 3: Install Required Software on Server

### 3.1 Update System

```bash
sudo apt update && sudo apt upgrade -y
```

### 3.2 Install Python & Pip

```bash
sudo apt install python3 python3-pip python3-venv -y
```

### 3.3 Install Nginx (Web Server)

```bash
sudo apt install nginx -y
```

### 3.4 Install Supervisor (Keep App Running)

```bash
sudo apt install supervisor -y
```

---

## Step 4: Deploy Your Application

### 4.1 Clone Your Repository

```bash
cd /var/www
sudo git clone https://github.com/Yiannis1234/beem-billboard-optimizer.git britmetrics
cd britmetrics
```

### 4.2 Create Virtual Environment

```bash
sudo python3 -m venv venv
sudo chown -R $USER:$USER venv
source venv/bin/activate
```

### 4.3 Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4.4 Test the App Locally First

```bash
streamlit run app.py --server.port 8501 --server.address localhost
```

Press `Ctrl+C` to stop after verifying it works.

---

## Step 5: Configure Nginx Reverse Proxy

### 5.1 Create Nginx Configuration

```bash
sudo nano /etc/nginx/sites-available/britmetrics.com
```

Paste this configuration:

```nginx
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
```

Save: `Ctrl+X`, then `Y`, then `Enter`

### 5.2 Enable the Site

```bash
sudo ln -s /etc/nginx/sites-available/britmetrics.com /etc/nginx/sites-enabled/
```

### 5.3 Test Nginx Configuration

```bash
sudo nginx -t
```

Should say "syntax is ok" and "test is successful"

### 5.4 Reload Nginx

```bash
sudo systemctl reload nginx
```

---

## Step 6: Configure Supervisor (Auto-restart)

### 6.1 Create Supervisor Config

```bash
sudo nano /etc/supervisor/conf.d/britmetrics.conf
```

Paste this:

```ini
[program:britmetrics]
command=/var/www/britmetrics/venv/bin/streamlit run app.py --server.port 8501 --server.address localhost --server.headless true
directory=/var/www/britmetrics
user=root
autostart=true
autorestart=true
stderr_logfile=/var/log/britmetrics.err.log
stdout_logfile=/var/log/britmetrics.out.log
environment=PATH="/var/www/britmetrics/venv/bin"
```

Save: `Ctrl+X`, then `Y`, then `Enter`

### 6.2 Update Supervisor

```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start britmetrics
```

### 6.3 Check Status

```bash
sudo supervisorctl status britmetrics
```

Should say "RUNNING"

---

## Step 7: Configure Domain DNS (If Not Done)

### 7.1 In Hostinger Control Panel:

1. Go to **Domains** → **britmetrics.com** → **DNS/Name Servers**
2. Add/Update these records:

```
Type    Name    Content              TTL
A       @       YOUR_VPS_IP          14400
A       www     YOUR_VPS_IP          14400
```

3. Wait 5-60 minutes for DNS propagation

---

## Step 8: Install SSL Certificate (HTTPS)

### 8.1 Install Certbot

```bash
sudo apt install certbot python3-certbot-nginx -y
```

### 8.2 Get SSL Certificate

```bash
sudo certbot --nginx -d britmetrics.com -d www.britmetrics.com
```

Follow the prompts:
- Enter your email
- Agree to terms
- Choose option 2 (redirect HTTP to HTTPS)

### 8.3 Test Auto-Renewal

```bash
sudo certbot renew --dry-run
```

---

## Step 9: Verify Deployment

### 9.1 Check if App is Running

```bash
sudo supervisorctl status britmetrics
curl http://localhost:8501
```

### 9.2 Check Nginx

```bash
sudo systemctl status nginx
```

### 9.3 Visit Your Site

Open browser and go to:
- http://britmetrics.com (should redirect to HTTPS)
- https://britmetrics.com (should show your app!)

---

## 🔧 Troubleshooting

### App Not Starting?

```bash
# Check logs
sudo tail -f /var/log/britmetrics.err.log
sudo tail -f /var/log/britmetrics.out.log

# Restart app
sudo supervisorctl restart britmetrics
```

### Nginx Errors?

```bash
# Check Nginx logs
sudo tail -f /var/log/nginx/error.log

# Restart Nginx
sudo systemctl restart nginx
```

### Domain Not Working?

```bash
# Check DNS
nslookup britmetrics.com

# Verify it points to your VPS IP
```

### 502 Bad Gateway?

```bash
# Check if Streamlit is running
sudo supervisorctl status britmetrics
curl http://localhost:8501

# If not, check logs and restart
sudo supervisorctl restart britmetrics
```

---

## 🔄 Updating Your App (Future Changes)

When you make changes to your code:

```bash
# On your VPS:
cd /var/www/britmetrics
sudo git pull origin main
source venv/bin/activate
pip install -r requirements.txt  # If new dependencies
sudo supervisorctl restart britmetrics
```

---

## 📊 Quick Command Reference

```bash
# Start app
sudo supervisorctl start britmetrics

# Stop app
sudo supervisorctl stop britmetrics

# Restart app
sudo supervisorctl restart britmetrics

# Check status
sudo supervisorctl status britmetrics

# View logs
sudo tail -f /var/log/britmetrics.out.log

# Reload Nginx
sudo systemctl reload nginx

# Restart Nginx
sudo systemctl restart nginx
```

---

## 🎯 Final Checklist

- [ ] Code pushed to GitHub
- [ ] SSH access to Hostinger VPS working
- [ ] Python 3.9+ installed on server
- [ ] App cloned to `/var/www/britmetrics`
- [ ] Virtual environment created and dependencies installed
- [ ] Nginx configured and running
- [ ] Supervisor configured and app running
- [ ] Domain DNS pointing to VPS IP
- [ ] SSL certificate installed (HTTPS working)
- [ ] Site accessible at https://britmetrics.com
- [ ] App loads and works correctly

---

## 🆘 Need Help?

Common issues and solutions in the troubleshooting section above.

For Hostinger-specific help:
- Hostinger Support: https://www.hostinger.com/contact
- VPS Documentation: https://support.hostinger.com/en/collections/1796870-vps

---

**Your BritMetrics platform should now be live at https://britmetrics.com!** 🎉

