# Setting Stripe Secret Key on Hostinger Server

## Step 1: SSH into your Hostinger server

```bash
ssh root@your-server-ip
# or
ssh root@britmetrics.com
```

## Step 2: Set the environment variable

You have two options:

### Option A: Set in Supervisor config (Recommended)

Edit the supervisor config file:

```bash
sudo nano /etc/supervisor/conf.d/britmetrics-api.conf
```

Add the environment variable to the `[program:britmetrics-api]` section:

```ini
[program:britmetrics-api]
command=/path/to/venv/bin/uvicorn backend.api_server:app --host 0.0.0.0 --port 8000
directory=/var/www/britmetrics
user=www-data
autostart=true
autorestart=true
environment=STRIPE_SECRET_KEY="sk_test_YOUR_SECRET_KEY_HERE",STRIPE_PUBLISHABLE_KEY="pk_test_51SQ4hnBoIqMUQLys40me9RfJxojooBK8LBGkDDgfCrwcflo78YDQ2DebdCunXRPGCNA0P4bL1HBznhcepuz3Nnf000kHrOsGa0"
```

Save and exit (Ctrl+X, then Y, then Enter).

### Option B: Set in systemd environment file

Create an environment file:

```bash
sudo nano /etc/systemd/system/britmetrics-api.env
```

Add:
```
STRIPE_SECRET_KEY=sk_test_YOUR_SECRET_KEY_HERE
STRIPE_PUBLISHABLE_KEY=pk_test_51SQ4hnBoIqMUQLys40me9RfJxojooBK8LBGkDDgfCrwcflo78YDQ2DebdCunXRPGCNA0P4bL1HBznhcepuz3Nnf000kHrOsGa0
```

## Step 3: Reload and restart

If using Supervisor (Option A):
```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl restart britmetrics-api
```

If using systemd (Option B):
```bash
sudo systemctl daemon-reload
sudo systemctl restart britmetrics-api
```

## Step 4: Verify it's working

Check the API logs:
```bash
sudo supervisorctl tail -f britmetrics-api
# or
sudo journalctl -u britmetrics-api -f
```

You should see: `"Stripe configured successfully"` in the logs.

## Alternative: Quick test

You can also test by setting it temporarily in your current shell session:

```bash
export STRIPE_SECRET_KEY="sk_test_YOUR_SECRET_KEY_HERE"
export STRIPE_PUBLISHABLE_KEY="pk_test_51SQ4hnBoIqMUQLys40me9RfJxojooBK8LBGkDDgfCrwcflo78YDQ2DebdCunXRPGCNA0P4bL1HBznhcepuz3Nnf000kHrOsGa0"
```

Then restart the service (this only works for the current session, use Option A for permanent).

## Troubleshooting

If it's still not working:
1. Check if the environment variable is set: `echo $STRIPE_SECRET_KEY`
2. Check API logs for errors
3. Make sure the supervisor config has the correct path to your Python venv
4. Verify the API server is actually reading the env var by checking logs

