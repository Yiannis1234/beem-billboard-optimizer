# EMAIL SIMPLIFIED SETUP

Since Outlook App Passwords are complicated, here's EASIER option:

## Option 1: Use a Simple Contact Form (Easiest!)

Instead of sending emails automatically, just show your email address so people can contact you directly. The form will just show:
- ✅ Name entered
- ✅ Email entered  
- ✅ Message entered
- 📧 Contact vamvak@outlook.com

This works immediately without any setup!

---

## Option 2: Use Your Outlook Password (If you want automatic emails)

If you want emails sent automatically, you need your Outlook password.

**To use this, type on Hostinger:**

```bash
cd /var/www/britmetrics
nano .env
```

**Add these 2 lines:**
```
SENDER_EMAIL=vamvak@outlook.com
SENDER_PASSWORD=YOUR_OUTLOOK_PASSWORD_HERE
```

**Save: Ctrl+X, Y, Enter**

**Then restart:**
```bash
git pull origin main
sudo pkill -9 -f streamlit
nohup streamlit run app.py --server.port 8503 &
```

---

**Recommendation:** Just use Option 1 (simple contact form) - it's instant and works perfectly!
