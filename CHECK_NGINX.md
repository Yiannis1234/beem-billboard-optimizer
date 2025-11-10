# Check Nginx Configuration

## The Problem:
You're visiting `fast.hostingervps.com/2330/` which is the Hostinger control panel, NOT your website!

## The Correct URL:
Visit: **`https://britmetrics.com`** or **`http://147.93.85.115`**

## Check Nginx Config:

Run on your server:

```bash
# Check if Nginx config exists
cat /etc/nginx/sites-available/britmetrics

# Should show something like:
# server {
#     listen 80;
#     server_name britmetrics.com www.britmetrics.com;
#     root /var/www/britmetrics/frontend-react/dist;
#     ...
# }
```

## Verify Nginx is serving the right files:

```bash
# Check if the symlink exists
ls -la /etc/nginx/sites-enabled/britmetrics

# Should show a link to sites-available/britmetrics
```

## Test the website directly:

```bash
# Test from server
curl http://localhost
# Should return HTML from dist/index.html

# Test API
curl http://localhost:8000/api/health
# Should return {"status":"ok",...}
```

## If Nginx config is wrong, fix it:

```bash
sudo nano /etc/nginx/sites-available/britmetrics
```

Make sure it has:
```
server {
    listen 80;
    server_name britmetrics.com www.britmetrics.com;
    
    root /var/www/britmetrics/frontend-react/dist;
    index index.html;
    
    location / {
        try_files $uri $uri/ /index.html;
    }
    
    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

Then:
```bash
sudo nginx -t  # Test config
sudo systemctl reload nginx
```

## Most Important:
**Visit the correct URL in your browser:**
- `https://britmetrics.com` 
- Or `http://147.93.85.115`

NOT the Hostinger panel URL!

