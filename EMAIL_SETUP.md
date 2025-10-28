# Email Configuration for BritMetrics Contact Form

## Setup Instructions

1. **Create a Gmail account** (or use existing one) for sending emails
2. **Enable 2-Factor Authentication** on the Gmail account
3. **Generate App Password**:
   - Go to Google Account settings
   - Security → 2-Step Verification → App passwords
   - Generate password for "Mail"

4. **Set Environment Variables** on Hostinger:

```bash
# Add to your .env file or set as environment variables
export SENDER_EMAIL="your-gmail@gmail.com"
export SENDER_PASSWORD="your-16-character-app-password"
```

## How it works:
- Contact form messages are sent to vamvak@outlook.com
- Auto-reply is sent to the person who submitted the form
- Uses Gmail SMTP server for reliable delivery

## Alternative: Use a service like SendGrid, Mailgun, or AWS SES for production
