# Deploy Latest Changes to Hostinger

## Step 1: SSH into Server

```bash
ssh root@147.93.85.115
```

## Step 2: Pull Latest Code

```bash
cd /var/www/britmetrics
git pull origin main
```

## Step 3: Rebuild React Frontend

```bash
cd /var/www/britmetrics/frontend-react
npm install  # only if package.json changed
npm run build
```

This creates the production build in `frontend-react/dist/`

## Step 4: Restart Backend API

```bash
sudo supervisorctl restart britmetrics-api
```

## Step 5: Reload Nginx

```bash
sudo systemctl reload nginx
```

## Step 6: Clear Browser Cache

**On your Mac:**
- Chrome/Safari: Press `Cmd + Shift + R` (hard refresh)
- Or open in Incognito/Private mode
- Or clear browser cache completely

## Step 7: Verify

1. Visit `https://britmetrics.com`
2. You should see the **Login page** (not the old campaign planner)
3. Enter email and click "Start Free Trial"
4. You should be redirected to the campaign planner

## If It Still Doesn't Work:

### Check if changes are on server:
```bash
# On server
cd /var/www/britmetrics
git log --oneline -5
# Should show recent commits about authentication
```

### Check if React build exists:
```bash
# On server
ls -la /var/www/britmetrics/frontend-react/dist/
# Should show index.html and assets
```

### Check Nginx config:
```bash
# On server
sudo nginx -t
# Should say "syntax is ok"
```

### Check API is running:
```bash
# On server
sudo supervisorctl status britmetrics-api
# Should show "RUNNING"
```

### Check logs for errors:
```bash
# On server
sudo supervisorctl tail -100 britmetrics-api
```

## Quick Full Deployment Script

Run this on your server:

```bash
cd /var/www/britmetrics && \
git pull origin main && \
cd frontend-react && \
npm run build && \
cd .. && \
sudo supervisorctl restart britmetrics-api && \
sudo systemctl reload nginx && \
echo "✅ Deployment complete!"
```

