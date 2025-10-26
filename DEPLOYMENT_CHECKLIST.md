# ✅ BritMetrics Deployment Checklist

## Pre-Deployment (On Your Mac)

- [ ] All code tested locally (`./restart_app.sh` works)
- [ ] BritMetrics branding complete (no "AdPersona" references)
- [ ] Pink box shows Overall Score (not percentage)
- [ ] Audience matching works (not all 20%)
- [ ] Dark mode works
- [ ] All changes committed to git
- [ ] Code pushed to GitHub

```bash
cd /Users/ioannisvamvakas/beem-billboard-optimizer
git add .
git commit -m "BritMetrics v1.0 - Ready for production"
git push origin main
```

---

## Hostinger Setup

### 1. VPS Information
- [ ] VPS IP Address: __________________
- [ ] SSH Username: __________________
- [ ] SSH Password/Key: Available

### 2. Domain Configuration
- [ ] Domain `britmetrics.com` owned
- [ ] DNS A record `@` → VPS IP
- [ ] DNS A record `www` → VPS IP
- [ ] DNS propagated (check: `nslookup britmetrics.com`)

### 3. Server Access
```bash
ssh root@YOUR_VPS_IP
```
- [ ] Can connect successfully

---

## Server Installation (First Time Only)

### Install Software
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install python3 python3-pip python3-venv nginx supervisor certbot python3-certbot-nginx git -y
```
- [ ] All packages installed

### Clone Application
```bash
cd /var/www
sudo git clone https://github.com/Yiannis1234/beem-billboard-optimizer.git britmetrics
cd britmetrics
```
- [ ] Repository cloned

### Setup Python Environment
```bash
sudo python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
- [ ] Virtual environment created
- [ ] Dependencies installed

### Test Locally
```bash
streamlit run app.py --server.port 8501
```
- [ ] App runs without errors
- [ ] Press Ctrl+C to stop

---

## Configure Web Server

### Nginx Configuration
```bash
sudo nano /etc/nginx/sites-available/britmetrics.com
```
- [ ] Configuration file created (see DEPLOY_QUICK_START.md for content)
- [ ] Symlink created: `sudo ln -s /etc/nginx/sites-available/britmetrics.com /etc/nginx/sites-enabled/`
- [ ] Config tested: `sudo nginx -t` (should pass)
- [ ] Nginx reloaded: `sudo systemctl reload nginx`

### Supervisor Configuration
```bash
sudo nano /etc/supervisor/conf.d/britmetrics.conf
```
- [ ] Configuration file created (see DEPLOY_QUICK_START.md for content)
- [ ] Supervisor updated: `sudo supervisorctl reread && sudo supervisorctl update`
- [ ] App started: `sudo supervisorctl start britmetrics`
- [ ] App running: `sudo supervisorctl status britmetrics` shows RUNNING

---

## SSL Certificate (HTTPS)

```bash
sudo certbot --nginx -d britmetrics.com -d www.britmetrics.com
```
- [ ] SSL certificate obtained
- [ ] HTTPS enabled
- [ ] Auto-renewal configured

---

## Final Verification

### Check Services
```bash
# App status
sudo supervisorctl status britmetrics
# Should show: RUNNING

# Nginx status
sudo systemctl status nginx
# Should show: active (running)

# Check logs (should have no errors)
sudo tail -20 /var/log/britmetrics.out.log
```
- [ ] BritMetrics app: RUNNING
- [ ] Nginx: Active
- [ ] No errors in logs

### Test URLs
- [ ] http://britmetrics.com → Redirects to HTTPS
- [ ] https://britmetrics.com → Shows BritMetrics app
- [ ] https://www.britmetrics.com → Shows BritMetrics app
- [ ] App fully functional (can select campaign, see results)

### Test Features
- [ ] Campaign selection works
- [ ] Location selection works
- [ ] Pink box shows Overall Score (not %)
- [ ] Metrics display correctly
- [ ] Audience match varies by campaign
- [ ] Creative recommendations appear
- [ ] Tables load and sort
- [ ] Dark mode works (if browser is in dark mode)

---

## Post-Deployment Monitoring

### First 24 Hours
- [ ] Check logs every few hours: `sudo tail -f /var/log/britmetrics.out.log`
- [ ] Monitor for errors: `sudo tail -f /var/log/britmetrics.err.log`
- [ ] Test from different devices/browsers
- [ ] Verify SSL certificate is valid

### Performance Check
```bash
# CPU/Memory usage
top
# Press 'q' to quit

# Disk space
df -h

# App uptime
sudo supervisorctl status britmetrics
```

---

## Future Updates

### When You Make Changes:

**On Your Mac:**
```bash
cd /Users/ioannisvamvakas/beem-billboard-optimizer
git add .
git commit -m "Description of changes"
git push origin main
```

**On Hostinger VPS:**
```bash
cd /var/www/britmetrics
git pull origin main
source venv/bin/activate
pip install -r requirements.txt  # Only if dependencies changed
sudo supervisorctl restart britmetrics
```

**Or use the automated script:**
```bash
./deploy_to_hostinger.sh
```

---

## Emergency Procedures

### App Crashed?
```bash
# Check what went wrong
sudo tail -50 /var/log/britmetrics.err.log

# Restart
sudo supervisorctl restart britmetrics
```

### Site Down?
```bash
# Check all services
sudo systemctl status nginx
sudo supervisorctl status britmetrics

# Restart everything
sudo systemctl restart nginx
sudo supervisorctl restart britmetrics
```

### Rollback to Previous Version
```bash
cd /var/www/britmetrics
git log  # Find the commit hash you want
git checkout COMMIT_HASH
sudo supervisorctl restart britmetrics
```

---

## Support Contacts

- **Hostinger Support:** https://www.hostinger.com/contact
- **GitHub Repo:** https://github.com/Yiannis1234/beem-billboard-optimizer
- **Streamlit Docs:** https://docs.streamlit.io

---

## 🎉 Success Criteria

✅ App is live at https://britmetrics.com  
✅ SSL certificate is active (HTTPS works)  
✅ All features work correctly  
✅ No errors in logs  
✅ App auto-restarts if it crashes  
✅ Can deploy updates easily  

**Your BritMetrics platform is now live!** 🇬🇧📊

