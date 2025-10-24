# Hostinger Deployment Guide

## Option 1: Streamlit Cloud (Easiest) ⭐

1. **Go to Streamlit Cloud**: https://share.streamlit.io/
2. **Sign in** with your GitHub account
3. **Click "New app"**
4. **Select repository**: `Yiannis1234/beem-billboard-optimizer`
5. **Set main file**: `simple_ad_success.py`
6. **Click "Deploy!"**

Your app will be live at: `https://beem-billboard-optimizer.streamlit.app/`

### Custom Domain Setup:
1. In Streamlit Cloud settings, add custom domain: `britmetrics.com`
2. Update your DNS records to point to Streamlit Cloud
3. Your app will be available at `https://britmetrics.com`

---

## Option 2: Hostinger VPS (Advanced)

### Prerequisites:
- Hostinger VPS with Docker support
- Domain `britmetrics.com` pointing to your VPS

### Deployment Steps:

1. **SSH into your Hostinger VPS**:
   ```bash
   ssh your-username@your-vps-ip
   ```

2. **Install Docker**:
   ```bash
   curl -fsSL https://get.docker.com -o get-docker.sh
   sh get-docker.sh
   ```

3. **Clone your repository**:
   ```bash
   git clone https://github.com/Yiannis1234/beem-billboard-optimizer.git
   cd beem-billboard-optimizer
   ```

4. **Deploy with Docker Compose**:
   ```bash
   docker-compose up -d
   ```

5. **Set up Nginx reverse proxy**:
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
       }
   }
   ```

6. **Enable HTTPS** (recommended):
   ```bash
   certbot --nginx -d britmetrics.com -d www.britmetrics.com
   ```

---

## Option 3: Hostinger Shared Hosting (Static Version)

If you only have shared hosting, we can create a static version:

1. **Create a static HTML version** of your app
2. **Upload to Hostinger** via File Manager or FTP
3. **Set up automatic updates** from GitHub

---

## Recommended: Streamlit Cloud ⭐

**Why Streamlit Cloud is best:**
- ✅ Free hosting
- ✅ Automatic deployments from GitHub
- ✅ Custom domain support
- ✅ HTTPS included
- ✅ No server management
- ✅ Scales automatically
- ✅ Perfect for Streamlit apps

**Next Steps:**
1. Deploy to Streamlit Cloud (5 minutes)
2. Set up custom domain `britmetrics.com`
3. Your app will be live and automatically updated!
