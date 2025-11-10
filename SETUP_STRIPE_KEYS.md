# Step-by-Step: Set Stripe Keys on Hostinger Server

## Step 1: Connect to Your Server

Open Terminal on your Mac and SSH into your Hostinger server:

```bash
ssh root@147.93.85.115
```

(Or use your Hostinger web terminal if SSH doesn't work)

## Step 2: Navigate to Your Project Directory

```bash
cd /var/www/britmetrics
```

## Step 3: Check Current Supervisor Config

First, let's see what your current supervisor config looks like:

```bash
cat /etc/supervisor/conf.d/britmetrics-api.conf
```

## Step 4: Edit the Supervisor Config

Edit the supervisor configuration file:

```bash
sudo nano /etc/supervisor/conf.d/britmetrics-api.conf
```

You should see something like this:

```ini
[program:britmetrics-api]
command=/path/to/venv/bin/uvicorn backend.api_server:app --host 0.0.0.0 --port 8000
directory=/var/www/britmetrics
user=www-data
autostart=true
autorestart=true
```

## Step 5: Add Environment Variables

Add this line to the `[program:britmetrics-api]` section (right after `autorestart=true`):

**Replace `YOUR_SECRET_KEY_HERE` with your actual secret key from Stripe dashboard.**

```ini
environment=STRIPE_SECRET_KEY="YOUR_SECRET_KEY_HERE",STRIPE_PUBLISHABLE_KEY="pk_test_51SQ4hnBoIqMUQLys40me9RfJxojooBK8LBGkDDgfCrwcflo78YDQ2DebdCunXRPGCNA0P4bL1HBznhcepuz3Nnf000kHrOsGa0"
```

**Your actual secret key:** See `STRIPE_SECRET_KEY.txt` file in your project root (not committed to git for security).
*(Copy the key from that file and replace `YOUR_SECRET_KEY_HERE` in the config above)*

**Your complete config should look like this:**

```ini
[program:britmetrics-api]
command=/path/to/venv/bin/uvicorn backend.api_server:app --host 0.0.0.0 --port 8000
directory=/var/www/britmetrics
user=www-data
autostart=true
autorestart=true
environment=STRIPE_SECRET_KEY="YOUR_SECRET_KEY_HERE",STRIPE_PUBLISHABLE_KEY="pk_test_51SQ4hnBoIqMUQLys40me9RfJxojooBK8LBGkDDgfCrwcflo78YDQ2DebdCunXRPGCNA0P4bL1HBznhcepuz3Nnf000kHrOsGa0"
```

**Important:** Replace `/path/to/venv/bin/uvicorn` with the actual path to your Python virtual environment. Common paths:
- `/var/www/britmetrics/venv/bin/uvicorn`
- `/root/venv/bin/uvicorn`
- `/usr/local/bin/uvicorn`

## Step 6: Save the File

In nano editor:
1. Press `Ctrl + X` to exit
2. Press `Y` to confirm save
3. Press `Enter` to confirm filename

## Step 7: Reload Supervisor

Run these commands to apply the changes:

```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl restart britmetrics-api
```

## Step 8: Verify It's Working

Check the API logs to see if Stripe is configured:

```bash
sudo supervisorctl tail -f britmetrics-api
```

You should see: `"Stripe configured successfully"` in the logs.

Press `Ctrl + C` to exit the log viewer.

## Step 9: Test the API

Test if the API is running and can create checkout sessions:

```bash
curl http://localhost:8000/api/health
```

You should get: `{"status":"ok","timestamp":"..."}`

## Troubleshooting

### If supervisor commands don't work:

```bash
# Check if supervisor is running
sudo systemctl status supervisor

# Start supervisor if needed
sudo systemctl start supervisor

# Check your config syntax
sudo supervisorctl reread
```

### If the API doesn't start:

```bash
# Check the error logs
sudo supervisorctl tail -100 britmetrics-api stderr

# Check if the Python path is correct
which python3
which uvicorn
```

### If you need to find your Python venv path:

```bash
# Common locations
ls -la /var/www/britmetrics/venv/bin/uvicorn
ls -la ~/venv/bin/uvicorn
ls -la /root/venv/bin/uvicorn

# Or find it
find /var/www -name uvicorn 2>/dev/null
```

## Alternative: Quick Test (Temporary)

If you want to test quickly without editing supervisor config:

```bash
export STRIPE_SECRET_KEY="YOUR_SECRET_KEY_HERE"
export STRIPE_PUBLISHABLE_KEY="pk_test_51SQ4hnBoIqMUQLys40me9RfJxojooBK8LBGkDDgfCrwcflo78YDQ2DebdCunXRPGCNA0P4bL1HBznhcepuz3Nnf000kHrOsGa0"
cd /var/www/britmetrics
source venv/bin/activate  # if you have a venv
uvicorn backend.api_server:app --host 0.0.0.0 --port 8000
```

This only works for the current session. Use the supervisor method for permanent setup.

## Summary Checklist

- [ ] SSH into server
- [ ] Navigate to `/var/www/britmetrics`
- [ ] Edit `/etc/supervisor/conf.d/britmetrics-api.conf`
- [ ] Add `environment=` line with both Stripe keys
- [ ] Save file (Ctrl+X, Y, Enter)
- [ ] Run `sudo supervisorctl reread`
- [ ] Run `sudo supervisorctl update`
- [ ] Run `sudo supervisorctl restart britmetrics-api`
- [ ] Check logs for "Stripe configured successfully"
- [ ] Test API health endpoint

Done! Your Stripe keys are now configured.

