# Debug: Why Changes Aren't Showing

Run these commands on your server to check what's wrong:

## Step 1: Check if code is pulled

```bash
cd /var/www/britmetrics
git log --oneline -5
```

You should see commits about "authentication" or "Login" - if not, run:
```bash
git pull origin main
```

## Step 2: Check if React build exists

```bash
ls -la /var/www/britmetrics/frontend-react/dist/
```

Should see `index.html` and `assets/` folder. If not:
```bash
cd /var/www/britmetrics/frontend-react
npm run build
```

## Step 3: Check Nginx is serving the right files

```bash
cat /etc/nginx/sites-available/britmetrics | grep root
```

Should show: `root /var/www/britmetrics/frontend-react/dist;`

If it shows something else, Nginx config needs updating.

## Step 4: Check API is running

```bash
sudo supervisorctl status britmetrics-api
```

Should show "RUNNING". If not:
```bash
sudo supervisorctl start britmetrics-api
```

## Step 5: Check API logs

```bash
sudo supervisorctl tail -50 britmetrics-api
```

Look for errors or "Stripe configured" message.

## Step 6: Test API directly

```bash
curl http://localhost:8000/api/health
```

Should return: `{"status":"ok",...}`

## Step 7: Check if Login.jsx exists

```bash
ls -la /var/www/britmetrics/frontend-react/src/pages/Login.jsx
```

If file doesn't exist, code wasn't pulled.

## Step 8: Rebuild everything from scratch

```bash
cd /var/www/britmetrics
git pull origin main
cd frontend-react
rm -rf dist node_modules
npm install
npm run build
cd ..
sudo supervisorctl restart britmetrics-api
sudo systemctl reload nginx
```

## Step 9: Check browser cache

On your Mac, open browser in **Incognito/Private mode** and visit:
- `https://britmetrics.com`
- Or `https://britmetrics.com/login`

You should see the login page.

## Common Issues:

1. **Old React build** - Need to run `npm run build`
2. **Nginx serving wrong directory** - Check Nginx config
3. **Browser cache** - Use Incognito mode
4. **Code not pulled** - Run `git pull origin main`
5. **API not restarted** - Run `sudo supervisorctl restart britmetrics-api`

## Quick Fix Script:

Run this entire block on your server:

```bash
cd /var/www/britmetrics && \
git pull origin main && \
cd frontend-react && \
npm run build && \
cd .. && \
sudo supervisorctl restart britmetrics-api && \
sudo systemctl reload nginx && \
echo "✅ Done! Now test in Incognito browser."
```

